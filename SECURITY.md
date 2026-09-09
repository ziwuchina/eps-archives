# 🔒 安全策略

## 敏感信息处理

**绝对禁止**在代码仓库中提交以下内容：

- API Token / Key（包括 GitHub Token、OpenAI Key、ModelScope Key、Cloudflare API）
- 密码、私钥（含 SSH 私钥如 `id_ed25519*`）
- 个人身份信息（身份证、护照等）
- 内部系统访问凭证
- 客户数据 / 业务待办数据（如 `worklist_*.json`）

**常见敏感文件名模式（出现即警惕，禁止提交）**：

```
*KEY*.txt / API KEY.txt / Cloudflare API.txt
*密钥* / *凭据* / *credential*
tokens*.json / *keys*.json / extracted_keys*.txt
cookies*.json / localStorage*.json / login 状态快照
id_ed25519* / *.pem / *.key（私钥类）
对话记录（*_msgs.txt / *_user_msgs.txt）
```

## 共享盘 / 外部目录归档实践

从 `\\Amd\ai相关` 等共享盘归档内容到本仓库时，按以下类别排除：

| 类别 | 示例 | 处置 |
|---|---|---|
| API 凭据 | `API KEY.txt`、`Cloudflare API.txt`、凭据清单 | ⛔ 排除 |
| 平台密钥/会话 | 元衡中转站（tokens/cookies/localStorage） | ⛔ 排除 |
| SSH 私钥 | `id_ed25519_remote` | ⛔ 排除 |
| 隐私数据 | 微信聊天解密、对话记录 | ⛔ 排除 |
| 业务数据 | 待办/报件明细 | ⛔ 排除 |
| 授权规避工具 | 时间锁规避脚本/工具 | ⛔ 排除 |
| 分析/知识文档 | 逆向报告、API 手册、双狗互通档案 | ✅ 可归档 |

归档前核对：`git status` 确认无敏感路径泄露；只复制文件、不改动原目录。

## 本地路径风险

本项目涉及 Windows 路径（`D:\`、`C:\Users\`），包含开发者本机路径。
**不要**将本地路径推送到 GitHub（README 中的路径仅为参考文档）。

建议 `git add` 前执行：
```powershell
git status
# 确认无敏感路径泄露
```

## Frida / 调试工具使用注意

- Frida Hook 脚本仅用于已知可信的 EPS 二进制文件
- 不对来路不明的 DLL / EDB 文件进行动态调试
- IDA 调试前确保样本文件做过备份
- 动态注入受限时（如目标为他人运行中的进程），不得提权/强攻，改用静态分析证明

## 报告安全漏洞

如发现安全漏洞，请私聊联系 `openclawzeng`，不要在公开 issue 中描述细节。

---

*本文件由 openclawzeng 生成于 2026-04-10，更新于 2026-09-09*
