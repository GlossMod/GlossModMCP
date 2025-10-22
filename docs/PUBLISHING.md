# 📦 GlossModMCP 发布指南

你的 MCP 服务器已经成功构建！现在可以发布了。

---

## ✅ 已完成的设置

- ✅ **标准包结构** - `glossmod_mcp/` 包含 `__init__.py` 和 `server.py`
- ✅ **完整的 pyproject.toml** - 包含所有元数据和构建配置
- ✅ **LICENSE 文件** - MIT 许可证
- ✅ **MANIFEST.in** - 文件清单
- ✅ **构建成功** - 生成了 wheel 和 source distribution

---

## 📦 生成的文件

构建后在 `dist/` 目录中：

```
dist/
├── glossmod_mcp-1.0.0-py3-none-any.whl       (Wheel 包 - 推荐用于 pip 安装)
└── glossmod_mcp-1.0.0.tar.gz                  (Source distribution)
```

---

## 🚀 发布步骤

### 方式 1: 发布到 PyPI（推荐 - 最正式）

#### 1. 注册 PyPI 账户

访问 [https://pypi.org/account/register/](https://pypi.org/account/register/) 注册账户

#### 2. 创建 PyPI 密钥

1. 登录 PyPI
2. 进入 Account Settings → API tokens
3. 创建 API token
4. 复制 token（格式类似 `pypi-AgEIcHlwaS...`）

#### 3. 配置本地认证（选一种）

**选项 A：使用 .pypirc 文件（推荐）**

在用户目录创建 `~/.pypirc` 文件：

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS... (你的 API token)
```

**选项 B：使用环境变量**

```powershell
# Windows PowerShell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-AgEIcHlwaS..."
```

#### 4. 上传到 PyPI

```powershell
# 首先安装 twine
pip install twine

# 上传包
twine upload dist/*

# 如果已设置 .pypirc，只需：
twine upload dist/* --config-file ~/.pypirc
```

#### 5. 验证发布

上传后访问：https://pypi.org/project/glossmod-mcp/

---

### 方式 2: 发布到 GitHub Releases

#### 1. 推送代码到 GitHub

```powershell
git add .
git commit -m "Release v1.0.0: Initial release"
git push origin main
```

#### 2. 创建 Git 标签

```powershell
git tag -a v1.0.0 -m "Release version 1.0.0 - Initial MCP server"
git push origin v1.0.0
```

#### 3. 在 GitHub 上创建 Release

1. 访问 GitHub 项目页面
2. 点击 **Releases** → **Create a new release**
3. 选择标签 `v1.0.0`
4. 填写信息：

```
Title: GlossModMCP v1.0.0

Description:
🎉 Initial release of GlossModMCP

## Features
- 7 tool functions for accessing 3DM Mod API
- 4 resource endpoints
- 4 prompt templates
- Full type annotations
- Comprehensive documentation

## Installation
```bash
pip install glossmod-mcp
```

## Usage
See documentation at: https://github.com/GlossMod/gloss-mod-mcp
```

5. 上传分发文件（可选）：
   - 选择 "Attach binaries by dropping them here or selecting them"
   - 上传 `dist/glossmod_mcp-1.0.0-py3-none-any.whl`
   - 上传 `dist/glossmod_mcp-1.0.0.tar.gz`

---

### 方式 3: 提交到 MCP Registry

MCP Registry 是发现 MCP 服务器的官方地方。

1. 访问 [MCP Registry](https://modelcontextprotocol.io/servers)
2. 点击 **Submit a new server**
3. 填写表单：

```
Server Name: GlossModMCP
Description: MCP server for accessing 3DM Mod API with game and mod information

Repository URL: https://github.com/GlossMod/gloss-mod-mcp
Installation: pip install glossmod-mcp

Command:
uv run --with glossmod-mcp python -m glossmod_mcp.server

Categories: 
- API Integration
- Game Development

Documentation: https://github.com/GlossMod/gloss-mod-mcp/blob/main/README.md
```

---

## ✨ 版本管理建议

### 更新版本号

编辑 `pyproject.toml` 和 `glossmod_mcp/__init__.py`：

```toml
# pyproject.toml
version = "0.1.1"

# glossmod_mcp/__init__.py
__version__ = "0.1.1"
```

### 语义版本控制

- **1.0.0** → **0.1.1**: Bug 修复
- **1.0.0** → **0.2.0**: 新功能
- **1.0.0** → **1.0.0**: 重大变更

---

## 📝 发布前检查清单

在每次发布前：

```powershell
# 1. 检查代码质量
uv run ruff check .
uv run ruff format . --check

# 2. 验证包的完整性
twine check dist/*

# 3. 本地测试安装
pip install dist/glossmod_mcp-1.0.0-py3-none-any.whl

# 4. 测试导入
python -c "import glossmod_mcp; print(glossmod_mcp.__version__)"

# 5. 测试入口点
glossmod-mcp --help
```

---

## 🔄 持续发布工作流

### 创建 GitHub Actions 工作流（可选）

在 `.github/workflows/publish.yml` 中：

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install build tools
        run: |
          python -m pip install --upgrade pip
          pip install build twine
      
      - name: Build package
        run: python -m build
      
      - name: Publish to PyPI
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: twine upload dist/*
```

---

## 🎯 推荐的首次发布步骤

### Step 1: 本地验证
```powershell
twine check dist/*
```

### Step 2: 测试安装
```powershell
pip install dist/glossmod_mcp-1.0.0-py3-none-any.whl
```

### Step 3: 发布到 PyPI
```powershell
twine upload dist/*
```

### Step 4: 创建 GitHub Release
- 标签：v1.0.0
- 包含更新日志
- 附加 wheel 和 tar.gz 文件

### Step 5: 提交到 MCP Registry
- 填写官方 Registry 表单

---

## 📚 用户安装方式

发布后，用户可以通过以下方式安装：

```powershell
# 从 PyPI 安装
pip install glossmod-mcp

# 在 Claude Desktop 中配置
# ~/.claude_desktop_config.json
{
  "mcpServers": {
    "glossmod": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "glossmod-mcp",
        "python",
        "-m",
        "glossmod_mcp.server"
      ],
      "env": {
        "GLOSSMOD_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

---

## ❓ 常见问题

### Q: 首次发布需要付费吗？
A: 不需要。PyPI 是免费的，但需要验证邮箱。

### Q: 如何更新已发布的包？
A: 只需增加版本号，重新构建和上传。PyPI 会自动关联版本。

### Q: 能删除已发布的版本吗？
A: 不建议。可以标记为已弃用，但不能完全删除。PyPI 政策是为了避免破坏依赖关系。

### Q: 如何回滚到旧版本？
A: 用户可以指定版本号：`pip install glossmod-mcp==1.0.0`

---

## 🚀 现在就开始发布吧！

```powershell
# 最快速的发布方式：
twine upload dist/*
```

祝发布顺利！🎉
