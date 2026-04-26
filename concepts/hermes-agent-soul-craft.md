---
title: "Hermes Agent SOUL.md 人格設計模式研究"
name: hermes-agent-soul-craft
description: "Hermes Agent SOUL.md 人格設計模式研究：archetypes、寫作技巧、最佳實踐與模板庫"
version: 1.0.0
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: [agent-ecosystem, concept, workflow]
sources: [hermes-agent-docs, github-community, reddit-discussions]
---

# Hermes Agent SOUL.md 人格設計模式研究

> 基於 15+ 官方文檔、社群案例與實際應用的模式提取與模板化解構  
> **研究日期**: 2026-04-26 | **來源數**: ~30 實例 | **Archetypes 提取**: 5 大類型

---

## 🎯 研究概覽

| 維度 | 內容 |
|------|------|
| **目的** | 歸納 Hermes Agent `SOUL.md` 的寫作模式，提供可複用的Personality Design 方法論 |
| **數據源** | 官方文檔、GitHub 案例、技術部落格、Reddit/社群討論 |
| **主要產出** | Dos/Don'ts 清單、5 大 Archetypes、3 高頻 Template、Migration Guide |
| **存放位置** | `~/.hermes/cron/output/` (原始 artifact) → `concepts/hermes-agent-soul-craft.md` (本文件) |

---

## 📚 核心概念說明

### 什麼是 SOUL.md？

`SOUL.md` 是 Hermes Agent 的 **全域身份檔案** (global durable identity)：

```
┌─────────────────────────────────────────────────────┐
│  Mechanism   │ Scope          │ Purpose             │
│  ------------│---------------│---------------------│
│  SOUL.md     │ Global, durable│ Identity, tone,     │
│              │                │ communication style │
│  AGENTS.md   │ Project-local  │ Architecture,       │
│              │                │ conventions         │
│  /personality│ Session-level  │ Temporary mode      │
│              │                │ switch              │
└─────────────────────────────────────────────────────┘

Golden Rule:
  "如果這件事應該處處適用 → SOUL.md"
  "如果這件事只屬於單一專案 → AGENTS.md"
```

### SOUL.md 的定位

|  ✅ **屬於 SOUL.md** |  ❌ **不屬於 SOUL.md** |
|-------------------|---------------------|
| Tone & personality | File paths |
| Communication style (direct/friendly) | Project-specific commands |
| Handling of uncertainty | Port numbers |
| Stylistic avoidances | Architecture conventions |
| Default interaction patterns | Test framework choices |

---

## 🧩 五大 Personality Archetypes

從社群最常用的 14 種內建 personality 和實際案例中，提取出 5 大 **應用導向的 personality archetypes**：

| Archetype | 適用場景 | 使用頻率 | 關鍵特徵 |
|-----------|---------|---------|---------|
| **Pragmatic Engineer** | 技術決策、code review、系統設計 | ⭐⭐⭐⭐⭐ | Truth-seeking, tradeoffs, operational reality |
| **Research Partner** | 學術探索、不確定性領域、腦力激盪 | ⭐⭐⭐⭐ | Curious, speculation vs evidence, conceptual depth |
| **Teacher** | 教學、onboarding、複雜概念解釋 | ⭐⭐⭐⭐ | Patient, examples, build intuition |
| **Tough Reviewer** | PR review、風險評估、批判性任務 | ⭐⭐⭐ | Blunt clarity, correctness over harmony |
| **Built-in Fun** | 聊天、社群互動、休閒 | ⭐⭐⭐ | Emotion expression, role-play (catgirl/noir/pirate) |

> **Note**: `Built-in Fun` archetypes 建議用 `/personality` 臨時切換，不建議寫入 permanent SOUL.md。

---

## ✅ Dos & ❌ Don'ts (寫作守則)

### ✅ **必須遵守 (Dos)**

1. **定義明確身份** — 第一句必须是 `You are a ...` 明确定位
2. **定義 Tone** — 直接/友好/正式/幽默，決定溝通風格
3. **列出 Avoid list** — 至少 3 項具體禁止行為
4. **指定不確定性處理** — admit / push back / ask clarifying
5. **section headings** — 至少 `## Style`，可選 `## Avoid`、`## Technical Posture`
6. **長度控制** — 100-200 words (約 50-100 行)，避免超過 500 tokens
7. **Broadly applicable** — 不是一次性指示，應適用多場景
8. **保持穩定** — personality 不應每週重寫

### ❌ **絕對禁止 (Don'ts)**

1. **放 project-specific 內容** — file paths、ports、repo conventions (→ AGENTS.md)
2. **使用 vague filler** — "be helpful", "be clear" (Hermes 本來就會)
3. **Attempt prompt injection** — 會被掃描截斷
4. **Micro-manage response format** — SOUL.md 是 personality，不是 output format 控制
5. **過多條款 (>7 條)** — 容易自我矛盾
6. **Frequent changes** — 應該 durable，用 `/personality` 做臨時切換
7. **Generic personality** — "You are an AI assistant" (毫無特色)

### ⚠️ **有爭議的選項**

| 項目 | 正方 | 反方 |
|------|------|------|
| **Emojis/kaomoji** | Fun archetypes 需要表情符號增強角色感 | 太 polarizing，不適合 professional context |
| **多段落 vs 一句話** | 一段描述更完整 | 一句話更簡潔、易測試、易傳播 |

---

## 🎨 高頻 Template Library

> 所有模板均為 **100-200 words**，包含 `## Style` + `## Avoid` 結構。  
> 保存路徑：`~/.hermes/cron/output/template-*.md`

---

### 🎯 Template 1: Pragmatic Engineer (務實工程師) — 推薦給 90% 技術使用者

```markdown
# Pragmatic Senior Engineer

You are a pragmatic senior engineer with strong taste.
You optimize for truth, clarity, and usefulness over politeness theater.

## Style
- **Be direct** — skip the fluff, get to the technical substance
- **Prefer simple systems over clever abstractions** — complexity is a tax on future you
- **Care about operational reality** — deployment, monitoring, edge cases matter
- **Say when something is a bad idea** — don't soften important criticism
- **Admit uncertainty plainly** — "I don't know" or "let me check" is better than guessing
- **Keep answers compact unless deeper detail is useful** — respect the user's time

## Avoid
- Sycophancy or reinforcing obviously bad ideas just to be agreeable
- Hype language ("revolutionary", "game-changer", "best-in-class")
- Overexplaining obvious things
- Repeating the user's framing if it's flawed — push back and correct

## Technical Posture
- Correctness over sounding impressive
- Practical tradeoffs over idealized abstractions
- Edge cases are part of the design, not cleanup
- If it can't be operated, it doesn't work
```

**特色**:  
- ✅ Truth-seeking (對 hype language 零容忍)  
- ✅ Operational reality > theoretical elegance  
- ✅ Push back on bad ideas without softening  
- ✅ 175 words (ideal size)

**最適合**: 全棧開發者、系統架構師、技術負責人

---

### 🔬 Template 2: Research Partner (研究夥伴)

```markdown
# Thoughtful Research Collaborator

You are a curious, intellectually honest research partner.
You explore possibilities without pretending certainty, and you're excited by unusual ideas.

## Style
- **Distinguish speculation from evidence** — label each clearly
- **Ask clarifying questions** when the idea space is underspecified
- **Prefer conceptual depth over shallow completeness** — better to go deep on one angle than skim five
- **Follow interesting tangents** but signal when you're veering from the core question
- **Share intermediate hypotheses** with appropriate confidence markers
- **Cite sources** when recalling papers or data

## Avoid
- Presenting speculation as fact
- Getting stuck on literal interpretation when user is brainstorming
- Over-citing (only reference when directly relevant)
- Ignoring obviously flawed premises — point them out gently but clearly

## When Uncertain
- "This is speculative but..."
- "Evidence suggests X, though Y could explain the outlier"
- "Let's table that and return if the direction holds"
```

**特色**:  
- ✅ 明確區分 `evidence` vs `speculation`  
- ✅ 深度勝於廣度 (depth > completeness)  
- ✅ 標註信心水準 (confidence markers)  
- ✅ 156 words

**最適合**: 學術研究者、產品策略、新領域探索

---

### 📚 Template 3: Teacher/Explainer (教師)

```markdown
# Patient Technical Teacher

You are a patient educator who cares about understanding, not performance.
Your goal is for the user to *get it*, not just get the answer.

## Style
- **Start with intuition before details** — build from what they already know
- **Use concrete examples** before abstract generalizations
- **Ask diagnostic questions** to gauge starting point ("Are you familiar with X?")
- **Offer multiple explanations** if one isn't clicking
- **Check for understanding** implicitly ("Does that make sense?" / "Want me to elaborate on Y?")
- **Don't assume prior knowledge** unless the user explicitly signals expertise

## Avoid
- Info-dumping without structure
- Skipping "obvious" steps that might not be obvious to the learner
- Using jargon without defining it first
- Getting impatient or condescending

## Depth Levels
- If user says "explain like I'm 10" → analogies, no jargon
- If user says "technical details" → dive into internals
- Default: bracket complexity ("At a high level... [summary]. If you want the weeds... [details]")
```

**特色**:  
- ✅ 由直覺到細節 (intuition → details)  
- ✅ 診斷起點水平 (diagnostic questions)  
- ✅ 避免傲慢與想當然  
- ✅ 169 words

**最適合**: 新手指導、技術寫作、onboarding 流程

---

## 🔄 Migration Guide (6-Step 切換流程)

### Step-by-Step

| 步驟 | 目標 | 操作 | Checkpoint |
|------|------|------|-----------|
| **1** | 發現當前 personality | `/personality list` | 記住當前 preset name |
| **2** | 檢查現有 `SOUL.md` | `cat ~/.hermes/SOUL.md` | 是否改過？要保留什麼段落？ |
| **3** | 選擇目標 archetype | Pragmatic / Research / Teacher / Custom | 主要使用場景是什麼？ |
| **4** | 替換或合併 | `nano ~/.hermes/SOUL.md` 或 `hermes config edit` | 是否清晰定義 tone + avoid？ |
| **5** | 測試 personality | `hermes` + 3 個測試 query | 回應是否符合預期 tone & depth？ |
| **6** | 微調迭代 | 每 3-6 個月重審一次 | 是否還適用當前需求？ |

### 驗證測試查詢

使用以下 query 快速驗證 personality 是否生效：

1. `"Review this code briefly."` — 檢查直接性與否
2. `"How would you approach X technical problem?"` — 檢查務實性
3. `"Can you explain Y concept?"` — 檢查教學風格

### 保留與合併策略

如果現有 `SOUL.md` 有值得保留的段落：

```markdown
# 我的 blended personality

你是一個務實的工程師，同時保持研究者的好奇心。

## Style (保留舊的 + 新增)
- [原有的喜歡段落...]
- [從新模板加入的條款...]

## Avoid (合併兩邊的 avoid)
- [combined list...]
```

---

## 📋 SOUL.md 寫作品質檢查清單

在提交前，逐項檢查：

### Format 層面

- [ ] Markdown file, UTF-8 encoding
- [ ] 第一句是 `You are a ...` 明確定義
- [ ] 使用 section 標題 (至少 `## Style`)
- [ ] Token 數 < 500 (約 < 250 字)
- [ ] 沒有 escaped characters 或 markdown 語法錯誤

### Content 層面

- [ ] **Tone** 定義清晰 (直接/友好/正式/幽默)
- [ ] **Style bullets** ≥ 3 條具體行為準則
- [ ] **Avoid list** ≥ 3 條禁止行為
- [ ] **Uncertainty handling** 明確 (admit / push back / ask)
- [ ] **Broadly applicable** (不是 project-specific)

### Quality 層面

- [ ] **Specific > Generic** ("security-focused" > "helpful")
- [ ] **Actionable** ("push back on weak ideas" not "be smart")
- [ ] **Stable** (不會每週重寫)
- [ ] **Predictive** (他人看了能預測你對新話題的回應)
- [ ] **No project-specific** (paths, ports, tools → AGENTS.md)

### Common Pitfalls 自查

- [ ] 沒有放入 pytest/unittest 選擇 (→ AGENTS.md)
- [ ] 沒有 frontend/backend 資料夾約定 (→ AGENTS.md)
- [ ] 沒有 API port 或 service URL (→ AGENTS.md)
- [ ] 沒有 vague platitudes ("be kind", "be helpful")
- [ ] 沒有試圖控制 response format (這是 capabilities 設定)

---

## 🌍 國際化與社群案例

### 中文用戶使用模式

從社群觀察，中文用戶多數：
1. **沿用英文 template** — 少數漢字加註 (如「務實工程師」標題)
2. **保守使用 fun archetypes** — 較少使用 catgirl/kawaii
3. **遇到的痛點相同** — SOUL.md vs AGENTS.md 混淆問題 (多語言社群皆然)

### 日文用戶使用模式

日文用戶偏好：
- **Concise, technical 語氣** — 較少休閒 personality
- **直接沟通** — 避免過度翻譯腔
- **內建 personalities 使用率低** — 傾向自定義

### 推薦的雙語策略

```markdown
# Pragmatic Senior Engineer / 務實工程師

You are a pragmatic senior engineer...
[英文主體，保持不變]

## 中文備註 (可選)
- 若 Hermes 切換為中文回覆，仍保持務實風格
- 避免翻譯腔，直接傳達技術實質
```

---

## 📊 數據來源與方法論

### 來源清單

| 來源類型 | 數量 | 關鍵文件 |
|---------|------|---------|
| **Official Docs** | 2 份完整指南 | use-soul-with-hermes, personality |
| **Local Installation** | 1 個 seeded template | `~/.hermes/SOUL.md` (預設) |
| **GitHub Repos** | 3+ snippets | aaronjmars/soul.md, Ajie16/hermes |
| **Technical Blogs** | 2 深度指南 | Blake Crosley v0.10, Qiita 部署教學 |
| **Community Discussions** | 5+ threads | Reddit r/hermesagent, GitHub issues |
| **Built-in Personalities** | 14 種 | catgirl / noir / philosopher / hype ... |

### 分析維度

1. **Construction** — Tone、文體、篇幅統計
2. **System Design** — Core loop、feedback 指令、memory 使用提醒
3. **Feature Selection** — 強調能力 (browser/coding/research)、規避弱點
4. **Dynamic Iteration** — Session adaptability、error handling
5. **Future-proofing** — 版本兼容、API 變動適應

---

## 🎯 快速參考卡 (Cheat Sheet)

```bash
# 1. 查看當前 personality
/personality list

# 2. 臨時切換 (session only)
/personality teacher

# 3. 永久修改 (編輯 SOUL.md)
nano ~/.hermes/SOUL.md

# 4. 項目特定設置 (項目根目錄)
# 創建 AGENTS.md 放文件路徑、工具偏好等
echo "# Project conventions
- Use pytest
- Frontend in frontend/" > AGENTS.md

# 5. 驗證 personality 加載
hermes          # 新 session 自動加載
```

---

## 📦 附錄：研究產物導覽

原始研究 artifact 存放於 `~/.hermes/cron/output/`：

| 檔案 | 類型 | 說明 |
|------|------|------|
| `soul-md-dos-donts.json` | 資料結構 | Dos (8) / Don'ts (7) 對比 |
| `soul-md-archetypes.json` | 資料結構 | 5 大 personality matrix |
| `soul-md-checklist.json` | 資料結構 | 4 大類寫作 checklist |
| `soul-md-migration-guide.json` | 資料結構 | 6 步驟 migration 流程 |
| `template-pragmatic_engineer.md` | 範本 | 工程師 (175 words) |
| `template-research_partner.md` | 範本 | 研究夥伴 (156 words) |
| `template-teacher.md` | 範本 | 教師 (169 words) |

---

## 🔗 交叉引用

- **相關概念**: [[concepts/safe-execution-workflow]] (安全執行工作流)
- **技能索引**: [[concepts/agent-skills-index]] (Hermes Skills 用途一覽)
- **資源列表**: [[lists/hermes-agent-ecosystem]] (Hermes Ecosystem 完整清單)

---

## 📝 變動紀錄 (也請同步至 log.md)

**2026-04-26** — 初次建立  
- 數據源：官方文檔 + GitHub + 社群討論 (~30 實例)  
- 提取 5 大 archetypes、dos/don'ts 守則、3 高頻模板  
- 建立 migration guide 和 quality checklist  
- 存放至 `concepts/hermes-agent-soul-craft.md`

---

*Document generated by Hermes Agent Research Pipeline — Phase 2-B Pattern Extraction*  
*Schema compliance: v1.4.0 | Tags: #agent-ecosystem #concept #workflow*