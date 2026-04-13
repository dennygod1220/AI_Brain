# Hermes 多 Agent 通訊：系統底層 (discord.py) 修改指南

如果你未來更新了 Hermes Agent 導致 `discord.py` 被官方版本覆蓋，造成多台 Agent 之間無法溝通或開始搶話。不用擔心，你可以透過這份指南快速把失去的功能補回來。

## 方法一：自動打補丁 (最快)
我都幫你準備好了！只要在更新 Hermes 後，在終端機中執行以下指令，就能瞬間把修改加回去：
```bash
cd /root/.hermes/hermes-agent
git apply /root/hermes_multiagent_discord.patch
```

---

## 方法二：手動修改指南 (如果你想自己看懂並微調)
如果因為官方把 `discord.py` 進行了大幅度的改寫，導致上面的 `.patch` 補丁檔案因為「行數對不上」而失效（這是很常見的），請不要慌張，只要按照以下的核心邏輯，手動把代碼貼上即可。

### 核心修改 1：讓 Bot 能聽懂「身分組 (@Role)」標記
**目的**：讓 Bot 在收到其他 Bot 傳來的訊息時，如果對方標記的是「身分組」而非「使用者」，也能正確識別我們被點名了。

**修改位置**： 搜尋 `allow_bots == "mentions":`
在你看到以下這段原始官方代碼時：
```python
if allow_bots == "mentions":
    if not self._client.user or self._client.user not in message.mentions:
        return
```
**將其改寫或替換為以下邏輯**：
```python
if allow_bots == "mentions":
    _self_mentioned = (
        self._client.user is not None
        and (
            self._client.user in message.mentions
            or (
                message.guild
                and any(r in message.role_mentions for r in message.guild.me.roles)
            )
        )
    )
    if not _self_mentioned:
        return
```

---

### 核心修改 2：多 Agent「防止搶話」的絕對過濾器
**目的**：如果 Jason 在同一個討論串中標記了 `@蝦蝦`，那麼 `@小低能` 就算身在同一個討論串也要保持絕對沉默。官方的代碼在這裡有漏洞，它只檢查了使用者標記，沒有檢查「身分組標記」。

**修改位置**： 搜尋 `_other_bots_mentioned`
在你看到以下這段官方代碼時：
```python
_other_bots_mentioned = any(
    m.bot and m != self._client.user
    for m in message.mentions
)
# If other bots are mentioned but we're not → not for us
if _other_bots_mentioned and not _self_mentioned:
    return
```
**將其擴展為以下邏輯**（加入對身分組的判斷）：
```python
_other_bots_mentioned = any(
    (m.bot and m != self._client.user)
    for m in message.mentions
)

# 檢查是否有標記別人的「身分組」
_other_bot_roles_mentioned = False
if message.guild and message.role_mentions:
    my_role_ids = [r.id for r in message.guild.me.roles]
    for role in message.role_mentions:
        if role.id not in my_role_ids:
            # 第一層：檢查這個身分組是不是綁定給其他 Bot 的
            if role.tags and role.tags.bot_id and self._client.user and role.tags.bot_id != self._client.user.id:
                _other_bot_roles_mentioned = True
                break
            # 第二層：如果名字裡包含其他代理的常見名字，也當作別人的
            my_name = self.name.lower()
            role_name = role.name.lower()
            if any(name in role_name for name in ["蝦蝦", "蝦搬", "小低能"]) and my_name not in role_name:
                _other_bot_roles_mentioned = True
                break

# 如果別人被標記了且我們沒有被標記 → 強制閉嘴 (Return)丟棄封包
if (_other_bots_mentioned or _other_bot_roles_mentioned) and not _self_mentioned:
    return
```

---

### 核心修改 3：讓討論串具備「自動拉人」功能
**目的**：Discord 在建立私密討論串時，不會自動把身分組（如 `@小低能`）裡的 Bot 拉進去。這會讓小低能變成又聾又瞎的狀態。

**修改位置**：搜尋 `_auto_create_thread`，然後往下找 `await message.create_thread`
在官方的這段建構代碼底下：
```python
try:
    thread = await message.create_thread(name=thread_name, auto_archive_duration=1440)
    # <-- 在這個位置插入以下代碼
    return thread
```
**插入這段「強制邀請」邏輯**：
```python
    # 自動邀請被標記的使用者與身分組成員進入討論串，確保他們不會視線受阻
    if thread:
        # 邀請明確被提到的人
        for mention in message.mentions:
            if self._client.user and mention != self._client.user:
                try:
                    await thread.add_user(mention)
                except Exception: pass
        
        # 展開被提到的身分組，把裡面的成員都拉進來
        if message.guild and message.role_mentions:
            for role in message.role_mentions:
                for member in role.members:
                    if self._client.user and member != self._client.user:
                        try:
                            await thread.add_user(member)
                        except Exception: pass
```

---
> 💡 **結語**：只要確保這 3 大核心邏輯存在於你的 `gateway/platforms/discord.py` 之中，你的多 Agent 協作就能安穩運行，不會再出現「裝死」、「無限迴圈搶話」或是「建了討論串卻拉不到人」的情況。
