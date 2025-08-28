#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Loki SDK 使用示例
演示如何使用Loki SDK发送日志到Loki服务器
"""

import time
import threading
from loki_sdk import init_sdk, debug, info, warning, error, critical, flush


def example_basic_usage():
    """示例1: 基本使用"""
    print("=== 示例1: 基本使用 ===")
    
    # 初始化SDK（参考H5 SDK格式）
    init_sdk(
        app_name="demo-python",
        environment="staging",
        endpoints={"loki": "http://47.77.196.223:3100/loki/api/v1/push"},
        use_send_beacon=True,
        enable_offline_buffer=True,
        buffer_size=1000,
        flush_interval=5,
        max_retries=3
    )
    
    # 发送不同级别的日志
    debug("这是一条调试日志", label_user_id="12345", label_action="login")
    info("用户登录成功", label_user_id="12345", label_action="login")
    warning("用户尝试访问受限资源", label_user_id="12345", label_action="access_denied")
    error("数据库连接失败", label_component="database", label_error_code="DB001")
    critical("系统严重错误，需要立即处理", label_component="system", label_priority="high")
    
    # 使用自定义标签
    info("自定义标签示例", 
         labels={"service": "user-service", "version": "1.0.0", "region": "us-west-1"})
    
    # 强制刷新缓冲区
    flush()
    
    print("基本使用示例完成\n")


def example_concurrent_logging():
    """示例2: 并发日志发送"""
    print("=== 示例2: 并发日志发送 ===")
    
    # 初始化SDK
    init_sdk(
        app_name="demo-concurrent",
        environment="production",
        endpoints={"loki": "http://47.77.196.223:3100/loki/api/v1/push"},
        enable_offline_buffer=True,
        buffer_size=2000,
        flush_interval=2
    )
    
    def worker(worker_id):
        """工作线程函数"""
        for i in range(10):
            info(f"工作线程 {worker_id} 处理任务 {i}", 
                 label_worker_id=str(worker_id), 
                 label_task_id=str(i))
            time.sleep(0.1)
    
    # 启动多个工作线程
    threads = []
    for i in range(5):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    # 强制刷新
    flush()
    
    print("并发日志示例完成\n")


def example_custom_sdk():
    """示例3: 自定义SDK实例"""
    print("=== 示例3: 自定义SDK实例 ===")
    
    # 创建自定义SDK实例
    from loki_sdk import LokiSDK
    
    custom_sdk = LokiSDK()
    custom_sdk.init(
        app_name="custom-app",
        environment="development",
        endpoints={"loki": "http://47.77.196.223:3100/loki/api/v1/push"},
        use_send_beacon=False,  # 禁用异步发送
        enable_offline_buffer=True,
        buffer_size=100,
        flush_interval=1,
        max_retries=5
    )
    
    # 使用自定义SDK发送日志
    custom_sdk.info("自定义SDK测试", label_test_type="custom_sdk")
    custom_sdk.warning("自定义配置警告", label_config="development")
    
    # 清理
    custom_sdk.flush()
    
    print("自定义SDK示例完成\n")


if __name__ == "__main__":
    print("Loki SDK Python 示例程序")
    print("=" * 50)
    
    try:
        # 运行所有示例
        example_basic_usage()
        example_concurrent_logging()
        example_custom_sdk()
        
        print("所有示例执行完成！")
        print("\n注意事项：")
        print("1. 确保Loki服务器正在运行并可访问")
        print("2. 修改endpoints中的URL为你的实际Loki服务器地址")
        print("3. 本地控制台日志输出不受影响")
        print("4. 日志会异步发送到Loki服务器")
        
    except Exception as e:
        print(f"示例执行出错: {e}")
        print("请检查Loki服务器配置和网络连接")
