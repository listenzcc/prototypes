# Logging Levels Doc

[toc]

## 代码的 logging 级别， debug 和 info 何时使用，有何区别？

在代码中使用 logging 时，`debug` 和 `info` 是两种常用的日志级别，它们的核心区别在于**使用场景和目标受众**。以下是具体区别和使用时机：

---

### **1. DEBUG 级别**

- **用途**：记录详细的调试信息，用于开发或排查问题时了解程序内部状态。
- **使用场景**：
  - 打印变量值、循环进度、条件分支的进入/退出。
  - 记录函数调用的参数、中间结果或复杂计算的步骤。
  - 临时性日志，问题解决后可能移除或保留（但通常不输出到生产环境）。
- **目标受众**：开发人员。
- **示例**：

  ```python
  logger.debug(f"Processing item {item_id}, current state: {state}")
  logger.debug(f"API request params: {params}")
  ```

---

### **2. INFO 级别**

- **用途**：记录程序正常运行时的关键事件，用于跟踪业务流程。
- **使用场景**：
  - 记录系统启动/关闭、配置加载完成等生命周期事件。
  - 用户操作（如登录、订单提交）、外部调用（如 API 请求发送）。
  - 业务逻辑中的重要步骤（如“支付成功”“数据已保存”）。
- **目标受众**：运维人员、技术支持或需要监控系统状态的用户。
- **示例**：

  ```python
  logger.info("Server started on port 8080")
  logger.info(f"User {user_id} logged in successfully")
  ```

---

### **关键区别**

| 特性         | DEBUG                          | INFO             |
| ------------ | ------------------------------ | ---------------- |
| **重要性**   | 低（细节信息）                 | 中（关键事件）   |
| **使用阶段** | 开发/测试环境                  | 开发 + 生产环境  |
| **日志量**   | 多（高频、详细）               | 少（仅重要节点） |
| **性能影响** | 可能较大（需避免生产环境开启） | 通常可接受       |

---

### **最佳实践**

1. **环境区分**：

   - 开发环境：默认输出 `DEBUG` 及以上级别。
   - 生产环境：通常只输出 `INFO` 或更高级别（如 `WARNING`）。

   ```python
   logging.basicConfig(level=logging.DEBUG)  # 开发
   logging.basicConfig(level=logging.INFO)   # 生产
   ```

2. **避免过度使用 INFO**：

   - 如果日志用于临时调试，用 `DEBUG`；如果事件对运维有意义，用 `INFO`。

3. **结构化日志**：
   - 在复杂系统中，可通过额外字段（如 `user_id`、`request_id`）增强日志可读性。

---

### **总结**

- **DEBUG**：“这个函数内部发生了什么？” → 给开发者看。
- **INFO**：“系统正在做什么？” → 给运维和监控看。

合理使用这两个级别，既能保证问题排查效率，又能避免生产环境日志爆炸。

## 为什么是 sys.stderr 而不是 sys.stdout

在 Loguru（以及大多数日志系统）中，默认使用 `sys.stderr`（标准错误流）而非 `sys.stdout`（标准输出流）输出日志，主要基于以下几个原因：

---

### **1. 分离日志与正常输出**

- **`stdout`**  
  通常用于程序的**预期输出**（如计算结果、用户可见的内容），属于业务逻辑的一部分。  
  例如：`print("计算结果:", x)`。

- **`stderr`**  
  专门用于**错误、警告、日志等非预期输出**，与业务逻辑解耦。  
  例如：`logger.error("文件读取失败")`。

**优势**：

- 避免日志混杂在正常输出中，影响其他程序解析（如管道操作 `|` 或重定向 `>`）。
- 方便单独重定向错误流（如 `2> error.log`）。

---

### **2. 避免缓冲问题**

- **`stdout`**  
  通常是**行缓冲**（遇到换行符 `\n` 才刷新）或**全缓冲**（缓冲区满才刷新），可能导致日志延迟显示。

- **`stderr`**  
  默认是**无缓冲**（立即刷新），确保日志实时输出，尤其在崩溃或死锁时能立即看到错误。

**场景**：  
 当程序崩溃时，`stderr` 的日志能立即显示，而 `stdout` 可能因缓冲未刷新而丢失。

---

### **3. 遵循 Unix/Linux 惯例**

Unix 系操作系统约定：

- `stdout`：正常输出，可被重定向（如 `> file`）。
- `stderr`：错误和诊断信息，默认显示在终端，便于调试。

**工具兼容性**：  
 日志默认到 `stderr` 后，可以通过 shell 灵活处理：

```bash
python app.py > output.log 2> error.log  # 分离业务输出和日志
python app.py 2>&1 | grep "ERROR"       # 合并流并过滤
```

---

### **4. 防止日志干扰管道操作**

若日志输出到 `stdout`，通过管道传递数据时会被污染：

```bash
python generate_data.py | jq .  # 如果日志混在 stdout，jq 会解析失败
```

而日志到 `stderr` 后，管道仅处理 `stdout` 的纯净数据。

---

### **何时使用 `stdout` 输出日志？**

少数场景可能需要：

1. **特定日志分析工具**：某些工具明确要求日志从 `stdout` 采集（如 Docker 容器日志）。
2. **自定义日志架构**：需要统一将所有输出（包括日志）写入同一个文件。

此时可显式配置：

```python
logger.add(sys.stdout, level="INFO")  # 强制使用 stdout
```

---

### **总结**

| 特性             | `sys.stderr` (默认)  | `sys.stdout`              |
| ---------------- | -------------------- | ------------------------- |
| **用途**         | 错误、日志、诊断信息 | 正常业务输出              |
| **缓冲**         | 无缓冲（实时）       | 行缓冲/全缓冲（可能延迟） |
| **重定向友好性** | 易分离日志与业务数据 | 易混杂日志与输出          |
| **系统约定**     | Unix 标准错误流      | Unix 标准输出流           |

Loguru 选择 `stderr` 是为了遵循行业惯例、保证实时性，并与现有工具链兼容。如果需要更改，只需在 `logger.add()` 中显式指定 `sink=sys.stdout`。

## loguru 如何记录 traceback

在 **Loguru** 中记录 `traceback`（异常堆栈信息）非常简单，主要通过以下两种方式实现：

---

### **1. 使用 `logger.exception()` 自动捕获并记录 traceback**

当在 `try-except` 块中捕获异常时，`logger.exception()` 会自动记录完整的 `traceback` 信息（类似于 `logger.error()`，但会额外附加异常堆栈）。

#### **示例代码**

```python
from loguru import logger

try:
    1 / 0  # 触发 ZeroDivisionError
except Exception:
    logger.exception("发生异常！")  # 自动记录 traceback
```

#### **输出示例**

```
2024-05-06 12:00:00.000 | ERROR    | __main__:<module>:6 - 发生异常！
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ZeroDivisionError: division by zero
```

##### **特点**

- 自动关联当前捕获的异常，无需手动提取 `traceback`。
- 日志级别默认是 `ERROR`，但可以用 `logger.opt(exception=True).warning(...)` 调整级别。

---

### **2. 使用 `logger.opt(exception=True)` 记录任意异常**

如果不想用 `logger.exception()`，但仍然想记录 `traceback`，可以用 `logger.opt(exception=True)`。

#### **示例代码**

```python
from loguru import logger

try:
    raise ValueError("Oops!")
except Exception as e:
    logger.opt(exception=True).error("捕获到异常")  # 手动记录 traceback
```

#### **输出示例**

```
2024-05-06 12:00:00.000 | ERROR    | __main__:<module>:6 - 捕获到异常
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ValueError: Oops!
```

##### **适用场景**

- 需要自定义日志级别（如 `warning`、`critical`）但仍需记录 `traceback`。
- 需要额外添加上下文信息（如变量值）。

---

### **3. 手动提取并记录 traceback（高级用法）**

如果希望更灵活地控制 `traceback` 的格式，可以使用 `traceback` 模块手动提取并传给 Loguru。

#### **示例代码**

```python
import traceback
from loguru import logger

try:
    1 / 0
except Exception:
    tb = traceback.format_exc()  # 获取 traceback 字符串
    logger.error(f"异常发生！\n{tb}")  # 手动记录
```

#### **输出示例**

```
2024-05-06 12:00:00.000 | ERROR    | __main__:<module>:7 - 异常发生！
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ZeroDivisionError: division by zero
```

#### **适用场景**

- 需要自定义 `traceback` 的格式（如只保留部分堆栈）。
- 需要将 `traceback` 存储到数据库或发送到外部监控系统。

---

### **4. 全局捕获未处理异常（崩溃日志）**

Loguru 可以自动捕获未被 `try-except` 处理的异常并记录 `traceback`，使用 `logger.catch()` 装饰器。

#### **示例代码**

```python
from loguru import logger

@logger.catch
def risky_function():
    1 / 0  # 未捕获的异常会自动记录

risky_function()
```

#### **输出示例**

```
2024-05-06 12:00:00.000 | ERROR    | __main__:<module>:6 - An error occurred
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "<stdin>", line 4, in risky_function
ZeroDivisionError: division by zero
```

#### **适用场景**

- 确保程序崩溃时仍有完整的 `traceback` 记录。
- 适用于长期运行的服务（如 Web 服务器）。

---

### **总结**

| 方法                         | 适用场景                    | 特点                                    |
| ---------------------------- | --------------------------- | --------------------------------------- |
| `logger.exception()`         | `try-except` 块内自动记录   | 默认 `ERROR` 级别，自动附加 `traceback` |
| `logger.opt(exception=True)` | 需要自定义日志级别          | 灵活控制日志级别                        |
| `traceback.format_exc()`     | 需要自定义 `traceback` 格式 | 手动提取堆栈信息                        |
| `logger.catch()`             | 全局捕获未处理异常          | 防止程序崩溃无日志                      |

**推荐做法**：

- 在 `try-except` 块内优先使用 `logger.exception()`。
- 在长期运行的服务中使用 `logger.catch()` 确保崩溃可追溯。
