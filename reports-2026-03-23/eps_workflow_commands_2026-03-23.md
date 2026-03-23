# EPS 工作流命令逆向报告
**日期**: 2026-03-23
**模块**: SSERPTools.exe (端口12002)

---

## 已确认的 ERP 工作流命令

| 命令字符串 | 地址 | 函数地址 | 说明 |
|-----------|------|---------|------|
| `WorkSubmit` | 0x10049698 | 0x1001DC40 | 提交工作 |
| `WorkProgressReport` | 0x10049654 | 0x10017E00 | 工作进度上报 |
| `CNewWorkDlg` | 0x1004909d | 0x10014330 | 新建工作对话框 |
| `CancelAcceptWork` | 0x10049678 | 0x1000EC00 | 取消接件 |
| `GetWorkList` | (rdata) | 0x10011130 | 获取工作列表(对话框) |
| `WorkInfo` | (rdata) | - | 工作信息 |
| `GetWorkInfo` | 0x10045eb8 | - | 获取工作信息(CString参数×3) |

---

## 关键函数签名

### sub_10017E00 (WorkProgressReport)
```
int __cdecl sub_10017E00(CScaleMap *a1)
{
  struct CERPManager *ERPManager; // esi
  sub_10018BD0(v51); // init
  ERPManager = GetERPManager(); // 获取ERP管理器单例
  sub_10018770(0); // 初始化
  ...
}
```

### sub_10011130 (GetWorkList)
```
void __cdecl sub_10011130(int a1)
{
  CDialog *v1; // esi
  v1 = operator new(0x6C4); // 分配6C4字节
  v1 = sub_100111B0(a1, 0);
  CDialog::Create(v1, (const char *)0x3E8, 0); // 创建对话框(ID=0x3E8=1000)
  CWnd::ShowWindow(v1, 5);
  ssCenterWindow(v1);
}
```

### sub_10014330 (NewWork)
```
int __thiscall sub_10014330(int this, int a2, struct CWnd *a3)
{
  CBCGPDialog::CBCGPDialog((CBCGPDialog *)this, 0x3EDu, a3); // ID=0x3ED=1005
  *(this+140) = &off_100372DC; // vtable
}
```

---

## SSERPTools 资源对话框ID

| ID | 16进制 | 功能 |
|----|--------|------|
| 0x3E8 | 1000 | GetWorkList 对话框 |
| 0x3ED | 1005 | NewWork 对话框 |

---

## 重要结论

1. **URL 无明文** — SSERPTools 中无 HTTP 服务器地址明文
2. **MFC CInternetSession** — HTTP 请求通过 MFC 库动态构建
3. **ERPManager 单例** — 所有 ERP 操作通过 `GetERPManager()` 获取
4. **CBCGPDialog** — UI 使用 BCGControlBar Pro 库（对话框风格）
5. **WorkSubmit** — 设置 this[69]=参数2, this[71]=CString, this[72]=CString（存储工作数据）

---

## 完整工作流调用链

### WorkProgressReport (0x10017E00) — 进度上报

```
用户输入工作信息 → GetWorkInfo() → 获取3个对话框字段
    ↓
CERPManager::GetToken() → 获取 ACCESS_TOKEN
    ↓
Format("时间,Token,工作信息,进度百分比")
    ↓
SetShareParameter("ERPManager", "Progressreport", 参数)
    ↓
ssExcuteFunction("SscriptDll", "ExecuteScript", "ERPManager", "Progressreport")
    ↓
SscriptDll.dll 动态加载 → HTTP请求 → ERP服务器
```

### 关键地址
- ssExcuteFunction @ 0x1000fd8c (SSCore32.dll)
- SscriptDll.dll（小写s！）动态加载路径

## ERPManager 工作流命令清单

| 命令名 | 类型 | 作用 |
|--------|------|------|
| `Progressreport` | 进度上报 | 上报工作进度到服务器 |
| `WorkSubmit` | 工作提交 | 提交新建工作 |
| `NewWork` | 新建工作 | 打开新建工作对话框 |
| `CancelAcceptWork` | 取消接件 | 取消工作接件 |
| `GetWorkList` | 获取列表 | 获取当前工作列表 |
| `GetWorkInfo` | 获取信息 | 获取指定工作详情 |
| `SetWorkInfo` | 设置信息 | 修改工作信息 |

## 核心结论

1. **HTTP 请求在 SscriptDll.dll 里** — 动态加载后组装 HTTP 请求（解释了为什么 SSERPTools 无明文 URL）
2. **所有 ERP 操作通过 SDL 脚本引擎** — 统一的命令分发机制
3. **ACCESS_TOKEN 通过 CERPManager::GetToken() 获取** — 在 WorkProgressReport 中实时取 Token
4. **命令名即 SDL 脚本名** — "Progressreport" 等于 SscriptDll 中的脚本名称
