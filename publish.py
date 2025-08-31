#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发布脚本 - 用于将loki-sdk-py发布到PyPI
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """运行命令并处理错误"""
    print(f"正在{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description}成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"✗ {description}失败: {e}")
        print(f"错误输出: {e.stderr}")
        sys.exit(1)

def clean_build():
    """清理构建文件"""
    print("正在清理构建文件...")
    dirs_to_clean = ['dist', 'build']
    files_to_clean = ['*.egg-info']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ 删除目录: {dir_name}")
    
    for pattern in files_to_clean:
        for file_path in Path('.').glob(pattern):
            if file_path.is_dir():
                shutil.rmtree(file_path)
            else:
                file_path.unlink()
            print(f"✓ 删除文件: {file_path}")

def build_package():
    """构建包"""
    run_command("python -m build", "构建包")

def check_package():
    """检查包"""
    run_command("twine check dist/*", "检查包")

def upload_to_testpypi():
    """上传到测试PyPI"""
    print("正在上传到测试PyPI...")
    print("请确保你已经注册了TestPyPI账号: https://test.pypi.org/account/register/")
    input("按回车键继续...")
    run_command("twine upload --repository testpypi dist/*", "上传到测试PyPI")

def upload_to_pypi():
    """上传到正式PyPI"""
    print("正在上传到正式PyPI...")
    print("请确保你已经注册了PyPI账号: https://pypi.org/account/register/")
    input("按回车键继续...")
    run_command("twine upload dist/*", "上传到正式PyPI")

def test_install():
    """测试安装"""
    print("正在测试安装...")
    run_command("pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ loki-sdk-py", "从测试PyPI安装")
    
    # 测试导入
    try:
        import loki_sdk
        print("✓ 导入测试成功")
        print(f"版本: {loki_sdk.__version__}")
    except ImportError as e:
        print(f"✗ 导入测试失败: {e}")
        sys.exit(1)

def main():
    """主函数"""
    print("=== Loki SDK Python 发布工具 ===")
    print()
    
    while True:
        print("请选择操作:")
        print("1. 清理构建文件")
        print("2. 构建包")
        print("3. 检查包")
        print("4. 上传到测试PyPI")
        print("5. 上传到正式PyPI")
        print("6. 测试安装")
        print("7. 完整发布流程 (清理 -> 构建 -> 检查 -> 上传到测试PyPI)")
        print("8. 退出")
        print()
        
        choice = input("请输入选项 (1-8): ").strip()
        
        if choice == '1':
            clean_build()
        elif choice == '2':
            build_package()
        elif choice == '3':
            check_package()
        elif choice == '4':
            upload_to_testpypi()
        elif choice == '5':
            upload_to_pypi()
        elif choice == '6':
            test_install()
        elif choice == '7':
            print("开始完整发布流程...")
            clean_build()
            build_package()
            check_package()
            upload_to_testpypi()
            print("✓ 完整发布流程完成！")
        elif choice == '8':
            print("退出程序")
            break
        else:
            print("无效选项，请重新选择")
        
        print()

if __name__ == "__main__":
    main()
