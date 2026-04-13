# AI Brain Raw 歸檔執行計劃

> **For Hermes:** 本計劃由 Agent 逐步執行，每個步驟皆為獨立的檔案操作。

**Goal:** 將 `raw/` 中的 5 個檔案消化為 Layer 2 Wiki 實體頁，並歸檔已消化來源。

**Architecture:** 
- Phase 1：先在 Layer 2 (`entities/`) 建立 Hermes 實體頁
- Phase 2：將已消化的 raw 檔案移入 `_archive/raw/`
- Phase 3：更新 `index.md` 與 `log.md`

**Tech Stack:** Markdown + YAML frontmatter + [[wikilinks]]

---

## Task 1: 建立 Hermes Gateway Systemd Fix 實體頁

**Objective:** 建立 `entities/hermes/hermes-gateway-systemd-fix.md`，消化 `Hermes_Gateway_Fix_Summary.md`

**Files:**
- Create: `AI_Brain/entities/hermes/hermes-gateway-systemd-fix.md`

**Step 1: 寫入實體頁（含完整 frontmatter + 正文）**

```markdown
---
title: Hermes Gateway Systemd Fix
created: 2026-04-13
updated: 2026-04-13
type: entity
tags: [Hermes, Discord, Systemd, Python, Bug-Fix]
sources: [_archive/raw/Hermes_Gateway_Fix_Summary.md]
---

# Hermes Gateway Systemd Fix

## Overview
2026-04-13 修復 Hermes Gateway 服務在執行 `hermes gateway restart --system` 後無法啟動的問題。

## 問題現象
執行 `hermes gateway restart --system` 後，Gateway 服務崩潰，系統日誌出現：
`ModuleNotFoundError: No module named 'yaml'`

## 根本原因
1. **UV Python 路徑衝突**：Hermes 內部使用 `uv` 下載獨立的 CPython 3.11，但服務嘗試用這個乾淨的 3.11 執行，而非已安裝所有依賴的 venv。
2. **CLI 產生 Bug**：`--system` 參數讓 CLI 抓錯 Python 路徑，導致 Systemd 服務檔指向無依賴的 `uv` Python。

## 修復步驟
1. 手動修正 `/etc/systemd/system/hermes-gateway.service` 中 `ExecStart` 指向正確 venv：
   `/root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run --replace`
2. 建立持久化覆蓋：`/etc/systemd/system/hermes-gateway.service.d/python-override.conf`

## 未來建議
- 避免使用 `--system` 參數，改用 `hermes gateway restart`（User Service）
- 一鍵修復指令：
  `sudo sed -i 's|ExecStart=.*/python3\\.11 -m hermes_cli\\.main gateway run|ExecStart=/root/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main gateway run|' /etc/systemd/system/hermes-gateway.service && sudo systemctl daemon-reload && sudo systemctl restart hermes-gateway.service`

## 相關頁面
- [[concepts/safe-execution-workflow]] — 安全執行工作流（含 Systemd 日誌處理）
- [[entities/hermes/hermes-multiagent-discord-system]] — 多 Agent Discord 系統
```

**Step 2: 驗證**
確認檔案存在且 frontmatter 完整（title, created, updated, type, tags, sources）。

---

## Task 2: 建立 Hermes Multi-Agent Discord System 實體頁

**Objective:** 建立 `entities/hermes/hermes-multiagent-discord-system.md`，消化 `Hermes_Discord_Mod_Guide.md` + `Hermes_MultiAgent_Fix_Report.md`

**Files:**
- Create: `AI_Brain/entities/hermes/hermes-multiagent-discord-system.md`

**Step 1: 寫入實體頁**

```markdown
---
title: Hermes Multi-Agent Discord System
created: 2026-04-13
updated: 2026-04-13
type: entity
tags: [Hermes, Discord, Multi-Agent, Bot, Discord.py]
sources: [_archive/raw/Hermes_Discord_Mod_Guide.md, _archive/raw/Hermes_MultiAgent_Fix_Report.md, _archive/raw/hermes_multiagent_discord.patch]
---

# Hermes Multi-Agent Discord System

## Overview
Hermes 雙 Agent（主 Agent 蝦蝦 + 本地 Agent 小低能）在 Discord 環境下的通訊障礙修復總結。涵蓋 6 階段修復歷程與 3 大核心代碼修改。

## 修復歷程

### 階段一：底層通訊架構
| 問題 | 根因 | 解法 |
|------|------|------|
| Bot 訊息靜音 | Discord Adapter 預設過濾 Bot 訊息 | 設定 `DISCORD_ALLOW_BOTS=mentions`，雙方 ID 互加至 `DISCORD_ALLOWED_USERS` |
| Systemd 啟動崩潰 | UV Python 路徑衝突 | 建立 Systemd Override，綁定正確 venv Python |

### 階段二：標記偵測與討論串邀請
| 問題 | 根因 | 解法 |
|------|------|------|
| 身分組標記解析失敗 | `on_message` 只看 `mentions` 未看 `role_mentions` | 修改 `discord.py` 增加 Role Mention 比對 |
| 討論串成員資格盲區 | Discord 不會自動拉 Bot 進私密討論串 | 在 `_auto_create_thread` 加入 `thread.add_user()` 自動邀請邏輯 |

### 階段三：解決搶話與視覺屏障
| 問題 | 根因 | 解法 |
|------|------|------|
| 雙機搶話 (Crosstalk) | Agent 監聽所有討論串發言 | 嚴格沉默原則：其他 Bot 被標記時，未被標記的自己強制 Return |
| 小模型幻覺 | LLM 角色扮演假裝自己權限受限 | 重寫 `SOUL.md`，強制具體指令 |

## 三大核心修改（discord.py）

### 修改 1：讓 Bot 听懂「身分組 (@Role)」標記
讓 Bot 在收到其他 Bot 傳來的訊息時，正確識別被身分組標記的情況。

核心邏輯：同時檢查 `message.mentions` 與 `message.role_mentions`，並確保自己的身分組在 `role_mentions` 中。

### 修改 2：多 Agent 防搶話過濾器
當訊息中標記了「其他 Bot 或別人的身分組」，且自己未被標記時，強制 Return 丟棄封包。

### 修改 3：討論串自動拉人功能
在 `message.create_thread` 後自動邀請被標記的使用者與身分組成員。

## Patch 檔
代碼補丁位於 `[[_archive/raw/hermes_multiagent_discord.patch]]`。

## 未來協作最佳實踐
1. **單點指揮**：直接 `@蝦蝦` 或 `@小低能` 交付獨立任務
2. **傳遞工作流**：`@小低能，請將該成果展示給 @蝦蝦 繼續處理`

## 相關頁面
- [[concepts/safe-execution-workflow]] — 安全執行工作流
- [[entities/hermes/hermes-gateway-systemd-fix]] — Gateway Systemd 修復
```

**Step 2: 驗證**
確認檔案存在且 frontmatter 完整。

---

## Task 3: 執行歸檔（已消化來源移至 _archive）

**Objective:** 將 4 個已消化的 raw 檔案移入 `_archive/raw/`

**Files:**
- Move: `AI_Brain/raw/Hermes_Gateway_Fix_Summary.md` → `AI_Brain/_archive/raw/`
- Move: `AI_Brain/raw/Hermes_Discord_Mod_Guide.md` → `AI_Brain/_archive/raw/`
- Move: `AI_Brain/raw/Hermes_MultiAgent_Fix_Report.md` → `AI_Brain/_archive/raw/`
- Move: `AI_Brain/raw/hermes_multiagent_discord.patch` → `AI_Brain/_archive/raw/`

**Step 1: 確保目錄存在**
```bash
mkdir -p AI_Brain/_archive/raw
```

**Step 2: 移動檔案**
```bash
mv AI_Brain/raw/Hermes_Gateway_Fix_Summary.md AI_Brain/_archive/raw/
mv AI_Brain/raw/Hermes_Discord_Mod_Guide.md AI_Brain/_archive/raw/
mv AI_Brain/raw/Hermes_MultiAgent_Fix_Report.md AI_Brain/_archive/raw/
mv AI_Brain/raw/hermes_multiagent_discord.patch AI_Brain/_archive/raw/
```

**Step 3: 驗證**
```bash
ls AI_Brain/_archive/raw/
# 預期：Hermes_Discord_Mod_Guide.md, Hermes_Gateway_Fix_Summary.md, Hermes_MultiAgent_Fix_Report.md, hermes_multiagent_discord.patch
```

---

## Task 4: 刪除 CSAM 檔案

**Objective:** 刪除 `raw/articles/Sillytavern QR illustrious生圖.md`（Log 已記錄此為 CSAM 內容）

**Files:**
- Delete: `AI_Brain/raw/articles/Sillytavern QR illustrious生圖.md`

**Step 1: 刪除**
```bash
rm "AI_Brain/raw/articles/Sillytavern QR illustrious生圖.md"
```

**Step 2: 驗證**
```bash
ls AI_Brain/raw/articles/
# 預期：目錄為空
```

---

## Task 5: 更新 index.md

**Objective:** 將 2 個新實體頁加入 index.md

**Files:**
- Modify: `AI_Brain/index.md`

**Step 1: 新增 Entities 條目**
在 `## 👤 Entities` 區段新增：
```markdown
- [[entities/hermes/hermes-gateway-systemd-fix]] — Hermes Gateway Systemd 服務修復：UV Python 路徑衝突 + Systemd Override 解法
- [[entities/hermes/hermes-multiagent-discord-system]] — Hermes 雙 Agent Discord 協作系統：6 階段修復 + 3 大核心 discord.py 修改
```

**Step 2: 更新 header**
- `最後更新: YYYY-MM-DD` → 今日日期
- `總頁數: 5` → `7`

---

## Task 6: 更新 log.md

**Objective:** 記錄 ingest + archive 動作

**Files:**
- Modify: `AI_Brain/log.md`

**Step 1: Append**
```markdown
## [YYYY-MM-DD] ingest+archive | Hermes Multi-Agent System 歸檔
- 建立 [[entities/hermes/hermes-gateway-systemd-fix]]（消化 Hermes_Gateway_Fix_Summary.md）
- 建立 [[entities/hermes/hermes-multiagent-discord-system]]（消化 Hermes_Discord_Mod_Guide.md + Hermes_MultiAgent_Fix_Report.md）
- 歸檔 4 個 raw 檔案至 _archive/raw/
- 刪除 CSAM 檔案：raw/articles/Sillytavern QR illustrious生圖.md
- index.md 總頁數更新為 7
```

---

## Task 7: 確認 _archive/plans/ 目錄建立

**Files:**
- Create: `AI_Brain/_archive/plans/`（存放本計劃）

---

---

## Task 7: 消化 WSL DNS Resolution Fix 計劃

**Objective:** 將 `wsl-dns-resolution-fix-plan.md` 轉為 Layer 2 Wiki Concept 頁並歸檔

**Files:**
- Create: `AI_Brain/concepts/wsl-dns-resolution.md`
- Delete: `AI_Brain/_archive/raw/wsl-dns-resolution-fix-plan.md`

**Step 1: 建立 Concept 頁**

```markdown
---
title: WSL DNS Resolution Fix
created: 2026-04-14
updated: 2026-04-14
type: concept
tags: [WSL, DNS, Network, Windows]
sources: []
---

# WSL DNS Resolution Fix

## 問題
WSL 預設使用 Windows Host 的 DNS 解析器，無法解析某些外部域名（如 `*.trycloudflare.com`）。

## 解法
將 WSL 設定為使用公共 DNS 伺服器，繞過 Windows Host DNS 代理。

### 步驟 1：停用自動生成 resolv.conf
修改 `/etc/wsl.conf`：
```ini
[network]
generateResolvConf = false
```

### 步驟 2：替換為靜態 DNS
修改 `/etc/resolv.conf`：
```text
nameserver 1.1.1.1
nameserver 8.8.8.8
```

## 驗證
```bash
ping properties-evaluating-hearts-represents.trycloudflare.com
curl -I https://properties-evaluating-hearts-represents.trycloudflare.com/v1/models
```

## 注意事項
停用自動生成後，更換網路（如從家用 Wi-Fi 切到公司 VPN）需手動更新 `/etc/resolv.conf`。

## 相關頁面
- [[entities/hermes/hermes-gateway-systemd-fix]] — 相關 Systemd/WSL 環境問題
```

**Step 2: 刪除歸檔中的計劃檔**
```bash
rm AI_Brain/_archive/raw/wsl-dns-resolution-fix-plan.md
```

**Step 3: 更新 index.md**
在 Concepts 區段新增：
```markdown
- [[concepts/wsl-dns-resolution]] — WSL DNS 解析修復：停用 generateResolvConf + 設定靜態公共 DNS（1.1.1.1 / 8.8.8.8）
```

**Step 4: 更新 log.md**
追加：
```markdown
## [2026-04-14] ingest+archive | WSL DNS Resolution 計劃消化
- 建立 [[concepts/wsl-dns-resolution]]
- 刪除 _archive/raw/wsl-dns-resolution-fix-plan.md（已消化）
- index.md 總頁數更新為 8
```

---

## 驗收清單

- [ ] `entities/hermes/hermes-gateway-systemd-fix.md` 已建立，frontmatter 完整
- [ ] `entities/hermes/hermes-multiagent-discord-system.md` 已建立，frontmatter 完整
- [ ] 4 個 raw 檔案已移至 `_archive/raw/`
- [ ] CSAM 檔案已刪除
- [ ] `index.md` 已更新（Entities 條目 + 總頁數）
- [ ] `log.md` 已 append
- [ ] `concepts/wsl-dns-resolution.md` 已建立，frontmatter 完整
- [ ] `_archive/raw/wsl-dns-resolution-fix-plan.md` 已刪除
- [ ] `index.md` 總頁數更新為 8
- [ ] `log.md` 已追加 WSL 消化記錄
- [ ] 執行 `ls _archive/raw/` 確認 `wsl-dns-resolution-fix-plan.md` 已移除
