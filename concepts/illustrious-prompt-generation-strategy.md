---
title: Illustrious Prompt Generation Strategy
description: SillyTavern Quick Reply 專用提示詞生成策略
created: 2026-04-11
updated: 2026-04-12
type: concept
tags: [sillytavern, illustrious, prompt-engineering, workflow]
sources: [concepts/illustrious-prompt-guide]
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

## 預期輸出格式
`masterpiece, best quality, high detail, [Subject Description], [Action], [Environment], [Lighting/Atmosphere]`

*Note: 輸出應僅包含提示詞本身，不含任何解釋性文字。*

## 相關頁面
- [[concepts/illustrious-prompt-guide]] — Illustrious XL Prompt 完整指南
