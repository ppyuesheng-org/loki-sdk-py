# Loki SDK for Python

基于`python-logging-loki`的Python日志SDK，支持异步发送日志到Loki服务器，不影响本地控制台日志输出。

## 特性

- 🚀 **异步发送**: 使用后台线程异步发送日志，不阻塞主程序
- 📦 **离线缓冲**: 支持离线缓冲，网络异常时不会丢失日志
- 🔧 **灵活配置**: 支持多种配置选项，适应不同场景
- 🏷️ **丰富标签**: 支持自定义标签和元数据
- 🛡️ **异常安全**: 异常处理机制，确保主程序稳定运行
- 🔄 **自动重试**: 网络异常时自动重试，支持指数退避

## 安装

```bash
pip install loki-sdk-py
```

## 快速开始

### 基本使用

```python
from loki_sdk import init_sdk, info, error, flush

# 初始化SDK（参考H5 SDK格式）
init_sdk(
    app_name="demo-python",
    environment="staging",
    endpoints={"loki": "https://loki.example.com/loki/api/v1/push"},
    use_send_beacon=True,
    enable_offline_buffer=True,
    buffer_size=1000,
    flush_interval=5,
    max_retries=3
)

# 发送日志
info("用户登录成功", label_user_id="12345", label_action="login")
error("数据库连接失败", label_component="database", label_error_code="DB001")

# 强制刷新缓冲区
flush()
```

### 自定义SDK实例

```python
from loki_sdk import LokiSDK

# 创建自定义SDK实例
custom_sdk = LokiSDK()
custom_sdk.init(
    app_name="custom-app",
    environment="development",
    endpoints={"loki": "http://localhost:3100/loki/api/v1/push"},
    use_send_beacon=False,  # 禁用异步发送
    enable_offline_buffer=True,
    buffer_size=100,
    flush_interval=1,
    max_retries=5
)

# 使用自定义SDK
custom_sdk.info("自定义SDK测试", label_test_type="custom_sdk")
custom_sdk.flush()
```

## 配置参数

### LokiSDK.init() 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `app_name` | str | - | 应用名称（必需） |
| `environment` | str | "production" | 环境（production, staging, development等） |
| `endpoints` | dict | `{"loki": "http://localhost:3100/loki/api/v1/push"}` | 端点配置 |
| `use_send_beacon` | bool | True | 是否使用异步发送 |
| `enable_offline_buffer` | bool | True | 是否启用离线缓冲 |
| `buffer_size` | int | 1000 | 缓冲区大小 |
| `flush_interval` | int | 5 | 刷新间隔（秒） |
| `max_retries` | int | 3 | 最大重试次数 |

## 日志级别

支持以下日志级别：

- `debug()`: 调试信息
- `info()`: 一般信息
- `warning()`: 警告信息
- `error()`: 错误信息
- `critical()`: 严重错误

## 标签和元数据

### 使用label_前缀添加标签

```python
info("用户操作", label_user_id="12345", label_action="login", label_service="auth")
```

### 直接传入labels字典

```python
info("系统信息", labels={
    "service": "user-service",
    "version": "1.0.0",
    "region": "us-west-1"
})
```

### 添加元数据

```python
info("业务操作", 
     label_user_id="12345",
     operation_type="payment",
     amount=100.50,
     currency="USD")
```

## 并发日志发送

```python
import threading
import time
from loki_sdk import init_sdk, info, flush

init_sdk(
    app_name="demo-concurrent",
    environment="production",
    endpoints={"loki": "https://loki.example.com/loki/api/v1/push"},
    enable_offline_buffer=True,
    buffer_size=2000,
    flush_interval=2
)

def worker(worker_id):
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

flush()
```

## 示例

运行示例程序：

```bash
python example.py
```

## 注意事项

1. **Loki服务器**: 确保Loki服务器正在运行并可访问
2. **网络连接**: SDK会自动处理网络异常和重试
3. **本地日志**: 不会影响本地控制台日志输出
4. **资源清理**: 程序退出时会自动清理资源
5. **线程安全**: 支持多线程并发使用

## 错误处理

SDK内置了完善的错误处理机制：

- 网络异常时自动重试，支持指数退避
- 缓冲区满时丢弃最旧的日志
- 工作线程异常不会影响主程序
- 程序退出时自动清理资源

## 许可证

MIT License
