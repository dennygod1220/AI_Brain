# GuidedGenerations-Extension 分析報告

## 1. 概述

| 項目 | 內容 |
|------|------|
| **名稱** | Guided Generations Extension |
| **作者** | Samueras |
| **版本** | 1.6.6 (manifest v3) |
| **許可證** | GPL-3.0 |
| **定位** | 將「Quick Reply」集的引導式生成功能轉換為 SillyTavern 原生擴展 |

**核心價值**：讓用戶通過 UI 按鈕和自動觸發機制，以自然語言指令精確控制 AI 的角色扮演輸出——包括角色思想、服裝、狀態、規則等持久化上下文注入。

---

## 2. 架構設計

### 2.1 目錄結構

```
GuidedGenerations-Extension/
├── manifest.json                     # 擴展元數據
├── index.js                          # 入口（1993 行）— 初始化、事件監聽、按鈕管理
├── settings.html                     # 設置面板 HTML（611 行）
├── style.css                         # 樣式（613 行）
├── GGSytemPrompt.json                # 默認預設文件
├── scripts/
│   ├── guidedResponse.js             # 引導回應
│   ├── guidedSwipe.js                # 引導滑動
│   ├── guidedContinue.js             # 引導續寫 + Undo/Revert
│   ├── guidedImpersonate.js          # 第一人稱模擬
│   ├── guidedImpersonate2nd.js       # 第二人稱模擬
│   ├── guidedImpersonate3rd.js       # 第三人稱模擬
│   ├── simpleSend.js                 # 直接發送
│   ├── inputRecovery.js              # 輸入恢復
│   ├── settingsPanel.js              # 設置面板加載
│   ├── persistentGuides/             # 持久化引導模組（17 文件）
│   │   ├── runGuide.js               # 通用引導執行引擎
│   │   ├── thinkingGuide.js          # 思想引導
│   │   ├── clothesGuide.js           # 服裝引導
│   │   ├── stateGuide.js             # 狀態引導
│   │   ├── situationalGuide.js       # 情境引導
│   │   ├── rulesGuide.js             # 規則引導
│   │   ├── customGuide.js            # 自定義引導
│   │   ├── customAutoGuide.js        # 自定義自動引導
│   │   ├── funGuide.js               # 趣味提示
│   │   ├── trackerGuide.js           # 統計追蹤
│   │   ├── trackerLogic.js           # 追蹤核心邏輯
│   │   ├── editGuides.js             # 編輯引導
│   │   ├── editGuidesPopup.js        # 編輯彈窗
│   │   ├── showGuides.js             # 顯示引導
│   │   ├── flushGuides.js            # 清除引導
│   │   ├── updateCharacter.js        # 更新角色（已註釋）
│   │   └── guideExports.js           # 中央匯出樞紐
│   ├── tools/                        # 工具模組
│   │   ├── clearInput.js             # 清空輸入
│   │   ├── corrections.js            # 糾正最後消息
│   │   ├── spellchecker.js           # 拼寫檢查
│   │   ├── editIntros.js             # 編輯開場白入口
│   │   ├── editIntrosPopup.js        # 開場白編輯彈窗（570 行）
│   │   ├── funPopup.js               # 趣味提示彈窗
│   │   └── funPrompts.txt            # 趣味提示數據
│   ├── ui/
│   │   └── versionNotificationPopup.js  # 版本通知彈窗
│   └── utils/
│       └── presetUtils.js            # 配置檔/預設切換工具（1154 行）
```

### 2.2 架構模式：Hub-and-Spoke（樞紐輻射）

```
                    ┌─────────────────────┐
                    │   guideExports.js   │  ← 中央匯出樞紐
                    │  (re-exports all)   │
                    └─────────┬───────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌────▼────┐          ┌─────▼────┐
   │ 核心操作 │          │ 持久引導 │          │  工具模組  │
   │ Response │          │ Thinking │          │Corrections│
   │ Swipe    │          │ Clothes  │          │Spellcheck │
   │ Continue │          │ State    │          │EditIntros │
   │Impersonate│         │ Rules    │          │ClearInput │
   └───────────┘          └─────────┘          └───────────┘
```

**關鍵設計決策**：所有模組從 `guideExports.js` 導入，避免深層相對路徑和循環依賴。

---

## 3. 核心功能模組詳解

### 3.1 引導式生成（Guided Generation）

| 功能 | 按鈕 | STScript 核心命令 | 行為 |
|------|------|-------------------|------|
| **Guided Response** | `fa-dog` | `/inject id=instruct` + 生成 | 將用戶指令注入聊天上下文，引導下一條 AI 回复 |
| **Guided Swipe** | `fa-forward` | `/inject` + `context.swipe.right()` | 帶新指令重新生成最後一條 AI 消息（swipe） |
| **Guided Continue** | `fa-arrow-right` | `/continue await=true` | 在現有消息末尾續寫，支持 Undo/Revert |
| **Impersonate 1st/2nd/3rd** | `fa-user`/`fa-user-group`/`fa-users` | `/impersonate await=true` | 將大綱擴展為指定視角的完整消息 |

**共同模式**：
1. 捕獲 textarea 原始輸入
2. 填充 prompt 模板（替換 `{{input}}`）
3. 通過 `/inject` 注入指令（支持 `ephemeral=true`、`scan=true`、可配置 depth/role）
4. 觸發生成
5. `finally` 塊恢復原始輸入

### 3.2 持久化引導（Persistent Guides）

| 引導類型 | 注入 ID | 自動觸發 | 功能 |
|---------|---------|---------|------|
| Situational | `situation` | 否 | 生成當前場景摘要（位置、角色、事件） |
| Thinking | `thinking` | 可選 | 生成角色內心想法 |
| Clothes | `clothes` | 可選 | 描述角色服裝 |
| State | `state` | 可選 | 描述角色物理狀態/姿勢 |
| Rules | `rule_guide` | 否 | 生成/更新角色遵循的規則列表 |
| Custom | `Custom` | 否 | 用戶自定義上下文注入 |
| Custom Auto | 可配置 | 可選 | 用戶自定義自動引導 |
| Fun | - | 否 | 趣味提示彈窗 |

**管理操作**：
- Edit Guides — 創建/編輯/刪除持久引導
- Show Guides — 顯示所有活躍引導內容
- Flush Guides — 清除選定或全部引導

### 3.3 統計追蹤器（Stat Tracker）

**兩階段架構**：
1. **Determine 階段**：使用 `/gen` 分析聊天變化（可配置 profile/preset）
2. **Update 階段**：使用 `/genraw` 生成追蹤更新 → `/inject id=tracker` 注入

追蹤結果同時以：
- 不可見注入（發送到 LLM）
- 可見系統消息（`<details>` 折疊 HTML，展示給用戶）

### 3.4 自動觸發系統

監聽 `GENERATION_AFTER_COMMANDS` 事件，條件過濾：
```javascript
if ((type === 'normal' || typeof type === 'undefined') && !dryRun && !generateArgsObject?.signal)
```

執行順序：
1. 保存 ephemeral `instruct` 注入（防止被覆蓋）
2. 檢查 `send_if_empty` 兼容性（有則彈窗警告並禁用所有自動引導）
3. 按序執行：Thinking → State → Clothes → Custom Auto
4. 執行 Tracker（如啟用）
5. 恢復 `instruct` 注入

### 3.5 配置檔/預設切換系統（`presetUtils.js`，1154 行）

這是擴展中最複雜的單一模組，提供：

| 功能 | 說明 |
|------|------|
| `handleSwitching(profile, preset, originalProfile)` | 返回 `{ switch, restore }` 配對函數 |
| `withProfile(targetProfile, operation)` | 臨時切換配置檔執行操作後恢復 |
| `getProfileApiType(profileName)` | 查詢配置檔對應的 API 類型 |
| `getPresetsForApiType(apiType)` | 獲取指定 API 類型的預設列表 |

**切換策略**：事件等待為主 → 輪詢回退 → 安全延遲（profile 500ms / preset 200ms）

---

## 4. SillyTavern API 集成點

| API | 用途 |
|-----|------|
| `SillyTavern.getContext().executeSlashCommandsWithOptions()` | 執行所有 STScript 命令 |
| `context.swipe.right()` | 觸發新 swipe 生成 |
| `eventSource.on(event_types.XXX)` | 監聽聊天事件（GENERATION_AFTER_COMMANDS、CHARACTER_MESSAGE_RENDERED 等） |
| `eventSource.makeLast(eventName, callback)` | 在事件鏈末尾掛接回調 |
| `extension_settings[extensionName]` | 持久化設置存儲 |
| `context.chatMetadata.script_injects` | 讀取/管理注入狀態 |
| `context.chatMetadata[extensionName + '_trackers']` | 追蹤器狀態（per-chat） |
| `context.getPresetManager(apiId)` | 預設管理器 |
| `context.extensionSettings.connectionManager` | 連接配置檔管理 |
| `/inject`, `/flushinject`, `/gen`, `/genraw`, `/continue`, `/impersonate`, `/buttons`, `/trigger` | STScript 命令 |

---

## 5. 設置系統

### 5.1 設置類別

| 類別 | 關鍵設置 |
|------|---------|
| **按鈕可見性** | `showImpersonate1stPerson`, `showGuidedResponse`, `showGuidedSwipe`, `showGuidedContinue` 等 |
| **自動觸發** | `autoTriggerClothes`, `autoTriggerState`, `autoTriggerThinking`, `enableAutoCustomAutoGuide` |
| **注入設置** | `injectionEndRole`（system/assistant/user） |
| **UI 偏好** | `integrateQrBar`, `debugMode`, `persistentGuidesInChatlog` |
| **Profile/Preset** | 每個引導獨立的 `profileXxx` / `presetXxx` / `profileXxxApiType` |
| **Prompt 覆蓋** | `promptXxx`（可自定義模板）、`rawPromptXxx`（原始模式）、`depthPromptXxx`（注入深度） |
| **安全超時** | `profileSwitchTimeout`（500ms）、`presetSwitchTimeout`（200ms） |

### 5.2 設置持久化

- 通過 `saveSettingsDebounced()` 異步保存
- 使用事件委託（`handleSettingsChangeDelegated`）統一處理所有設置變更
- 支持配置檔變更時自動刷新對應預設下拉列表

---

## 6. 代碼質量評估

### 優點
- **模塊化設計清晰**：hub-and-spoke 架構有效避免循環依賴
- **健壯的錯誤處理**：關鍵操作均有 try/catch，profile switching 有事件+輪詢雙重保障
- **詳細的調試系統**：`debugLog`/`debugWarn`/`debugError` 帶堆棧追蹤，支持複製/下載/清除
- **良好的用戶體驗**：版本通知、按鈕可見性控制、QR Bar 集成、持久引導計數器
- **配置檔/預設系統完善**：支持每個引導使用不同模型/API

### 潛在問題
- **`index.js` 過大**（1993 行）：入口文件承載了過多職責（按鈕創建、事件監聽、設置管理、自動觸發）
- **QR Bar 集成使用輪詢 + MutationObserver 雙重機制**：略顯冗餘，可簡化為單一 Observer
- **`guideExports.js` 循環導入風險**：該文件從 `index.js` 導入 `loadSettings`/`updateSettingsUI`/`addSettingsEventListeners`，而 `index.js` 又從 `guideExports.js` 導入其他模組——存在潛在循環依賴
- **硬編碼的延遲**：多處使用 `setTimeout`（100ms、500ms、700ms、2000ms、3000ms、5000ms）作為等待機制，不夠可靠
- **`updateCharacter` 功能已註釋**：代碼存在但未啟用
- **設置 key 命名不一致**：部分使用 camelCase（`autoTriggerClothes`），部分使用 PascalCase 風格

---

## 7. 依賴關係圖

```
index.js
├── scripts/simpleSend.js
├── scripts/inputRecovery.js
├── scripts/guidedResponse.js
├── scripts/guidedSwipe.js
├── scripts/guidedContinue.js
├── scripts/guidedImpersonate.js / 2nd / 3rd
├── scripts/persistentGuides/updateCharacter.js
├── scripts/persistentGuides/customAutoGuide.js
├── scripts/persistentGuides/thinkingGuide.js
├── scripts/persistentGuides/stateGuide.js
├── scripts/persistentGuides/clothesGuide.js
├── scripts/persistentGuides/trackerLogic.js
├── scripts/persistentGuides/guideExports.js  ← 中央樞紐
│   ├── utils/presetUtils.js
│   ├── persistentGuides/runGuide.js
│   ├── persistentGuides/*.js (all guides)
│   ├── tools/*.js
│   └── index.js (settings functions) ← 循環引用
├── scripts/settingsPanel.js
├── scripts/ui/versionNotificationPopup.js
├── SillyTavern extensions.js (getContext, extension_settings, renderExtensionTemplateAsync)
├── SillyTavern script.js (eventSource, event_types, saveSettingsDebounced)
└── SillyTavern preset-manager.js (getPresetManager)
```

---

## 8. 總結

這是一個功能豐富、架構合理的 SillyTavern 第三方擴展，成功將 Quick Reply 集的引導式生成能力轉換為原生擴展體驗。其核心競爭力在於：

1. **多維度引導控制**：從一次性指令（Response/Swipe/Continue）到持久化上下文（Thinking/Clothes/State/Rules）
2. **自動化能力**：自動觸發機制 + 統計追蹤器減少手動操作
3. **靈活的模型配置**：每個引導可獨立配置 Profile/Preset，實現「用不同模型做不同事」
4. **完善的工具集**：糾正、拼寫檢查、開場白編輯、輸入恢復等實用工具
