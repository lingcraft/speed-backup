# SpeedBackup / Backup_script 数据备份脚本【简体中文版】

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

Backup_script 是一款专为 Android 设计的应用数据备份／恢复 Shell 脚本，支持应用数据、Split APK、SSAID、运行时权限、AppOps、特殊访问、电池策略、安装来源、OBB 数据包、Wi-Fi 设置与自定义文件夹备份。适合换机、刷机、重装系统后快速还原应用状态。

脚本提供本地备份与远程备份两种模式。远程备份支持 WebDAV / SMB，可上传到 NAS、区网电脑、rclone serve webdav、Nextcloud 等服务，可先下载备份回手机再恢复，也可直接从远程串流解压恢复。

新版支持流式备份：数据可直接 `tar | zstd | 传输`，不需要先落地成本机压缩包，适合本机空间不足的设备。对于没有变化的应用，脚本会通过版本、数据大小、AppState、SSAID 与远程文件状态进行 fast-skip，避免重复压缩与重复上传。

新版 AppState metadata 采用 `app_details_bundle.tar.zst` bundle-only 远程同步流程：功能 7 会先汇总本地 metadata 再上传，功能 10 会先下载 bundle 并同级解包，再下载所选备份；恢复需另外运行。

> 作者为台湾人，预设发布繁体版本。简体中文环境下脚本可自动切换语言。

**系统需求：** `Android 9+` · `arm64 架构` · `Root 权限(Magisk / KernelSU)`

本仓库为**简体中文修正版**，对原脚本中**部分专有名词**进行了**修正**，脚本执行逻辑无任何修改，具体使用哪个版本请自行决定，**原版**可前往这里下载：
> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。

简体中文版使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。

---

## 功能特色

| 功能 | 说明 |
|------|------|
| 应用数据备份 | 备份应用数据、APK、Split APK、user / user_de / data / OBB 等数据 |
| 应用恢复 | 支持批量与单 App 恢复，核对文件与 AppState；受系统限制的项目会分开显示 |
| Play 商店来源还原 | 支持恢复 installer / install source，依备份记录与支持的安装流程设置来源 |
| SSAID 备份与恢复 | 支持备份与恢复 Android SSAID，协助保留依赖此识别码的应用状态，不保证免登录 |
| 权限与 AppOps | 支持运行时权限、AppOps、特殊访问、电池策略等状态备份与恢复 |
| AppState metadata bundle | 新版 metadata 统一汇总为根层 `app_details_bundle.tar.zst`，远程同步与下载以 bundle 为准 |
| 本地旧 JSON 恢复兼容 | 本地既有旧备份的 `app_details.json` 可在恢复时转换为新版 AppState restore record |
| Split APK | 支持多 split APK 备份与恢复 |
| OBB 数据包 | 可选备份外部 OBB 数据，如大型游戏数据报 |
| Wi-Fi 备份 | 支持 Wi-Fi 设置备份与恢复 |
| 自定义文件夹 | 可备份与恢复 DCIM、Download、Music 等任意自定义目录 |
| 压缩方式 | 支持 `zstd` 压缩与 `tar` 仅打包 |
| 增量备份 | 多维度比对版本、数据大小、权限、SSAID、AppState，无变化则跳过 |
| 全量 fast-skip | 本地 / WebDAV / SMB 全部无变化时可整批折叠跳过，不进逐 App 主流程 |
| 远程备份 | 支持 WebDAV / SMB 备份、下载、恢复、列表与健康检查 |
| 流式备份／恢复 | 不先暂存完整数据压缩包；仍需 metadata、日志与恢复后数据的空间 |
| 远程已卸载应用清理 | 功能 9 比对本机已安装套件与远程备份，列出候选并确认后删除；信息不足不直接判为可删除 |
| 统一备份统计 | 汇总逐项、每个 App 与整轮结果，分开核对预估与实际大小；跳过不计本轮实际量，APK 仅重打包才计入 |
| 恢复文件核对 | 依备份包清单核对落地文件、目录、大小与链接；不包含逐档内容哈希及完整 SELinux／ACL 验证 |
| 事件等待与进程稳定检查 | 使用 `eventwait` / `procwait` 辅助远程串流等待、备份前稳定等待与恢复守护收尾 |
| 远程预扫 | 远程备份前批量取得远程列表与 metadata 状态，降低主循环网络开销 |
| 远程 metadata 健康检查 | 远程 `app_details_bundle.tar.zst` 缺失、损坏或内容不完整会明确提示，不静默忽略 |
| SMB 扫描 | 自动扫描区网 SMB 主机与 share，免手动找 IP |
| WebDAV 兼容 | 支持逐层建目录、PUT/MOVE/STAT/GET 校验、404 非致命判断等 WebDAV 兼容处理 |
| 日志与 debug 包 | 自动生成 speed_debug 诊断包，legacy `log/log_yyyy-mm-dd_hh-mm.txt` 会同步主日志摘要 |
| 后台运行 | 支持后台运行模式，log 持续刷新 |
| 状态通知 | 支持备份 / 恢复进度与结果通知 |
| 多用户支持 | 支持 user 0、999 等多用户环境，可指定或自动选择用户 |
| 配置自动修补 | 升级后自动补齐 `backup_settings.conf` 缺少项目，不需手动重写 |
| 自动更新 | 支持本地 ZIP 更新、Download / QQ 下载目录检测与 GitHub release 检查 |
| 完整性检查 | 工具 SHA-256、压缩包检查、远程大小与恢复清单核对分别处理；未知或未检查不等同通过 |
| 启动自我检测 | `tools/dex_check.sh` 检查 Dex／原生工具能力与目前使用的流程，汇整成功、警告与失败 |
| 单一原生工具 | 八个 Rust 工具集成为 `speednative`，启动后创建原名称软链接 |

---

## 主菜单功能

备份与恢复模式的编号不同，请先确认目前位于工具根目录或备份目录。以下为 r718 菜单。

### 备份模式

| 编号 | 功能 | 说明 |
|---|---|---|
| 1 | 生成应用列表 | 产生 `appList.txt` |
| 2 | 备份应用 | 依列表与设置备份，符合跳过条件的项目不重打包 |
| 3 | 备份已更新应用 | 备份版本有变化的应用 |
| 4 | 备份自定义文件夹 | 使用 `Custom_path` 设置 |
| 5 | 备份 Wi-Fi | 备份目前设备的 Wi-Fi 设置 |
| 6 | 测试远程连接 | 检查 WebDAV／SMB 连接与写入能力 |
| 7 | 单独上传当前备份 | 上传现有本地备份并汇总 metadata bundle，不重新备份数据 |
| 8 | 列出远程备份 | 产生 `appList_network.txt` |
| 9 | 删除远程已卸载应用 | 列出本机已卸载、远程仍有备份的候选，确认后删除 |
| 10 | 从远程下载备份 | 下载 metadata bundle 与所选备份，补齐本地恢复入口 |
| 11 | 从远程流式恢复 | 直接传输并解压所选备份，不先存整包 |
| 12 | 从远程流式恢复自定义文件夹 | 直接恢复远程 Media／自定义目录 |
| 13 | 目前备份统计 | 查看备份统计 |
| 14 | 重生现有备份 JSON | 更新 metadata，保留既有大小、版本、时间与 SSAID，不重打包数据 |
| 15 | 杀死运行中脚本 | 终止正在运行的脚本流程 |
| 0 | 离开脚本 | 结束菜单 |

### 恢复模式

| 编号 | 功能 | 说明 |
|---|---|---|
| 1 | 重新生成应用列表 | 刷新备份目录的 `appList.txt` |
| 2 | 恢复备份 | 依列表恢复应用、数据与 AppState |
| 3 | 仅恢复包含 SSAID 应用（含数据） | 筛选有 SSAID 备份值的应用后恢复 |
| 4 | 仅恢复包含 SSAID 应用的 App 状态（不含数据） | 对已安装的应用恢复 App 状态，不覆盖应用数据；并非只写 SSAID |
| 5 | 恢复自定义文件夹 | 恢复已备份的自定义目录 |
| 6 | 恢复 Wi-Fi | 恢复 Wi-Fi 设置 |
| 7 | 压缩档完整性检查 | 检查备份压缩包，不等同确认 App 恢复后可正常登录 |
| 8 | JSON 结构检查 | 检查 metadata 结构 |
| 9 | 重生现有备份 JSON | 保留大小、版本、时间与 SSAID，更新 metadata |
| 10 | 转换文档夹名称 | 转换备份文件夹名称格式 |
| 11 | 杀死运行中脚本 | 终止正在运行的脚本流程 |
| 0 | 离开脚本 | 结束菜单 |

「重生 JSON」会使用本机目前可取得的应用状态，不能补回从未备份的历史状态。一般备份／恢复不需要每次手动运行。

---

## 目录结构

完整发行包解压后的主要文件如下；源代码包的目录配置不同。

```text
SpeedBackup/
├── tools/
│   ├── busybox             # 内核工具集
│   ├── speednative         # 八个 Rust 工具共用的原生程序
│   ├── zstd                # 压缩工具
│   ├── tar                 # 打包工具
│   ├── smbclient           # SMB 传输
│   ├── jq                  # JSON 处理
│   ├── find                # 文件搜索
│   ├── keycheck            # 音量键输入
│   ├── cmd                 # 系统指令桥接
│   ├── classes.dex         # Android 系统操作与远程传输辅助
│   ├── soc.json            # 处理器数据库
│   ├── dex_check.sh        # Dex／原生能力与流程自检
│   └── tools.sh            # 内核脚本
├── backup_settings.conf    # 备份设置，可由脚本补齐
└── start.sh                # 运行入口
```

启动时会在 `/data/backup_tools/` 释放工具，并把 `cgfreezer`、`eventwait`、`filewatch`、`netwatch`、`procwait`、`speedscan`、`uidexec`、`unixsock` 创建为指向 `speednative` 的软链接。原有调用名称保留，不必自行在手机共享保存空间创建链接。

**请保留完整 `tools/`，并使用同一发行包的脚本、Dex 与原生工具。** 不要把不同版本的单一文件混用。

本地备份的 App 子目录可生成 `backup.sh`／`recover.sh`／`upload.sh`，供单 App 操作。远程不必保存这些入口与整套工具；功能 10 下载后会使用本机工具补齐。因此远程只有数据压缩包与 metadata，没有 `tools/`，可以是正常状态。

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
| `mount_point` | 屏蔽外部挂载点，多个用 `\|` 分隔 | 自订 |
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
| `Compression_method` | App 数据使用 `zstd` 或 `tar`；一般 Media／自定义目录另走 tar 仅打包 | `zstd` |
| `Zstd_level` | 压缩等级 `1`～`22`；`20`～`22` 会激活 ultra | `6` |
| `Zstd_threads` | 一般压缩线程 `0`～`64`；`0` 自动使用可用内核 | 新建设置 `0`；旧设置补齐可能为 `4` |
| `Zstd_small_max_bytes` | 已知 tar 输入不超过此大小时使用小档线程；`0` 关闭切换 | `1048576`（1 MiB） |
| `Zstd_small_threads` | 小档使用的线程数，与 `--single-thread` 不同 | `1` |
| `Zstd_size_hint` | 使用既有大小计划提供压缩提示，不另外扫描 | `1` |
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
| `remote_keep_local` | 非流式上传成功后：`1` 保留本地数据报、`0` 删除；不会让流式备份额外保存整包 | `0` |
| `remote_upload_per_app` | 每个 App 备份后立即上传，非流式模式下节省空间 | `0` |
| `log_max_size_mb` | `log/` 目录大小上限，留空或 `0` 关闭自动清理 | 留空 |

---

## 使用方式

### 调整 zstd 压缩

直接修改 `backup_settings.conf`，不用重新编译。例如：

```conf
Compression_method=zstd
Zstd_level=6
Zstd_threads=0
Zstd_small_max_bytes=1048576
Zstd_small_threads=1
Zstd_size_hint=1
```

想提高压缩率可调高 `Zstd_level`，代价是更多时间与内存；影音、APK 等已压缩内容可能改善有限。`Zstd_threads` 控制并进程度，不是压缩等级。已有设置不会自动改成新预设；r718 对缺少此字段的旧设置仍补入 `4`，想自动使用内核请明确填 `0`。

一般 Media／自定义文件夹采 tar 仅打包，调整 `Zstd_level` 不会让这些 tar 变小。小档切换与大小提示也只在取得有效大小计划时生效。debug 的 `ZSTD_EFFECTIVE_PARAMS` 可查看每个项目实际使用的值。

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

若恢复结束后提示存在 SSAID，建议立刻重启后再打开应用。打开 App 后仍需确认登录与数据状态；SSAID 核对成功不代表服务器登录验证一定通过。

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
remote_keep_local=0
```

上述为流式范例，不会额外保留本机整包。若要保留本机备份并上传，请改为 `remote_stream=0`、`remote_keep_local=1`。

| 协议 | 地址格式 | 适用场景 |
|------|----------|---------|
| SMB | `smb://192.168.1.100/share/path` | Windows 共享 / Samba / NAS |
| WebDAV | `http://192.168.1.100:8080/dav/` | NAS / Nextcloud / rclone serve webdav |

### 远程目录结构

脚本会在远程地址下创建 `Backup_<压缩方式>_<用户ID>/`。以下为示意，实际项目依备份内容而定：

```text
Backup_zstd_0/
├── app_details_bundle.tar.zst  # AppState 与备份 metadata
├── LINE/
│   ├── apk.tar.zst
│   ├── user.tar.zst
│   └── user_de.tar.zst
├── Media/
│   └── Download.tar           # 自定义文件夹，文件名依设置而定
└── wifi/
    └── wifi.json
```

远程数据目录不需要与本地工具目录完全相同。`start.sh`、App 操作入口、设置与 `tools/` 由下载流程在本机补齐；不要因远程缺少这些文件就判定备份不完整。

不同 Android 用户会分开到不同目录，例如 `Backup_zstd_0/`、`Backup_zstd_999/`。

新版远程 metadata 采用 bundle-only 流程。远程根层的 `app_details_bundle.tar.zst` 是恢复与远程下载所需的 metadata 主档；bundle 内部保留 App 目录结构，下载后会在本地备份根目录同级解包成 `<App目录>/app_details.json`。

### 远程备份特性

- **流式备份**：`remote_stream=1` 时，数据直接打包并传输到远程，不先暂存完整数据报；metadata 与日志仍会保存在本机。
- **远程 fast-skip**：比对版本、大小、AppState 等记录，符合条件时跳过；这不是逐档内容哈希比对。
- **远程 metadata bundle 健康检查**：缺失、损坏或内容不完整的 `app_details_bundle.tar.zst` 会明确提示。
- **失败保护**：流式上传失败时不更新远程 metadata 状态，避免下轮误判已备份完成。
- **WebDAV 兼容处理**：依服务实际能力选择目录枚举与提交方式；上传后核对远程文件，大小无法取得时明确标示核验范围。
- **SMB 写入预检**：正式备份前会测试远程目录创建与写入能力。

---

## AppState metadata bundle

新版 AppState metadata 以备份根目录的 `app_details_bundle.tar.zst` 为主，不再把远程逐 App `app_details.json` 作为功能 7 / 功能 10 的 metadata 同步主路径。

### 产生与上传

远程备份流程会汇总根层 `app_details_bundle.tar.zst`。使用功能 7「单独上传当前备份」时，脚本会先扫描本地备份目录内的：

```text
<App目录>/app_details.json
```

并重新汇总成：

```text
app_details_bundle.tar.zst
```

然后再上传到远程根层。功能 7 的上传清单会过滤逐 App `app_details.json`，metadata 只同步 bundle。

### 下载与解包

功能 10「从远程下载备份」会要求远程根层存在：

```text
app_details_bundle.tar.zst
```

下载成功后，脚本会在本地备份根目录同级解包，恢复成：

```text
<App目录>/app_details.json
```

如果远程缺少 `app_details_bundle.tar.zst`，功能 10 会中止下载；不再 fallback 到远程逐 App `app_details.json`。

---

## 流式备份模式

`remote_stream=1` 激活后，数据直接走：

```text
tar → zstd（选用压缩时）→ WebDAV / SMB
```

优点：

- 不先暂存完整数据压缩包，但仍需 metadata、工具与日志空间
- 适合本机剩余空间不足的设备
- 支持 WebDAV / SMB
- 支持远程 fast-skip 与传输结果、远程大小核对；不是远程逐字节内容校验

限制：

- 传输过程依赖网络稳定性；流式不可用时会中止，不会偷偷改成整包本机暂存
- 本地不保留压缩包时，无法做本地 tar/zstd 完整性校验
- 若远程上传失败，该 App 会保留失败状态，下轮重新备份

---

## 从远程下载备份

需要在本地保存压缩包时使用功能 **10**；想直接恢复 App 使用功能 **11**，只恢复自定义文件夹使用功能 **12**。流式恢复仍需要足够空间放解压后的数据。

**Step 1 — 列出远程备份**

备份模式选功能 **8「列出远程备份」**，产生 `appList_network.txt`。

**Step 2 — 编辑下载列表**

打开 `appList_network.txt`，用 `#` 注解掉不需要下载的应用。

**Step 3 — 从远程下载备份**

备份模式选功能 **10「从远程下载备份」**。脚本会先下载远程根层 `app_details_bundle.tar.zst`，并在本地备份根目录同级解包出各 App 的 `app_details.json`。若远程缺少 `app_details_bundle.tar.zst`，下载会中止，避免产生 metadata 不完整的本地备份。

下载完成后，直接运行下载文件夹中的 `start.sh` 进行恢复。

---

## 本地旧版 JSON 恢复兼容

本地既有旧备份仍可在恢复时读取逐 App `app_details.json`。若旧 JSON 没有新版 `app_state` 字段，但仍保留：

```text
permissions
battery_settings
Ssaid
installer / install_diagnostics
apk_version
PackageName
user / user_de / data Size
```

脚本会在恢复时尝试转换为新版 AppState restore record，等效于：

```text
sourceFormat=legacy-app-details-migrated
recordType=snapshot
schemaVersion=2
```

旧 JSON 已有的 SSAID、权限、AppOps、电池策略与安装来源会尽量恢复；旧 JSON 本来没有的新字段则无法凭空补出。

> 注意：此兼容仅针对本地既有旧备份恢复。新版功能 7 / 功能 10 的远程同步流程采 `app_details_bundle.tar.zst` bundle-only，不再使用远程逐 App `app_details.json` 作为 metadata 主路径。

---

## AppState / Dex 功能

`classes.dex` 用于实现 Shell 难以稳定完成的系统操作。目前主要负责：

- AppState snapshot / restore / verify
- SSAID 备份与恢复辅助
- 运行时权限、AppOps、特殊访问、电池策略状态处理
- 安装来源、installer、Play 来源恢复辅助
- 批量取得 App 名称、包名、版本、split 信息与安装后状态
- WebDAV 连接、相对路径检查与传输服务
- SMB 主机与 share 扫描辅助
- 通知批量更新
- 权限 / AppOps / 特殊访问中文语意输出
- 查找预设桌面、输入法、电话、短信、浏览器与助理
- 查找保存空间与媒体路径
- 内置设备型号数据库，release 内不再需要外置 `tools/Device_List`

Rust 原生工具负责文件树、备份计划、统计与文件验证；Dex 负责 Android 状态及相关传输能力。AppState／SSAID 的恢复与验证由 Dex 直接产生分类摘要，避免脚本靠消息措辞重新猜结果。

启动自检由 `tools/dex_check.sh` 运行，依实际能力检查兼容性，不只比较版本字符串。摘要会分开列出成功、警告、失败与内核失败；部分新流程使用 `SBRESULT` 统一结果格式。

**自检通过不等于完成一轮真实备份与恢复。** `partial` 可能表示有警告或核验不完整，请看原因；受厂商限制、数据不符与运行失败也不能视为同一种结果。

---

## 脚本更新方式

1. **本地 ZIP 更新**：将完整 release `.zip` 不解压，放到脚本目录或其上层目录，运行脚本时自动检测更新。
2. **Download 目录更新**：将完整 release `.zip` 放到 `/storage/emulated/0/Download/`，运行脚本时自动检测。
3. **QQ 下载目录更新**：从 QQ 下载的完整 release `.zip` 可直接放置后运行脚本更新。
4. **联网自动更新**：`update=1` 时会检查 GitHub release。

**旧版升级请整套更新，不要只替换 `tools.sh`。** 旧更新器可能仍要求原先的独立工具文件名，因而拒绝新版 `speednative` 配置。遇到「缺少旧工具」时，使用发行者提供的兼容更新包，或把完整发行包解压到新的工具目录后使用，保留原备份数据。

请从工具根目录运行更新。位於单一 App 的备份目录时，只提示返回工具根目录，不在该目录下载或应用更新。

更新规则：

- 本地完整 release 同版本允许覆盖更新，成功后删除更新 ZIP。
- 低于目前版本的 ZIP 会拒绝更新。
- 在线 release 与本地版本相同时不提示新版。
- 更新只同步 release 内工具与入口档，不会删除既有备份数据。
- 更新失败、拒绝或中止时会清理 `/data/local/tmp` 更新暂存。

> 本地备份可脱机使用。打开远程功能会向你设置的服务发送备份；打开在线更新会连接 GitHub 或所选 CDN。

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
- `stderr.log`：Shell 错误输出
- `root_daemon_stderr.log`：Root daemon 错误输出
- `webdav_daemon_stderr.log`：WebDAV daemon 错误输出
- `app_state_output.log`：AppState restore 输出
- `verify_app_state_output.log`：AppState verify 输出
- `stream_upload.log` / `stream_download.log`：流式上传 / 下载日志
- `extract.log`：恢复解压日志
- `restore_app_phase_timing.tsv`：恢复阶段耗时统计
- `restore_apk_timing.tsv`：APK 安装阶段耗时统计

stderr 为 0KB 只代表该输出档没有记录，不代表所有检查通过。请一并看 `main.log` 的结果摘要、失败原因、备份预估／实际差异，以及 AppState／SSAID 验证结果。没有有效计划时，单看 `mismatch=0` 也不能判定核对通过。

一般模式会精简成功恢复的详细清单；需要深入排查时才打开 `diagnostic_mode=1`，debug 包也会变大。实际文件名与输出位置以当轮提示为准。

---

## 常见问题

<details>
<summary><b>Q1：批量备份 / 恢复大量提示失败？</b></summary>

请先查看当轮 speed_debug 的第一个失败原因及自检摘要。若提示工具 SHA-256 或能力不符，先结束正在运行的工作，再使用同一完整发行包修复工具；不要在备份途中删除 `/data/backup_tools/`。仍失败时请提交 debug 包。
</details>

<details>
<summary><b>Q2：微信 / QQ 能完美备份恢复吗？</b></summary>

无法保证。大型实时通信 App 可能有服务常驻、数据库锁、服务器校验或加密状态。建议同时使用你信任的官方或第三方方式额外备份重要数据。
</details>

<details>
<summary><b>Q3：为什么部分应用备份很久？</b></summary>

可能是 user data、user_de、OBB 或外部 data 很大，也可能包含保存、传输或守护收尾等待。确认不需要这些外部数据后，才在 `backup_settings.conf` 将 `Backup_obb_data=0` 跳过外部 OBB / data 类大型数据。
</details>

<details>
<summary><b>Q4：脚本每次都是全量备份吗？</b></summary>

不是。脚本会比对版本号、数据大小、SSAID、权限、AppOps、AppState 与远程文件状态。无变化时会跳过；若全部选中 App 都无变化，本地与远程都可整批 fast-skip。这是依记录判断是否需要重新打包，不是区块增量或逐档哈希比对；内容改动但大小等条件相同时，不能保证一定辨识。
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

注意：新版远程恢复 metadata 以根层 `app_details_bundle.tar.zst` 为准。若手动运行单 App `upload.sh`，建议再回主菜单运行「单独上传当前备份」，让脚本重新汇总并上传 metadata bundle。
</details>

<details>
<summary><b>Q8：WebDAV 上传显示 HTTP 423 Locked？</b></summary>

先查看服务端日志中的文件锁定原因，确认是否有其他用户端正在写入同一目标，再使用功能 6 测试写入。请保留失败请求与 debug；不能只凭 HTTP 423 判定手机压缩或备份内容有错。
</details>

<details>
<summary><b>Q9：WebDAV 上传或列表显示 HTTP 404？</b></summary>

请检查 `webdav_url` 是否指向正确 WebDAV 端点，例如 `/dav/`、`/remote.php/webdav/` 或 rclone serve 的根路径。若是 `app_details_bundle.tar.zst` 不存在，功能 10 会中止下载；备份或上传流程请先生成并同步 metadata bundle。
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

未激活远程时，本地备份可脱机运行。非流式模式在远程连接预检失败时，会禁用上传并保留本地备份；`remote_stream=1` 则会中止，不会自动改成占用本机整包空间的备份。
</details>

<details>
<summary><b>Q12：流式备份和一般备份有什么差别？</b></summary>

| | 一般备份 | 流式备份 |
|---|---|---|
| 本机空间占用 | 保存数据报，远程模式再上传 | 不先存完整数据报，仍有 metadata／日志等 |
| 增量 / fast-skip | 支持 | 支持 |
| 本机完整性校验 | 支持 | 不支持完整本地校验 |
| 适合场景 | 本机空间充足 | 本机空间有限、区网稳定 |
</details>

<details>
<summary><b>Q13：功能 10 提示缺少 app_details_bundle.tar.zst？</b></summary>

新版远程下载需要根层 `app_details_bundle.tar.zst`。请先使用新版完整备份，或在本地备份文件夹使用「单独上传当前备份」，让脚本汇总本地各 App 的 `app_details.json` 并上传 metadata bundle。
</details>

<details>
<summary><b>Q14：为什么 log 里有些 stderr 是 0KB？</b></summary>

`stderr.log`、`root_daemon_stderr.log`、`webdav_daemon_stderr.log` 为 0KB 通常是正常现象，代表没有错误输出。主流程请看 `main.log` 或 `log/log_yyyy-mm-dd_hh-mm.txt`。
</details>

---

## 目前核验范围

- 备份预估大小与实际打包大小分开核对，跳过、未知与失败项目分开处理。Media 尚未完整纳入全局精确大小计划。
- 恢复清单检查可发现缺档、类型、大小与链接等差异，不包含逐档内容哈希及完整 SELinux／ACL 验证。
- AppState／SSAID 核对通过后，仍需实际打开 App 确认数据与登录；系统、厂商及服务器限制不一定能由脚本还原。
- WebDAV 的串流耗时可能包含打包、压缩、网络、读取与守护收尾等待，小档显示的低速不能直接当成网络测速结果。

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
 <sub>GPL-3.0 Licensed · Made with ❤️ by <a href="https://github.com/YAWAsau">YAWAsau</a></sub>
</p>