---
name: illustrious-prompt-guide
description: Illustrious XL 圖像生成模型的 Prompt 撰寫與優化完整指南
version: 1.0.1
created: 2026-04-09
updated: 2026-04-10
type: concept
tags: [AI, 圖像生成, Stable Diffusion, Prompt Engineering, Illustrious, SDXL]
sources: [_archive/raw/articles/illustrious-prompt-guide-2026-04-09.md]
---

# Illustrious XL Prompt 撰寫與優化指南

Illustrious XL 是一款專為插畫設計的 Stable Diffusion XL (SDXL) 模型，支援從 256 到 2048 的任意解析度。

## 核心特色

- **v2.x 系列**：1536 原生解析度，解決 512x512 偽影問題
- **v3.x 系列**：大幅提升自然語言理解能力，可處理 424+ tokens 的複雜提示詞
- **Creative（EPS）**：風格化輸出，適合插畫創作
- **Expressive（VPred）**：提示詞遵循能力強，色彩控制精準

## Prompt 基本結構

```
[主體描述] → [風格/藝術家] → [光照/氛圍] → [品質標籤] → [技術參數]
```

## 模型選擇決策樹

```
需要訓練 LoRA？
├── 是 → 選 Base 模型（其他極難訓練）
└── 否
    ├── 複雜自然語言提示詞？→ Expressive / Expressive+
    ├── 追求美學品質？→ Creative / Creative+
    └── 通用場景 → Base 或 Refined
```

## 官方推薦參數

| 參數 | 建議值 |
|------|--------|
| Sampler | Euler a |
| CFG Scale | 7.5 |
| Steps | 28 |
| Schedule | Automatic |

## 必備品質標籤

```
masterpiece, best quality, high detail, absurdres, depth of field
```

## 負面提示詞

```
worst quality, low quality, lowres, low details, bad quality,
poorly drawn, bad anatomy, multiple views, bad hands, blurry,
artist signature
```

## 資料來源

- 官方網站：https://www.illustrious-xl.ai
- 原始分析：[raw/articles/illustrious-prompt-guide-2026-04-09.md](https://www.illustrious-xl.ai/blog)

## 相關頁面

- [[raw/articles/illustrious-prompt-guide-2026-04-09.md]] — 完整分析報告
