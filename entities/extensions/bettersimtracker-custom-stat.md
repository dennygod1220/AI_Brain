---
name: bettersimtracker-custom-stat
description: BetterSimTracker 擴充套件的 Custom Stat 實作分析，含現有 6 種 stat kind 的結構、各層檔案職責對照，以及服裝/姿勢/位置 + Illustrious 生圖的具體應用規劃
version: 1.0.0
created: 2026-04-12
updated: 2026-04-12
type: analysis
tags:
  - #entity
  - #extension
  - #bettersimtracker
  - #custom-stat
  - #project
  - #illustrious
sources:
  - public/scripts/extensions/third-party/BetterSimTracker/src/types.ts
  - public/scripts/extensions/third-party/BetterSimTracker/src/customStatRuntime.ts
  - public/scripts/extensions/third-party/BetterSimTracker/src/statRegistry.ts
  - public/scripts/extensions/third-party/BetterSimTracker/src/parse.ts
  - public/scripts/extensions/third-party/BetterSimTracker/src/prompts.ts
  - public/scripts/extensions/third-party/BetterSimTracker/src/ui.ts
  - public/scripts/extensions/third-party/BetterSimTracker/src/settingsModal.ts
  - public/scripts/extensions/third-party/BetterSimTracker/src/graphTimeline.ts
  - public/scripts/extensions/third-party/BetterSimTracker/src/extractorHelpers.ts
  - public/scripts/extensions/third-party/BetterSimTracker/docs/ui-system.md
---

# BetterSimTracker Custom Stat 實作分析

## 擴充資訊

- **版本**: v2.5.3.1
- **原始碼**: `/mnt/c/Users/denny/Downloads/SillyTavern/SillyTavern/public/scripts/extensions/third-party/BetterSimTracker/`
- **入口**: `src/index.ts` (5097 行)
- **建構**: Webpack，`dist/` 已 committed，不需本地 build

---

## 一、Custom Stat 的 6 種 Kind

| Kind | 資料型別 | 萃取方式 | 圖表 | 預設顯示 |
|-------|---------|---------|------|---------|
| `numeric` | `number` (0-100) | delta + confidence 縮放 | ✅ | 進度條 |
| `enum_single` | `string` | 從 `enumOptions` 選一 | ❌ | 晶片 |
| `boolean` | `boolean` | true/false | ❌ | 開/關 |
| `text_short` | `string` | free text 有 maxLength | ❌ | 文字 |
| `array` | `string[]` | 項目列表 | ❌ | 晶片 + `+N more` |
| `date_time` | `string` | timestamp 或 structured | ❌ | 時間格式 |

---

## 二、`CustomStatDefinition` 核心結構

```typescript
interface CustomStatDefinition {
  id: CustomStatKey;              // 唯一 ID，用於 macro key
  kind?: CustomStatKind;          // 種類，預設 "numeric"
  label: string;                  // 顯示名稱
  description?: string;            // 萃取時給 LLM 的說明
  behaviorGuidance?: string;      // 僅用於 prompt injection

  // numeric 專屬
  defaultValue: number;           // 0-100
  maxDeltaPerTurn?: number;       // 單次 delta 上限

  // enum_single 專屬
  enumOptions?: string[];         // 最多 30 項

  // boolean 專屬
  booleanTrueLabel?: string;
  booleanFalseLabel?: string;

  // text_short / array 專屬
  textMaxLength?: number;          // 預設 120，上限 200

  // date_time 專屬
  dateTimeMode?: "timestamp" | "structured";

  // 追蹤範圍
  track: boolean;
  trackCharacters?: boolean;
  trackUser?: boolean;
  globalScope?: boolean;           // 全域 stat → Scene Card
  privateToOwner?: boolean;        // owner-scoped privacy

  // 顯示控制
  showOnCard: boolean;
  showInGraph: boolean;            // 目前僅 numeric 有效
  includeInInjection: boolean;    // 加入 prompt injection
  color?: string;                  // 卡上顏色

  // Prompt 控制
  promptOverride?: string;         // per-stat prompt template
  sequentialGroup?: string;        // 分組批次萃取
}
```

---

## 三、檔案職責對照

| 檔案 | 職責 | 與 Kind 的關聯方式 |
|------|------|---------------------|
| `types.ts` | `CustomStatKind` 型別、`CustomStatDefinition` 結構、儲存型別 | 所有 kind 源頭定義 |
| `customStatRuntime.ts` | 值正規化 | 每個 kind 在 `normalizeCustomNonNumericValue()` 有一條分支 |
| `statRegistry.ts` | `CustomStatDefinition` → `NumericStatDefinition` 統一介面 | 僅 `kind === "numeric"` 進這條線 |
| `prompts.ts` | 萃取 prompt 生成 | `buildSequentialCustomNumericPrompt()` / `buildSequentialCustomNonNumericPrompt()`，kind 決定用哪個 builder |
| `parse.ts` | 解析 LLM JSON 回應 | `parseCustomDeltaResponse()`（numeric）/ `parseCustomValueResponse()`（其餘五種） |
| `ui.ts` | 追蹤卡渲染 | kind 決定晶片/文字/陣列/`+N more` 呈現方式 |
| `settingsModal.ts` | 新增/編輯精靈 | kind 影響步驟二的約束欄位顯示 |
| `graphTimeline.ts` | 圖表繪製 | 目前僅 `numeric` 支援 |

---

## 四、萃取資料流

```
LLM 回應（JSON 字串）
    ↓
parseCustomDeltaResponse()        ← numeric 用
parseCustomValueResponse()        ← 其餘五種用（傳入 kind）
    ↓
normalizeCustomNonNumericValue()  ← 正规化
    ↓
寫入 TrackerData:
  - numeric    → customStatistics[id][ownerName] = number
  - 非 numeric → customNonNumericStatistics[id][ownerName] = string|boolean|string[]
```

---

## 五、Prompt Macro 組合

BST 輸出以下 macro 供外部使用（對應你的生圖需求）：

| Macro | 說明 | 範例值 |
|-------|------|--------|
| `{{bst_injection}}` | 整塊 injection 內容 | 完整追蹤狀態文字 |
| `{{bst_stat_<id>}}` | 特定 stat 的現值 | `{{bst_stat_clothing}}` → `"wearing a black dress"` |
| `{{bst_stat_char_<id>_<target_slug>}}` | 指定角色的特定 stat | Dynamic Characters 模式下解析 |
| `{{bst_char_<id>}}` | 角色 macro | 需確認準確名稱 |

---

## 六、應用場景：服裝 / 姿勢 / 位置 → Illustrious 生圖

### 6.1 建議的 Stat 規劃

| Stat ID | Kind | 說明 | Prompt 組合用途 |
|---------|------|------|----------------|
| `clothing` | `enum_single` 或 `text_short` | 角色穿著 | 直接嵌入正向提示詞 |
| `pose` | `enum_single` | 姿勢狀態 | 姿態描述 |
| `location` | `enum_single` 或 `text_short` | 場景位置 | 背景/環境 |

**推荐 Kind 選擇**：
- `clothing` → `text_short`（彈性最大，free text）
- `pose` → `enum_single`（列舉保證值一致性，諸如 `standing`, `sitting`, `lying`, `leaning`）
- `location` → `text_short`（描述性文字）

### 6.2 生圖 Macro 組合流程

1. 在 BST 設定中新增這三個 custom stat，`includeInInjection: true`
2. 萃取日後，每則 AI 回應自動更新這三個 stat 的現值
3. 在 Illustrious 的正向提示詞中，使用 BST macro 組合：
   ```
   {{bst_stat_clothing}}, {{bst_stat_pose}}, {{bst_stat_location}}, highly detailed, porcelain-like skin
   ```

### 6.2 需要確認的事項

- [ ] BST 的 `{{bst_stat_<id>}}` macro 是否在 Illustrious 生圖階段已展开？（需確認 BST 與 Illustrious 的 macro 擴展順序）
- [ ] 若需要更精確的服裝描述，`clothing` 用 `text_short` 而非 `enum_single` 是否足夠？（建議先試 `text_short`）
- [ ] 姿勢是否需要分為「上半身」/`下半身` 兩個 stat？（視需求決定）

---

## 七、新增 Kind 的實作路線（若有需要）

若現有六種 kind 不足以滿足需求（例如需要圖片 URL 或情緒枚舉），新增方式：

1. **`src/types.ts`** — `CustomStatKind` 加一項
2. **`src/customStatRuntime.ts`** — `normalizeCustomNonNumericValue()` 加分支
3. **`src/parse.ts`** — `parseCustomValueResponse()` 加分支
4. **`src/prompts.ts`** — 確認 prompt builder 已經 kind-agnostic（多數情況不需改）
5. **`src/ui.ts`** — 渲染邏輯加新分支
6. **`src/settingsModal.ts`** — wizard 步驟二加新 kind 的欄位條件

---

## 八、相關原始檔案路徑

```
BetterSimTracker/
├── src/
│   ├── types.ts                    ← CustomStatKind, CustomStatDefinition, TrackerData
│   ├── customStatRuntime.ts        ← normalizeCustomNonNumericValue()
│   ├── statRegistry.ts             ← NumericStatDefinition 統一介面
│   ├── prompts.ts                  ← buildSequentialCustomNonNumericPrompt()
│   ├── parse.ts                    ← parseCustomValueResponse()
│   ├── ui.ts                       ← 追蹤卡渲染
│   ├── settingsModal.ts            ← Custom stat wizard UI
│   ├── graphTimeline.ts            ← 圖表繪製
│   ├── extractorHelpers.ts         ← enabledCustomStats(), groupCustomStatsForSequential()
│   └── extractor.ts                ← 萃取主管線
└── docs/
    └── ui-system.md                ← UI 合約文件
```
