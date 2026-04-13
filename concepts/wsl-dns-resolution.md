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
