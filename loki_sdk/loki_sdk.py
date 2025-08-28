#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loki SDK for Python
基于python-logging-loki的Python日志SDK，支持异步发送日志到Loki服务器
"""

import json
import logging
import threading
import time
import queue
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
import atexit
from logging_loki import LokiHandler


class LokiSDK:
    """Loki SDK主类"""
    
    def __init__(self):
        self._config = {}
        self._buffer = queue.Queue()
        self._worker_thread = None
        self._running = False
        self._session = requests.Session()
        self._loki_handler = None
        
        # 注册退出时的清理函数
        atexit.register(self._cleanup)
    
    def init(self, app_name: str, environment: str = "production", 
             endpoints: Optional[Dict[str, str]] = None,
             use_send_beacon: bool = True, 
             enable_offline_buffer: bool = True,
             buffer_size: int = 1000,
             flush_interval: int = 5,
             max_retries: int = 3):
        """
        初始化SDK配置
        
        Args:
            app_name: 应用名称
            environment: 环境（production, staging, development等）
            endpoints: 端点配置，包含loki服务器地址
            use_send_beacon: 是否使用异步发送（类似sendBeacon）
            enable_offline_buffer: 是否启用离线缓冲
            buffer_size: 缓冲区大小
            flush_interval: 刷新间隔（秒）
            max_retries: 最大重试次数
        """
        self._config = {
            'app_name': app_name,
            'environment': environment,
            'endpoints': endpoints or {'loki': 'http://localhost:3100/loki/api/v1/push'},
            'use_send_beacon': use_send_beacon,
            'enable_offline_buffer': enable_offline_buffer,
            'buffer_size': buffer_size,
            'flush_interval': flush_interval,
            'max_retries': max_retries
        }
        
        # 创建LokiHandler
        loki_endpoint = self._config.get('endpoints', {}).get('loki')
        if loki_endpoint:
            self._loki_handler = LokiHandler(
                url=loki_endpoint,
                tags={"app": app_name, "environment": environment},
                version="1",
            )
        
        # 启动工作线程
        if enable_offline_buffer:
            self._start_worker()
    
    def _start_worker(self):
        """启动后台工作线程"""
        if self._worker_thread is None or not self._worker_thread.is_alive():
            self._running = True
            self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
            self._worker_thread.start()
    
    def _worker_loop(self):
        """工作线程主循环"""
        while self._running:
            try:
                # 处理缓冲区中的日志
                self._process_buffer()
                time.sleep(self._config.get('flush_interval', 5))
            except Exception as e:
                # 工作线程异常不应该影响主程序
                print(f"Loki SDK worker thread error: {e}")
                time.sleep(1)
    
    def _process_buffer(self):
        """处理缓冲区中的日志"""
        logs_to_send = []
        
        # 收集缓冲区中的日志
        while not self._buffer.empty() and len(logs_to_send) < self._config.get('buffer_size', 1000):
            try:
                log_entry = self._buffer.get_nowait()
                logs_to_send.append(log_entry)
            except queue.Empty:
                break
        
        if logs_to_send and self._loki_handler:
            self._send_logs_to_loki(logs_to_send)
    
    def _send_logs_to_loki(self, logs: List[Dict[str, Any]]):
        """发送日志到Loki服务器"""
        if not logs or not self._loki_handler:
            return
        
        # 使用LokiHandler发送日志
        for log_entry in logs:
            try:
                # 创建LogRecord
                record = logging.LogRecord(
                    name=log_entry.get('logger', 'loki_sdk'),
                    level=getattr(logging, log_entry.get('level', 'INFO')),
                    pathname='',
                    lineno=0,
                    msg=log_entry.get('message', ''),
                    args=(),
                    exc_info=None
                )
                
                # 添加额外属性
                for key, value in log_entry.get('labels', {}).items():
                    setattr(record, key, value)
                
                # 发送日志
                self._loki_handler.emit(record)
                
            except Exception as e:
                print(f"Loki SDK: 发送日志异常: {e}")
    
    def log(self, level: str, message: str, **kwargs):
        """
        记录日志
        
        Args:
            level: 日志级别 (debug, info, warning, error, critical)
            message: 日志消息
            **kwargs: 额外的标签和元数据
        """
        # 构建日志条目
        log_entry = {
            'timestamp': time.time(),
            'level': level.upper(),
            'message': message,
            'labels': {
                'app': self._config.get('app_name', 'unknown'),
                'environment': self._config.get('environment', 'production'),
                'level': level.upper()
            }
        }
        
        # 添加额外标签
        for key, value in kwargs.items():
            if key.startswith('label_'):
                # 标签以label_开头
                label_key = key[6:]  # 移除'label_'前缀
                log_entry['labels'][label_key] = str(value)
            elif key == 'labels' and isinstance(value, dict):
                # 直接传入labels字典
                log_entry['labels'].update(value)
            else:
                # 其他参数作为元数据
                if 'metadata' not in log_entry:
                    log_entry['metadata'] = {}
                log_entry['metadata'][key] = value
        
        # 添加到缓冲区
        if self._config.get('enable_offline_buffer', True):
            try:
                self._buffer.put_nowait(log_entry)
            except queue.Full:
                # 缓冲区满了，丢弃最旧的日志
                try:
                    self._buffer.get_nowait()
                    self._buffer.put_nowait(log_entry)
                except queue.Empty:
                    pass
        
        # 如果启用异步发送，立即发送
        if self._config.get('use_send_beacon', True) and not self._config.get('enable_offline_buffer', True):
            self._send_logs_to_loki([log_entry])
    
    def debug(self, message: str, **kwargs):
        """记录调试日志"""
        self.log('debug', message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """记录信息日志"""
        self.log('info', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """记录警告日志"""
        self.log('warning', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """记录错误日志"""
        self.log('error', message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """记录严重错误日志"""
        self.log('critical', message, **kwargs)
    
    def flush(self):
        """强制刷新缓冲区"""
        self._process_buffer()
    
    def _cleanup(self):
        """清理资源"""
        self._running = False
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=5)
        self.flush()
        self._session.close()


# 全局SDK实例
_sdk_instance = None


def get_sdk() -> LokiSDK:
    """获取全局SDK实例"""
    global _sdk_instance
    if _sdk_instance is None:
        _sdk_instance = LokiSDK()
    return _sdk_instance


def init_sdk(**kwargs):
    """初始化全局SDK"""
    sdk = get_sdk()
    sdk.init(**kwargs)


def log(level: str, message: str, **kwargs):
    """全局日志函数"""
    sdk = get_sdk()
    sdk.log(level, message, **kwargs)


def debug(message: str, **kwargs):
    """全局调试日志"""
    log('debug', message, **kwargs)


def info(message: str, **kwargs):
    """全局信息日志"""
    log('info', message, **kwargs)


def warning(message: str, **kwargs):
    """全局警告日志"""
    log('warning', message, **kwargs)


def error(message: str, **kwargs):
    """全局错误日志"""
    log('error', message, **kwargs)


def critical(message: str, **kwargs):
    """全局严重错误日志"""
    log('critical', message, **kwargs)


def flush():
    """全局刷新函数"""
    sdk = get_sdk()
    sdk.flush()
