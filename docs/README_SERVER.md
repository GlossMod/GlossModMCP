# GlossModMCP - 3DM Mod API MCP 服务器

基于 Model Context Protocol (MCP) 的 3DM Mod API 服务器实现，为 LLM 提供对 3DM Mod 网站数据的访问。

## 功能概述

### 工具 (Tools)

MCP 服务器提供以下工具，可被 LLM 调用：

#### 游戏相关
- **`get_games`** - 获取游戏列表，支持搜索、筛选和排序
  - 参数: `page`, `page_size`, `search`, `game_type`, `sort_by`, `sort_order`
  
- **`get_game_detail`** - 获取指定游戏的详细信息
  - 参数: `game_id`

#### Mod 相关
- **`get_mods`** - 获取 Mod 列表，支持多种筛选条件
  - 参数: `page`, `page_size`, `game_id`, `search`, `time`, `order`
  - `time` 参数: 1=今天, 2=最近一周, 3=最近一个月, 4=最近三个月
  
- **`get_mod_detail`** - 获取指定 Mod 的详细信息
  - 参数: `mod_id`
  
- **`check_mod_updates`** - 批量检查 Mod 的版本信息
  - 参数: `mod_ids` (数组)

#### Minecraft Mod 相关
- **`get_minecraft_mods`** - 获取 Minecraft Mod 列表
  - 参数: `page`, `page_size`, `modules`, `search`, `sort_by`, `sort_order`
  - `sort_by` 选项: updateTime, createTime, downloadCnt, viewCnt, likeCnt
  
- **`get_minecraft_mod_detail`** - 获取指定 Minecraft Mod 的详细信息
  - 参数: `mod_id`

### 资源 (Resources)

MCP 资源提供结构化的数据访问：

- **`glossmod://games/list`** - 热门游戏列表资源
- **`glossmod://games/{game_id}`** - 特定游戏详情资源
- **`glossmod://mods/latest`** - 最新 Mod 列表资源
- **`glossmod://minecraft/latest`** - 最新 Minecraft Mod 列表资源

### 提示 (Prompts)

预定义的提示模板，帮助 LLM 有效地与服务器交互：

- **`search_game`** - 搜索游戏及其 Mod 的提示
  - 参数: `game_name`
  
- **`search_mod`** - 搜索特定 Mod 的提示
  - 参数: `mod_name`, `game_name` (可选)
  
- **`list_trending_mods`** - 列出趋势 Mod 的提示
  - 参数: `time_range` (today, week, month, quarter)
  
- **`minecraft_mod_guide`** - Minecraft Mod 使用指南提示

## 安装和运行

### 前置要求

- Python 3.11+
- `uv` 包管理器

### 安装依赖

```bash
uv sync
```

### 环境变量配置

设置 3DM Mod API 密钥（可选，用于无限制访问）：

```bash
$env:GLOSSMOD_API_KEY = "your-api-key"
```

### 运行服务器

#### 1. 开发模式（使用 MCP Inspector）

```bash
uv run mcp dev server.py
```

这将启动 MCP Inspector，允许你交互式地测试工具、资源和提示。

#### 2. 标准输入输出模式

```bash
uv run server stdio
```

#### 3. Claude Desktop 集成

```bash
uv run mcp install server.py
```

然后在 Claude Desktop 中使用此服务器。

## 使用示例

### 示例 1：搜索游戏

```
要求 LLM: "帮我搜索《赛博朋克2077》的 Mod"
```

LLM 将调用 `get_games` 工具搜索游戏，然后使用 `get_game_detail` 获取详细信息。

### 示例 2：查看最新 Mod

```
要求 LLM: "获取最近一周最新发布的 Mod"
```

LLM 将使用 `get_mods` 工具，设置 `time=2` 参数获取最近一周的 Mod。

### 示例 3：Minecraft Mod 推荐

```
要求 LLM: "推荐一些热门的 Fabric Minecraft Mod"
```

LLM 将使用 `get_minecraft_mods` 工具获取 Fabric 模组列表。

## API 返回格式

所有工具返回 API 的 JSON 响应，格式如下：

```json
{
  "success": true,
  "message": "请求成功",
  "data": {
    // 实际数据内容
  }
}
```

错误响应格式：

```json
{
  "success": false,
  "message": "错误描述",
  "data": null
}
```

## 错误处理

服务器会自动处理 HTTP 错误。如果 API 调用失败，将抛出异常并由 MCP 框架处理。

## 架构说明

### 数据模型

- **Game** - 游戏信息（ID, 名称, 描述等）
- **Mod** - Mod 信息（ID, 标题, 作者, 版本等）
- **MinecraftMod** - Minecraft Mod 信息（ID, 名称, 作者, 模组类型等）

### 异步操作

所有 API 调用都使用 `httpx.AsyncClient` 进行异步处理，确保高效的并发操作。

## 文件结构

```
GlossModMCP/
├── server.py              # MCP 服务器主文件
├── pyproject.toml         # 项目配置和依赖
├── GlossModAPI.md         # 3DM API 文档
├── MCP Python SDK.md      # MCP SDK 文档
├── README.md              # 项目说明
└── README_SERVER.md       # 服务器使用说明（本文件）
```

## 相关文档

- [3DM Mod API 文档](./GlossModAPI.md) - API 端点和参数详情
- [MCP Python SDK 文档](./MCP%20Python%20SDK.md) - MCP 框架使用指南
- [MCP 官方网站](https://modelcontextprotocol.io) - 协议规范和标准

## 常见问题

### Q: 如何添加 API 密钥？

A: 设置环境变量 `GLOSSMOD_API_KEY`：
```bash
$env:GLOSSMOD_API_KEY = "your-api-key"
```

### Q: 可以自定义 API 基础 URL 吗？

A: 可以，修改 `server.py` 中的 `API_BASE_URL` 常量。

### Q: 支持批量操作吗？

A: 支持，可以使用 `check_mod_updates` 工具进行批量检查 Mod 版本。

## 许可证

MIT License

## 贡献

欢迎提交问题和改进建议！
