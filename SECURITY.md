# 🔒 安全策略

## 敏感信息处理

**绝对禁止**在代码仓库中提交以下内容：

- API Token / Key（包括 GitHub Token、OpenAI Key、ModelScope Key）
- 密码、私钥
- 个人身份信息（身份证、护照等）
- 内部系统访问凭证
- 客户数据

## 本地路径风险

本项目涉及 Windows 路径（`D:\`、`C:\Users\`），包含开发者本机路径。
**不要**将本地路径推送到 GitHub。

建议 `git add` 前执行：
```powershell
git status
# 确认无敏感路径泄露
```

## Frida / 调试工具使用注意

- Frida Hook 脚本仅用于已知可信的 EPS 二进制文件
- 不对来路不明的 DLL / EDB 文件进行动态调试
- IDA 调试前确保样本文件做过备份

## 报告安全漏洞

如发现安全漏洞，请私聊联系 `openclawzeng`，不要在公开 issue 中描述细节。

---

*本文件由 openclawzeng 生成于 2026-04-10*
