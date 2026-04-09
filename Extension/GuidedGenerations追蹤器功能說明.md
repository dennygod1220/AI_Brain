# GuidedGenerations擴充功能 - 追蹤器功能說明

## 功能概述
GuidedGenerations擴充功能的「統計追蹤器」(Stat Tracker) 是一個強大的工具，允許您追蹤角色狀態、故事進展或任何自定義指標。它通過兩階段的AI處理過程來分析最近的聊天訊息並更新追蹤資訊。

## 三個關鍵設定說明

### 1. 初始追蹤器格式 (Initial Tracker Format)
這是追蹤器的起始模板。當您首次設置追蹤器時，它會用這個格式建立一個注入。

**範例：**
```
> Distance {{char}} has moved in meters: 0
```

**說明：**
- 此格式會在聊天中建立一個初始的追蹤器項目
- `{{char}}` 佔位符會被替換為角色的名稱
- 您可以自訂這個格式來追蹤任何數值或狀態（例如：HP、親密度、故事進度等）

### 2. 引導提示詞 (Guide Prompt)
這告訴 AI 要在最近的訊息中尋找什麼來判斷有什麼變化。它用於第一個 API 呼叫 (`/gen`) 來分析對話。

**範例：**
```
[OOC: Answer me out of Character! Don't continue the RP. Considering the last message alone, write me how far {{char}} has moved in meter in the last message. Give an exact number of your best estimate.]
```

**說明：**
- 此提示詞要求 AI 檢查最近的訊息並確定特定變化（在這個例子中是角色移動的距離）
- 它是「分析階段」的核心，決定要追蹤什麼資訊
- 您可以修改這個提示詞來追蹤不同類型的變化（例如：情緒狀態、關係變化、故事進展等）

### 3. 追蹤器提示詞 (Tracker Prompt)
這告訴 AI 如何用新資訊更新你的追蹤器。它用於第二個 API 呼叫 (`/genraw`) 並接收兩個內容：
1. "Last Update" - 來自 Guide Prompt 的結果（什麼改變了）
2. "Tracker" - 目前的追蹤器內容

**範例：**
```
[OOC: Answer me out of Character! Don't continue the RP. Update the Tracker with the Last update without any preamble. Use the follwing format for your output:]
> Distance {{char}} has moved in meters: X
```

**說明：**
- 此提示詞取自 Guide Prompt 的分析結果，並將其格式化為追蹤器格式
- 它是「更新階段」的核心，決定如何呈現追蹤結果
- `[Tracker Information ...]` 部分會被插入到追蹤器注入中
- 最後的格式（如 `> Distance {{char}} has moved in meters: X`）決定了追蹤器在聊天中的顯示樣式

## 兩階段運作流程

追蹤器的運作分為兩個主要階段：

### 第一階段：決定階段 (Determine Phase)
1. 使用 **Guide Prompt** 分析最近的聊天訊息
2. AI 判斷在指定時間範圍內發生了什麼變化
3. 輸出這個變化的描述（例如：「角色向前移動了5公尺」）

### 第二階段：更新階段 (Update Phase)
1. 使用 **Tracker Prompt** 接收兩個內容：
   - "Last Update"：第一階段的分析結果
   - "Tracker"：目前的追蹤器內容
2. AI 根據這兩個內容生成更新後的追蹤器值
3. 更新追蹤器注入並建立可見的 Stat Tracker 注意

## 實際運作範例

假設我們要追蹤角色移動的距離：

**初始設置：**
- 初始追蹤器格式：`> Distance {{char}} has moved in meters: 0`
- 引導提示詞：`[OOC: Answer me out of Character! Don't continue the RP. Considering the last message alone, write me how far {{char}} has moved in meter in the last message. Give an exact number of your best estimate.]`
- 追蹤器提示詞：`[OOC: Answer me out of Character! Don't continue the RP. Update the Tracker with the Last update without any preamble. Use the follwing format for your output:]\n> Distance {{char}} has moved in meters: X`

**運作流程：**
1. 初始時，追蹤器顯示：`> Distance 冒險者 has moved in meters: 0`
2. 用戶發送訊息：「我們向前走了一段距離來到山腳下」
3. 第一階段：AI 根據引導提示詞分析訊息，判斷角色移動了大約300公尺
4. 第二階段：AI 使用追蹤器提示詞，將「角色移動了300公尺」格式化為追蹤器更新
5. 結果：追蹤器更新為 `> Distance 冒險者 has moved in meters: 300`
6. 同時在聊天中建立一個可見的 Stat Tracker 注意，顯示這次的更新內容

## 進階功能

### 包含目前追蹤器內容
在追蹤器設定中有一個選項：「Include Current Tracker in Guide Prompt Context」，當啟用時：
- 在第一階段的 Guide Prompt 中會加入目前的追蹤器內容
- 這對於需要參考先前狀態的追蹤很有用（例如：追蹤情緒變化時需要知道之前的情緒狀態）

### 自動觸發
追蹤器可以設定為在每次發送訊息時自動運行，無需手動觸發。

## 使用建議

1. **從簡單開始**：先追蹤易於量測的變化（如移動距離、數值變化）
2. **明確定義**：確保您的 Guide Prompt 能讓 AI 明確理解要尋找什麼變化
3. **格式一致**：確保 Tracker Prompt 輸出的格式與初始追蹤器格式匹配
4. **測試調整**：先在測試對話中試用，調整提示詞直到得到預期結果
5. **利用佔位符**：除了 `{{char}}` 之外，您還可以使用其他標準佔位符如 `{{user}}`、`{{random}}` 等

這個追蹤器功能讓您能夠以自然語言方式追蹤故事中的任何可量測變化，極大地增強了角色扮演的沉浸感和故事連續性。