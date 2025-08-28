# 发布指南

## 发布到PyPI

### 1. 准备工作

1. 注册PyPI账号：https://pypi.org/account/register/
2. 安装发布工具：
   ```bash
   pip install twine build
   ```

### 2. 更新版本号

在以下文件中更新版本号：
- `setup.py` 中的 `version`
- `loki_sdk/__init__.py` 中的 `__version__`

### 3. 构建包

```bash
python -m build
```

### 4. 检查构建结果

```bash
twine check dist/*
```

### 5. 上传到PyPI

```bash
# 上传到测试PyPI（推荐先测试）
twine upload --repository testpypi dist/*

# 上传到正式PyPI
twine upload dist/*
```

### 6. 验证安装

```bash
# 从测试PyPI安装
pip install --index-url https://test.pypi.org/simple/ loki-sdk-py

# 从正式PyPI安装
pip install loki-sdk-py
```

## 发布到GitHub

### 1. 创建GitHub仓库

1. 在GitHub上创建新仓库
2. 更新 `setup.py` 中的URL和项目链接

### 2. 推送代码

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/loki-sdk-py.git
git push -u origin main
```

### 3. 创建Release

1. 在GitHub上创建新的Release
2. 添加版本标签（如 v1.0.0）
3. 添加发布说明

## 注意事项

1. 确保所有文件都使用UTF-8编码
2. 测试包在不同Python版本下的兼容性
3. 更新文档中的示例代码
4. 检查所有依赖项是否正确列出
