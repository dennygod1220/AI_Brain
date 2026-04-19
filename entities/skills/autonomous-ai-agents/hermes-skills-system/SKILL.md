---
name: hermes-skills-system
category: autonomous-ai-agents
description: Hermes Agent 技能系統完整指南 — 技能結構、載入機制、Skills Hub、外部技能目錄與代理管理
created: 2026-04-14
updated: 2026-04-19
sources:
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
  - raw/articles/Skills System  Hermes Agent.md
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [Hermes, Skills, Agent-System, API, Configuration]
    related_skills: [skill-manage, writing-plans]
prerequisites:
  commands: [hermes]
  env_vars: []
---

# Hermes Skills System

## 核心概念

Skills 是 Hermes Agent 的**按需載入知識文件**，採用 **progressive disclosure** 模式以最小化 token 使用量。兼容 [agentskills.io](https://agentskills.io/specification) 開放標準。

### 技能存放位置

| 位置 | 用途 | 讀寫權限 |
|------|------|---------|
| `~/.hermes/skills/` | 主要目錄，真相來源 | 讀寫 |
| `~/.hermes/skills/.hub/` | Skills Hub 狀態 | 只寫 |
| `entities/skills/` (AI Brain) | 歸檔技能庫 | 唯讀 (external_dirs) |

所有技能自動作為 slash command 可用：
```bash
/gif-search funny cats
/axolotl help me fine-tune Llama 3
/plan design a rollout
/excalidraw
```

## Progressive Disclosure 載入模式

```markdown
Level 0: skills_list()           → [{name, description, category}, ...]   (~3k tokens)
Level 1: skill_view(name)        → 完整內容 + metadata                    (varies)
Level 2: skill_view(name, path)  → 特定參考文件                           (varies)
```

Agent 僅在實際需要時才載入完整技能內容。

## SKILL.md 格式模板

```yaml
---
name: my-skill
description: Brief description
version: 1.0.0
platforms: [macos, linux]     # Optional
metadata:
  hermes:
    tags: [python, automation]
    category: devops
    fallback_for_toolsets: [web]    # Optional
    requires_toolsets: [terminal]   # Optional
    config:                          # Optional
      - key: my.setting
        description: "What this controls"
        default: "value"
        prompt: "Prompt for setup"
---

# Skill Title

## When to Use
Trigger conditions.

## Procedure
1. Step one
2. Step two

## Pitfalls
- Known failure modes

## Verification
How to confirm.
```

### 平台特定技能

```yaml
platforms: [macos]            # macOS only
platforms: [macos, linux]     # macOS + Linux
platforms: [windows]          # Windows only
```

### 條件激活 (Fallback Skills)

```yaml
metadata:
  hermes:
    fallback_for_toolsets: [web]      # 僅在 web toolset 不可用時顯示
    requires_toolsets: [terminal]     # 僅在 terminal 可用時顯示
    fallback_for_tools: [web_search]  # 僅在特定工具不可用時顯示
    requires_tools: [terminal]        # 僅在特定工具可用時顯示
```

| 欄位 | 行為 |
|------|------|
| `fallback_for_toolsets` | 當列出的 toolsets **可用時隱藏**，不可用時顯示 |
| `requires_toolsets` | 當列出的 toolsets **不可用時隱藏**，可用時顯示 |

**範例：** `duckduckgo-search` 使用 `fallback_for_toolsets: [web]`。有 `FIRECRAWL_API_KEY` 時使用 `web_search`，沒有時自動顯示 DuckDuckGo 作為 fallback。

## 安全設置 (Secure Setup on Load)

技能可聲明所需的環境變數：

```yaml
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: Tenor API key
    help: Get a key from https://developers.google.com/tenor
    required_for: full functionality
```

Hermes 會在本地 CLI 載入時安全地詢問，訊息平台則指示使用 `hermes setup` 或 `~/.hermes/.env`。

## 技能目錄結構

```
~/.hermes/skills/
├── mlops/
│   ├── axolotl/
│   │   ├── SKILL.md               # 主要指令 (必需)
│   │   ├── references/            # 額外文件
│   │   ├── templates/             # 輸出格式
│   │   ├── scripts/               # 輔助腳本
│   │   └── assets/                # 補充文件
│   └── vllm/
├── devops/
│   └── deploy-k8s/                # Agent 創建的技能
├── .hub/                          # Skills Hub 狀態
│   ├── lock.json
│   ├── quarantine/
│   └── audit.log
└── .bundled_manifest              # 追蹤已種子的 bundled skills
```

## 外部技能目錄 (External Skill Directories)

在 `~/.hermes/config.yaml` 中配置：

```yaml
skills:
  external_dirs:
    - ~/.agents/skills
    - /mnt/c/Users/denny/Downloads/SillyTavern/koboldcpp-config/AI_Brain/entities/skills
    - ${SKILLS_REPO}/skills
```

### 關鍵行為

- **唯讀**：外部目錄僅供掃描發現，Agent 創建的技能寫入 `~/.hermes/skills/`
- **本地優先**：同名技能在本地和外部都存在時，本地版本勝出
- **完整整合**：外部技能出現在 `skills_list`、`skill_view`、`/skill-name` 指令
- **無聲跳過**：不存在的目錄被忽略，適合跨機器的可選共享目錄

## Agent 管理技能 (skill_manage)

Agent 可透過 `skill_manage` 工具創建、更新、刪除自己的技能 — 這是**程序記憶**。

### 創建時機

- 完成複雜任務 (5+ tool calls) 後成功
- 遇到錯誤但找到解決路徑
- 用戶糾正方法
- 發現非平凡工作流程

### Actions

| Action | 用途 | 關鍵參數 |
|--------|------|----------|
| `create` | 從零創建新技能 | `name`, `content`, `category` |
| `patch` | 針對性修復 (首選) | `name`, `old_string`, `new_string` |
| `edit` | 重大結構重寫 | `name`, `content` |
| `delete` | 刪除技能 | `name` |
| `write_file` | 添加/更新支持文件 | `name`, `file_path`, `file_content` |
| `remove_file` | 刪除支持文件 | `name`, `file_path` |

> **Tip:** `patch` 比 `edit` 更 token-efficient，因為只包含變更的文字。

## Skills Hub

瀏覽、搜尋、安裝來自線上註冊表的技能。

### 常用指令

```bash
hermes skills browse                              # 瀏覽所有 hub 技能
hermes skills search kubernetes                   # 搜尋
hermes skills inspect openai/skills/k8s           # 預覽
hermes skills install openai/skills/k8s           # 安裝
hermes skills list --source hub                   # 列出已安裝
hermes skills check                               # 檢查更新
hermes skills update                              # 更新
hermes skills audit                               # 重新掃描安全
hermes skills uninstall k8s                       # 卸載
```

### 支持的 Hub 來源

| Source | 範例 | 說明 |
|--------|------|------|
| `official` | `official/security/1password` | Hermes 內建可選技能 |
| `skills-sh` | `skills-sh/vercel-labs/json-render` | Vercel 公共技能目錄 |
| `well-known` | `well-known:https://mintlify.com/docs` | 網站 `/.well-known/skills/` 端點 |
| `github` | `openai/skills/k8s` | 直接 GitHub 安裝 |
| `clawhub` | - | 第三方技能市場 |
| `lobehub` | - | LobeHub 代理目錄 |

### 信任等級

| Level | Source | Policy |
|-------|--------|--------|
| `builtin` | 隨 Hermes 發布 | 永遠可信 |
| `official` | `optional-skills/` | 內建信任，無第三方警告 |
| `trusted` | `openai/skills`, `anthropics/skills` | 比社區來源更寬鬆 |
| `community` | 其他所有 | 可用 `--force` 覆蓋非危險警告 |

### 安全掃描

所有 hub 安裝的技能都經過**安全掃描器**檢查：
- 數據外洩
- 提示注入
- 破壞性指令
- 供應鏈風險

`--force` 可覆蓋 caution/warn 級別，但**不能**覆蓋 `dangerous` 裁決。

### 更新生命週期

```bash
hermes skills check          # 報告哪些技能有上游更新
hermes skills update         # 重新安裝有更新的技能
hermes skills update react   # 更新特定技能
```

## 在聊天中使用 Slash Commands

```markdown
/skills browse
/skills search react --source skills-sh
/skills inspect skills-sh/vercel-labs/json-render
/skills install openai/skills/skill-creator --force
/skills check
/skills update
/skills list
```

## 常見問題

### GitHub Rate Limits

Skills Hub 使用 GitHub API，未認證用戶限制 60 請求/小時。設定 `GITHUB_TOKEN` 可提升到 5000 請求/小時。

```bash
# 在 ~/.hermes/.env 中添加:
GITHUB_TOKEN=your_token_here
```
