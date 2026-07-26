# Backup_script 数据备份脚本【简体中文版】

<p align="center">
 <a href="https://deepwiki.com/YAWAsau/backup_script"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki" /></a>
 <a href="https://github.com/YAWAsau/backup_script/stargazers"><img src="https://img.shields.io/github/stars/YAWAsau/backup_script?label=stars&style=flat-square" /></a>
 <a href="https://github.com/YAWAsau/backup_script/releases"><img src="https://img.shields.io/github/downloads/YAWAsau/backup_script/total?style=flat-square" /></a>
 <a href="https://github.com/YAWAsau/backup_script/releases/latest"><img src="https://img.shields.io/github/v/release/YAWAsau/backup_script?label=release&style=flat-square" /></a>
 <a href="https://choosealicense.com/licenses/gpl-3.0"><img src="https://img.shields.io/github/license/YAWAsau/backup_script?label=License&style=flat-square" /></a>
 <a href="https://t.me/yawasau_script"><img src="https://img.shields.io/badge/Follow-Telegram-blue.svg?logo=telegram&style=flat-square" /></a>
</p>

---

## 概述

Backup_script 是一款专为 Android 设计的完整应用数据备份／恢复 Shell 脚本，支持应用数据、Split APK、SSAID、运行时权限、AppOps、特殊访问、电池策略、安装来源、OBB 数据包、Wi-Fi 设置与自定义文件夹备份。适合换机、刷机、重装系统后快速还原应用状态。

脚本提供本地备份与远程备份两种模式。远程备份支持 WebDAV / SMB，可上传到 NAS、区网电脑、rclone serve webdav、Nextcloud 等服务，也可从远程下载备份回手机后直接恢复。

新版支持流式备份：数据可直接 `tar | zstd | 传输`，不需要先落地成本机压缩包，适合本机空间不足的设备。对于没有变化的应用，脚本会通过版本、数据大小、AppState、SSAID 与远程文件状态进行 fast-skip，避免重复压缩与重复上传。

> 作者为台湾人，预设发布繁体版本。简体中文环境下脚本可自动切换语言。

**系统需求：** `Android 8+` · `arm64 架构` · `Root 权限(Magisk / KernelSU)`

本仓库为**简体中文修正版**，对原脚本中**部分专有名词**进行了**修正**，脚本执行逻辑无任何修改，具体使用哪个版本请自行决定，**原版**可前往这里下载：
> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。

简体中文版使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。

---

## 功能特色

| 功能 | 说明 |
|------|------|
| 完整数据备份 | 备份应用数据、APK、Split APK、user / user_de / data / OBB 等数据 |
| 完整恢复 | 支持批量恢复与单 App 恢复，恢复后自动校验 AppState |
| Play 商店来源还原 | 支持恢复 installer / install source，使应用在系统中正确显示来源 |
| SSAID 备份与恢复 | 支持备份与恢复 Android SSAID，适合 LINE 等依赖设备识别码的应用 |
| 权限与 AppOps | 支持运行时权限、AppOps、特殊访问、电池策略等状态备份与恢复 |
| 旧 JSON 兼容 | 旧版 `app_details.json` 会自动转换为新版 AppState restore record，不需手动转档 |
| Split APK | 支持多 split APK 备份与恢复 |
| OBB 数据包 | 可选备份外部 OBB 数据，如大型游戏数据报 |
| Wi-Fi 备份 | 支持 Wi-Fi 设置备份与恢复 |
| 自定义文件夹 | 可备份与恢复 DCIM、Download、Music 等任意自定义目录 |
| 压缩方式 | 支持 `zstd` 压缩与 `tar` 仅打包 |
| 增量备份 | 多维度比对版本、数据大小、权限、SSAID、AppState，无变化则跳过 |
| 全量 fast-skip | 本地 / WebDAV / SMB 全部无变化时可整批折叠跳过，不进逐 App 主流程 |
| 远程备份 | 支持 WebDAV / SMB 备份、下载、恢复、列表与健康检查 |
| 流式备份 | 边压缩边传输，数据不落本机，节省本地空间 |
| 远程预扫 | 远程备份前批量取得远程列表与 JSON，降低主循环网络开销 |
| 远程 JSON 健康检查 | 远程 `app_details.json` 缺失或损坏会列出清单，不静默忽略 |
| SMB 扫描 | 自动扫描区网 SMB 主机与 share，免手动找 IP |
| WebDAV 兼容 | 支持逐层建目录、PUT/MOVE/STAT/GET 校验、404 非致命判断等 WebDAV 兼容处理 |
| 日志与 debug 包 | 自动生成 speed_debug 诊断包，legacy `log/log_yyyy-mm-dd_hh-mm.txt` 会同步主日志摘要 |
| 后台运行 | 支持后台运行模式，log 持续刷新 |
| 状态通知 | 支持备份 / 恢复进度与结果通知 |
| 多用户支持 | 支持 user 0、999 等多用户环境，可指定或自动选择用户 |
| 配置自动修补 | 升级后自动补齐 `backup_settings.conf` 缺少项目，不需手动重写 |
| 自动更新 | 支持本地 ZIP 更新、Download / QQ 下载目录检测与 GitHub release 检查 |
| 完整性校验 | 内置工具 SHA-256 校验、压缩包完整性检查与最终文件核验 |
| 启动自我检测 | `dex_check.sh` 检测目前 Dex 能力与 tools.sh 使用的 Dex route |

---

## 主菜单功能

### 备份模式

| 选项 | 功能 |
|------|------|
| 生成应用列表 | 扫描可备份应用并生成 `appList.txt` |
| 备份应用 | 根据列表与设置完整备份应用与数据 |
| 备份已更新应用 | 仅备份自上次备份后版本有变化的应用 |
| 备份自定义文件夹 | 备份 `backup_settings.conf` 中设置的自定义目录 |
| 备份 Wi-Fi | 备份目前设备的 Wi-Fi 设置 |
| 测试远程连接 | 验证 WebDAV / SMB 设置与写入能力 |
| 单独上传当前备份 | 将现有本地备份同步到远程，不重新运行备份 |
| 列出远程备份 | 连接远程并产生 `appList_network.txt` |
| 从远程下载备份 | 依清单下载远程备份到本地，可直接恢复 |
| 杀死运行中脚本 | 安全终止正在运行的备份脚本进程树 |

### 恢复模式

| 选项 | 功能 |
|------|------|
| 重新生成应用列表 | 刷新恢复文件夹内的 `appList.txt` |
| 恢复备份 | 根据列表完整恢复应用、数据与 AppState |
| 仅恢复包含 SSAID 应用(含数据) | 只恢复有 SSAID 的应用与完整数据 |
| 仅恢复包含 SSAID 应用(不含数据) | 只应用 SSAID，不覆盖现有数据 |
| 恢复自定义文件夹 | 恢复备份的自定义目录 |
| 恢复 Wi-Fi | 恢复已备份的 Wi-Fi 设置 |
| 压缩档完整性检查 | 验证备份压缩包是否完整无损 |
| 转换文档夹名称 | 将备份文件夹名称格式转换，用于跨版本兼容 |
| 杀死运行中脚本 | 安全终止正在运行的恢复脚本进程树 |

---

## 目录结构

```text
speed-backup.zip
│
├── tools/
│   ├── busybox        # 内核工具集
│   ├── zstd           # zstd 压缩工具
│   ├── tar            # tar 打包工具
│   ├── smbclient      # SMB 远程传输
│   ├── jq             # JSON 处理
│   ├── find           # 文件搜索
│   ├── keycheck       # 音量键监听
│   ├── cmd            # 系统指令桥接
│   ├── uidexec        # 指定 UID 运行辅助工具
│   ├── unixsock       # AF_UNIX socket 辅助工具
│   ├── filewatch      # 文件状态辅助工具
│   ├── procwait       # 进程等待辅助工具
│   ├── classes.dex    # Java / Dex 功能扩展
│   ├── soc.json       # 处理器数据库
│   ├── Device_List    # 设备型号数据库
│   └── tools.sh       # 内核脚本
│
├── backup_settings.conf # 备份行为配置
├── dex_check.sh         # Dex 能力与 route 自检
└── start.sh             # 主运行入口
```

> **重要：** 无论备份或恢复，都必须确保 `tools/` 目录完整存在，否则脚本可能无法正常运作。

备份完成后，每个 App 子目录会生成 `backup.sh` / `recover.sh` / `upload.sh`，可单独备份、恢复或上传单一应用。

---

## 配置说明(`backup_settings.conf`)

| 设置项 | 说明 | 常用值 / 预设 |
|--------|------|---------------|
| `low_battery_mode` | 低电量行为：`1` 强制拒绝、`2` 不提示继续、留空音量键选择 | 留空 |
| `keyboard_input` | `1` 改用键盘输入确认，留空使用音量键 | 留空 |
| `background_execution` | 后台运行：`1` 可关闭终端、`0` 保持终端显示 | `0` |
| `notification_enable` | 状态栏通知与进度条：`1` 打开、`0` 关闭 | `1` |
| `Shell_LANG` | 语言：`0` 繁体中文、`1` 简体中文、留空自动侦测 | 留空 / `0` |
| `setDisplayPowerMode` | 备份 / 恢复期间伪装亮屏，避免 IO 因息屏降速 | `0` |
| `Output_path` | 自定义备份输出位置，支持相对路径 | 空 |
| `Backup_suffix` | 自定义备份目录后缀，支持日期时间变量 | 空 |
| `list_location` | 自定义 `appList.txt` 位置 | 空 |
| `update` | 自动更新：`1` 打开、`0` 关闭 | `1` |
| `cdn` | 更新 CDN 节点：`0` 直连、`1` ghfast、`2` workers | `0` |
| `mount_point` | 屏蔽外部挂载点，多个用 `|` 分隔 | 自订 |
| `user` | 指定 Android 用户 ID，例如 `0`、`999`；留空时自动判断或询问 | 空 |
| `Backup_Mode` | `1` 应用 + 数据、`0` 仅安装包 | `1` |
| `Backup_user_data` | 是否备份 `/data/user/<user>/<package>` | `1` |
| `Backup_obb_data` | 是否备份 OBB / data 外部数据 | `1` |
| `backup_media` | App 备份后是否一并备份自定义文件夹 | `0` |
| `Background_apps_ignore` | 正在运行中的应用：`1` 忽略、`0` 尝试停止后备份 | `0` |
| `Custom_path` | 自定义备份路径，每行一个绝对路径 | 依需求 |
| `blacklist_mode` | 黑名单：`1` 完全忽略、`0` 仅备份安装包 | `0` |
| `blacklist` | 黑名单应用包名列表 | 空 |
| `whitelist` | 预装应用白名单 | 依需求 |
| `system` | 系统应用白名单 | 依需求 |
| `Compression_method` | 压缩方式：`zstd` 或 `tar`；`tar` 仅打包不压缩 | `zstd` |
| `rgb_a` / `rgb_b` / `rgb_c` | 终端输出主色与辅色，使用 256 色 ANSI 编号 | `220` / `51` / `213` |
| `remote_type` | 远程备份类型：`webdav`、`smb`，留空不激活 | 空 |
| `smb_url` | SMB 服务器地址，例如 `smb://192.168.1.100/Backup` | 空 |
| `smb_remote_user` | SMB 认证用户名 | 空 |
| `smb_remote_pass` | SMB 认证密码 | 空 |
| `webdav_url` | WebDAV 地址，例如 `http://192.168.1.100:8080/dav/` | 空 |
| `webdav_remote_user` | WebDAV 认证用户名 | 空 |
| `webdav_remote_pass` | WebDAV 认证密码 | 空 |
| `remote_stream` | 流式备份：`1` 边压边传、`0` 先本地备份再上传 | `0` |
| `diagnostic_mode` | 诊断模式：`1` 保留更多排查数据、`0` 一般使用 | `0` |
| `remote_keep_local` | 远程备份完成后是否保留本地文件 | `1` / 依需求 |
| `remote_upload_per_app` | 每个 App 备份后立即上传，非流式模式下节省空间 | `0` |
| `log_max_size_mb` | `log/` 目录大小上限，留空或 `0` 关闭自动清理 | `1` |

---

## 使用方式

> 推荐使用 MT 管理器或其他可授权 Root 的终端环境运行 `start.sh`。若使用 Termux，请直接授权 Root，不建议使用 `tsu` 包一层运行。

### 备份流程

**Step 1 — 生成应用列表**

解压后运行 `start.sh`，选择「生成应用列表」。运行完毕后，当前目录会生成 `appList.txt`。

**Step 2 — 编辑应用列表**

打开 `appList.txt`，依需求调整：

- 行首加 `#`：注释该应用，不备份
- 行首加 `!`：仅备份安装包，不备份数据

**Step 3 — 调整配置**

编辑 `backup_settings.conf`，设置用户、备份项目、远程地址、流式备份与自定义路径。

**Step 4 — 运行备份**

运行 `start.sh`，选择「备份应用」。备份完成后会生成 `Backup_<压缩方式>_<用户ID>/` 目录，例如 `Backup_zstd_0/`。

---

### 恢复流程

**Step 1 — 编辑恢复列表**

进入备份文件夹，打开 `appList.txt`，删除或注释不需要恢复的应用。

**Step 2 — 运行恢复**

运行备份文件夹内的 `start.sh`，选择「恢复备份」。脚本会依列表恢复 APK、数据、SSAID、权限、AppOps、特殊访问、电池策略与安装来源。

**Step 3 — 依提示重启**

若恢复结束后提示存在 SSAID，建议立刻重启后再打开应用。若先打开应用，Android 可能生成新的 SSAID，导致部分应用需要重新登录或状态异常。

> 备份文件夹内每个应用子目录都有 `backup.sh`、`recover.sh`、`upload.sh`，可单独操作单一应用。

---

## 远程备份

### 设置方式

SMB 与 WebDAV 地址分开设置，切换 `remote_type` 时不需要重复输入另一种协议的地址：

```conf
remote_type=webdav

smb_url=smb://192.168.1.100/Backup
smb_remote_user=用户名
smb_remote_pass=密码

webdav_url=http://192.168.1.100:8080/dav/
webdav_remote_user=用户名
webdav_remote_pass=密码

remote_stream=1
remote_keep_local=1
```

| 协议 | 地址格式 | 适用场景 |
|------|----------|---------|
| SMB | `smb://192.168.1.100/share/path` | Windows 共享 / Samba / NAS |
| WebDAV | `http://192.168.1.100:8080/dav/` | NAS / Nextcloud / rclone serve webdav |

### 远程目录结构

脚本会在远程地址下创建 `Backup_<压缩方式>_<用户ID>/`，与本地结构保持一致：

```text
Backup_zstd_0/
├── LINE/
│   ├── apk.tar.zst
│   ├── user.tar.zst
│   ├── user_de.tar.zst
│   ├── app_details.json
│   ├── backup.sh
│   ├── recover.sh
│   └── upload.sh
├── wifi/
│   └── wifi.json
├── tools/
├── start.sh
├── restore_settings.conf
└── appList.txt
```

不同 Android 用户会分开到不同目录，例如 `Backup_zstd_0/`、`Backup_zstd_999/`。

### 远程备份特性

- **流式备份**：`remote_stream=1` 时，数据直接压缩并传输到远程，本地不落压缩包。
- **远程 fast-skip**：若远程数据、版本、AppState 与文件状态都未变化，会整批跳过。
- **远程 JSON 健康检查**：缺失、损坏或格式不合法的 `app_details.json` 会列出清单。
- **失败保护**：流式上传失败时不更新远程 JSON，避免下轮误判已备份完成。
- **WebDAV 目录创建**：会逐层创建远程目录并 verify，降低不同 WebDAV server 的兼容问题。
- **SMB 写入预检**：正式备份前会测试远程目录创建与写入能力。

---

## 流式备份模式

`remote_stream=1` 激活后，数据直接走：

```text
tar → zstd → WebDAV / SMB
```

优点：

- 不占用本机压缩包空间
- 适合本机剩余空间不足的设备
- 支持 WebDAV / SMB
- 支持远程 fast-skip 与最终文件核验

限制：

- 传输过程依赖网络稳定性
- 本地不保留压缩包时，无法做本地 tar/zstd 完整性校验
- 若远程上传失败，该 App 会保留失败状态，下轮重新备份

---

## 从远程下载备份

**Step 1 — 列出远程备份**

主菜单选「列出远程备份」，产生 `appList_network.txt`。

**Step 2 — 编辑下载列表**

打开 `appList_network.txt`，用 `#` 注解掉不需要下载的应用。

**Step 3 — 从远程下载备份**

主菜单选「从远程下载备份」。下载完成后，直接运行下载文件夹中的 `start.sh` 进行恢复。

---

## 旧版 JSON 兼容

新版恢复流程支持旧版 `app_details.json`。若旧 JSON 没有新版 `app_state` 字段，但仍保留：

```text
permissions
battery_settings
Ssaid
installer / install_diagnostics
apk_version
PackageName
user / user_de / data Size
```

脚本会在恢复时自动转换为新版 AppState restore record，等效于：

```text
sourceFormat=legacy-app-details-migrated
recordType=snapshot
schemaVersion=2
```

也就是旧备份不需要手动转档。旧 JSON 已有的 SSAID、权限、AppOps、电池策略与安装来源会尽量恢复；旧 JSON 本来没有的新字段则无法凭空补出。

---

## AppState / Dex 功能

`classes.dex` 用于实现 Shell 难以稳定完成的系统操作。目前主要负责：

- AppState snapshot / restore / verify
- SSAID 备份与恢复辅助
- 运行时权限、AppOps、特殊访问、电池策略状态处理
- 安装来源、installer、Play 来源恢复辅助
- App 名称、包名、版本、split 信息查找
- WebDAV rel API、AF_UNIX daemon 与传输辅助
- SMB 主机与 share 扫描辅助
- 通知批量更新
- 权限 / AppOps / 特殊访问中文语意输出

启动自检由 `dex_check.sh` 运行，只检查目前 Dex 版本实际具备的能力与 `tools.sh` 当前使用的 Dex route。

---

## 脚本更新方式

1. **本地 ZIP 更新**：将完整 release `.zip` 不解压，放到脚本目录或其上层目录，运行脚本时自动检测更新。
2. **Download 目录更新**：将完整 release `.zip` 放到 `/storage/emulated/0/Download/`，运行脚本时自动检测。
3. **QQ 下载目录更新**：从 QQ 下载的完整 release `.zip` 可直接放置后运行脚本更新。
4. **联网自动更新**：`update=1` 时会检查 GitHub release。

更新规则：

- 本地完整 release 同版本允许覆盖更新，成功后删除更新 ZIP。
- 低于目前版本的 ZIP 会拒绝更新。
- 在线 release 与本地版本相同时不提示新版。
- 更新只同步 release 内工具与入口档，不会删除既有备份数据。
- 更新失败、拒绝或中止时会清理 `/data/local/tmp` 更新暂存。

> 脚本联网仅用于检查更新，不会收集或上传用户数据。

---

## 日志与 debug

一般使用时，脚本会在 `log/` 目录生成 legacy log，例如：

```text
log/log_2026-07-25_21-40.txt
```

同时，完整诊断数据会打包到 speed_debug：

```text
/data/speed_debug/speed_debug_yyyyMMdd-HHmmss.tar
```

排查问题时，请优先提供 speed_debug tar。里面通常包含：

- `main.log`：主流程日志
- `stderr.log`：Shell stderr，0KB 通常代表没有错误
- `root_daemon_stderr.log`：Root daemon stderr，0KB 通常代表没有错误
- `webdav_daemon_stderr.log`：WebDAV daemon stderr，0KB 通常代表没有错误
- `app_state_output.log`：AppState restore 输出
- `verify_app_state_output.log`：AppState verify 输出
- `stream_upload.log` / `stream_download.log`：流式上传 / 下载日志
- `extract.log`：恢复解压日志

---

## 常见问题

<details>
<summary><b>Q1：批量备份 / 恢复大量提示失败？</b></summary>

请先查看 `/data/speed_debug/` 内最新 debug 包。若是工具残留或权限异常，可尝试删除 `/data/backup_tools/` 后重新运行。若仍失败，请提交 speed_debug tar。
</details>

<details>
<summary><b>Q2：微信 / QQ 能完美备份恢复吗？</b></summary>

无法保证。大型实时通信 App 可能有服务常驻、数据库锁、服务器校验或加密状态。建议同时使用你信任的官方或第三方方式额外备份重要数据。
</details>

<details>
<summary><b>Q3：为什么部分应用备份很久？</b></summary>

可能是 user data、user_de、OBB 或外部 data 很大。可在 `backup_settings.conf` 将 `Backup_obb_data=0` 跳过外部 OBB / data 类大型数据。
</details>

<details>
<summary><b>Q4：脚本每次都是全量备份吗？</b></summary>

不是。脚本会比对版本号、数据大小、SSAID、权限、AppOps、AppState 与远程文件状态。无变化时会跳过；若全部选中 App 都无变化，本地与远程都可整批 fast-skip。
</details>

<details>
<summary><b>Q5：为什么脚本包含 classes.dex？</b></summary>

`classes.dex` 用于处理 Shell 难以稳定完成的 Android 系统能力，例如 AppState snapshot / restore / verify、SSAID、AppOps、WebDAV daemon、SMB 扫描、安装来源恢复与通知更新。

感谢 [XayahSuSuSu](https://github.com/XayahSuSuSu) 的 [Android-DataBackup](https://github.com/XayahSuSuSu/Android-DataBackup) 提供 App 支持。
</details>

<details>
<summary><b>Q6：息屏后备份速度变慢？</b></summary>

这通常是 Android 内核或厂商 ROM 的 IO / CPU 节能策略。可在 `backup_settings.conf` 设置 `setDisplayPowerMode=1`，或备份期间保持屏幕常亮。
</details>

<details>
<summary><b>Q7：如何单独备份 / 恢复 / 上传单一应用？</b></summary>

进入备份文件夹内对应应用子目录，运行：

- `backup.sh`：单独备份该 App
- `recover.sh`：单独恢复该 App
- `upload.sh`：单独上传该 App 到远程
</details>

<details>
<summary><b>Q8：WebDAV 上传显示 HTTP 423 Locked？</b></summary>

通常是 WebDAV server 对文件锁定或大档策略限制。建议改用自家 NAS、rclone serve webdav、Nextcloud，或改用 SMB 测试。
</details>

<details>
<summary><b>Q9：WebDAV 上传或列表显示 HTTP 404？</b></summary>

请检查 `webdav_url` 是否指向正确 WebDAV 端点，例如 `/dav/`、`/remote.php/webdav/` 或 rclone serve 的根路径。若是 app_details 不存在的 404，脚本会按「远程尚无备份」处理，不一定是错误。
</details>

<details>
<summary><b>Q10：SMB 提示找不到 share 或写入失败？</b></summary>

请确认：

- Windows / Samba / NAS 已打开 SMB2 / SMB3
- 共享名称与路径正确
- 帐号具备写入权限
- 防火墙允许 445 port
- 主菜单 SMB 扫描结果与 `smb_url` 一致
</details>

<details>
<summary><b>Q11：没网络会影响本地备份吗？</b></summary>

不会。若远程不可用，脚本会在预检阶段中止远程流程或禁用远程上传；本地备份可继续完成。
</details>

<details>
<summary><b>Q12：流式备份和一般备份有什么差别？</b></summary>

| | 一般备份 | 流式备份 |
|---|---|---|
| 本机空间占用 | 先压缩到本机再上传 | 不落本机，直接传输 |
| 增量 / fast-skip | 支持 | 支持 |
| 本机完整性校验 | 支持 | 不支持完整本地校验 |
| 适合场景 | 本机空间充足 | 本机空间有限、区网稳定 |
</details>

<details>
<summary><b>Q13：为什么 log 里有些 stderr 是 0KB？</b></summary>

`stderr.log`、`root_daemon_stderr.log`、`webdav_daemon_stderr.log` 为 0KB 通常是正常现象，代表没有错误输出。主流程请看 `main.log` 或 `log/log_yyyy-mm-dd_hh-mm.txt`。
</details>

---

## 问题反馈

遇到问题请携带截屏与 speed_debug 压缩包，通过以下方式反馈：

- [GitHub Issues](https://github.com/YAWAsau/backup_script/issues)
- [Telegram 频道](https://t.me/yawasau_script)
- QQ 群：`976613477`
- 酷安：[@落叶凄凉TEL](http://www.coolapk.com/u/2277637)

---

## 支持作者

备份脚本耗费了大量时间与精力，如果你觉得好用，欢迎赞助支持。

[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg?style=flat-square&logo=paypal)](https://paypal.me/YAWAsau?country.x=TW&locale.x=zh_TW)

---

## 感谢贡献者

| 贡献者 | 贡献内容 |
|--------|----------|
| [kmou424](https://github.com/kmou424)(臭批老k) | 提供部分验证函数思路 |
| [雄氏老方](http://www.coolapk.com/u/665894)(屑老方) | 提供自动更新脚本方案 |
| [sakuradairong](https://github.com/sakuradairong)(雨季骚年/胖子老陈) | 添加 WebDAV / SMB 功能与测试 |
| [XayahSuSuSu](https://github.com/XayahSuSuSu) | 提供 App 支持与 Dex 功能支持 |

`文档编辑：Petit-Abba, YuKongA`

---

<p align="center">
 <sub>GPL-3.0 Licensed · Made with ❤️ by <a href="https://github.com/YAWAsau">YAWAsau</a></a></sub>
</p>