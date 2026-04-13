# Fix WSL DNS Resolution Issue

The domain `properties-evaluating-hearts-represents.trycloudflare.com` is active and reachable, but the default WSL DNS resolver (bridged from Windows) is failing to resolve it. We will switch WSL to use public DNS servers directly to bypass this limitation.

## Proposed Changes

### [WSL System Configuration]

#### [MODIFY] [/etc/wsl.conf](file:///etc/wsl.conf)
We will add a configuration to prevent WSL from automatically regenerating `/etc/resolv.conf` with the Windows host IP.

```ini
[network]
generateResolvConf = false
```

#### [MODIFY] [/etc/resolv.conf](file:///etc/resolv.conf)
We will replace the auto-generated file with a static one pointing to reliable public DNS servers.

```text
nameserver 1.1.1.1
nameserver 8.8.8.8
```

## Verification Plan

### Manual Verification
1. Run `ping properties-evaluating-hearts-represents.trycloudflare.com` (just the domain, not the URL).
2. Run `curl -I https://properties-evaluating-hearts-represents.trycloudflare.com/v1/models`.
3. Verify that `koboldcpp_local` can now reach the endpoint.

> [!IMPORTANT]
> Since we are disabling automatic generation of `/etc/resolv.conf`, you might need to manually update it if you change networks (e.g., switching from a home Wi-Fi to a corporate VPN that requires specific DNS).
