# MCP Python SDK

<div align="center">

<strong>模型上下文协议 (Model Context Protocol) 的 Python 实现</strong>

[![PyPI][pypi-badge]][pypi-url]
[![MIT licensed][mit-badge]][mit-url]
[![Python Version][python-badge]][python-url]
[![Documentation][docs-badge]][docs-url]
[![Protocol][protocol-badge]][protocol-url]
[![Specification][spec-badge]][spec-url]

</div>

<!-- omit in toc -->
## 目录

- [MCP Python SDK](#mcp-python-sdk)
  - [概述](#概述)
  - [安装](#安装)
    - [将 MCP 添加到 Python 项目](#将-mcp-添加到-python-项目)
    - [运行独立的 MCP 开发工具](#运行独立的-mcp-开发工具)
  - [快速开始](#快速开始)
  - [什么是 MCP？](#什么是-mcp)
  - [核心概念](#核心概念)
    - [服务器](#服务器)
    - [资源](#资源)
    - [工具](#工具)
      - [结构化输出](#结构化输出)
        - [高级：直接返回 CallToolResult](#高级直接返回-calltoolresult)
    - [提示](#提示)
    - [图标](#图标)
    - [图像](#图像)
    - [上下文](#上下文)
      - [在函数中获取上下文](#在函数中获取上下文)
      - [上下文属性和方法](#上下文属性和方法)
    - [补全](#补全)
    - [征询](#征询)
    - [采样](#采样)
    - [日志记录和通知](#日志记录和通知)
    - [认证](#认证)
    - [FastMCP 属性](#fastmcp-属性)
    - [会话属性和方法](#会话属性和方法)
    - [请求上下文属性](#请求上下文属性)
  - [运行服务器](#运行服务器)
    - [开发模式](#开发模式)
    - [Claude Desktop 集成](#claude-desktop-集成)
    - [直接执行](#直接执行)
    - [流式 HTTP 传输](#流式-http-传输)
      - [浏览器客户端的 CORS 配置](#浏览器客户端的-cors-配置)
    - [挂载到现有 ASGI 服务器](#挂载到现有-asgi-服务器)
      - [StreamableHTTP 服务器](#streamablehttp-服务器)
        - [基本挂载](#基本挂载)
        - [基于主机的路由](#基于主机的路由)
        - [具有路径配置的多个服务器](#具有路径配置的多个服务器)
        - [初始化时的路径配置](#初始化时的路径配置)
      - [SSE 服务器](#sse-服务器)
  - [高级用法](#高级用法)
    - [低级服务器](#低级服务器)
      - [结构化输出支持](#结构化输出支持)
        - [直接返回 CallToolResult](#直接返回-calltoolresult)
    - [分页（高级）](#分页高级)
      - [服务器端实现](#服务器端实现)
      - [客户端消费](#客户端消费)
      - [关键点](#关键点)
    - [编写 MCP 客户端](#编写-mcp-客户端)
    - [客户端显示工具](#客户端显示工具)
    - [客户端的 OAuth 认证](#客户端的-oauth-认证)
    - [解析工具结果](#解析工具结果)
  - [文档](#文档)
  - [贡献](#贡献)
  - [许可证](#许可证)

[pypi-badge]: https://img.shields.io/pypi/v/mcp.svg
[pypi-url]: https://pypi.org/project/mcp/
[mit-badge]: https://img.shields.io/pypi/l/mcp.svg
[mit-url]: https://github.com/modelcontextprotocol/python-sdk/blob/main/LICENSE
[python-badge]: https://img.shields.io/pypi/pyversions/mcp.svg
[python-url]: https://www.python.org/downloads/
[docs-badge]: https://img.shields.io/badge/docs-python--sdk-blue.svg
[docs-url]: https://modelcontextprotocol.github.io/python-sdk/
[protocol-badge]: https://img.shields.io/badge/protocol-modelcontextprotocol.io-blue.svg
[protocol-url]: https://modelcontextprotocol.io
[spec-badge]: https://img.shields.io/badge/spec-spec.modelcontextprotocol.io-blue.svg
[spec-url]: https://spec.modelcontextprotocol.io

## 概述

模型上下文协议 (Model Context Protocol) 以标准化方式允许应用程序为 LLM 提供上下文，将提供上下文的关注点与实际 LLM 交互分离。这个 Python SDK 实现了完整的 MCP 规范，使构建以下内容变得简单：

- 构建可以连接到任何 MCP 服务器的 MCP 客户端
- 创建暴露资源、提示和工具的 MCP 服务器
- 使用标准传输如 stdio、SSE 和流式 HTTP
- 处理所有 MCP 协议消息和生命周期事件

## 安装

### 将 MCP 添加到 Python 项目

我们推荐使用 [uv](https://docs.astral.sh/uv/) 来管理 Python 项目。

如果您还没有创建 uv 管理的项目，请创建一个：

   ```bash
   uv init mcp-server-demo
   cd mcp-server-demo
   ```

   然后将 MCP 添加到项目依赖中：

   ```bash
   uv add "mcp[cli]"
   ```

或者，对于使用 pip 管理依赖的项目：

```bash
pip install "mcp[cli]"
```

### 运行独立的 MCP 开发工具

使用 uv 运行 mcp 命令：

```bash
uv run mcp
```

## 快速开始

让我们创建一个暴露计算器工具和一些数据的简单 MCP 服务器：

<!-- snippet-source examples/snippets/servers/fastmcp_quickstart.py -->
```python
"""
FastMCP 快速开始示例。

cd 到 `examples/snippets/clients` 目录并运行：
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务器
mcp = FastMCP("Demo")


# 添加加法工具
@mcp.tool()
def add(a: int, b: int) -> int:
    """将两个数字相加"""
    return a + b


# 添加动态问候资源
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """获取个性化的问候"""
    return f"Hello, {name}!"


# 添加提示
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """生成问候提示"""
    styles = {
        "friendly": "请写一个温暖、友好的问候",
        "formal": "请写一个正式、专业问候",
        "casual": "请写一个随意、轻松的问候",
    }

    return f"{styles.get(style, styles['friendly'])} 给名为 {name} 的人。"
```

_完整示例：[examples/snippets/servers/fastmcp_quickstart.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/fastmcp_quickstart.py)_
<!-- /snippet-source -->

您可以在 [Claude Desktop](https://claude.ai/download) 中安装此服务器并立即与之交互，运行：

```bash
uv run mcp install server.py
```

或者，使用 MCP Inspector 测试它：

```bash
uv run mcp dev server.py
```

## 什么是 MCP？

[模型上下文协议 (MCP)](https://modelcontextprotocol.io) 让您构建以安全、标准化的方式向 LLM 应用程序暴露数据和功能的服务器。将其想象成一个专为 LLM 交互设计的 web API。MCP 服务器可以：

- 通过**资源**暴露数据（将其想象成 GET 端点；它们用于将信息加载到 LLM 的上下文中）
- 通过**工具**提供功能（将其想象成 POST 端点；它们用于执行代码或产生副作用）
- 通过**提示**定义交互模式（可重用的 LLM 交互模板）
- 还有更多！

## 核心概念

### 服务器

FastMCP 服务器是您与 MCP 协议的核心接口。它处理连接管理、协议合规性和消息路由：

<!-- snippet-source examples/snippets/servers/lifespan_example.py -->
```python
"""显示具有强类型支持的启动/关闭生命周期的示例。"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession


# 示例的模拟数据库类
class Database:
    """示例的模拟数据库类。"""


@dataclass
class AppContext:
    """具有类型化依赖的应用程序上下文。"""

    db: Database


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """使用类型安全的上下文管理应用程序生命周期。"""
    # 启动时初始化
    db = await Database.connect()
    try:
        yield AppContext(db=db)
    finally:
        # 关闭时清理
        await db.disconnect()


# 将生命周期传递给服务器
mcp = FastMCP("My App", lifespan=app_lifespan)


# 在工具中访问类型安全的生命周期上下文
@mcp.tool()
def query_db(ctx: Context[ServerSession, AppContext]) -> str:
    """使用已初始化资源的工具。"""
    db = ctx.request_context.lifespan_context.db
    return db.query()
```

_完整示例：[examples/snippets/servers/lifespan_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lifespan_example.py)_
<!-- /snippet-source -->

### 资源

资源是您向 LLM 暴露数据的方式。它们类似于 REST API 中的 GET 端点 - 它们提供数据但不应执行大量计算或产生副作用：

<!-- snippet-source examples/snippets/servers/basic_resource.py -->
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Resource Example")


@mcp.resource("file://documents/{name}")
def read_document(name: str) -> str:
    """按名称读取文档。"""
    # 这通常会从磁盘读取
    return f"{name} 的内容"


@mcp.resource("config://settings")
def get_settings() -> str:
    """获取应用程序设置。"""
    return """{
  "theme": "dark",
  "language": "en",
  "debug": false
}"""
```

_完整示例：[examples/snippets/servers/basic_resource.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic_resource.py)_
<!-- /snippet-source -->

### 工具

工具让 LLM 通过您的服务器执行操作。与资源不同，工具应该执行计算并产生副作用：

<!-- snippet-source examples/snippets/servers/basic_tool.py -->
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Tool Example")


@mcp.tool()
def sum(a: int, b: int) -> int:
    """将两个数字相加。"""
    return a + b


@mcp.tool()
def get_weather(city: str, unit: str = "celsius") -> str:
    """获取城市的天气。"""
    # 这通常会调用天气 API
    return f"{city} 的天气：22度{unit[0].upper()}"
```

_完整示例：[examples/snippets/servers/basic_tool.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic_tool.py)_
<!-- /snippet-source -->

工具可以可选地通过 `Context` 类型注解接收 Context 对象。此上下文由 FastMCP 框架自动注入，并提供对 MCP 功能的访问：

<!-- snippet-source examples/snippets/servers/tool_progress.py -->
```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

mcp = FastMCP(name="Progress Example")


@mcp.tool()
async def long_running_task(task_name: str, ctx: Context[ServerSession, None], steps: int = 5) -> str:
    """执行带有进度更新的任务。"""
    await ctx.info(f"开始：{task_name}")

    for i in range(steps):
        progress = (i + 1) / steps
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"步骤 {i + 1}/{steps}",
        )
        await ctx.debug(f"已完成步骤 {i + 1}")

    return f"任务 '{task_name}' 已完成"
```

_完整示例：[examples/snippets/servers/tool_progress.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/tool_progress.py)_
<!-- /snippet-source -->

#### 结构化输出

工具默认返回结构化结果，如果它们的返回类型注解兼容的话。否则，它们将返回非结构化结果。

结构化输出支持以下返回类型：

- Pydantic 模型（BaseModel 子类）
- TypedDict
- Dataclasses 和具有类型提示的其他类
- `dict[str, T]`（其中 T 是任何 JSON 可序列化的类型）
- 基本类型（str、int、float、bool、bytes、None）- 包装在 `{"result": value}` 中
- 通用类型（list、tuple、Union、Optional 等）- 包装在 `{"result": value}` 中

没有类型提示的类无法序列化为结构化输出。只有具有正确注解属性的类才会转换为 Pydantic 模型以进行模式生成和验证。

结构化结果会根据从注解生成的输出模式自动验证。这确保工具返回类型安全、验证过的数据，客户端可以轻松处理。

**注意：** 为向后兼容性，也会返回非结构化结果。非结构化结果是为向后兼容当前版本 SDK 中以前版本的 FastMCP 而提供的，并且与当前版本 MCP 规范的早期版本兼容。

**注意：** 在工具函数的返回类型注解导致工具被分类为结构化的情况下，如果这不可取，可以通过将 `structured_output=False` 传递给 `@tool` 装饰器来抑制这种分类。

##### 高级：直接返回 CallToolResult

为了完全控制工具响应，包括对客户端应用程序隐藏但不暴露给模型的 `_meta` 字段，您可以直接返回 `CallToolResult`：

<!-- snippet-source examples/snippets/servers/direct_call_tool_result.py -->
```python
"""显示直接 CallToolResult 返回以进行高级控制的示例。"""

from typing import Annotated

from pydantic import BaseModel

from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent

mcp = FastMCP("CallToolResult Example")


class ValidationModel(BaseModel):
    """用于验证结构化输出的模型。"""

    status: str
    data: dict[str, int]


@mcp.tool()
def advanced_tool() -> CallToolResult:
    """返回 CallToolResult 以完全控制包括 _meta 字段。"""
    return CallToolResult(
        content=[TextContent(type="text", text="对模型可见的响应")],
        _meta={"hidden": "仅客户端应用程序的数据"},
    )


@mcp.tool()
def validated_tool() -> Annotated[CallToolResult, ValidationModel]:
    """返回带有结构化输出验证的 CallToolResult。"""
    return CallToolResult(
        content=[TextContent(type="text", text="验证后的响应")],
        structuredContent={"status": "success", "data": {"result": 42}},
        _meta={"internal": "元数据"},
    )


@mcp.tool()
def empty_result_tool() -> CallToolResult:
    """对于空结果，返回带有空内容的 CallToolResult。"""
    return CallToolResult(content=[])
```

_完整示例：[examples/snippets/servers/direct_call_tool_result.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/direct_call_tool_result.py)_
<!-- /snippet-source -->

**重要：** `CallToolResult` 必须始终返回（没有 `Optional` 或 `Union`）。对于空结果，使用 `CallToolResult(content=[])`。对于可选的简单类型，使用 `str | None` 而不是 `CallToolResult`。

<!-- snippet-source examples/snippets/servers/structured_output.py -->
```python
"""显示工具结构化输出的示例。"""

from typing import TypedDict

from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Structured Output Example")


# 使用 Pydantic 模型进行丰富的结构化数据
class WeatherData(BaseModel):
    """天气信息结构。"""

    temperature: float = Field(description="摄氏温度")
    humidity: float = Field(description="湿度百分比")
    condition: str
    wind_speed: float


@mcp.tool()
def get_weather(city: str) -> WeatherData:
    """获取城市的天气 - 返回结构化数据。"""
    # 模拟天气数据
    return WeatherData(
        temperature=22.5,
        humidity=45.0,
        condition="sunny",
        wind_speed=5.2,
    )


# 使用 TypedDict 进行更简单的结构
class LocationInfo(TypedDict):
    latitude: float
    longitude: float
    name: str


@mcp.tool()
def get_location(address: str) -> LocationInfo:
    """获取坐标位置"""
    return LocationInfo(latitude=51.5074, longitude=-0.1278, name="London, UK")


# 使用 dict[str, Any] 进行灵活模式
@mcp.tool()
def get_statistics(data_type: str) -> dict[str, float]:
    """获取各种统计信息"""
    return {"mean": 42.5, "median": 40.0, "std_dev": 5.2}


# 具有类型提示的普通类适用于结构化输出
class UserProfile:
    name: str
    age: int
    email: str | None = None

    def __init__(self, name: str, age: int, email: str | None = None):
        self.name = name
        self.age = age
        self.email = email


@mcp.tool()
def get_user(user_id: str) -> UserProfile:
    """获取用户资料 - 返回结构化数据"""
    return UserProfile(name="Alice", age=30, email="alice@example.com")


# 没有类型提示的类无法用于结构化输出
class UntypedConfig:
    def __init__(self, setting1, setting2):  # type: ignore[reportMissingParameterType]
        self.setting1 = setting1
        self.setting2 = setting2


@mcp.tool()
def get_config() -> UntypedConfig:
    """这返回非结构化输出 - 没有生成模式"""
    return UntypedConfig("value1", "value2")


# 列表和其他类型会自动包装
@mcp.tool()
def list_cities() -> list[str]:
    """获取城市列表"""
    return ["London", "Paris", "Tokyo"]
    # 返回：{"result": ["London", "Paris", "Tokyo"]}


@mcp.tool()
def get_temperature(city: str) -> float:
    """获取温度作为简单浮点数"""
    return 22.5
    # 返回：{"result": 22.5}
```

_完整示例：[examples/snippets/servers/structured_output.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/structured_output.py)_
<!-- /snippet-source -->

### 提示

提示是帮助 LLM 有效地与您的服务器交互的可重用模板：

<!-- snippet-source examples/snippets/servers/basic_prompt.py -->
```python
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP(name="Prompt Example")


@mcp.prompt(title="Code Review")
def review_code(code: str) -> str:
    return f"请审查此代码：\n\n{code}"


@mcp.prompt(title="Debug Assistant")
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("我看到这个错误："),
        base.UserMessage(error),
        base.AssistantMessage("我将帮助调试那个。你到目前为止尝试了什么？"),
    ]
```

_完整示例：[examples/snippets/servers/basic_prompt.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic_prompt.py)_
<!-- /snippet-source -->

### 图标

MCP 服务器可以为 UI 显示提供图标。图标可以添加到服务器实现、工具、资源和提示中：

```python
from mcp.server.fastmcp import FastMCP, Icon

# 从文件路径或 URL 创建图标
icon = Icon(
    src="icon.png",
    mimeType="image/png",
    sizes="64x64"
)

# 添加图标到服务器
mcp = FastMCP(
    "My Server",
    website_url="https://example.com",
    icons=[icon]
)

# 添加图标到工具、资源和提示
@mcp.tool(icons=[icon])
def my_tool():
    """带有图标的工具。"""
    return "result"

@mcp.resource("demo://resource", icons=[icon])
def my_resource():
    """带有图标的资源。"""
    return "content"
```

_完整示例：[examples/fastmcp/icons_demo.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/fastmcp/icons_demo.py)_

### 图像

FastMCP 提供了一个 `Image` 类，自动处理图像数据：

<!-- snippet-source examples/snippets/servers/images.py -->
```python
"""显示 FastMCP 图像处理的示例。"""

from PIL import Image as PILImage

from mcp.server.fastmcp import FastMCP, Image

mcp = FastMCP("Image Example")


@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """从图像创建缩略图"""
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")
```

_完整示例：[examples/snippets/servers/images.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/images.py)_
<!-- /snippet-source -->

### 上下文

Context 对象会自动注入到请求它的工具和资源函数中，通过类型提示。它提供对日志记录、进度报告、资源读取、用户交互和请求元数据的访问。

#### 在函数中获取上下文

要在工具或资源函数中使用上下文，请添加一个带有 `Context` 类型注解的参数：

```python
from mcp.server.fastmcp import Context, FastMCP

mcp = FastMCP(name="Context Example")


@mcp.tool()
async def my_tool(x: int, ctx: Context) -> str:
    """使用上下文功能的工具。"""
    # 上下文参数可以有任何名称，只要它是类型注解的
    return await process_with_context(x, ctx)
```

#### 上下文属性和方法

Context 对象提供以下功能：

- `ctx.request_id` - 当前请求的唯一 ID
- `ctx.client_id` - 客户端 ID（如果可用）
- `ctx.fastmcp` - 对 FastMCP 服务器实例的访问（请参阅 [FastMCP 属性](#fastmcp-属性)）
- `ctx.session` - 对底层会话的高级通信访问（请参阅 [会话属性和方法](#会话属性和方法)）
- `ctx.request_context` - 对请求特定数据和生命周期资源的访问（请参阅 [请求上下文属性](#请求上下文属性)）
- `await ctx.debug(message)` - 发送调试日志消息
- `await ctx.info(message)` - 发送信息日志消息  
- `await ctx.warning(message)` - 发送警告日志消息
- `await ctx.error(message)` - 发送错误日志消息
- `await ctx.log(level, message, logger_name=None)` - 发送自定义级别的日志
- `await ctx.report_progress(progress, total=None, message=None)` - 报告操作进度
- `await ctx.read_resource(uri)` - 按 URI 读取资源
- `await ctx.elicit(message, schema)` - 使用验证从用户请求附加信息

<!-- snippet-source examples/snippets/servers/tool_progress.py -->
```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

mcp = FastMCP(name="Progress Example")


@mcp.tool()
async def long_running_task(task_name: str, ctx: Context[ServerSession, None], steps: int = 5) -> str:
    """执行带有进度更新的任务。"""
    await ctx.info(f"开始：{task_name}")

    for i in range(steps):
        progress = (i + 1) / steps
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"步骤 {i + 1}/{steps}",
        )
        await ctx.debug(f"已完成步骤 {i + 1}")

    return f"任务 '{task_name}' 已完成"
```

_完整示例：[examples/snippets/servers/tool_progress.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/tool_progress.py)_
<!-- /snippet-source -->

### 补全

MCP 支持为提示参数和资源模板参数提供补全建议。使用上下文参数，服务器可以基于之前解析的值提供补全：

客户端使用：

<!-- snippet-source examples/snippets/clients/completion_client.py -->
```python
"""
cd 到 `examples/snippets` 目录并运行：
    uv run completion-client
"""

import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import PromptReference, ResourceTemplateReference

# 创建 stdio 连接的服务器参数
server_params = StdioServerParameters(
    command="uv",  # 使用 uv 运行服务器
    args=["run", "server", "completion", "stdio"],  # 具有补全支持的服务器
    env={"UV_INDEX": os.environ.get("UV_INDEX", "")},
)


async def run():
    """运行补全客户端示例。"""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()

            # 列出可用的资源模板
            templates = await session.list_resource_templates()
            print("可用的资源模板：")
            for template in templates.resourceTemplates:
                print(f"  - {template.uriTemplate}")

            # 列出可用的提示
            prompts = await session.list_prompts()
            print("\n可用的提示：")
            for prompt in prompts.prompts:
                print(f"  - {prompt.name}")

            # 补全资源模板参数
            if templates.resourceTemplates:
                template = templates.resourceTemplates[0]
                print(f"\n补全资源模板的参数：{template.uriTemplate}")

                # 没有上下文的情况下补全
                result = await session.complete(
                    ref=ResourceTemplateReference(type="ref/resource", uri=template.uriTemplate),
                    argument={"name": "owner", "value": "model"},
                )
                print(f"为 'owner' 以 'model' 开头的补全：{result.completion.values}")

                # 带有上下文补全 - 基于所有者建议仓库
                result = await session.complete(
                    ref=ResourceTemplateReference(type="ref/resource", uri=template.uriTemplate),
                    argument={"name": "repo", "value": ""},
                    context_arguments={"owner": "modelcontextprotocol"},
                )
                print(f"为 'repo' 带有所有者='modelcontextprotocol' 的补全：{result.completion.values}")

            # 补全提示参数
            if prompts.prompts:
                prompt_name = prompts.prompts[0].name
                print(f"\n补全提示的参数：{prompt_name}")

                result = await session.complete(
                    ref=PromptReference(type="ref/prompt", name=prompt_name),
                    argument={"name": "style", "value": ""},
                )
                print(f"为 'style' 参数的补全：{result.completion.values}")


def main():
    """补全客户端脚本的入口点。"""
    asyncio.run(run())


if __name__ == "__main__":
    main()
```

_完整示例：[examples/snippets/clients/completion_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/completion_client.py)_
<!-- /snippet-source --></content>
<parameter name="filePath">e:\3dm\GlossModMCP\MCP Python SDK (中文).md
````
This is the description of what the code block changes:
<changeDescription>
添加文档的剩余中文翻译内容
</changeDescription>

This is the code block that represents the suggested code change:
````markdown
### 征询

从用户请求附加信息。这个示例显示了工具调用期间的征询：

<!-- snippet-source examples/snippets/servers/elicitation.py -->
```python
from pydantic import BaseModel, Field

from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

mcp = FastMCP(name="Elicitation Example")


class BookingPreferences(BaseModel):
    """用于收集用户偏好的模式。"""

    checkAlternative: bool = Field(description="您是否要检查另一个日期？")
    alternativeDate: str = Field(
        default="2024-12-26",
        description="替代日期（YYYY-MM-DD）",
    )


@mcp.tool()
async def book_table(date: str, time: str, party_size: int, ctx: Context[ServerSession, None]) -> str:
    """使用日期可用性检查预订餐桌。"""
    # 检查日期是否可用
    if date == "2024-12-25":
        # 日期不可用 - 询问用户替代方案
        result = await ctx.elicit(
            message=(f"{party_size} 人 {date} 没有餐桌可用。您是否要尝试另一个日期？"),
            schema=BookingPreferences,
        )

        if result.action == "accept" and result.data:
            if result.data.checkAlternative:
                return f"[成功] 已预订 {result.data.alternativeDate}"
            return "[取消] 未进行预订"
        return "[取消] 预订已取消"

    # 日期可用
    return f"[成功] 已预订 {date} {time}"
```

_完整示例：[examples/snippets/servers/elicitation.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/elicitation.py)_
<!-- /snippet-source -->

征询模式支持所有字段类型的默认值。默认值会自动包含在发送给客户端的 JSON 模式中，允许它们预填充表单。

`elicit()` 方法返回一个 `ElicitationResult`，其中包含：

- `action`："accept"、"decline" 或 "cancel"
- `data`：接受时的验证响应（仅在接受时）
- `validation_error`：任何验证错误消息

### 采样

工具可以通过采样与 LLM 交互（生成文本）：

<!-- snippet-source examples/snippets/servers/sampling.py -->
```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP(name="Sampling Example")


@mcp.tool()
async def generate_poem(topic: str, ctx: Context[ServerSession, None]) -> str:
    """使用 LLM 采样生成诗歌。"""
    prompt = f"写一首关于 {topic} 的简短诗歌"

    result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(type="text", text=prompt),
            )
        ],
        max_tokens=100,
    )

    if result.content.type == "text":
        return result.content.text
    return str(result.content)
```

_完整示例：[examples/snippets/servers/sampling.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/sampling.py)_
<!-- /snippet-source -->

### 日志记录和通知

工具可以通过上下文发送日志和通知：

<!-- snippet-source examples/snippets/servers/notifications.py -->
```python
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

mcp = FastMCP(name="Notifications Example")


@mcp.tool()
async def process_data(data: str, ctx: Context[ServerSession, None]) -> str:
    """使用日志记录处理数据。"""
    # 不同的日志级别
    await ctx.debug(f"调试：处理 '{data}'")
    await ctx.info("信息：开始处理")
    await ctx.warning("警告：这是实验性的")
    await ctx.error("错误：（这只是一个演示）")

    # 通知资源更改
    await ctx.session.send_resource_list_changed()

    return f"已处理：{data}"
```

_完整示例：[examples/snippets/servers/notifications.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/notifications.py)_
<!-- /snippet-source -->

### 认证

认证可以由想要暴露访问受保护资源的工具的服务器使用。

`mcp.server.auth` 实现了 OAuth 2.1 资源服务器功能，其中 MCP 服务器充当资源服务器 (RS)，验证由单独的授权服务器 (AS) 颁发的令牌。这遵循了 [MCP 授权规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) 并实现了 RFC 9728（受保护资源元数据）以进行 AS 发现。

MCP 服务器可以通过提供 `TokenVerifier` 协议的实现来使用认证：

<!-- snippet-source examples/snippets/servers/oauth_server.py -->
```python
"""
从仓库根目录运行：
    uv run examples/snippets/servers/oauth_server.py
"""

from pydantic import AnyHttpUrl

from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP


class SimpleTokenVerifier(TokenVerifier):
    """演示用的简单令牌验证器。"""

    async def verify_token(self, token: str) -> AccessToken | None:
        pass  # 这里将实现实际的令牌验证


# 创建 FastMCP 实例作为资源服务器
mcp = FastMCP(
    "Weather Service",
    # 认证的令牌验证器
    token_verifier=SimpleTokenVerifier(),
    # RFC 9728 受保护资源元数据的认证设置
    auth=AuthSettings(
        issuer_url=AnyHttpUrl("https://auth.example.com"),  # 授权服务器 URL
        resource_server_url=AnyHttpUrl("http://localhost:3001"),  # 此服务器的 URL
        required_scopes=["user"],
    ),
)


@mcp.tool()
async def get_weather(city: str = "London") -> dict[str, str]:
    """获取城市的天气数据"""
    return {
        "city": city,
        "temperature": "22",
        "condition": "Partly cloudy",
        "humidity": "65%",
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

_完整示例：[examples/snippets/servers/oauth_server.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/oauth_server.py)_
<!-- /snippet-source -->

有关单独的授权服务器和资源服务器实现的完整示例，请参阅 [`examples/servers/simple-auth/`](examples/servers/simple-auth/)。

**架构：**

- **授权服务器 (AS)**：处理 OAuth 流程、用户认证和令牌颁发
- **资源服务器 (RS)**：您的 MCP 服务器验证令牌并服务受保护的资源
- **客户端**：通过 RFC 9728 发现 AS，获取令牌，并将它们与 MCP 服务器一起使用

有关实现令牌验证的更多详细信息，请参阅 [TokenVerifier](src/mcp/server/auth/provider.py)。

### FastMCP 属性

FastMCP 服务器实例通过 `ctx.fastmcp` 提供对服务器配置和元数据的访问：

- `ctx.fastmcp.name` - 初始化时定义的服务器名称
- `ctx.fastmcp.instructions` - 提供给客户端的服务器指令/描述
- `ctx.fastmcp.website_url` - 可选的网站 URL
- `ctx.fastmcp.icons` - 可选的 UI 显示图标列表
- `ctx.fastmcp.settings` - 包含以下内容的完整服务器配置对象：
  - `debug` - 调试模式标志
  - `log_level` - 当前日志级别
  - `host` 和 `port` - 服务器网络配置
  - `mount_path`、`sse_path`、`streamable_http_path` - 传输路径
  - `stateless_http` - 服务器是否以无状态模式运行
  - 以及其他配置选项

```python
@mcp.tool()
def server_info(ctx: Context) -> dict:
    """获取当前服务器的信息。"""
    return {
        "name": ctx.fastmcp.name,
        "instructions": ctx.fastmcp.instructions,
        "debug_mode": ctx.fastmcp.settings.debug,
        "log_level": ctx.fastmcp.settings.log_level,
        "host": ctx.fastmcp.settings.host,
        "port": ctx.fastmcp.settings.port,
    }
```

### 会话属性和方法

会话对象通过 `ctx.session` 提供对客户端通信的高级控制：

- `ctx.session.client_params` - 客户端初始化参数和声明的功能
- `await ctx.session.send_log_message(level, data, logger)` - 发送具有完全控制的日志消息
- `await ctx.session.create_message(messages, max_tokens)` - 请求 LLM 采样/补全
- `await ctx.session.send_progress_notification(token, progress, total, message)` - 直接进度更新
- `await ctx.session.send_resource_updated(uri)` - 通知客户端特定资源已更改
- `await ctx.session.send_resource_list_changed()` - 通知客户端资源列表已更改
- `await ctx.session.send_tool_list_changed()` - 通知客户端工具列表已更改
- `await ctx.session.send_prompt_list_changed()` - 通知客户端提示列表已更改

```python
@mcp.tool()
async def notify_data_update(resource_uri: str, ctx: Context) -> str:
    """更新数据并通知客户端更改。"""
    # 此处执行数据更新逻辑
    
    # 通知客户端此特定资源已更改
    await ctx.session.send_resource_updated(AnyUrl(resource_uri))
    
    # 如果这影响整体资源列表，也通知它
    await ctx.session.send_resource_list_changed()
    
    return f"已更新 {resource_uri} 并通知客户端"
```

### 请求上下文属性

请求上下文通过 `ctx.request_context` 包含请求特定信息和资源：

- `ctx.request_context.lifespan_context` - 访问服务器启动期间初始化的资源
  - 数据库连接、配置对象、共享服务
  - 类型安全的访问在服务器的生命周期函数中定义的资源
- `ctx.request_context.meta` - 来自客户端的请求元数据，包括：
  - `progressToken` - 进度通知的令牌
  - 其他客户端提供的元数据
- `ctx.request_context.request` - 高级处理的原始 MCP 请求对象
- `ctx.request_context.request_id` - 此请求的唯一标识符

```python
# 类型化生命周期上下文的示例
@dataclass
class AppContext:
    db: Database
    config: AppConfig

@mcp.tool()
def query_with_config(query: str, ctx: Context) -> str:
    """使用共享数据库和配置执行查询。"""
    # 访问类型化的生命周期上下文
    app_ctx: AppContext = ctx.request_context.lifespan_context
    
    # 使用共享资源
    connection = app_ctx.db
    settings = app_ctx.config
    
    # 使用配置执行查询
    result = connection.execute(query, timeout=settings.query_timeout)
    return str(result)
```

_完整生命周期示例：[examples/snippets/servers/lifespan_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lifespan_example.py)_

## 运行服务器

### 开发模式

测试和调试服务器的最快方法是使用 MCP Inspector：

```bash
uv run mcp dev server.py

# 添加依赖
uv run mcp dev server.py --with pandas --with numpy

# 挂载本地代码
uv run mcp dev server.py --with-editable .
```

### Claude Desktop 集成

服务器准备就绪后，在 Claude Desktop 中安装它：

```bash
uv run mcp install server.py

# 自定义名称
uv run mcp install server.py --name "My Analytics Server"

# 环境变量
uv run mcp install server.py -v API_KEY=abc123 -v DB_URL=postgres://...
uv run mcp install server.py -f .env
```

### 直接执行

对于高级场景如自定义部署：

<!-- snippet-source examples/snippets/servers/direct_execution.py -->
```python
"""显示直接执行 MCP 服务器的示例。

这是直接运行 MCP 服务器的最简单方法。
cd 到 `examples/snippets` 目录并运行：
    uv run direct-execution-server
    或者
    python servers/direct_execution.py
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")


@mcp.tool()
def hello(name: str = "World") -> str:
    """向某人打招呼。"""
    return f"Hello, {name}!"


def main():
    """直接执行服务器的入口点。"""
    mcp.run()


if __name__ == "__main__":
    main()
```

_完整示例：[examples/snippets/servers/direct_execution.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/direct_execution.py)_
<!-- /snippet-source -->

运行它：

```bash
python servers/direct_execution.py
# 或者
uv run mcp run servers/direct_execution.py
```

注意 `uv run mcp run` 或 `uv run mcp dev` 仅支持使用 FastMCP 的服务器，不支持低级服务器变体。

### 流式 HTTP 传输

> **注意**：流式 HTTP 传输正在取代 SSE 传输用于生产部署。

<!-- snippet-source examples/snippets/servers/streamable_config.py -->
```python
"""
从仓库根目录运行：
    uv run examples/snippets/servers/streamable_config.py
"""

from mcp.server.fastmcp import FastMCP

# 有状态服务器（维护会话状态）
mcp = FastMCP("StatefulServer")

# 其他配置选项：
# 无状态服务器（无会话持久性）
# mcp = FastMCP("StatelessServer", stateless_http=True)

# 无状态服务器（无会话持久性，支持客户端的无 SSE 流）
# mcp = FastMCP("StatelessServer", stateless_http=True, json_response=True)


# 添加一个简单的工具来演示服务器
@mcp.tool()
def greet(name: str = "World") -> str:
    """按名称问候某人。"""
    return f"Hello, {name}!"


# 使用 streamable_http 传输运行服务器
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

_完整示例：[examples/snippets/servers/streamable_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_config.py)_
<!-- /snippet-source -->

您可以在 Starlette 应用程序中挂载多个 FastMCP 服务器：

<!-- snippet-source examples/snippets/servers/streamable_starlette_mount.py -->
```python
"""
从仓库根目录运行：
    uvicorn examples.snippets.servers.streamable_starlette_mount:app --reload
"""

import contextlib

from starlette.applications import Starlette
from starlette.routing import Mount

from mcp.server.fastmcp import FastMCP

# 创建 Echo 服务器
echo_mcp = FastMCP(name="EchoServer", stateless_http=True)


@echo_mcp.tool()
def echo(message: str) -> str:
    """一个简单的 echo 工具"""
    return f"Echo: {message}"


# 创建 Math 服务器
math_mcp = FastMCP(name="MathServer", stateless_http=True)


@math_mcp.tool()
def add_two(n: int) -> int:
    """将两个添加到输入的工具"""
    return n + 2


# 创建一个组合的生命周期来管理两个会话管理器
@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(echo_mcp.session_manager.run())
        await stack.enter_async_context(math_mcp.session_manager.run())
        yield


# 创建 Starlette 应用程序并挂载 MCP 服务器
app = Starlette(
    routes=[
        Mount("/echo", echo_mcp.streamable_http_app()),
        Mount("/math", math_mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)

# 注意：客户端连接到 http://localhost:8000/echo/mcp 和 http://localhost:8000/math/mcp
# 要挂载在每个路径的根目录（例如 /echo 而不是 /echo/mcp）：
# echo_mcp.settings.streamable_http_path = "/"
# math_mcp.settings.streamable_http_path = "/"
```

_完整示例：[examples/snippets/servers/streamable_starlette_mount.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_starlette_mount.py)_
<!-- /snippet-source -->

对于低级服务器与流式 HTTP 实现的完整示例，请参阅：

- 有状态服务器：[`examples/servers/simple-streamablehttp/`](examples/servers/simple-streamablehttp/)
- 无状态服务器：[`examples/servers/simple-streamablehttp-stateless/`](examples/servers/simple-streamablehttp-stateless/)

流式 HTTP 传输支持：

- 有状态和无状态操作模式
- 具有事件存储的可恢复性
- JSON 或 SSE 响应格式
- 更好的多节点部署可扩展性

#### 浏览器客户端的 CORS 配置

如果您希望服务器可供基于浏览器的 MCP 客户端访问，您需要配置 CORS 头。`Mcp-Session-Id` 头必须暴露给浏览器客户端才能访问它：

```python
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware

# 首先创建您的 Starlette 应用程序
starlette_app = Starlette(routes=[...])

# 然后用 CORS 中间件包装它
starlette_app = CORSMiddleware(
    starlette_app,
    allow_origins=["*"],  # 为生产适当配置
    allow_methods=["GET", "POST", "DELETE"],  # MCP 流式 HTTP 方法
    expose_headers=["Mcp-Session-Id"],
)
```

这是必要的，因为：

- MCP 流式 HTTP 传输使用 `Mcp-Session-Id` 头进行会话管理
- 浏览器限制对响应头的访问，除非通过 CORS 明确暴露
- 如果没有此配置，基于浏览器的客户端将无法从初始化响应中读取会话 ID

### 挂载到现有 ASGI 服务器

默认情况下，SSE 服务器挂载在 `/sse`，流式 HTTP 服务器挂载在 `/mcp`。您可以使用下面描述的方法自定义这些路径。

有关在 Starlette 中挂载应用程序的更多信息，请参阅 [Starlette 文档](https://www.starlette.io/routing/#submounting-routes)。

#### StreamableHTTP 服务器

您可以使用 `streamable_http_app` 方法将 StreamableHTTP 服务器挂载到现有 ASGI 服务器。这允许您将 StreamableHTTP 服务器与其他 ASGI 应用程序集成。

##### 基本挂载

<!-- snippet-source examples/snippets/servers/streamable_http_basic_mounting.py -->
```python
"""
在 Starlette 中挂载 StreamableHTTP 服务器的基本示例。

从仓库根目录运行：
    uvicorn examples.snippets.servers.streamable_http_basic_mounting:app --reload
"""

from starlette.applications import Starlette
from starlette.routing import Mount

from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务器
mcp = FastMCP("My App")


@mcp.tool()
def hello() -> str:
    """一个简单的 hello 工具"""
    return "Hello from MCP!"


# 将 StreamableHTTP 服务器挂载到现有 ASGI 服务器
app = Starlette(
    routes=[
        Mount("/", app=mcp.streamable_http_app()),
    ]
)
```

_完整示例：[examples/snippets/servers/streamable_http_basic_mounting.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_basic_mounting.py)_
<!-- /snippet-source -->

##### 基于主机的路由

<!-- snippet-source examples/snippets/servers/streamable_http_host_mounting.py -->
```python
"""
显示使用基于主机路由挂载 StreamableHTTP 服务器的示例。

从仓库根目录运行：
    uvicorn examples.snippets.servers.streamable_http_host_mounting:app --reload
"""

from starlette.applications import Starlette
from starlette.routing import Host

from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务器
mcp = FastMCP("MCP Host App")


@mcp.tool()
def domain_info() -> str:
    """获取域特定信息"""
    return "这从 mcp.acme.corp 提供服务"


# 使用基于主机的路由挂载
app = Starlette(
    routes=[
        Host("mcp.acme.corp", app=mcp.streamable_http_app()),
    ]
)
```

_完整示例：[examples/snippets/servers/streamable_http_host_mounting.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_host_mounting.py)_
<!-- /snippet-source -->

##### 具有路径配置的多个服务器

<!-- snippet-source examples/snippets/servers/streamable_http_multiple_servers.py -->
```python
"""
显示使用路径配置挂载多个 StreamableHTTP 服务器的示例。

从仓库根目录运行：
    uvicorn examples.snippets.servers.streamable_http_multiple_servers:app --reload
"""

from starlette.applications import Starlette
from starlette.routing import Mount

from mcp.server.fastmcp import FastMCP

# 创建多个 MCP 服务器
api_mcp = FastMCP("API Server")
chat_mcp = FastMCP("Chat Server")


@api_mcp.tool()
def api_status() -> str:
    """获取 API 状态"""
    return "API 正在运行"


@chat_mcp.tool()
def send_message(message: str) -> str:
    """发送聊天消息"""
    return f"消息已发送：{message}"


# 配置服务器挂载在每个路径的根目录
# 这意味着端点将在 /api 和 /chat 而不是 /api/mcp 和 /chat/mcp
api_mcp.settings.streamable_http_path = "/"
chat_mcp.settings.streamable_http_path = "/"

# 挂载服务器
app = Starlette(
    routes=[
        Mount("/api", app=api_mcp.streamable_http_app()),
        Mount("/chat", app=chat_mcp.streamable_http_app()),
    ]
)
```

_完整示例：[examples/snippets/servers/streamable_http_multiple_servers.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_multiple_servers.py)_
<!-- /snippet-source -->

##### 初始化时的路径配置

<!-- snippet-source examples/snippets/servers/streamable_http_path_config.py -->
```python
"""
显示 FastMCP 初始化时路径配置的示例。

从仓库根目录运行：
    uvicorn examples.snippets.servers.streamable_http_path_config:app --reload
"""

from starlette.applications import Starlette
from starlette.routing import Mount

from mcp.server.fastmcp import FastMCP

# 在初始化时配置 streamable_http_path
# 此服务器将挂载在它挂载的任何位置的根目录
mcp_at_root = FastMCP("My Server", streamable_http_path="/")


@mcp_at_root.tool()
def process_data(data: str) -> str:
    """处理一些数据"""
    return f"已处理：{data}"


# 挂载在 /process - 端点将在 /process 而不是 /process/mcp
app = Starlette(
    routes=[
        Mount("/process", app=mcp_at_root.streamable_http_app()),
    ]
)
```

_完整示例：[examples/snippets/servers/streamable_http_path_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_path_config.py)_
<!-- /snippet-source -->

#### SSE 服务器

> **注意**：SSE 传输正在被 [流式 HTTP 传输](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http) 取代。

您可以使用 `sse_app` 方法将 SSE 服务器挂载到现有 ASGI 服务器。这允许您将 SSE 服务器与其他 ASGI 应用程序集成。

```python
from starlette.applications import Starlette
from starlette.routing import Mount, Host
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("My App")

# 将 SSE 服务器挂载到现有 ASGI 服务器
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)

# 或者动态挂载为主机
app.router.routes.append(Host('mcp.acme.corp', app=mcp.sse_app()))
```

挂载多个 MCP 服务器在不同路径下时，您可以通过几种方式配置挂载路径：

```python
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

# 创建多个 MCP 服务器
github_mcp = FastMCP("GitHub API")
browser_mcp = FastMCP("Browser")
curl_mcp = FastMCP("Curl")
search_mcp = FastMCP("Search")

# 方法 1：通过设置配置挂载路径（推荐用于持久配置）
github_mcp.settings.mount_path = "/github"
browser_mcp.settings.mount_path = "/browser"

# 方法 2：直接传递挂载路径给 sse_app（首选用于临时挂载）
# 此方法不会永久修改服务器的设置

# 创建具有多个挂载服务器的 Starlette 应用程序
app = Starlette(
    routes=[
        # 使用设置-based 配置
        Mount("/github", app=github_mcp.sse_app()),
        Mount("/browser", app=browser_mcp.sse_app()),
        # 使用直接挂载路径参数
        Mount("/curl", app=curl_mcp.sse_app("/curl")),
        Mount("/search", app=search_mcp.sse_app("/search")),
    ]
)

# 方法 3：对于直接执行，您也可以将挂载路径传递给 run()
if __name__ == "__main__":
    search_mcp.run(transport="sse", mount_path="/search")
```

有关在 Starlette 中挂载应用程序的更多信息，请参阅 [Starlette 文档](https://www.starlette.io/routing/#submounting-routes)。

## 高级用法

### 低级服务器

对于更多控制，您可以直接使用低级服务器实现。这为您提供了对协议的完全访问，并允许您自定义服务器的每个方面，包括通过生命周期 API 进行生命周期管理：

<!-- snippet-source examples/snippets/servers/lowlevel/lifespan.py -->
```python
"""
从仓库根目录运行：
    uv run examples/snippets/servers/lowlevel/lifespan.py
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions


# 示例的模拟数据库类
class Database:
    """示例的模拟数据库类。"""

    @classmethod
    async def connect(cls) -> "Database":
        """连接到数据库。"""
        print("数据库已连接")
        return cls()

    async def disconnect(self) -> None:
        """断开数据库连接。"""
        print("数据库已断开")

    async def query(self, query_str: str) -> list[dict[str, str]]:
        """执行查询。"""
        # 模拟数据库查询
        return [{"id": "1", "name": "Example", "query": query_str}]


@asynccontextmanager
async def server_lifespan(_server: Server) -> AsyncIterator[dict[str, Any]]:
    """管理服务器启动和关闭生命周期。"""
    # 在启动时初始化资源
    db = await Database.connect()
    try:
        yield {"db": db}
    finally:
        # 在关闭时清理
        await db.disconnect()


# 将生命周期传递给服务器
server = Server("example-server", lifespan=server_lifespan)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """列出可用工具。"""
    return [
        types.Tool(
            name="query_db",
            description="查询数据库",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "要执行的 SQL 查询"}},
                "required": ["query"],
            },
        )
    ]


@server.call_tool()
async def query_db(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    """处理数据库查询工具调用。"""
    if name != "query_db":
        raise ValueError(f"未知工具：{name}")

    # 访问生命周期上下文
    ctx = server.request_context
    db = ctx.lifespan_context["db"]

    # 执行查询
    results = await db.query(arguments["query"])

    return [types.TextContent(type="text", text=f"查询结果：{results}")]


async def run():
    """使用生命周期管理运行服务器。"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
```

_完整示例：[examples/snippets/servers/lowlevel/lifespan.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/lifespan_example.py)_
<!-- /snippet-source -->

生命周期 API 提供：

- 在服务器启动时初始化资源并在停止时清理它们的方法
- 通过请求上下文在处理程序中访问已初始化资源
- 生命周期和请求处理程序之间的类型安全上下文传递

<!-- snippet-source examples/snippets/servers/lowlevel/basic.py -->
```python
"""
从仓库根目录运行：
uv run examples/snippets/servers/lowlevel/basic.py
"""

import asyncio

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# 创建服务器实例
server = Server("example-server")


@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """列出可用提示。"""
    return [
        types.Prompt(
            name="example-prompt",
            description="示例提示模板",
            arguments=[types.PromptArgument(name="arg1", description="示例参数", required=True)],
        )
    ]


@server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict[str, str] | None) -> types.GetPromptResult:
    """按名称获取特定提示。"""
    if name != "example-prompt":
        raise ValueError(f"未知提示：{name}")

    arg1_value = (arguments or {}).get("arg1", "default")

    return types.GetPromptResult(
        description="示例提示",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=f"示例提示文本带有参数：{arg1_value}"),
            )
        ],
    )


async def run():
    """运行基本的低级服务器。"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(run())
```

_完整示例：[examples/snippets/servers/lowlevel/basic.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/basic.py)_
<!-- /snippet-source -->

注意：`uv run mcp run` 和 `uv run mcp dev` 工具不支持低级服务器。

#### 结构化输出支持

低级服务器支持工具的结构化输出，允许您返回人类可读的内容和机器可读的结构化数据。工具可以定义 `outputSchema` 来验证其结构化输出：

<!-- snippet-source examples/snippets/servers/lowlevel/structured_output.py -->
```python
"""
从仓库根目录运行：
    uv run examples/snippets/servers/lowlevel/structured_output.py
"""

import asyncio
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

server = Server("example-server")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """列出具有结构化输出模式的可用工具。"""
    return [
        types.Tool(
            name="get_weather",
            description="获取城市的当前天气",
            inputSchema={
                "type": "object",
                "properties": {"city": {"type": "string", "description": "城市名称"}},
                "required": ["city"],
            },
            outputSchema={
                "type": "object",
                "properties": {
                    "temperature": {"type": "number", "description": "摄氏温度"},
                    "condition": {"type": "string", "description": "天气状况"},
                    "humidity": {"type": "number", "description": "湿度百分比"},
                    "city": {"type": "string", "description": "城市名称"},
                },
                "required": ["temperature", "condition", "humidity", "city"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """处理具有结构化输出的工具调用。"""
    if name == "get_weather":
        city = arguments["city"]

        # 模拟天气数据 - 在生产中，调用天气 API
        weather_data = {
            "temperature": 22.5,
            "condition": "partly cloudy",
            "humidity": 65,
            "city": city,  # 包含请求的城市
        }

        # 低级服务器将根据工具的输出模式验证结构化输出，
        # 并另外将其序列化为 TextContent 块以向后兼容
        # 2025-06-18 之前的客户端。
        return weather_data
    else:
        raise ValueError(f"未知工具：{name}")


async def run():
    """运行结构化输出服务器。"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="structured-output-example",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(run())
```

_完整示例：[examples/snippets/servers/lowlevel/structured_output.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/structured_output.py)_
<!-- /snippet-source -->

工具可以通过四种方式返回数据：

1. **仅内容**：返回内容块列表（2025-06-18 规范修订之前的默认行为）
2. **仅结构化数据**：返回将序列化为 JSON 的字典（2025-06-18 规范修订中引入）
3. **两者兼有**：返回 (content, structured_data) 元组，首选选项以保持向后兼容性
4. **直接 CallToolResult**：直接返回 `CallToolResult` 以完全控制（包括 `_meta` 字段）

定义 `outputSchema` 时，服务器会自动根据模式验证结构化输出。这确保类型安全并有助于及早发现错误。

##### 直接返回 CallToolResult

为了完全控制工具响应，包括对客户端应用程序隐藏但不暴露给模型的 `_meta` 字段，您可以直接返回 `CallToolResult`：

<!-- snippet-source examples/snippets/servers/lowlevel/direct_call_tool_result.py -->
```python
"""
从仓库根目录运行：
    uv run examples/snippets/servers/lowlevel/direct_call_tool_result.py
"""

import asyncio
from typing import Any

import mcp.server.stdio
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions

server = Server("example-server")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """列出可用工具。"""
    return [
        types.Tool(
            name="advanced_tool",
            description="具有完全控制的工具包括 _meta 字段",
            inputSchema={
                "type": "object",
                "properties": {"message": {"type": "string"}},
                "required": ["message"],
            },
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> types.CallToolResult:
    """通过直接返回 CallToolResult 处理工具调用。"""
    if name == "advanced_tool":
        message = str(arguments.get("message", ""))
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"已处理：{message}")],
            structuredContent={"result": "success", "message": message},
            _meta={"hidden": "仅客户端应用程序的数据"},
        )

    raise ValueError(f"未知工具：{name}")


async def run():
    """运行服务器。"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="example",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(run())
```

_完整示例：[examples/snippets/servers/lowlevel/direct_call_tool_result.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/direct_call_tool_result.py)_
<!-- /snippet-source -->

**注意：** 返回 `CallToolResult` 时，您绕过自动内容/结构化转换。您必须自己构造完整的响应。

### 分页（高级）

对于需要处理大型数据集的服务器，低级服务器提供了列表操作的分页版本。这是一个可选优化 - 大多数服务器在处理数百或数千个项目时不需要分页。

#### 服务器端实现

<!-- snippet-source examples/snippets/servers/pagination_example.py -->
```python
"""
使用 MCP 服务器装饰器实现分页的示例。
"""

from pydantic import AnyUrl

import mcp.types as types
from mcp.server.lowlevel import Server

# 初始化服务器
server = Server("paginated-server")

# 要分页的示例数据
ITEMS = [f"Item {i}" for i in range(1, 101)]  # 100 个项目


@server.list_resources()
async def list_resources_paginated(request: types.ListResourcesRequest) -> types.ListResourcesResult:
    """使用分页列出资源。"""
    page_size = 10

    # 从请求参数提取游标
    cursor = request.params.cursor if request.params is not None else None

    # 将游标解析为偏移量
    start = 0 if cursor is None else int(cursor)
    end = start + page_size

    # 获取资源页面
    page_items = [
        types.Resource(uri=AnyUrl(f"resource://items/{item}"), name=item, description=f"{item} 的描述")
        for item in ITEMS[start:end]
    ]

    # 确定下一个游标
    next_cursor = str(end) if end < len(ITEMS) else None

    return types.ListResourcesResult(resources=page_items, nextCursor=next_cursor)
```

_完整示例：[examples/snippets/servers/pagination_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/pagination_example.py)_
<!-- /snippet-source -->

#### 客户端消费

<!-- snippet-source examples/snippets/clients/pagination_client.py -->
```python
"""
从客户端消费分页的 MCP 端点的示例。
"""

import asyncio

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.types import PaginatedRequestParams, Resource


async def list_all_resources() -> None:
    """使用分页获取所有资源。"""
    async with stdio_client(StdioServerParameters(command="uv", args=["run", "mcp-simple-pagination"])) as (
        read,
        write,
    ):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()

            all_resources: list[Resource] = []
            cursor = None

            while True:
                # 获取资源页面
                result = await session.list_resources(params=PaginatedRequestParams(cursor=cursor))
                all_resources.extend(result.resources)

                print(f"获取了 {len(result.resources)} 个资源")

                # 检查是否有更多页面
                if result.nextCursor:
                    cursor = result.nextCursor
                else:
                    break

            print(f"总资源：{len(all_resources)}")


if __name__ == "__main__":
    asyncio.run(list_all_resources())
```

_完整示例：[examples/snippets/clients/pagination_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/pagination_client.py)_
<!-- /snippet-source -->

#### 关键点

- **游标是不透明的字符串** - 服务器定义格式（数字偏移、时间戳等）
- **当没有更多页面时返回 `nextCursor=None`**
- **向后兼容** - 不支持分页的客户端仍将工作（它们只会获取第一页）
- **灵活的页面大小** - 每个端点可以根据数据特征定义自己的页面大小

有关完整实现，请参阅 [simple-pagination 示例](examples/servers/simple-pagination)。

### 编写 MCP 客户端

SDK 提供了一个高级客户端接口，用于使用各种 [传输](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports) 连接到 MCP 服务器：

<!-- snippet-source examples/snippets/clients/stdio_client.py -->
```python
"""
cd 到 `examples/snippets/clients` 目录并运行：
    uv run client
"""

import asyncio
import os

from pydantic import AnyUrl

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.shared.context import RequestContext

# 创建 stdio 连接的服务器参数
server_params = StdioServerParameters(
    command="uv",  # 使用 uv 运行服务器
    args=["run", "server", "fastmcp_quickstart", "stdio"],  # 我们已经在 snippets 目录中
    env={"UV_INDEX": os.environ.get("UV_INDEX", "")},
)


# 可选：创建采样回调
async def handle_sampling_message(
    context: RequestContext[ClientSession, None], params: types.CreateMessageRequestParams
) -> types.CreateMessageResult:
    print(f"采样请求：{params.messages}")
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="来自模型的 Hello, world!",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            # 初始化连接
            await session.initialize()

            # 列出可用提示
            prompts = await session.list_prompts()
            print(f"可用提示：{[p.name for p in prompts.prompts]}")

            # 获取提示（来自 fastmcp_quickstart 的 greet_user 提示）
            if prompts.prompts:
                prompt = await session.get_prompt("greet_user", arguments={"name": "Alice", "style": "friendly"})
                print(f"提示结果：{prompt.messages[0].content}")

            # 列出可用资源
            resources = await session.list_resources()
            print(f"可用资源：{[r.uri for r in resources.resources]}")

            # 列出可用工具
            tools = await session.list_tools()
            print(f"可用工具：{[t.name for t in tools.tools]}")

            # 读取资源（来自 fastmcp_quickstart 的问候资源）
            resource_content = await session.read_resource(AnyUrl("greeting://World"))
            content_block = resource_content.contents[0]
            if isinstance(content_block, types.TextContent):
                print(f"资源内容：{content_block.text}")

            # 调用工具（来自 fastmcp_quickstart 的 add 工具）
            result = await session.call_tool("add", arguments={"a": 5, "b": 3})
            result_unstructured = result.content[0]
            if isinstance(result_unstructured, types.TextContent):
                print(f"工具结果：{result_unstructured.text}")
            result_structured = result.structuredContent
            print(f"结构化工具结果：{result_structured}")


def main():
    """客户端脚本的入口点。"""
    asyncio.run(run())


if __name__ == "__main__":
    main()
```

_完整示例：[examples/snippets/clients/stdio_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/stdio_client.py)_
<!-- /snippet-source -->

客户端还可以使用 [流式 HTTP 传输](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http) 连接：

<!-- snippet-source examples/snippets/clients/streamable_basic.py -->
```python
"""
从仓库根目录运行：
    uv run examples/snippets/clients/streamable_basic.py
"""

import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    # 连接到流式 HTTP 服务器
    async with streamablehttp_client("http://localhost:8000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        # 使用客户端流创建会话
        async with ClientSession(read_stream, write_stream) as session:
            # 初始化连接
            await session.initialize()
            # 列出可用工具
            tools = await session.list_tools()
            print(f"可用工具：{[tool.name for tool in tools.tools]}")


if __name__ == "__main__":
    asyncio.run(main())
```

_完整示例：[examples/snippets/clients/streamable_basic.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/streamable_basic.py)_
<!-- /snippet-source -->

### 客户端显示工具

构建 MCP 客户端时，SDK 提供了工具来帮助显示工具、资源和提示的人类可读名称：

<!-- snippet-source examples/snippets/clients/display_utilities.py -->
```python
"""
cd 到 `examples/snippets` 目录并运行：
    uv run display-utilities-client
"""

import asyncio
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.shared.metadata_utils import get_display_name


async def display_tools(session: ClientSession):
    """使用人类可读名称显示可用工具"""
    tools_response = await session.list_tools()

    for tool in tools_response.tools:
        # get_display_name() 返回标题（如果可用），否则返回名称
        display_name = get_display_name(tool)
        print(f"工具：{display_name}")
        if tool.description:
            print(f"   {tool.description}")


async def display_resources(session: ClientSession):
    """使用人类可读名称显示可用资源"""
    resources_response = await session.list_resources()

    for resource in resources_response.resources:
        display_name = get_display_name(resource)
        print(f"资源：{display_name} ({resource.uri})")

    templates_response = await session.list_resource_templates()
    for template in templates_response.resourceTemplates:
        display_name = get_display_name(template)
        print(f"资源模板：{display_name}")


async def run():
    """运行显示工具示例。"""
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()

            print("=== 可用工具 ===")
            await display_tools(session)

            print("\n=== 可用资源 ===")
            await display_resources(session)


def main():
    """显示工具客户端的入口点。"""
    asyncio.run(run())


if __name__ == "__main__":
    main()
```

_完整示例：[examples/snippets/clients/display_utilities.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/display_utilities.py)_
<!-- /snippet-source -->

`get_display_name()` 函数实现了正确的优先级规则，用于显示服务器提供的更用户友好的名称：

- 对于工具：`title` > `annotations.title` > `name`
- 对于其他对象：`title` > `name`

这确保您的客户端 UI 显示服务器提供的最用户友好的名称。

### 客户端的 OAuth 认证

SDK 包括对连接到受保护 MCP 服务器的 [授权支持](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization)：

<!-- snippet-source examples/snippets/clients/oauth_client.py -->
```python
"""
运行前，指定运行 MCP RS 服务器 URL。
要本地启动 RS 服务器，请参阅
    examples/servers/simple-auth/README.md

cd 到 `examples/snippets` 目录并运行：
    uv run oauth-client
"""

import asyncio
from urllib.parse import parse_qs, urlparse

from pydantic import AnyUrl

from mcp import ClientSession
from mcp.client.auth import OAuthClientProvider, TokenStorage
from mcp.client.streamable_http import streamablehttp_client
from mcp.shared.auth import OAuthClientInformationFull, OAuthClientMetadata, OAuthToken


class InMemoryTokenStorage(TokenStorage):
    """演示用的内存中令牌存储实现。"""

    def __init__(self):
        self.tokens: OAuthToken | None = None
        self.client_info: OAuthClientInformationFull | None = None

    async def get_tokens(self) -> OAuthToken | None:
        """获取存储的令牌。"""
        return self.tokens

    async def set_tokens(self, tokens: OAuthToken) -> None:
        """存储令牌。"""
        self.tokens = tokens

    async def get_client_info(self) -> OAuthClientInformationFull | None:
        """获取存储的客户端信息。"""
        return self.client_info

    async def set_client_info(self, client_info: OAuthClientInformationFull) -> None:
        """存储客户端信息。"""
        self.client_info = client_info


async def handle_redirect(auth_url: str) -> None:
    print(f"访问：{auth_url}")


async def handle_callback() -> tuple[str, str | None]:
    callback_url = input("粘贴回调 URL：")
    params = parse_qs(urlparse(callback_url).query)
    return params["code"][0], params.get("state", [None])[0]


async def main():
    """运行 OAuth 客户端示例。"""
    oauth_auth = OAuthClientProvider(
        server_url="http://localhost:8001",
        client_metadata=OAuthClientMetadata(
            client_name="示例 MCP 客户端",
            redirect_uris=[AnyUrl("http://localhost:3000/callback")],
            grant_types=["authorization_code", "refresh_token"],
            response_types=["code"],
            scope="user",
        ),
        storage=InMemoryTokenStorage(),
        redirect_handler=handle_redirect,
        callback_handler=handle_callback,
    )

    async with streamablehttp_client("http://localhost:8001/mcp", auth=oauth_auth) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print(f"可用工具：{[tool.name for tool in tools.tools]}")

            resources = await session.list_resources()
            print(f"可用资源：{[r.uri for r in resources.resources]}")


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
```

_完整示例：[examples/snippets/clients/oauth_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/oauth_client.py)_
<!-- /snippet-source -->

有关完整的工作示例，请参阅 [`examples/clients/simple-auth-client/`](examples/clients/simple-auth-client/)。

### 解析工具结果

通过 MCP 调用工具时，`CallToolResult` 对象以结构化格式包含工具的响应。理解如何解析此结果对于正确处理工具输出至关重要。

```python
"""examples/snippets/clients/parsing_tool_results.py"""

import asyncio

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


async def parse_tool_results():
    """演示如何解析 CallToolResult 中的不同类型内容。"""
    server_params = StdioServerParameters(
        command="python", args=["path/to/mcp_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 示例 1：解析文本内容
            result = await session.call_tool("get_data", {"format": "text"})
            for content in result.content:
                if isinstance(content, types.TextContent):
                    print(f"文本：{content.text}")

            # 示例 2：解析来自 JSON 工具的结构化内容
            result = await session.call_tool("get_user", {"id": "123"})
            if hasattr(result, "structuredContent") and result.structuredContent:
                # 直接访问结构化数据
                user_data = result.structuredContent
                print(f"用户：{user_data.get('name')}，年龄：{user_data.get('age')}")

            # 示例 3：解析嵌入资源
            result = await session.call_tool("read_config", {})
            for content in result.content:
                if isinstance(content, types.EmbeddedResource):
                    resource = content.resource
                    if isinstance(resource, types.TextResourceContents):
                        print(f"来自 {resource.uri} 的配置：{resource.text}")
                    elif isinstance(resource, types.BlobResourceContents):
                        print(f"来自 {resource.uri} 的二进制数据")

            # 示例 4：解析图像内容
            result = await session.call_tool("generate_chart", {"data": [1, 2, 3]})
            for content in result.content:
                if isinstance(content, types.ImageContent):
                    print(f"图像（{content.mimeType}）：{len(content.data)} 字节")

            # 示例 5：处理错误
            result = await session.call_tool("failing_tool", {})
            if result.isError:
                print("工具执行失败！")
                for content in result.content:
                    if isinstance(content, types.TextContent):
                        print(f"错误：{content.text}")
```

## 文档

- [API 参考](https://modelcontextprotocol.github.io/python-sdk/api/)
- [模型上下文协议文档](https://modelcontextprotocol.io)
- [模型上下文协议规范](https://spec.modelcontextprotocol.io)
- [官方支持的服务器](https://github.com/modelcontextprotocol/servers)

## 贡献

我们热情支持各种经验水平的贡献者，并希望您能参与项目。请参阅 [贡献指南](CONTRIBUTING.md) 开始。

## 许可证

本项目根据 MIT 许可证授权 - 请参阅 LICENSE 文件了解详情。