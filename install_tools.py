#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装发布工具脚本
"""

import subprocess
import sys

def install_tools():
    """安装发布工具到当前环境"""
    tools = ["twine", "build"]
    
    print("正在安装发布工具...")
    
    for tool in tools:
        print(f"安装 {tool}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", tool], check=True)
            print(f"✓ {tool} 安装成功")
        except subprocess.CalledProcessError as e:
            print(f"✗ {tool} 安装失败: {e}")
            return False
    
    print("✓ 所有工具安装完成！")
    return True

if __name__ == "__main__":
    install_tools()
