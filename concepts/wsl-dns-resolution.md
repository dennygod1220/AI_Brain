---
name: wsl-dns-resolution
description: WSL DNS 解析問題修復方案與配置指南
version: 1.0.0
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [WSL, Networking, DNS, Fix]
sources: ['_archive/raw/wsl-dns-resolution-fix-plan.md']
---

# WSL DNS Resolution Fix

## Problem
WSL (Windows Subsystem for Linux) default DNS resolver, which is bridged from the Windows host, often fails to resolve specific domains (e.g., Cloudflare tunnels like `*.trycloudflare.com`).

## Solution
To bypass the automatic DNS generation, we must disable the automatic generation of `/etc/resolv.conf` and set a static configuration.

### 1. Modify `/etc/wsl.conf`
Add the following configuration to prevent WSL from automatically regenerating `/etc/resolv.conf` with the Windows host IP:

```ini
[network]
generateResolvConf = false
```

### 2. Modify `/etc/resolv.conf`
Replace the auto-generated file with a static one pointing to reliable public DNS servers:

```text
nameserver 1.1.1.1
nameserver 8.8.8.8
```

## Verification
1. Run `ping <domain>` to check connectivity.
2. Run `curl -I https://<domain>/v1/models` to verify API accessibility.

> [!IMPORTANT]
> Since automatic generation is disabled, you must manually update `/etc/resolv.conf` if you switch to networks (like corporate VPNs) that require specific DNS servers.
