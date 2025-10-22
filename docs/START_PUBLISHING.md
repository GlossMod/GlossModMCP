# 🎯 5分钟快速发布指南

## 现在就可以发布！

你的 MCP 服务器已经完全准备好。只需 3 个步骤：

---

## 步骤 1: 准备 PyPI 账户（首次 5 分钟）

**如果你已有 PyPI 账户，跳过这步**

访问: https://pypi.org/account/register/

- 注册账户
- 验证邮箱
- 进入 Account Settings → API tokens
- 创建新 API token
- 复制 token（看起来像: `pypi-AgEIcHlw...`）

---

## 步骤 2: 安装 twine（如果还没有）

```powershell
pip install twine
```

---

## 步骤 3: 上传包

```powershell
twine upload dist/*
```

系统会提示输入用户名和密码：
- **用户名**: `__token__`（不变）
- **密码**: 粘贴你的 API token

---

## ✅ 完成！

上传成功后，用户可以运行：

```bash
pip install glossmod-mcp
```

---

## 📝 查看结果

访问: https://pypi.org/project/glossmod-mcp/

---

## 📚 需要帮助？

| 需求     | 查看文档                     |
| -------- | ---------------------------- |
| 快速参考 | `QUICK_PUBLISH.md`           |
| 详细指南 | `docs/PUBLISHING.md`         |
| 检查清单 | `RELEASE_CHECKLIST.md`       |
| 自动工具 | `scripts/publish.py --check` |

---

## 🚀 其他发布方式

### GitHub Release（可选）

```powershell
git tag v1.0.0
git push origin v1.0.0
# 然后在 GitHub 网页创建 Release
```

### MCP Registry（可选）

访问: https://modelcontextprotocol.io/servers

---

## 🎉 就这样！

**现在开始发布吧：**

```powershell
twine upload dist/*
```
