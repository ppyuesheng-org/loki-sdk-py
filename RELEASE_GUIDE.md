# 发布指南

## 快速发布

### 方法1: 使用发布脚本（推荐）

```bash
# 如果在虚拟环境中，先安装发布工具
python install_tools.py

# 运行发布脚本
python publish.py
```

然后选择选项7进行完整发布流程。

### 方法2: 手动发布

#### 1. 安装发布工具
```bash
# 方法1: 直接安装
pip install twine build

# 方法2: 使用安装脚本（推荐）
python install_tools.py
```

#### 2. 构建包
```bash
python -m build
```

#### 3. 检查包
```bash
twine check dist/*
```

#### 4. 上传到测试PyPI（推荐先测试）
```bash
twine upload --repository testpypi dist/*
```

#### 5. 测试安装
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ loki-sdk-py
```

#### 6. 上传到正式PyPI
```bash
twine upload dist/*
```

## 账号注册

在发布之前，你需要注册以下账号：

1. **TestPyPI账号**: https://test.pypi.org/account/register/
   - 用于测试发布
   - 免费注册

2. **PyPI账号**: https://pypi.org/account/register/
   - 用于正式发布
   - 免费注册

## 版本更新

发布新版本时，需要更新以下文件中的版本号：

1. `setup.py` 中的 `version`
2. `pyproject.toml` 中的 `version`
3. `loki_sdk/__init__.py` 中的 `__version__`

## 注意事项

1. 确保所有文件都使用UTF-8编码
2. 测试包在不同Python版本下的兼容性
3. 更新文档中的示例代码
4. 检查所有依赖项是否正确列出
5. 建议先在TestPyPI上测试，确认无误后再发布到正式PyPI

## 安装使用

发布成功后，用户可以通过以下命令安装：

```bash
# 从正式PyPI安装
pip install loki-sdk-py

# 从测试PyPI安装
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ loki-sdk-py
```

## 使用示例

```python
from loki_sdk import init_sdk, log, info, error

# 初始化SDK
init_sdk(
    loki_url="http://localhost:3100",
    tags={"service": "my-app", "environment": "production"}
)

# 使用日志
info("应用启动成功")
error("发生错误", extra={"error_code": 500})
```
