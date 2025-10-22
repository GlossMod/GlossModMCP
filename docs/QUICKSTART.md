# 快速开始指南

## GlossModMCP 服务器快速启动

这个 MCP 服务器将 3DM Mod API 集成到 Claude 和其他支持 MCP 的应用中。

## 步骤 1: 准备环境

### 安装依赖

```bash
cd GlossModMCP
uv sync
```

## 步骤 2: 获取 API 密钥（可选）

如果您有 3DM API 密钥，设置环境变量：

```powershell
# Windows PowerShell
$env:GLOSSMOD_API_KEY = "your-api-key-here"

# 或者在系统环境变量中设置
```

## 步骤 3: 测试服务器

### 方法 A: 使用 MCP Inspector（推荐用于开发）

```bash
uv run mcp dev server.py
```

这将打开 MCP Inspector，让你可以：
- ✅ 测试所有工具
- ✅ 查看资源
- ✅ 测试提示
- ✅ 实时调试

### 方法 B: 在 Claude Desktop 中使用

```bash
uv run mcp install server.py
```

然后在 Claude Desktop 中的设置中启用此服务器。

## 步骤 4: 与 LLM 交互

### 示例 1: 搜索游戏

```
提示词: "帮我搜索有关《黑神话：悟空》的 Mod 信息"
```

服务器将调用 `get_games` 工具搜索游戏并返回结果。

### 示例 2: 查找 Mod

```
提示词: "找最近一周发布的热门 Mod，按热度排序"
```

### 示例 3: Minecraft 推荐

```
提示词: "推荐一些最新的 Fabric Minecraft Mod"
```

## 可用的工具和资源

### 🛠️ 工具

| 工具名                     | 描述                    |
| -------------------------- | ----------------------- |
| `get_games`                | 查询游戏列表            |
| `get_game_detail`          | 获取游戏详情            |
| `get_mods`                 | 查询 Mod 列表           |
| `get_mod_detail`           | 获取 Mod 详情           |
| `check_mod_updates`        | 检查 Mod 更新           |
| `get_minecraft_mods`       | 查询 Minecraft Mod      |
| `get_minecraft_mod_detail` | 获取 Minecraft Mod 详情 |

### 📚 资源

| 资源 URI                      | 描述               |
| ----------------------------- | ------------------ |
| `glossmod://games/list`       | 热门游戏列表       |
| `glossmod://games/{id}`       | 特定游戏详情       |
| `glossmod://mods/latest`      | 最新 Mod           |
| `glossmod://minecraft/latest` | 最新 Minecraft Mod |

### 💡 提示

| 提示名                | 描述               |
| --------------------- | ------------------ |
| `search_game`         | 游戏搜索提示       |
| `search_mod`          | Mod 搜索提示       |
| `list_trending_mods`  | 趋势 Mod 列表提示  |
| `minecraft_mod_guide` | Minecraft Mod 指南 |

## 常见问题

### Q: API 调用没有返回数据？

A: 这可能是由于：
1. API 服务暂时不可用
2. 网络连接问题
3. API 参数不正确

检查：
- 网络连接
- API 基础 URL 是否正确
- 参数是否有效

### Q: 如何自定义 API URL？

A: 编辑 `server.py` 中的：
```python
API_BASE_URL = "https://mod.3dmgame.com/api/v3"
```

### Q: 支持哪些排序选项？

A: 
- **游戏**: `allcount`（总 Mod 数）, `tcount`（最近30天 Mod 数）
- **Minecraft Mod**: `updateTime`, `createTime`, `downloadCnt`, `viewCnt`, `likeCnt`

### Q: 如何设置时间筛选？

A: 使用 `time` 参数：
- 1 = 今天
- 2 = 最近一周
- 3 = 最近一个月
- 4 = 最近三个月

## 架构

```
┌─────────────────┐
│  Claude/LLM     │
└────────┬────────┘
         │ (MCP Protocol)
         ▼
┌─────────────────┐
│  GlossModMCP    │
│   Server        │
├─────────────────┤
│ Tools (工具)    │
│ Resources (资源)│
│ Prompts (提示)  │
└────────┬────────┘
         │ (HTTP)
         ▼
┌─────────────────────────────┐
│  3DM Mod API                │
│ mod.3dmgame.com/api/v3      │
└─────────────────────────────┘
```

## 故障排除

### 1. 导入错误

如果遇到导入错误，确保依赖已安装：
```bash
uv sync
```

### 2. 连接错误

检查网络连接和防火墙设置。

### 3. 超时错误

增加请求超时时间，编辑 `server.py`：
```python
async with httpx.AsyncClient(timeout=30.0) as client:
    # ...
```

## 更多资源

- [3DM Mod API 文档](./GlossModAPI.md)
- [MCP 官方文档](https://modelcontextprotocol.io)
- [Claude Desktop 指南](https://claude.ai/download)

## 支持

遇到问题？
1. 查看日志输出
2. 检查 API 文档
3. 尝试使用 MCP Inspector 进行调试

---

**祝你使用愉快！** 🚀
