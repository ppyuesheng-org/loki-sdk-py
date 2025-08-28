# Loki SDK for Python

A Python SDK for sending logs to Loki server, based on `python-logging-loki`. Supports asynchronous log sending without affecting local console output.

## Features

- 🚀 **Asynchronous Sending**: Uses background threads for asynchronous log sending
- 📦 **Offline Buffer**: Supports offline buffering, logs won't be lost during network issues
- 🔧 **Flexible Configuration**: Multiple configuration options for different scenarios
- 🏷️ **Rich Labels**: Support for custom labels and metadata
- 🛡️ **Exception Safe**: Exception handling mechanism ensures stable program operation
- 🔄 **Auto Retry**: Automatic retry with exponential backoff for network issues

## Installation

```bash
pip install loki-sdk-py
```

## Quick Start

### Basic Usage

```python
from loki_sdk import init_sdk, info, error, flush

# Initialize SDK (similar to H5 SDK format)
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

# Send logs
info("User login successful", label_user_id="12345", label_action="login")
error("Database connection failed", label_component="database", label_error_code="DB001")

# Force flush buffer
flush()
```

### Custom SDK Instance

```python
from loki_sdk import LokiSDK

# Create custom SDK instance
custom_sdk = LokiSDK()
custom_sdk.init(
    app_name="custom-app",
    environment="development",
    endpoints={"loki": "http://localhost:3100/loki/api/v1/push"},
    use_send_beacon=False,
    enable_offline_buffer=True,
    buffer_size=100,
    flush_interval=1,
    max_retries=5
)

# Use custom SDK
custom_sdk.info("Custom SDK test", label_test_type="custom_sdk")
custom_sdk.flush()
```

## Configuration Parameters

### LokiSDK.init() Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `app_name` | str | - | Application name (required) |
| `environment` | str | "production" | Environment (production, staging, development, etc.) |
| `endpoints` | dict | `{"loki": "http://localhost:3100/loki/api/v1/push"}` | Endpoint configuration |
| `use_send_beacon` | bool | True | Whether to use asynchronous sending |
| `enable_offline_buffer` | bool | True | Whether to enable offline buffering |
| `buffer_size` | int | 1000 | Buffer size |
| `flush_interval` | int | 5 | Flush interval (seconds) |
| `max_retries` | int | 3 | Maximum retry attempts |

## Log Levels

Supports the following log levels:

- `debug()`: Debug information
- `info()`: General information
- `warning()`: Warning information
- `error()`: Error information
- `critical()`: Critical error

## Labels and Metadata

### Using label_ prefix for labels

```python
info("User operation", label_user_id="12345", label_action="login", label_service="auth")
```

### Direct labels dictionary

```python
info("System information", labels={
    "service": "user-service",
    "version": "1.0.0",
    "region": "us-west-1"
})
```

### Adding metadata

```python
info("Business operation", 
     label_user_id="12345",
     operation_type="payment",
     amount=100.50,
     currency="USD")
```

## Concurrent Logging

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
        info(f"Worker {worker_id} processing task {i}", 
             label_worker_id=str(worker_id), 
             label_task_id=str(i))
        time.sleep(0.1)

# Start multiple worker threads
threads = []
for i in range(5):
    thread = threading.Thread(target=worker, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

flush()
```

## Examples

Run the example program:

```bash
python example.py
```

## Notes

1. **Loki Server**: Ensure the Loki server is running and accessible
2. **Network Connection**: SDK automatically handles network exceptions and retries
3. **Local Logs**: Does not affect local console log output
4. **Resource Cleanup**: Automatically cleans up resources when program exits
5. **Thread Safe**: Supports multi-threaded concurrent usage

## Error Handling

The SDK has built-in comprehensive error handling:

- Automatic retry with exponential backoff for network exceptions
- Discard oldest logs when buffer is full
- Worker thread exceptions don't affect the main program
- Automatic resource cleanup when program exits

## License

MIT License
