# Backup_script 数据备份脚本【简体中文版】

<p align="center">
  <a href="https://github.com/YAWAsau/backup_script/stargazers"><img src="https://img.shields.io/github/stars/YAWAsau/backup_script?label=stars&style=flat-square" /></a>
  <a href="https://github.com/YAWAsau/backup_script/releases"><img src="https://img.shields.io/github/downloads/YAWAsau/backup_script/total?style=flat-square" /></a>
  <a href="https://github.com/YAWAsau/backup_script/releases/latest"><img src="https://img.shields.io/github/v/release/YAWAsau/backup_script?label=release&style=flat-square" /></a>
  <a href="https://choosealicense.com/licenses/gpl-3.0"><img src="https://img.shields.io/github/license/YAWAsau/backup_script?label=License&style=flat-square" /></a>
  <a href="https://t.me/yawasau_script"><img src="https://img.shields.io/badge/Follow-Telegram-blue.svg?logo=telegram&style=flat-square" /></a>
</p>

---

## 📖 概述

一款专为 Android 设计的完整应用数据备份／恢复 Shell 脚本,支持 SSAID、运行时权限、OBB 数据包、WiFi 设置等完整备份,让你换机换系统后能无缝还原所有应用状态。

新版增加**完整的远程备份系统**,支持 WebDAV / SMB 上传到 NAS / 云端 / 区网电脑,并可从远程下载备份回手机直接恢复。支持**流式备份模式**,边压缩边传输,数据完全不占用本机空间。

> 作者为台湾人,缺省发布繁体版本。CN 系统环境下脚本将自动翻译为简体中文。

**系统需求:** `Android 8+` · `arm64 架构` · `Root 权限(Magisk / KernelSU)`

本仓库为**简体中文修正版**，对原脚本中**部分专有名词**进行了**修正**，脚本执行逻辑无任何修改，具体使用哪个版本请自行决定，**原版**可前往这里下载：
> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。

简体中文版使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。

---

## ✨ 功能特色

| 功能 | 说明 |
|------|------|
| 📦 完整数据备份 | 换机换系统后原有数据完整保留,无需重新登录或下载额外数据包 |
| 🔑 SSAID 备份 | 支持 SSAID 备份,可完美备份 LINE 等依赖设备识别码的应用 |
| 🛡️ 权限备份 | 支持备份运行时权限(Runtime Permission)与 ops 权限 |
| 📂 Split APK | 支持备份与恢复 Split APK 格式 |
| 🎮 OBB 数据包 | 可选备份外部 OBB 数据(如原神、王者荣耀等大型游戏) |
| 📡 WiFi 备份 | 支持备份与恢复 WiFi 设置 |
| 📁 自定义文件夹备份 | 可备份 DCIM、Download、Music 等任意自定义目录 |
| 🗜️ 多种压缩算法 | 支持 `tar`(仅打包)与 `zstd`(高压缩率高速度) |
| ⚡ 高速压缩 | zstd 压缩速率快速,优于钛备份、Swift Backup |
| 🔒 完整性校验 | 内置 tools SHA-256 校验与压缩包完整性验证 |
| 🔄 增量备份 | 多维度比对(版本/大小/权限/SSAID),无变化则跳过 |
| ✅ 最终计数核验 | 备份结束后逐档核对存在性,三态显示结果 |
| 🖥️ 后台运行 | 支持后台运行模式,可完全关闭终端,log 持续刷新 |
| 💡 伪装亮屏 | 备份/恢复期间可伪装亮屏,避免 IO 因息屏降速 |
| 🌐 自动更新 | 联网侦测最新版本,支持 CDN 节点(适合中国大陆用户) |
| 🌏 多语言 | 自动识别系统语言环境,支持繁体中文/简体中文自动切换 |
| 👥 多用户支持 | 支持多用户环境(user 0、999 等),可手动或自动选择用户 |
| ⬛ 黑名单模式 | 黑名单应用可选「完全忽略」或「仅备份安装包」 |
| ⬜ 白名单支持 | 支持预装应用白名单与系统应用白名单,可指定备份范围 |
| 📱 进程侦测 | 可设置忽略正在运行中的应用,避免备份数据不一致 |
| ☁️ 远程备份上传 | 支持 WebDAV / SMB 两种协议,备份完成自动上传,智能增量 |
| 🚀 流式备份 | 边压缩边传输,数据不落本机,节省本地空间 |
| 📥 远程下载恢复 | 可从远程直接下载备份回手机,点 start.sh 即可恢复 |
| 🔍 区网扫描 | 自动扫描区网内所有 SMB 主机,免去手动找 IP |
| 🧪 连接测试 | 三层测试(TCP / 认证 / 路径),设置不需备份就能验证 |

---

## 🗂️ 主菜单功能

### 备份模式

| 选项 | 功能 |
|------|------|
| 生成应用列表 | 扫描已安装的第三方应用并生成 `appList.txt` |
| 备份应用 | 根据列表与设置完整备份应用数据 |
| 备份已更新应用 | 仅备份自上次备份以来有版本更新的应用 |
| 备份自定义文件夹 | 备份 `backup_settings.conf` 内设置的自定义目录 |
| 备份 WiFi | 备份当前设备的 WiFi 设置 |
| 测试远程连接 | 验证 WebDAV / SMB 设置,三层测试(TCP / 认证 / 路径) |
| 单独上传当前备份 | 上传现有本地备份到远程,不重新跑备份流程 |
| 列出远程备份 | 连接远程、产生 `appList_network.txt` 让你勾选要下载哪些 app |
| 从远程下载备份 | 依清单下载备份到本地,可直接运行恢复 |
| 杀死运行中脚本 | 安全终止正在运行的备份脚本(整棵进程树) |

### 恢复模式

| 选项 | 功能 |
|------|------|
| 重新生成应用列表 | 刷新恢复文件夹内的 `appList.txt` |
| 恢复备份 | 根据列表完整恢复应用与数据 |
| 仅恢复包含 SSAID 应用(含数据) | 只恢复有 SSAID 的应用及其完整数据 |
| 仅恢复包含 SSAID 应用(不含数据) | 只应用 SSAID,不覆盖现有数据 |
| 恢复自定义文件夹 | 恢复备份的自定义目录 |
| 恢复 WiFi | 恢复已备份的 WiFi 设置 |
| 压缩档完整性检查 | 验证备份压缩包是否完整无损 |
| 转换文档夹名称 | 将备份文件夹名称格式转换(用于跨版本兼容) |
| 杀死运行中脚本 | 安全终止正在运行的恢复脚本 |

---

## 📁 目录结构

```
speed-backup.zip
│
├── tools/
│   ├── busybox          # 内核工具集
│   ├── zstd             # zstd 压缩工具
│   ├── tar              # tar 打包工具
│   ├── curl             # 远程传输工具 (WebDAV)
│   ├── smbclient        # SMB 远程传输
│   ├── jq               # JSON 处理
│   ├── find             # 文档搜索
│   ├── keycheck         # 音量键监听
│   ├── cmd              # 系统指令桥接
│   ├── classes.dex      # Java 功能扩展(详见下方说明)
│   ├── soc.json         # 处理器数据库
│   ├── Device_List      # 设备型号数据库
│   └── tools.sh         # 内核脚本
│
├── backup_settings.conf  # 备份行为配置
└── start.sh              # 主运行脚本
```

> ⚠️ **重要:** 无论备份或恢复,都必须确保 `tools/` 目录完整存在,否则脚本将无法正常运作。

备份完成后,每个 app 子目录会额外生成 `backup.sh` / `recover.sh` / `upload.sh`,可单独备份、恢复或上传单一应用。

---

## ⚙️ 配置说明(backup_settings.conf)

| 设置项 | 说明 | 默认值 |
|--------|------|--------|
| `Lo` | 操作方式:`0` 音量键 / `1` 音量键(强制) / `2` 键盘输入 | `0` |
| `background_execution` | 后台运行:`1` 可关闭终端 / `0` 需保持终端打开 | `0` |
| `setDisplayPowerMode` | 备份期间伪装亮屏防止 IO 降速 | `0` |
| `Shell_LANG` | 语言:`0` 繁体中文 / `1` 简体中文(留空自动侦测) | 自动 |
| `Output_path` | 自定义备份输出路径(留空使用当前目录) | 空 |
| `list_location` | 自定义 appList.txt 位置(留空使用当前目录) | 空 |
| `update` | 自动更新:`1` 打开 / `0` 关闭 | `1` |
| `cdn` | 更新 CDN 节点:`0` 直连 / `1` ghfast.top / `2` workers.dev | `1` |
| `mount_point` | 屏蔽外部挂载点,多个用 `\|` 分隔 | `rannki\|0000-1` |
| `user` | 指定用户 ID(留空自动选择) | 空 |
| `Backup_Mode` | 备份模式:`1` 应用+数据 / `0` 仅安装包 | `1` |
| `Backup_user_data` | 备份 user 数据:`1` 是 / `0` 否 | `1` |
| `Backup_obb_data` | 备份 OBB 外部数据:`1` 是 / `0` 否 | `1` |
| `backup_media` | 备份完成后一并备份自定义文件夹 | `0` |
| `Background_apps_ignore` | 忽略正在运行中的应用:`1` 忽略 / `0` 备份 | `0` |
| `Custom_path` | 自定义备份目录列表(绝对路径,每行一个) | DCIM / Download 等 |
| `blacklist_mode` | 黑名单模式:`1` 完全忽略 / `0` 仅备份安装包 | `0` |
| `blacklist` | 黑名单应用包名列表 | 空 |
| `whitelist` | 预装应用白名单包名列表 | 小米系列预装 |
| `system` | 系统应用白名单包名列表 | Google 系列 |
| `Compression_method` | 压缩算法:`zstd` 或 `tar` | `zstd` |
| `rgb_a` / `rgb_b` / `rgb_c` | 终端输出主色/辅色1/辅色2(256 色代码) | `220` / `51` / `213` |
| `remote_type` | 远程备份协议:`webdav` / `smb`(留空不激活) | 空 |
| `smb_url` | SMB 服务器地址 | 空 |
| `smb_remote_user` | SMB 认证用户名 | 空 |
| `smb_remote_pass` | SMB 认证密码 | 空 |
| `webdav_url` | WebDAV 服务器地址 | 空 |
| `webdav_remote_user` | WebDAV 认证用户名 | 空 |
| `webdav_remote_pass` | WebDAV 认证密码 | 空 |
| `remote_keep_local` | 上传成功后本地文件:`1` 保留 / `0` 删除 | `0` |
| `remote_stream` | 流式备份:`1` 打开(边压边传,不占本机) / `0` 关闭 | `0` |

---

## 🚀 使用方式

> 推荐使用 [MT 管理器](https://www.coolapk.com/apk/bin.mt.plus) 运行脚本。若使用 Termux,请勿使用 `tsu`。

### 备份流程

**Step 1 — 生成应用列表**

解压脚本后运行 `start.sh`,选择「**生成应用列表**」。运行完毕后,当前目录会生成 `appList.txt`。

**Step 2 — 编辑应用列表**

打开 `appList.txt`,根据需求调整:
- 行首加 `#`:注释掉该应用,不备份
- 行首加 `!`:仅备份安装包,不备份数据

**Step 3 — 设置备份选项**

打开 `backup_settings.conf`,根据上方设置说明调整各选项后保存。

**Step 4 — 运行备份**

运行 `start.sh`,选择「**备份应用**」。备份完成后生成 `Backup_<压缩算法>_<用户ID>/` 文件夹。

---

### 恢复流程

**Step 1 — 编辑恢复列表**

进入备份文件夹,打开 `appList.txt`,删除或注释不需要恢复的应用行。

**Step 2 — 运行恢复**

运行备份文件夹内的 `start.sh`,选择「**恢复备份**」,等待脚本完成。

**Step 3 — 注意 SSAID**

若恢复结束后提示应用存在 SSAID,请**立刻重启**后再打开应用。若先打开应用,Android 会生成新的 SSAID,导致应用白屏或需要重新登录。

> 💡 备份文件夹内每个应用子目录都有独立的 `backup.sh`、`recover.sh`、`upload.sh`,可单独操作单一应用。

---

## ☁️ 远程备份

### 设置方式

编辑 `backup_settings.conf`,SMB 与 WebDAV 地址分开设置,切换协议免重输:

```conf
remote_type=smb

smb_url=smb://192.168.1.100/Backup
smb_remote_user=用户名
smb_remote_pass=密码

webdav_url=http://192.168.1.100:8080/dav/
webdav_remote_user=用户名
webdav_remote_pass=密码

remote_keep_local=0
remote_stream=0
```

| 协议 | 地址格式 | 适用场景 |
|------|----------|---------|
| SMB | `smb://192.168.1.100/share/` | Windows 共享 / Samba / NAS |
| WebDAV | `http://192.168.1.100:8080/dav/` | NAS / Nextcloud / rclone serve |

### 远程目录结构

脚本在 `remote_url` 下自动创建 `Backup_<压缩算法>_<用户ID>/`,与本地结构完全镜像:

```
smb://NAS/Backup/
    Backup_zstd_0/
        1DM+/
        LINE/
        Keep记事/
        wifi/wifi.json
        tools/
        start.sh
        restore_settings.conf
        appList.txt
        MT管理器.apk
```

不同用户(0、999)自动分开到 `Backup_zstd_0/`、`Backup_zstd_999/`,互不冲突。

### 特性

- **智能增量** — 多维度比对(版本/大小/权限/SSAID),只上传本次有变更的 app
- **远程预扫** — 单次连接取全部列表 + 批量下载 json,主循环零网络开销
- **流式备份** — `remote_stream=1` 边压缩边传输,数据完全不占本机空间
- **最终核验** — 备份结束后逐档核对存在性,缺失文件列出清单
- **连接预检** — 没网络时 3 秒内判断并禁用上传,不卡死脚本
- **失败保护** — 流式上传失败不更新远程 json,确保下轮整体重备

---

### 流式备份模式

`remote_stream=1` 激活流式备份,数据直接 `tar | zstd | 传输`,本机不产生任何备份文件:

```conf
remote_type=smb
smb_url=smb://192.168.1.100/Backup
smb_remote_user=用户名
smb_remote_pass=密码
remote_stream=1
```

> ⚠️ 流式模式为全量上传(无本机校验),建议搭配稳定的区网环境使用。

---

### 从远程下载备份

**Step 1** — 主菜单选「**列出远程备份**」,产生 `appList_network.txt`

**Step 2** — 打开 `appList_network.txt`,用 `#` 注解掉不要下载的 app

**Step 3** — 主菜单选「**从远程下载备份**」,下载完成后直接运行内附 `start.sh` 恢复

---

### 连接测试

设置完 `backup_settings.conf` 后,主菜单选「**测试远程连接**」:

```
—————— TCP 连接测试 ——————
目标: 192.168.1.100:445
TCP 连接通过
—————— 认证与列目录测试 ——————
SMB 认证通过, share 可访问
全部测试通过, 可以开始备份
```

---

## 🔄 脚本更新方式

1. **ZIP 放置更新**:将下载的 `.zip` 不解压,直接放到脚本任意目录(`tools/` 除外),运行任何脚本即自动更新
2. **联网自动更新**:脚本运行时自动连接 GitHub API 检查版本(需设置 `update=1`)
3. **Download 目录**:将 `.zip` 放置于 `/storage/emulated/0/Download/`,脚本自动侦测并更新
4. **QQ 群下载**:从 QQ 群下载的脚本不解压,直接放置后运行即可自动更新

> 🔒 脚本联网**仅用于检查更新**,无任何数据收集或非法操作。

---

## ❓ 常见问题

<details>
<summary><b>Q1:批量备份/恢复大量提示失败?</b></summary>

退出脚本,删除 `/data/backup_tools/` 目录后重新运行。若问题持续,请创建 [Issue](https://github.com/YAWAsau/backup_script/issues) 并附上截屏与 log。
</details>

<details>
<summary><b>Q2:微信/QQ 能完美备份恢复吗?</b></summary>

无法保证。建议同时使用其他你信赖的备份工具针对微信/QQ 额外备份,以防丢失重要数据。
</details>

<details>
<summary><b>Q3:为什么部分应用备份很久?</b></summary>

脚本会一同备份应用的 OBB 数据包,例如原神数据包超过 9GB。可在 `backup_settings.conf` 设置 `Backup_obb_data=0` 跳过 OBB 备份。
</details>

<details>
<summary><b>Q4:脚本每次都是全量备份吗?</b></summary>

否。脚本多维度比对上次备份(版本号/数据大小/权限/SSAID),无差异则跳过,节省时间与空间。
</details>

<details>
<summary><b>Q5:为什么脚本内包含 .dex 文件?</b></summary>

`classes.dex` 用于实现 Shell 脚本难以达成的功能:

- SSAID 备份与恢复
- 运行时权限(Runtime Permission)与 ops 权限批量备份恢复
- GitHub API 更新版本检查与下载
- 应用名称与包名查找
- 繁体中文 ↔ 简体中文自动翻译
- 后台运行模式的推送通知

感谢 [XayahSuSuSu](https://github.com/XayahSuSuSu) 的 [Android-DataBackup](https://github.com/XayahSuSuSu/Android-DataBackup) 提供 App 支持。
</details>

<details>
<summary><b>Q6:息屏后备份速度变慢?</b></summary>

这是 Android 内核的 IO 节能机制。建议在 `backup_settings.conf` 设置 `setDisplayPowerMode=1` 打开伪装亮屏,或备份期间保持屏幕常亮。
</details>

<details>
<summary><b>Q7:如何单独备份/恢复/上传单一应用?</b></summary>

进入备份文件夹内对应的应用子目录,直接运行:
- `backup.sh` — 单独备份该 app
- `recover.sh` — 单独恢复该 app
- `upload.sh` — 单独上传该 app 到远程
</details>

<details>
<summary><b>Q8:WebDAV 上传显示 HTTP 423 Locked?</b></summary>

某些云端网盘的 WebDAV 对大档有大小限制。建议改用:
- 自家 NAS / Windows SMB
- rclone serve webdav
- 群晖 / Nextcloud
</details>

<details>
<summary><b>Q9:WebDAV 上传显示 HTTP 404?</b></summary>

请检查:
- `webdav_url` 路径是否含正确的 webdav 端点(例如 `/dav/` 或 `/remote.php/webdav/`)
- 帐号是否有写入权限
</details>

<details>
<summary><b>Q10:SMB 提示「找不到 share」?</b></summary>

- Windows 端确认 SMB 共享已打开,且网络设成「私人」而非「公用」
- 防火墙放行 445 port
- 主菜单启动时的 `scan_smb` 会自动列出区网 SMB 主机与 share 名,可对照确认
</details>

<details>
<summary><b>Q11:没网络会影响备份吗?</b></summary>

不会。脚本启动时做 TCP 预检(3 秒内判断),没网络时自动禁用远程上传但**完整保留本地备份**,流程继续跑完。
</details>

<details>
<summary><b>Q12:流式备份和一般备份有什么差别?</b></summary>

| | 一般备份 | 流式备份 |
|---|---|---|
| 本机空间占用 | 先压缩到本机再上传 | 不占用(直接传输) |
| 增量比对 | ✅ 支持 | ✅ 支持 |
| 本机完整性校验 | ✅ 支持 | ❌ 不支持(信任传输) |
| 适合场景 | 本机空间充足 | 本机空间有限 |
</details>

---

## 📬 问题反馈

遇到问题请携带截屏与 log 档,通过以下方式反馈:

- 🐛 [GitHub Issues](https://github.com/YAWAsau/backup_script/issues)
- 💬 [Telegram 频道](https://t.me/yawasau_script)
- 🐧 QQ 群:`976613477`
- 🧊 酷安:[@落叶凄凉TEL](http://www.coolapk.com/u/2277637)

---

## ☕ 支持作者

备份脚本耗费了大量时间与精力,如果你觉得好用,欢迎赞助支持!

[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg?style=flat-square&logo=paypal)](https://paypal.me/YAWAsau?country.x=TW&locale.x=zh_TW)

---

## 🙏 感谢贡献者

| 贡献者 | 贡献内容 |
|--------|----------|
| [kmou424](https://github.com/kmou424)(臭批老k) | 提供部分验证函数思路 |
| [雄氏老方](http://www.coolapk.com/u/665894)(屑老方) | 提供自动更新脚本方案 |
| [sakuradairong](https://github.com/sakuradairong)(雨季骚年/胖子老陈) | 添加 WebDAV / SMB 功能与测试 |
| [XayahSuSuSu](https://github.com/XayahSuSuSu) | 提供 App 支持与 dex 功能支持 |

`文档编辑:Petit-Abba, YuKongA`

---

<p align="center">
  <sub>GPL-3.0 Licensed · Made with ❤️ by <a href="https://github.com/YAWAsau">YAWAsau</a></sub>
</p>