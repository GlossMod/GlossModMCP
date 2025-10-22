# 📚 GlossModMCP 完整指南目录

## 🎯 快速导航

### 🚀 快速开始（5分钟）
👉 **[QUICKSTART.md](./QUICKSTART.md)**
- 安装依赖
- 启动服务器
- 基本使用
- 常见问题

### 📖 详细文档（详细参考）
👉 **[README_SERVER.md](./README_SERVER.md)**
- 功能概述
- 工具详解
- 资源说明
- 提示参考
- 使用示例

### 🏗️ 实现细节（架构参考）
👉 **[IMPLEMENTATION.md](./IMPLEMENTATION.md)**
- 项目结构
- 技术栈
- 代码质量
- 性能考虑
- 扩展建议

### ✅ 验证报告（质量保证）
👉 **[VERIFICATION.md](./VERIFICATION.md)**
- 完成清单
- 测试结果
- 代码指标
- 部署就绪

---

## 📂 文件说明

### 核心文件

```
server.py (367 行)
├─ FastMCP 服务器实现
├─ 7 个工具函数
├─ 4 个资源函数
├─ 4 个提示函数
└─ 3 个数据模型
```

### 配置文件

```
pyproject.toml
├─ 项目元数据
├─ 依赖声明
└─ Python 版本要求

.vscode/settings.json
└─ VS Code 开发配置
```

### 测试文件

```
test_server.py
├─ 功能测试脚本
├─ API 集成测试
└─ 资源验证
```

### 示例文件

```
examples_advanced.py
├─ 缓存实现
├─ 速率限制
├─ 重试机制
├─ 性能优化
└─ 高级用法
```

### 文档文件

```
QUICKSTART.md           - 5分钟快速开始
README_SERVER.md        - 详细功能文档
IMPLEMENTATION.md       - 实现说明
VERIFICATION.md         - 验证报告
API_REFERENCE.md        - API 参考（此文件）
```

---

## 🛠️ 工具参考

### 游戏工具

```python
# 获取游戏列表
await get_games(
    page=1,                    # 页码
    page_size=20,              # 每页数量
    search="游戏名",           # 搜索关键词
    game_type="动作",          # 游戏类型
    sort_by="allcount",        # 排序字段
    sort_order="desc"          # 排序方向
)

# 获取游戏详情
await get_game_detail(game_id=123)
```

### Mod 工具

```python
# 获取 Mod 列表
await get_mods(
    page=1,                    # 页码
    page_size=20,              # 每页数量
    game_id=123,               # 游戏 ID
    search="Mod 名",           # 搜索关键词
    time=2,                    # 时间筛选
    order=0                    # 排序方式
)
# time 值: 1=今天, 2=最近一周, 3=最近一月, 4=最近三月

# 获取 Mod 详情
await get_mod_detail(mod_id=456)

# 批量检查 Mod 更新
await check_mod_updates(mod_ids=[123, 456, 789])
```

### Minecraft Mod 工具

```python
# 获取 Minecraft Mod 列表
await get_minecraft_mods(
    page=1,                    # 页码
    page_size=20,              # 每页数量
    modules="fabric",          # 模组类型
    search="优化",             # 搜索关键词
    sort_by="updateTime",      # 排序字段
    sort_order="desc"          # 排序方向
)
# sort_by 选项: updateTime, createTime, downloadCnt, viewCnt, likeCnt

# 获取 Minecraft Mod 详情
await get_minecraft_mod_detail(mod_id=789)
```

---

## 📚 资源参考

### 可用资源

```
glossmod://games/list
└─ 热门游戏列表
   ├─ 返回类型: Markdown
   ├─ 内容: 游戏名、ID、Mod数量
   └─ 示例: 10个热门游戏

glossmod://games/{game_id}
└─ 指定游戏详情
   ├─ 返回类型: Markdown
   ├─ 内容: 游戏详细信息
   └─ 示例: ID=123 的游戏详情

glossmod://mods/latest
└─ 最新 Mod 列表
   ├─ 返回类型: Markdown
   ├─ 内容: 最近一周发布的 Mod
   └─ 示例: 10个最新 Mod

glossmod://minecraft/latest
└─ 最新 Minecraft Mod
   ├─ 返回类型: Markdown
   ├─ 内容: 最新的 Minecraft Mod
   └─ 示例: 10个最新 Minecraft Mod
```

---

## 💡 提示参考

### 提示模板

```python
# 搜索游戏提示
search_game(game_name="赛博朋克2077")
# 返回: 优化的游戏搜索提示词

# 搜索 Mod 提示
search_mod(
    mod_name="RTX",
    game_name="赛博朋克2077"  # 可选
)
# 返回: 优化的 Mod 搜索提示词

# 趋势 Mod 列表提示
list_trending_mods(
    time_range="week"  # today, week, month, quarter
)
# 返回: 趋势 Mod 查询提示

# Minecraft 指南提示
minecraft_mod_guide()
# 返回: Minecraft Mod 使用指南
```

---

## 🚀 常见使用流程

### 流程 1: 游戏 Mod 推荐

```
1. 用户提问: "推荐《黑神话：悟空》的热门 Mod"
2. LLM 调用 search_game("黑神话悟空")
3. LLM 使用该提示调用 get_games(search="黑神话")
4. LLM 从结果中选择正确的游戏
5. LLM 调用 get_mods(game_id=GAME_ID)
6. LLM 分析和推荐
```

### 流程 2: Minecraft Mod 查找

```
1. 用户提问: "找一些 Minecraft 优化 Mod"
2. LLM 调用 minecraft_mod_guide()
3. LLM 使用指南调用 get_minecraft_mods(search="优化")
4. LLM 访问 glossmod://minecraft/latest 资源
5. LLM 综合推荐
```

### 流程 3: 版本检查

```
1. 用户提问: "我的 Mod 有新版本吗"
2. LLM 调用 check_mod_updates([mod_id_1, mod_id_2, ...])
3. LLM 返回更新信息
```

---

## ⚙️ 配置说明

### 环境变量

```bash
# API 密钥（可选）
GLOSSMOD_API_KEY=your-api-key

# Python 路径（自动）
PYTHONPATH=${workspaceFolder}
```

### API 配置

编辑 `server.py` 中的：

```python
API_BASE_URL = "https://mod.3dmgame.com/api/v3"
API_KEY = os.getenv("GLOSSMOD_API_KEY", "")
```

---

## 🧪 测试命令

### 运行所有测试

```bash
uv run test_server.py
```

### 运行单个测试

编辑 `test_server.py` 并选择特定函数运行

### 使用 MCP Inspector

```bash
uv run mcp dev server.py
```

---

## 🔍 故障排除

### 问题: 没有数据返回

**原因**: API 可能返回空结果或不可用

**解决**:
1. 检查网络连接
2. 尝试不同的搜索条件
3. 查看 API 响应状态

### 问题: 权限错误

**原因**: 某些操作需要 API 密钥

**解决**:
```bash
$env:GLOSSMOD_API_KEY = "your-key"
```

### 问题: 导入错误

**原因**: 依赖未安装

**解决**:
```bash
uv sync
```

---

## 📊 API 返回格式

### 成功响应

```json
{
  "success": true,
  "message": "请求成功",
  "data": {
    // 实际数据
  }
}
```

### 错误响应

```json
{
  "success": false,
  "message": "错误描述",
  "data": null
}
```

---

## 🎓 学习资源

### 官方文档
- [MCP 官网](https://modelcontextprotocol.io)
- [FastMCP 文档](./MCP%20Python%20SDK.md)
- [3DM API 文档](./GlossModAPI.md)

### 示例代码
- 基础示例: server.py
- 高级示例: examples_advanced.py
- 测试示例: test_server.py

---

## 📞 支持和反馈

### 获取帮助

1. 查看相应的文档文件
2. 运行 MCP Inspector 进行交互测试
3. 检查测试脚本了解功能
4. 查看高级示例学习最佳实践

### 报告问题

如遇到问题：
1. 检查文档中的故障排除部分
2. 运行测试脚本验证功能
3. 查看日志输出

---

## 📈 下一步

### 推荐学习路径

1. **快速开始** (5分钟)
   → QUICKSTART.md

2. **基本使用** (15分钟)
   → README_SERVER.md

3. **深入理解** (30分钟)
   → IMPLEMENTATION.md
   → examples_advanced.py

4. **高级应用** (1小时+)
   → 自定义扩展
   → 添加新工具
   → 集成新 API

---

## 🎉 开始使用

### 三步启动

```bash
# 1. 安装依赖
uv sync

# 2. 启动服务器
uv run mcp dev server.py

# 3. 开始使用
# 在 Claude 或其他应用中使用
```

---

**祝你使用愉快！** 🚀

需要帮助？查看相应的文档文件或运行 `uv run test_server.py` 进行验证。
