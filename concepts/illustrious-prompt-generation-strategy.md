---
title: Illustrious Prompt Generation Strategy
description: SillyTavern Quick Reply 專用提示詞生成策略，含 BetterSimTracker macro 整合實務
created: 2026-04-11
updated: 2026-04-12
type: concept
tags: [sillytavern, illustrious, prompt-engineering, workflow, bettersimtracker, macro]
sources: [concepts/illustrious-prompt-guide, entities/extensions/bettersimtracker-custom-stat]
---

# Illustrious Prompt Generation Strategy (SillyTavern Quick Reply)

## 核心設計邏輯
將聊天內容轉化為適用於 Illustrious XL 的自然語言提示詞，強調空間關係、材質與光影。

## 三層轉化架構
1. **情境萃取 (Context Extraction)**: 從對話中提取角色外貌、動作、環境、光影與情緒。
2. **語法轉化 (Syntax Transformation)**: 將對話敘述轉化為高品質的英文自然語言描述，避免破碎的 Tag 堆疊。
3. **品質注入 (Quality Injection)**: 自動補足高品質詞彙與光影術語。

## 提示詞組成模組
- **Subject**: 角色細節、服裝、神情。
- **Action**: 肢體語言、互動動作。
- **Environment**: 背景、天氣、場景深度。
- **Lighting/Atmosphere**: 光線方向、色調、空氣感 (e.g., cinematic lighting, dappled light, chiaroscuro)。

## BetterSimTracker Macro 整合實務 (2026-04-12 發現)

### Macro 格式
```
{{bst_stat_user_char_clothing}}  → {{user}} 服裝
{{bst_stat_char_char_clothing}}  → {{char}} 服裝
{{bst_stat_user_char_pose}}      → {{user}} 姿勢
{{bst_stat_char_char_pose}}      → {{char}} 姿勢
{{bst_stat_user_char_appearance}}→ {{user}} 外觀
{{bst_stat_char_char_appearance}}→ {{char}} 外觀
{{bst_stat_user_char_location}}  → {{user}} 位置
{{bst_stat_char_char_location}}  → {{char}} 位置
```

### 問題：Tag 格式模型會交換角色身份
即使 prompt 邏輯正確區分了角色，SDXL 模型仍可能在生圖時將 {{char}} 和 {{user}} 的服裝/外觀交換。

### 解決方案：自然語言 Fact-Statement 格式
放棄純 tag 格式，改用「先確立事實、再描述動作」的結構：

1. 先描述 {{char}} 的完整外觀和穿著（用 "is wearing" / "wears" 事實陳述）
2. 再描述 {{user}} 的完整外觀和穿著
3. 最後才描述場景動作
4. 明確禁止模型自行推斷服裝，只允許服裝出現在服裝描述區塊

### QR 模板結構
```
/gen [You are an image prompt writer.
[CHARACTER DATA BLOCK - 完整列出所有 macro]
[OUTPUT FORMAT - 一段自然語言]
[CRITICAL RULES - 先服裝確認再動作]
]
/imagine extend=false edit=true {{pipe}}
```

## 預期輸出格式
`masterpiece, best quality, high detail, [Subject Description], [Action], [Environment], [Lighting/Atmosphere]`

*Note: 輸出應僅包含提示詞本身，不含任何解釋性文字。*

## 相關頁面
- [[concepts/illustrious-prompt-guide]] — Illustrious XL Prompt 完整指南
- [[entities/extensions/bettersimtracker-custom-stat]] — BetterSimTracker Custom Stat 實作分析
