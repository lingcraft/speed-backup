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

> 本文档对应 v1123／原生界面 1.80（versionCode 81）。界面已迁移至 Kotlin／Compose，APK 直接连接本机 Rust API，不再使用 WebView／JavaScript 或浏览器操作入口。操作与接回见 [原生主菜单](WEB_MAIN_MENU.md)。[本次更新：v1102 → v1117](docs/updates-since-793d285.md) · [完整更新日志](CHANGELOG.md)

---

## 界面与脚本语言

切换繁体／简体后会保存语言设置，闲置时自动重新加载脚本并回到设置页；工作运行中收到语言切换时，会等工作安全收尾后再加载，不会重跑工作。既有日志维持原文。

繁简转换由 Dex CLI 单次启动、串流处理，加入 OpenCC 1.4.2 词组数据，改善「头发／发现」「干净／饼干」「皇后／后来」等字形选择，并保留项目用词。这是词组匹配，不是理解整句的翻译模型，也不是完整 OpenCC 原生引擎。

正式脚本切回繁体时，另以该版本生成的完整行对照表还原已知差异；v1117 已在备用机验证 11 次往返 SHA-256 相同。用户自行修改或其他版本未收录的行不保证无损，一般文字与 conf 也不应用脚本还原规则。

建置入口会自动生成词组索引与脚本还原表，CI 检查生成结果是否过期；词库在每个转换进程内只加载一次，不需外部词库或 JNI。

## 后端职责

Rust 负责配置的字面值解析、旧字段迁移与原子保存、远程地址追踪与帐密重填协调，以及诊断 tar 的锁定和原子更新。Dex 负责 Android 通知的文字、进度校正、节流与通知分类。Shell 保留备份／恢复流程、传输介接与设置模板；APK 保留原本界面。既有 conf、帐密重试／返回、地址记忆及单一诊断包的操作方式不变。

## 远程帐密与诊断

WebDAV 回传 401 或 SMB 明确认证拒绝时，前台操作会打开帐号、密码重填页。按「保存并重试」写回对应 conf，再重试连接预检；按「返回」停止本次操作。权限、路径与网络错误分开处理，不会自动重播上传或删除。背景模式需回到设置修正帐密。

同一工作服务阶段共用一份 `speed_debug_session_*.tar`，包内使用单一根目录及连续日志，不再为每次操作保留独立 run 子目录。快照与重试避免重复并入，JSON 保留最新有效内容及历史索引。关闭 APK 后接回仍属同一阶段；结束服务后重新启动才创建新包。每次安全收尾原子更新归档，失败保留原归档与待合并日志。

## 自动发现与地址追踪

在「设置 → 备份设置 → 远程连接与传输」选择 SMB 或 WebDAV，再设置「SMB／WebDAV 自动发现地址」开关：

- **关闭（手动地址）**：沿用原本网址与帐密输入，也能搜索后填入地址。本地备份不启动搜索。
- **打开（自动追踪设备）**：首次开始远程备份／恢复时，打开设备选择及连接设置；选择后填写帐密，SMB 需填共用文件夹。按底部「连接并继续」保存地址、帐密及设备身分至 conf，再由原本连接预检验证，未通过就停止本次操作。
- 下次优先使用原地址；确认同一设备只是换 IP 时，提示地址已更新，直接使用并写回 conf。帐密与文件夹路径保留。找不到原设备时重新打开选择，不会自动换成其他设备。
- 发现与追踪由 Rust 后端运行，APK 仅显示、选择及编辑。结果一到即显示，不需等 15 秒搜索结束；SMB 原地址先做识别验证，未匹配才并行探测私有 IPv4 网段（每段最多 /24、合计 512 地址、32 个工作线程）。
- SpeedBackup Server 若公告持久化 TXT `id`，以该 ID 跨重启与网卡变更追踪；其他 WebDAV 使用 DNS-SD 服务名称、主机名称与协定（服务名称须保持稳定）；SMB 可通过 SMB2/3 NEGOTIATE 读取 ServerGuid，不需安装广播服务，也不发送帐密。未取得识别码的「SMB 候选」只能手动使用。这些识别信息供换址追踪，并非密码学认证；实际连接仍须通过 SMB 认证／HTTPS 凭证验证。
- 选定地址、帐密与设备识别存于原 conf；自动换址只原子更新对应 URL，保留其他字段，遇到同时编辑则拒绝覆写。进行中的传输不切换目的地，也不因回到家中网络就自行开始作业。
- DNS-SD 支持 `_webdav._tcp`、`_webdavs._tcp`、`_smb._tcp`。隔离网络、跨网段、自订 SMB 端口或 IPv6 link-local scope 可能需手动输入。Windows／NAS 的既有 SMB 分享不用更换服务器。

## 概述

Backup_script 是一款专为 Android 设计的应用数据备份／恢复 Shell 脚本，支持应用数据、Split APK、SSAID、运行时权限、AppOps、特殊访问、电池策略、安装来源诊断、OBB 数据包、Wi-Fi 设置与自定义文件夹备份。适合换机、刷机、重装系统后快速还原应用状态。

脚本提供本地备份与远程备份两种模式。远程备份支持 WebDAV / SMB，可上传到 NAS、区网电脑、rclone serve webdav、Nextcloud 等服务，可先下载备份回手机再恢复，也可直接从远程串流解压恢复。

新版支持流式备份：数据可直接 `tar | zstd | 传输`，不需要先落地成本机压缩包，适合本机空间不足的设备。对于没有变化的应用，脚本会通过版本、数据大小、AppState、SSAID 与远程文件状态进行 fast-skip，避免重复压缩与重复上传。

AppState metadata 采用 `app_details_bundle.tar.zst` 集中同步。「单独上传当前备份」会先汇总 metadata 再上传；「从远程非串流恢复（先下载）」会下载 metadata 与所选数据后接着恢复。

> 作者为台湾人，预设发布繁体版本。简体中文环境下脚本可自动切换语言。

**系统需求：** `Android 9+` · `arm64 架构` · `Root 权限(Magisk / KernelSU)`

本仓库为**简体中文修正版**，对原脚本中**部分专有名词**进行了**修正**，脚本执行逻辑无任何修改，具体使用哪个版本请自行决定，**原版**可前往这里下载：
> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。

简体中文版使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。

---

## 从终端操作迁移至 App

原本在终端显示的主菜单、交互提示、备份／恢复进度与彩色运行日志，现已集中到 SpeedBackup App。应用选择、设置与一般确认改用画面点击，运行期间可在 App 查看进度、跟随最新日志或翻阅历史，不必一直停留在 MT 管理器的终端画面。

App 负责操作与显示，实际备份／恢复仍由背景的 Root 脚本、Dex 与原生工具运行。终端仍作为 `start.sh` 的启动入口，启动检查及部分更新流程仍可能显示终端提示；不是把整个备份引擎改写成 APK。

### 启动与操作

使用具 Root 权限的终端运行 `start.sh`，依启动提示进入原生界面。主菜单、应用清单、备份设置、路径选择与运行日志均在 APK 中操作。既有备份数据与配置继续沿用，不需因界面迁移重新备份。

- **工作接回**：工作启动后可关闭画面或终端，备份／恢复会继续。再次从相同入口启动可接回目前工作；需要中止时使用「停止工作」。关闭画面不会自动保存尚未确认的编辑。
- **应用清单**：支持搜索、筛选、分页及勾选。图标优先准备首批、分批加载并预载下一页，重用缓存以减少空图标闪烁。
- **逐行名单编辑**：黑名单、白名单与 system 清单可添加一行、按 × 删除及粘贴多行；超过 100 项分页。按「确定」先回填设置草稿，仍须「保存设置」才写入文件；路径选择同样先回填字段。
- **多行输入**：输入框随内容增高，删除后缩回，短内容不再固定占用三行。
- **返回与日志**：系统返回依页面及文件夹层级逐层退回，有未保存修改时提示确认。日志可跟随最新或回看历史；压缩／解压进度保留平滑过渡与等宽数字。

### 外观、壁纸与玻璃

一般控件统一使用 Miuix，主画面按钮与底部导览保留液态玻璃。浅色／深色采用与 KernelSU 相同的 Miuix 标准语意配色；星空／夜空保留背景动画，控件采标准深色。莫奈动态配色选项只在支持的外观显示。

「设置 → 壁纸」提供导入图片、使用系统静态壁纸、激活开关、还原背景，以及透明度／模糊度／压暗调整。图片缩略图后存于应用私有目录，模糊结果在背景线程计算并重用。动态壁纸不截取桌面；无法导入时依画面提示处理。

| 设置 | 行为 |
|---|---|
| 壁纸透明度 | 目前滑杆 100% 为完整显示壁纸、0% 隐藏壁纸；与玻璃透明度方向不同 |
| 壁纸模糊 | 调整背景图片；液态玻璃采样画面上已模糊的壁纸 |
| 全局高斯模糊 | 控制卡片、按钮、输入框、菜单及对话框等控件的背景模糊；关闭时一般控件使用实色，不支持 GPU 模糊时采实色回退 |
| 自适应玻璃亮度 | 打开时依背景调整玻璃效果及文字对比；关闭时不自动调整玻璃亮度，但使用壁纸时仍独立选择黑／白文字 |
| 玻璃透明度 | 100% 不额外加入底色填充、0% 使用不透明底色；没有强制最低不透明度，边界与折射效果仍保留 |
| 折射强度 | 0% 关闭折射、100% 使用原有效果 |

壁纸操作参考 [Tweak-Alpha](https://github.com/lumkit/Tweak-Alpha/tree/e86ff392b7a1d22408305c8ffd1a3a1b9130e299) 独立实作。程序及历史文档中的 `webview`／`web` 名称保留升级兼容，不代表目前仍使用网页界面。

---

## 功能特色

| 功能 | 说明 |
|------|------|
| 应用数据备份 | 备份应用数据、APK、Split APK、user / user_de / data / OBB 等数据 |
| 应用恢复 | 支持批量与单 App 恢复，核对文件与 AppState；受系统限制的项目会分开显示 |
| Play 安装者身分 | 目标用户的 Play 商店可用且通过检查时优先使用其身分安装；否则使用普通安装，不保证 Play 授权或认证 |
| 应用列表 | Dex 提供新鲜完整已安装集合，Rust 一次合并、清理、排序与验证，保留注解及既有已安装系统 App |
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
| 远程已卸载应用清理 | 比对本机已安装套件与远程备份，列出候选并确认后删除；信息不足不直接判为可删除 |
| 统一备份统计 | 汇总逐项、每个 App 与整轮结果，分开核对预估与实际大小；跳过不计本轮实际量，APK 仅重打包才计入 |
| 恢复文件核对 | 依备份包清单核对落地文件、目录、大小与链接；不包含逐档内容哈希及完整 SELinux／ACL 验证 |
| 事件等待与进程稳定检查 | 使用 `eventwait` / `procwait` 辅助远程串流等待、备份前稳定等待与恢复守护收尾 |
| 远程预扫 | 远程备份前批量取得远程列表与 metadata 状态，降低主循环网络开销 |
| 远程 metadata 健康检查 | 远程 `app_details_bundle.tar.zst` 缺失、损坏或内容不完整会明确提示，不静默忽略 |
| 远程串流测速 | 依目前设置进行 SMB／WebDAV 5 GiB 上传及下载，不在手机创建大型测速档 |
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

## App 功能入口

从工具根目录的 `start.sh` 启动后，在 App「功能」页点击功能分类；从备份目录的 `start.sh` 启动则进入本地恢复模式。以下使用功能名称，不需输入旧终端菜单编号。

| 要做的事 | 操作入口与行为 |
|---|---|
| 备份应用 | 选「备份应用」，等待清单同步后勾选「仅 APK」或「完整」，再按下一步 |
| 只备份更新过的应用 | 选「备份已更新应用」，依画面确认选择 |
| 备份文件夹／Wi-Fi | 选「备份自定义文件夹」或「备份WiFi」 |
| 调整备份设置 | 在设置页打开「备份设置」，修改后保存 |
| 测试远程／扫描区网 | 在网络连接相关功能选「测试远程连接」，再点击连接测试、SMB／WebDAV 扫描或测速 |
| 上传已有备份 | 选「单独上传当前备份」，同步本地备份及 metadata bundle |
| 远程恢复 | 选「从远程非串流恢复（先下载）」或「从远程串流恢复(不占本机)」，在远程清单勾选项目后继续 |
| 清理远程备份 | 选「编辑远程备份」多选删除，或「删除远程已卸载应用」检查候选；依画面确认后才删除 |
| 本地恢复 | 从备份目录入口选「恢复备份」，在清单勾选需要的项目 |
| SSAID 相关恢复 | 在本地恢复模式选「仅恢复包含ssaid应用(含数据)」或「仅恢复包含SSAID应用的App状态(不含数据)」；后者不覆盖数据，并非只写 SSAID |
| 恢复文件夹／Wi-Fi | 在本地恢复模式选「恢复自定义文件夹」或「恢复wifi」 |
| 检查与维护 | 工具相关功能提供统计、压缩档完整性检查、JSON 结构检查、重生 metadata 或转换文件夹名称；项目依目前模式显示 |
| 查看或停止工作 | 在「工作运行中」查看进度与日志；中止时使用「停止工作」，等待收尾 |

「重生现有备份JSON」会使用本机目前可取得的应用状态，不能补回从未备份的历史状态。一般备份／恢复不需要每次手动运行。

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
│   ├── find                # 文件搜索
│   ├── keycheck            # 部分启动／更新流程使用的按键工具
│   ├── cmd                 # 系统指令桥接
│   ├── classes.dex         # Android 系统操作与远程传输辅助
│   ├── soc.json            # 处理器数据库
│   ├── dex_check.sh        # Dex／原生能力与流程自检
│   └── tools.sh            # 内核脚本
├── backup_settings.conf    # 备份设置，可由脚本补齐
└── start.sh                # 运行入口
```

启动时会在 `/data/.speedbackup/tools/` 释放工具，并把 `cgfreezer`、`eventwait`、`filewatch`、`netwatch`、`procwait`、`speedscan`、`uidexec`、`unixsock` 创建为指向 `speednative` 的软链接。原有调用名称保留，不必自行在手机共享保存空间创建链接。

**请保留完整 `tools/`，并使用同一发行包的脚本、Dex 与原生工具。** 不要把不同版本的单一文件混用。

本地备份的 App 子目录可生成 `backup.sh`／`recover.sh`／`upload.sh`，供单 App 操作。远程不必保存这些入口与整套工具；远程下载流程完成后会使用本机工具补齐。因此远程只有数据压缩包与 metadata，没有 `tools/`，可以是正常状态。

---

## 在 App 备份与恢复

设置中的包名清单与自定义路径建议每行一项；不要把含空白的路径自行拆开。旧设置保留原值，添加字段由脚本补齐。`diagnostic_mode` 已不是公开设置，模板同步会移除旧字段；一般运行仍会保留 speed_debug。

### 备份流程

1. 将完整发行包解压，用具 Root 权限的 MT 管理器或终端运行根目录 `start.sh`，依提示进入 App。
2. 在设置页打开「备份设置」，选择用户、备份项目及本地备份位置；需要远程备份时一并设置连接与传输方式，完成后保存。
3. 回到功能页选「备份应用」。清单会在进入时同步；等待图标准备完成后，利用搜索或筛选选择应用，勾选「仅 APK」或「完整」，两者皆不勾选则略过。
4. 按清单的「下一步」，完成画面提示后开始工作。在 App 查看进度与日志；启动后可关闭画面或终端，重新启动相同入口可接回。
5. 完成后查看结果摘要与失败项目。本地备份预设位于 `Backup_<压缩方式>_<用户ID>/`，例如 `Backup_zstd_0/`，实际位置依设置而定。

不需要先在终端运行「生成应用列表」，也不需要用文字编辑器逐行修改 `appList.txt` 才能备份。清单同步会保留既有选择与注解；无法完整取得清单时会显示失败，不应把准备失败当成空清单继续。

### 本地恢复流程

1. 运行备份文件夹内的 `start.sh`，进入本地恢复模式；需要调整恢复项目时先打开「恢复设置」并保存。
2. 选「恢复备份」，在 App 清单搜索、筛选及勾选需要恢复的应用或其他项目。
3. 按下一步，依画面确认后开始恢复。App 显示 APK、数据与 AppState 等处理进度，完成后查看结果摘要。
4. 若结果提示存在 SSAID，依提示重启后再打开应用，确认登录与数据状态；SSAID 核对通过不代表服务器登录验证一定通过。

### 清单与设置的高级用法

App 会管理 `appList.txt`、远程清单及配置。需要手动维护时，请先结束工作并关闭未保存的编辑页，再修改对应文件：

- `appList.txt` 行首 `#` 表示略过该应用。
- 应用名称前 `!` 表示在 `Backup_Mode=1` 时仅备份安装包，不备份数据；不是 Play 安装来源开关。
- 黑名单、白名单与自定义路径每行一项；不要把含空白的路径拆开。日常使用可直接在 App 逐行添加、删除或使用路径选择器。
- 配置缺少新字段时会自动补齐，已有值会保留。

### 调整压缩

在「备份设置」调整「压缩格式」「压缩等级」「压缩线程」及小文件相关选项后保存，不需重新编译。提高 zstd 等级通常会增加耗时与内存；影音、APK 等已压缩内容改善可能有限。压缩线程 `0` 代表自动使用可用内核，不是压缩等级。

一般 Media／自定义文件夹采 tar 仅打包，不受 zstd 等级影响。小档切换与大小提示只在取得有效大小计划时生效；debug 的 `ZSTD_EFFECTIVE_PARAMS` 可查看实际参数。

---

## APK 安装策略与恢复安全

- 目标 Android 用户的 Play 商店存在、激活且身分可确认时，优先使用 Play 安装者身分，不依 JSON 原始 installer 分流。数据目录或静默安装权限不足时不切换 Play UID；没有可用 Play 身分则使用普通 PM 安装。
- Play 混合 session 由每 App 一次的 Rust 协调器运行：以 Play UID 创建／提交，root 写入 APK。系统 PM 仍有子进程成本；不是 Java 安装器，也不是整批常驻安装 worker。
- 不再需要 `!play`；旧恢复清单前缀只作兼容性处理。JSON 安装来源字段仍可用于诊断，不是本次选择路径的依据。此功能不保证 `packageSource=STORE`、Play 授权、免登录或完整性认证。
- 保留路径、owner、UID/GID、文件描述符、逾时与 commit guard 检查。提交结果不明会回报状态 75，封锁本轮同用户／套件重试及其数据／AppState 恢复；只有明确失败才可依既有政策回退。重启脚本前先确认前次 session 结果。
- 提交期间可能暂时禁用 Android BackupManager 的全域自动还原，再依日志恢复；同一窗口内其他来源的安装也可能受影响，并非单一 App 隔离开关。
- 内部数据依目前套件 UID／seInfo 修复 ownership 与 SELinux；外部 data／obb 另走 Android 保存政策。终端宿主与无法安全停止的 App 仍受保护；从 Termux 自身运行时不恢复其宿主数据。
- 直接串流恢复会改动目标数据，没有整批回滚；失败可能已有部分内容写入。请保留独立备份，勿把「来源预检通过」当成恢复一定成功。

---

## 远程备份

### 设置方式

在 App「备份设置」选择「备份方式」，填入对应 SMB 或 WebDAV 地址、帐号与密码，设置「远程数据交换方式」及非串流文件保留方式后保存。两种协议的地址分别保留，切换时不需重新输入。

WebDAV 可依服务器类型明确应用设置范本，再核对地址；应用范本不等于连接成功。回功能页使用「测试远程连接」确认。以下是高级配置范例，日常操作不必直接编辑：

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

### 5 GiB 串流测速

在 App 选「测试远程连接」，再选测速项目（5 GiB 串流），使用目前保存的远程类型与帐密。上传随机数据至本轮专用远程目录，下载时计数后丢弃；手机不创建 5 GiB 测速档。

- 远程需约 5 GiB 可用空间，上下传合计约 10 GiB 流量；请确认网络费用与服务器配额。
- App 运行日志显示进度与速度，最终摘要使用完整传输平均值。短传输或失败不给成功评级。
- 正常完成或一般中止会尝试清理本轮目录；清理失败或强制终止后可能残留，依提示确认，不要删除其他备份。
- 数字包含数据产生、协议、远程保存与缓存影响，是端到端吞吐量，不是纯网络测速或完整备份速度。

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
- **WebDAV 兼容处理**：依服务实际能力选择目录枚举与提交方式；覆写既有文件使用暂存上传后提交，MOVE 不可用时失败，不改成直接破坏旧档的 PUT。请预留新旧档共存空间；上传后核对远程文件，大小无法取得时明确标示核验范围。
- **SMB 写入预检**：正式备份前会测试远程目录创建与写入能力。

---

## AppState metadata bundle

新版 AppState metadata 以备份根目录的 `app_details_bundle.tar.zst` 为主，不再把远程逐 App `app_details.json` 作为上传／远程下载 的 metadata 同步主路径。

### 产生与上传

远程备份流程会汇总根层 `app_details_bundle.tar.zst`。使用「单独上传当前备份」时，脚本会先扫描本地备份目录内的：

```text
<App目录>/app_details.json
```

并重新汇总成：

```text
app_details_bundle.tar.zst
```

然后再上传到远程根层。「单独上传当前备份」的清单会过滤逐 App `app_details.json`，metadata 只同步 bundle。

### 下载与解包

远程非串流恢复的下载阶段会要求远程根层存在：

```text
app_details_bundle.tar.zst
```

下载成功后，脚本会在本地备份根目录同级解包，恢复成：

```text
<App目录>/app_details.json
```

如果远程缺少 `app_details_bundle.tar.zst`，远程下载会中止；不再 fallback 到远程逐 App `app_details.json`。

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

## 从远程恢复

在 App 功能页选择「从远程非串流恢复（先下载）」或「从远程串流恢复(不占本机)」。进入时会取得远程数据并同步清单，直接在画面搜索、筛选与勾选，再按下一步；不需要先运行旧「列出远程备份」或手动修改 `appList_network.txt`。

| 方式 | 工作流程 | 本地空间需求 |
|---|---|---|
| 非串流恢复（先下载） | 下载 metadata 与所选备份，完成后自动接着恢复 | 下载数据报、保留的旧内容及解压后数据 |
| 串流恢复 | 从远程传输并直接解压所选项目 | 不先保存完整数据报，仍需解压后数据及 metadata／日志空间 |

**「非串流恢复（先下载）」是下载后接着恢复的操作，不是只下载。** 确认下一步前请核对所选应用与恢复设置。

远程下载需要根层 `app_details_bundle.tar.zst`。下载阶段在交易暂存区处理 metadata 与所选数据，成功发布后，各 App 的 `app_details.json` 位于本地备份根目录对应子目录；缺少 bundle 时中止，不产生 metadata 不完整的本地备份。

非串流下载会保留发布日志及旧内容，失败时依日志回复；回复失败会停止，不把远程缺档当成删除本地旧备份的授权。这是可恢复的多步交易，不是整批原子替换，也不适用于直接串流恢复。请预留足够空间，不要在工作中手动删除交易目录。

---

## 高级：配置字段参考

一般操作请在 App 的「备份设置」或「恢复设置」调整并保存，不必手动编辑文件。以下列出 `backup_settings.conf` 的保存值，供高级使用、旧设置迁移及排查问题。请勿在工作运行中或编辑页仍有草稿时从外部改写配置。

| 设置项 | 说明 | 常用值 / 预设 |
|--------|------|---------------|
| `low_battery_mode` | 低电量行为：`1` 强制拒绝、`2` 不提示继续、留空在开始时由 App 提示确认 | 留空 |
| `background_execution` | 背景模式与交互策略：`1` 激活、`0` 关闭；原生界面的工作启动后可关闭终端，不以此设置作为接回开关 | `0` |
| `notification_enable` | 状态栏通知与进度条：`1` 打开、`0` 关闭 | `1` |
| `Shell_LANG` | 语言：`0` 繁体中文、`1` 简体中文、留空自动侦测 | 留空 / `0` |
| `setDisplayPowerMode` | 备份 / 恢复期间伪装亮屏，避免 IO 因息屏降速 | `0` |
| `Output_path` | 自定义备份输出位置，支持相对路径 | 空 |
| `Backup_suffix` | 自定义备份目录后缀，支持日期时间变量 | 空 |
| `list_location` | 自定义 `appList.txt` 位置 | 空 |
| `update` | 自动更新：`1` 打开、`0` 关闭 | `1` |
| `cdn` | 更新 CDN 节点：`0` 直连、`1` ghfast、`2` workers | 新建设置 `1` |
| `mount_point` | 屏蔽外部挂载点，多个用 `\|` 分隔 | 自订 |
| `user` | 指定 Android 用户 ID，例如 `0`、`999`；留空时自动判断或询问 | 空 |
| `Backup_Mode` | `1` 应用 + 数据、`0` 仅安装包 | `1` |
| `Backup_user_data` | 是否备份 `/data/user/<user>/<package>` | `1` |
| `Backup_obb_data` | 是否备份 OBB / data 外部数据 | `1` |
| `backup_media` | App 备份后是否一并备份自定义文件夹 | `0` |
| `backup_messages` / `backup_calllogs` | 备份短信／MMS与通话纪录，依系统 Provider 能力处理 | `1` |
| `Background_apps_ignore` | 正在运行中的应用：`1` 忽略、`0` 尝试停止后备份 | `0` |
| `Custom_path` | 自定义备份路径，每行一个绝对路径 | 依需求 |
| `blacklist_mode` | 黑名单：`1` 完全忽略、`0` 仅备份安装包 | `0` |
| `blacklist` | 黑名单应用包名，每行一项；列表生成会忽略注解中的包名 | 空 |
| `whitelist` | 预装应用白名单，每行一项；不覆盖黑名单优先级 | 依需求 |
| `system` | 系统应用白名单 | 依需求 |
| `Compression_method` | App 数据使用 `zstd` 或 `tar`；一般 Media／自定义目录另走 tar 仅打包 | `zstd` |
| `Zstd_level` | 压缩等级 `1`～`22`；`20`～`22` 会激活 ultra | `6` |
| `Zstd_threads` | 一般压缩线程 `0`～`64`；`0` 自动使用可用内核 | 新建与缺少字段补齐均为 `0` |
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
| `remote_keep_local` | 非流式上传成功后：`1` 保留本地数据报、`0` 删除；不会让流式备份额外保存整包 | `0` |
| `remote_upload_per_app` | 每个 App 备份后立即上传，非流式模式下节省空间 | `0` |
| `log_max_size_mb` | `log/` 目录大小上限，留空或 `0` 关闭自动清理 | 新建设置留空；旧设置缺项补入 `1` |

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

旧 JSON 已有的 SSAID、权限、AppOps、电池策略会尽量恢复；安装来源纪录保留作诊断，APK 依现行 Play 优先策略安装。旧 JSON 本来没有的新字段则无法凭空补出。

> 注意：此兼容仅针对本地既有旧备份恢复。新版上传／远程下载 的远程同步流程采 `app_details_bundle.tar.zst` bundle-only，不再使用远程逐 App `app_details.json` 作为 metadata 主路径。

---

## AppState / Dex 功能

`classes.dex` 用于实现 Shell 难以稳定完成的系统操作。目前主要负责：

- AppState snapshot / restore / verify
- SSAID 备份与恢复辅助
- 运行时权限、AppOps、特殊访问、电池策略状态处理
- 安装来源诊断、目标用户的 Play 身分及安装条件查找
- 批量取得 App 名称、包名、版本、split 信息与安装后状态
- WebDAV 连接、相对路径检查与传输服务
- SMB 主机与 share 扫描辅助
- 通知批量更新
- 权限 / AppOps / 特殊访问中文语意输出
- 查找预设桌面、输入法、电话、短信、浏览器与助理
- 查找保存空间与媒体路径
- 内置设备型号数据库，release 内不再需要外置 `tools/Device_List`

Rust 原生工具负责应用列表、JSON、备份计划、统计、受保护的文件操作及每 App 安装 session 协调；Dex 负责 Android 状态、保存政策及相关传输能力。一般文件查找仍保留 GNU find，未全面改为 Rust。AppState／SSAID 的恢复与验证由 Dex 直接产生分类摘要，避免脚本靠消息措辞重新猜结果。

启动自检由 `tools/dex_check.sh` 运行，依实际能力检查兼容性，不只比较版本字符串。摘要会分开列出成功、警告、失败与内核失败；部分新流程使用 `SBRESULT` 统一结果格式。

**自检通过不等于完成一轮真实备份与恢复。** `partial` 可能表示有警告或核验不完整，请看原因；受厂商限制、数据不符与运行失败也不能视为同一种结果。

---

## 脚本更新方式

1. **本地 ZIP 更新**：将完整 release `.zip` 不解压，放到脚本目录或其上层目录，运行脚本时自动检测更新。
2. **Download 目录更新**：将完整 release `.zip` 放到 `/storage/emulated/0/Download/`，运行脚本时自动检测。
3. **QQ 下载目录更新**：从 QQ 下载的完整 release `.zip` 可直接放置后运行脚本更新。
4. **联网自动更新**：在 App「备份设置」打开「脚本自更新」后，启动时检查 GitHub release。

**先让备份／恢复正常结束并退出脚本，再更新；不要修改运行中的工具。** 手动差异更新包只适用其标示的完整基底，按包内说明整组替换；来源码包不是手机安装包。例如 v1100 → v1101 更新包需先有完整 v1100，不能直接套到更旧版本。

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

日常请在 App 的「运行日志」查看工作状态，可跟随最新或翻页回看；不需要打开终端追踪输出。背景同时会在 `log/` 保存兼容日志，例如：

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
- `install_session.log` / `install_method.log`：安装 session 与路径判定诊断

stderr 为 0KB 只代表该输出档没有记录，不代表所有检查通过。请一并看 `main.log` 的结果摘要、失败原因、备份预估／实际差异，以及 AppState／SSAID 验证结果。没有有效计划时，单看 `mismatch=0` 也不能判定核对通过。

一般模式会精简成功恢复的详细清单，speed_debug 仍会保留。旧 `diagnostic_mode=1` 已不适用；深入排查请依维护者指示使用对应诊断环境变量。实际文件名与输出位置以当轮提示为准。分享前请检查包名、路径及其他个人信息。

---

## 常见问题

<details>
<summary><b>Q1：批量备份 / 恢复大量提示失败？</b></summary>

请先查看当轮 speed_debug 的第一个失败原因及自检摘要。若提示工具 SHA-256 或能力不符，先结束正在运行的工作，再使用同一完整发行包修复工具；不要在备份途中删除 `/data/.speedbackup/tools/`。仍失败时请提交 debug 包。
</details>

<details>
<summary><b>Q2：微信 / QQ 能完美备份恢复吗？</b></summary>

无法保证。大型实时通信 App 可能有服务常驻、数据库锁、服务器校验或加密状态。建议同时使用你信任的官方或第三方方式额外备份重要数据。
</details>

<details>
<summary><b>Q3：为什么部分应用备份很久？</b></summary>

可能是 user data、user_de、OBB 或外部 data 很大，也可能包含保存、传输或守护收尾等待。确认不需要这些外部数据后，才在 App「备份设置」关闭「备份obb数据」（`Backup_obb_data=0`） 跳过外部 OBB / data 类大型数据。
</details>

<details>
<summary><b>Q4：脚本每次都是全量备份吗？</b></summary>

不是。脚本会比对版本号、数据大小、SSAID、权限、AppOps、AppState 与远程文件状态。无变化时会跳过；若全部选中 App 都无变化，本地与远程都可整批 fast-skip。这是依记录判断是否需要重新打包，不是区块增量或逐档哈希比对；内容改动但大小等条件相同时，不能保证一定辨识。
</details>

<details>
<summary><b>Q5：为什么脚本包含 classes.dex？</b></summary>

`classes.dex` 用于处理 Shell 难以稳定完成的 Android 系统能力，例如 AppState snapshot / restore / verify、SSAID、AppOps、WebDAV daemon、SMB 扫描、安装条件查找与通知更新。APK session 协调由 Rust 运行，不是改用 Java 安装。

感谢 [XayahSuSuSu](https://github.com/XayahSuSuSu) 的 [Android-DataBackup](https://github.com/XayahSuSuSu/Android-DataBackup) 提供 App 支持。
</details>

<details>
<summary><b>Q6：息屏后备份速度变慢？</b></summary>

这通常是 Android 内核或厂商 ROM 的 IO / CPU 节能策略。可在 App「备份设置」打开「亮屏伪装」（`setDisplayPowerMode=1`），或备份期间保持屏幕常亮。
</details>

<details>
<summary><b>Q7：如何单独备份 / 恢复 / 上传单一应用？</b></summary>

单一应用备份／恢复可在 App 清单只勾选该应用后继续。高级用户也可从备份文件夹内对应应用子目录运行独立入口：

- `backup.sh`：单独备份该 App
- `recover.sh`：单独恢复该 App
- `upload.sh`：单独上传该 App 到远程

注意：新版远程恢复 metadata 以根层 `app_details_bundle.tar.zst` 为准。若手动运行单 App `upload.sh`，建议再回主菜单运行「单独上传当前备份」，让脚本重新汇总并上传 metadata bundle。
</details>

<details>
<summary><b>Q8：WebDAV 上传显示 HTTP 423 Locked？</b></summary>

先查看服务端日志中的文件锁定原因，确认是否有其他用户端正在写入同一目标，再在 App 使用「测试远程连接」检查写入。请保留失败请求与 debug；不能只凭 HTTP 423 判定手机压缩或备份内容有错。
</details>

<details>
<summary><b>Q9：WebDAV 上传或列表显示 HTTP 404？</b></summary>

请检查 `webdav_url` 是否指向正确 WebDAV 端点，例如 `/dav/`、`/remote.php/webdav/` 或 rclone serve 的根路径。若是 `app_details_bundle.tar.zst` 不存在，远程下载会中止；备份或上传流程请先生成并同步 metadata bundle。
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
<summary><b>Q13：远程恢复提示缺少 app_details_bundle.tar.zst？</b></summary>

新版远程下载需要根层 `app_details_bundle.tar.zst`。请先使用新版完整备份，或在本地备份文件夹使用「单独上传当前备份」，让脚本汇总本地各 App 的 `app_details.json` 并上传 metadata bundle。
</details>

<details>
<summary><b>Q14：为什么 log 里有些 stderr 是 0KB？</b></summary>

`stderr.log`、`root_daemon_stderr.log`、`webdav_daemon_stderr.log` 为 0KB 通常是正常现象，代表没有错误输出。主流程请看 `main.log` 或 `log/log_yyyy-mm-dd_hh-mm.txt`。
</details>

---

## 目前核验范围

- 备份预估大小与实际打包大小分开核对，跳过、未知与失败项目分开处理；没有有效预扫计划的项目不能只靠数值相同判定通过。
- 恢复清单检查可发现缺档、类型、大小与链接等差异，不包含逐档内容哈希及完整 SELinux／ACL 验证。
- AppState／SSAID 核对通过后，仍需实际打开 App 确认数据与登录；系统、厂商及服务器限制不一定能由脚本还原。
- WebDAV 的串流耗时可能包含打包、压缩、网络、读取与守护收尾等待，小档显示的低速不能直接当成网络测速结果。
- 进程观察器与稳定等待不是原子性的「禁止所有新进程启动」保证。自订进程名称、ROM 政策及内核能力仍有限制。
- 备份封装未因这些安全检查而加密；HTTP 或 HTTPS 由远程设置决定。重要数据请另存独立备份。
- 性能数据及未采用方案见 [更新日志](CHANGELOG.md)，单机微基准不代表所有 ROM 或完整备份／恢复的加速比例。

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

## 鸣谢贡献

App 内可从「关于 → 鸣谢」查看头像与贡献说明；说明跟随繁简语言，名称保留原样。

| 贡献者 | 贡献内容 |
|--------|----------|
| [kmou424](https://github.com/kmou424)(臭批老k) | 提供部分验证函数思路 |
| skkk-10p | 提供早期 native static 支持 |
| 雨季少年 | 提供早期 Samba 构建与服务器支持，远程备份思路发起者 |
| h1jacker | 提供自动发现 WebDAV 方案，以及早期各种构建支持 |
| [雄氏老方](http://www.coolapk.com/u/665894)(屑老方) | 提供自动更新脚本方案 |
| [sakuradairong](https://github.com/sakuradairong)(雨季骚年/胖子老陈) | 添加 WebDAV / SMB 功能与测试 |
| [XayahSuSuSu](https://github.com/XayahSuSuSu) | 数据备份 App 作者，提供 SELinux context 与脚本早期 Dex 支持 |

`文档编辑：Petit-Abba, YuKongA`

---

<p align="center">
 <sub>GPL-3.0 Licensed · Made with ❤️ by <a href="https://github.com/YAWAsau">YAWAsau</a></sub>
</p>