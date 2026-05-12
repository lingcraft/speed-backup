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

一款专为 Android 设计的完整应用数据备份／恢复 Shell 脚本，支持 SSAID、运行时权限、OBB 数据包、WiFi 设置等完整备份，让你换机换系统后能无缝还原所有应用状态。

> 作者为台湾人，缺省发布繁体版本。CN 系统环境下脚本将自动翻译为简体中文。

**系统需求：** `Android 8+` · `arm64 架构` · `Root 权限（Magisk / KernelSU）`

本仓库为**简体中文修正版**，对原脚本中**部分专有名词**进行了**修正**，脚本执行逻辑无任何修改，具体使用哪个版本请自行决定，**原版**可前往这里下载：
> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。

简体中文版使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。

---

## ✨ 功能特色

| 功能 | 说明 |
|------|------|
| 📦 完整数据备份 | 换机换系统后原有数据完整保留，无需重新登录或下载额外数据包 |
| 🔑 SSAID 备份 | 支持 SSAID 备份，可完美备份 LINE 等依赖设备识别码的应用 |
| 🛡️ 权限备份 | 支持备份运行时权限（Runtime Permission）与 ops 权限 |
| 📂 Split APK | 支持备份与恢复 Split APK 格式 |
| 🎮 OBB 数据包 | 可选备份外部 OBB 数据（如原神、王者荣耀等大型游戏） |
| 📡 WiFi 备份 | 支持备份与恢复 WiFi 设置 |
| 📁 自定义文件夹备份 | 可备份 DCIM、Download、Music 等任意自定义目录 |
| 🗜️ 多种压缩算法 | 支持 `tar`（仅打包）与 `zstd`（高压缩率高速度） |
| ⚡ 高速压缩 | zstd 压缩速率快速，优于钛备份、Swift Backup |
| 🔒 完整性校验 | 内置 tools SHA-256 校验与压缩包完整性验证 |
| 🔄 增量备份 | 比对上次备份大小，无变化则跳过，节省时间 |
| 🖥️ 后台运行 | 支持后台运行模式，可完全关闭终端，log 持续刷新 |
| 💡 伪装亮屏 | 备份／恢复期间可伪装亮屏，避免 IO 因息屏降速 |
| 🌐 自动更新 | 联网侦测最新版本，支持 CDN 节点（适合中国大陆用户） |
| 🌏 多语言 | 自动识别系统语言环境，支持繁体中文／简体中文自动切换 |
| 👥 多用户支持 | 支持多用户环境（user 0、999 等），可手动或自动选择用户 |
| ⬛ 黑名单模式 | 黑名单应用可选「完全忽略」或「仅备份安装包」 |
| ⬜ 白名单支持 | 支持预装应用白名单与系统应用白名单，可指定备份范围 |
| 📱 进程侦测 | 可设置忽略正在运行中的应用，避免备份数据不一致 |
| ☁️ 远程备份 | 支持 WebDAV / FTP / SMB / SCP 四种协议，备份完成后自动上传到远程服务器 |

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
| 杀死运行中脚本 | 安全终止正在运行的备份脚本 |

### 恢复模式

| 选项 | 功能 |
|------|------|
| 重新生成应用列表 | 刷新恢复文件夹内的 `appList.txt` |
| 恢复备份 | 根据列表完整恢复应用与数据 |
| 仅恢复包含 SSAID 应用（含数据） | 只恢复有 SSAID 的应用及其完整数据 |
| 仅恢复包含 SSAID 应用（不含数据） | 只应用 SSAID，不覆盖现有数据 |
| 恢复自定义文件夹 | 恢复备份的自定义目录 |
| 恢复 WiFi | 恢复已备份的 WiFi 设置 |
| 压缩档完整性检查 | 验证备份压缩包是否完整无损 |
| 转换文档夹名称 | 将备份文件夹名称格式转换（用于跨版本兼容） |
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
│   ├── curl             # 远程传输工具 (WebDAV/FTP/SMB)
│   ├── scp / ssh        # SCP 远程传输
│   ├── jq               # JSON 处理
│   ├── bc               # 数学计算
│   ├── find             # 文档搜索
│   ├── keycheck         # 音量键监听
│   ├── cmd              # 系统指令桥接
│   ├── classes.dex      # Java 功能扩展（详见下方说明）
│   ├── soc.json         # 处理器数据库
│   ├── Device_List      # 设备型号数据库
│   └── tools.sh         # 内核脚本
│
├── backup_settings.conf  # 备份行为配置
└── start.sh              # 主运行脚本
```

> ⚠️ **重要：** 无论备份或恢复，都必须确保 `tools/` 目录完整存在，否则脚本将无法正常运作。

---

## ⚙️ 配置说明（backup_settings.conf）

| 设置项 | 说明 | 默认值 |
|--------|------|--------|
| `Lo` | 操作方式：`0` 音量键 / `1` 音量键（强制） / `2` 键盘输入 | `0` |
| `background_execution` | 后台运行：`1` 可关闭终端 / `0` 需保持终端打开 | `0` |
| `setDisplayPowerMode` | 备份期间伪装亮屏防止 IO 降速 | `0` |
| `Shell_LANG` | 语言：`0` 繁体中文 / `1` 简体中文（留空自动侦测） | 自动 |
| `Output_path` | 自定义备份输出路径，支持相对路径（留空使用当前目录） | 空 |
| `list_location` | 自定义 appList.txt 位置（留空使用当前目录） | 空 |
| `update` | 自动更新：`1` 打开 / `0` 关闭 | `1` |
| `cdn` | 更新 CDN 节点：`0` 直连 / `1` ghfast.top / `2` workers.dev | `1` |
| `mount_point` | 屏蔽外部挂载点（OTG、虚拟 SD 等），多个用 `\|` 分隔 | `rannki\|0000-1` |
| `user` | 指定用户 ID（留空自动选择） | 空 |
| `Backup_Mode` | 备份模式：`1` 应用+数据 / `0` 仅安装包 | `1` |
| `Backup_user_data` | 备份 user 数据：`1` 是 / `0` 否 | `1` |
| `Backup_obb_data` | 备份 OBB 外部数据：`1` 是 / `0` 否 | `1` |
| `backup_media` | 备份完成后一并备份自定义文件夹 | `0` |
| `Background_apps_ignore` | 忽略正在运行中的应用：`1` 忽略 / `0` 备份 | `0` |
| `Custom_path` | 自定义备份目录列表（绝对路径，每行一个） | DCIM / Download 等 |
| `blacklist_mode` | 黑名单模式：`1` 完全忽略 / `0` 仅备份安装包 | `0` |
| `blacklist` | 黑名单应用包名列表 | 空 |
| `whitelist` | 预装应用白名单包名列表 | 小米系列预装 |
| `system` | 系统应用白名单包名列表 | Google 系列 |
| `Compression_method` | 压缩算法：`zstd` 或 `tar` | `zstd` |
| `rgb_a` / `rgb_b` / `rgb_c` | 终端输出主色／辅色（256 色代码） | `226` / `123` / `177` |
| `remote_type` | 远程备份协议：`webdav` / `ftp` / `smb` / `scp`（留空不激活） | 空 |
| `remote_url` | 远程服务器地址（见下方格式说明） | 空 |
| `remote_user` | 远程认证用户名 | 空 |
| `remote_pass` | 远程认证密码 | 空 |

---

## 🚀 使用方式

> 推荐使用 [MT 管理器](https://www.coolapk.com/apk/bin.mt.plus) 运行脚本。若使用 Termux，请勿使用 `tsu`。

### 备份流程

**Step 1 — 生成应用列表**

解压脚本后运行 `start.sh`，选择「**生成应用列表**」。运行完毕后，当前目录会生成 `appList.txt`，内含所有已安装的第三方应用（预装应用缺省屏蔽，可于 `backup_settings.conf` 加入白名单）。

**Step 2 — 编辑应用列表**

打开 `appList.txt`，根据需求调整：
- 行首加 `#`：注释掉该应用，不备份
- 行首加 `!`：仅备份安装包，不备份数据

**Step 3 — 设置备份选项**

打开 `backup_settings.conf`，根据上方设置说明调整各选项后保存。

**Step 4 — 运行备份**

运行 `start.sh`，选择「**备份应用**」。备份完成后，当前目录会生成 `Backup_<压缩算法>_<用户ID>/` 文件夹，将此文件夹完整保存至安全位置。

---

### 恢复流程

**Step 1 — 编辑恢复列表**

进入备份文件夹，打开 `appList.txt`，删除或注释不需要恢复的应用行。

**Step 2 — 运行恢复**

运行备份文件夹内的 `start.sh`，选择「**恢复备份**」，等待脚本完成。

**Step 3 — 注意 SSAID**

若恢复结束后提示应用存在 SSAID，请**立刻重启**后再打开应用。若先打开应用，Android 会生成新的 SSAID，导致应用白屏或需要重新登录。

> 💡 备份文件夹内每个应用子目录都有独立的 `backup.sh` 与 `recover.sh`，可单独备份或恢复单一应用。

---

### 远程备份

备份完成后自动将备份文件上传到远程服务器，支持四种协议：

| 协议 | `remote_url` 格式 |
|------|-------------------|
| WebDAV | `http://192.168.1.100:8080/dav/backup/` |
| FTP | `ftp://192.168.1.100/backup/` |
| SMB | `smb://192.168.1.100/share/backup/` |
| SCP | `192.168.1.100:/home/user/backup/` |

**设置方式：** 编辑 `backup_settings.conf`：
```conf
remote_type=webdav
remote_url=http://192.168.1.100:8080/dav/backup/
remote_user=用户名
remote_pass=密码
```

**SCP 注意事项：** SCP 优先使用 `sshpass` 进行密码认证，若不支持则自动尝试 SSH 密钥认证。需确保远程已安装 SSH 服务器。

**上传范围：** 仅上传备份数据（应用文件、WiFi、appList.txt），排除 `tools/`、`start.sh`、`restore_settings.conf` 等脚本文档。

---

## 🔄 脚本更新方式

支持以下四种更新方式：

1. **ZIP 放置更新**：将下载的 `.zip` 不解压，直接放到脚本任意目录（`tools/` 除外），运行任何脚本即自动更新。
2. **联网自动更新**：脚本运行时自动连接 GitHub API 检查版本，发现新版本时提示下载（需设置 `update=1`）。
3. **Download 目录**：将 `.zip` 放置于 `/storage/emulated/0/Download/`，脚本自动侦测并更新。
4. **QQ 群下载**：从 QQ 群下载的脚本不解压，直接放置后运行即可自动更新。

> 🔒 脚本联网**仅用于检查更新**，无任何数据收集或非法操作。

---

## ❓ 常见问题

<details>
<summary><b>Q1：批量备份／恢复大量提示失败？</b></summary>

退出脚本，删除 `/data/backup_tools/` 目录后重新运行。若问题持续，请创建 [Issue](https://github.com/YAWAsau/backup_script/issues) 并附上截屏与 log。
</details>

<details>
<summary><b>Q2：微信／QQ 能完美备份恢复吗？</b></summary>

无法保证。建议同时使用其他你信赖的备份工具针对微信／QQ 额外备份，以防丢失重要数据。
</details>

<details>
<summary><b>Q3：为什么部分应用备份很久？</b></summary>

脚本会一同备份应用的 OBB 数据包，例如原神数据包超过 9GB，备份与恢复时间自然较长。可在 `backup_settings.conf` 设置 `Backup_obb_data=0` 跳过 OBB 备份。
</details>

<details>
<summary><b>Q4：脚本每次都是全量备份吗？</b></summary>

否。脚本会比对上次备份的文件大小，若无差异则跳过该应用，节省时间与空间。
</details>

<details>
<summary><b>Q5：为什么脚本内包含 .dex 文件？</b></summary>

`classes.dex` 用于实现 Shell 脚本难以达成的功能，包含：

- SSAID 备份与恢复
- 运行时权限（Runtime Permission）与 ops 权限备份恢复
- GitHub API 更新版本检查与下载
- 应用名称与包名查找
- 繁体中文 ↔ 简体中文自动翻译
- 后台运行模式的推送通知

感谢 [XayahSuSuSu](https://github.com/XayahSuSuSu) 的 [Android-DataBackup](https://github.com/XayahSuSuSu/Android-DataBackup) 提供 App 支持。
</details>

<details>
<summary><b>Q6：息屏后备份速度变慢？</b></summary>

这是 Android 内核的 IO 节能机制导致的。建议在 `backup_settings.conf` 设置 `setDisplayPowerMode=1` 打开伪装亮屏，或在备份期间保持屏幕常亮。
</details>

<details>
<summary><b>Q7：如何单独备份或恢复单一应用？</b></summary>

进入备份文件夹内对应的应用子目录，直接运行 `backup.sh`（单独备份）或 `recover.sh`（单独恢复）即可。
</details>

---

## 📬 问题反馈

遇到问题请携带截屏与 log 档，通过以下方式反馈：

- 🐛 [GitHub Issues](https://github.com/YAWAsau/backup_script/issues)
- 💬 [Telegram 频道](https://t.me/yawasau_script)
- 🐧 QQ 群：`976613477`
- 🧊 酷安：[@落叶凄凉TEL](http://www.coolapk.com/u/2277637)

---

## ☕ 支持作者

备份脚本耗费了大量时间与精力，如果你觉得好用，欢迎赞助支持！

[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg?style=flat-square&logo=paypal)](https://paypal.me/YAWAsau?country.x=TW&locale.x=zh_TW)

---

## 🙏 感谢贡献者

| 贡献者 | 贡献内容 |
|--------|----------|
| [kmou424](https://github.com/kmou424)（臭批老k） | 提供部分验证函数思路 |
| [雄氏老方](http://www.coolapk.com/u/665894)（屑老方） | 提供自动更新脚本方案 |
| 雨季骚年（胖子老陈） | 协助测试 |
| [XayahSuSuSu](https://github.com/XayahSuSuSu) | 提供 App 支持与 dex 功能支持 |

`文档编辑：Petit-Abba, YuKongA`

---

<p align="center">
  <sub>GPL-3.0 Licensed · Made with ❤️ by <a href="https://github.com/YAWAsau">YAWAsau</a></sub>
</p>