#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python环境测试脚本
"""

import sys
import os

def main():
    print("Python环境测试")
    print("=" * 30)
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Python路径列表:")
    for path in sys.path:
        print(f"  - {path}")
    
    # 测试基本功能
    print("\n基本功能测试:")
    print("1. 基本运算:", 2 + 2)
    print("2. 字符串操作:", "Hello" + " World")
    print("3. 列表操作:", [1, 2, 3] + [4, 5, 6])
    
    # 测试导入
    print("\n导入测试:")
    try:
        import json
        print("✓ json模块导入成功")
    except ImportError as e:
        print(f"✗ json模块导入失败: {e}")
    
    try:
        import requests
        print("✓ requests模块导入成功")
    except ImportError as e:
        print(f"✗ requests模块导入失败: {e}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    main()
