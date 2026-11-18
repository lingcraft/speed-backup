# 架构与数据格式

[返回首页](../README.md) · [使用指南](USER_GUIDE.md) · [设置参考](CONFIGURATION.md) · [常见问题](FAQ.md) · [架构说明](ARCHITECTURE.md)

## 界面与脚本语言

切换繁体／简体后会保存语言设置，闲置时自动重新加载脚本并回到设置页；工作运行中收到语言切换时，会等工作安全收尾后再加载，不会重跑工作。既有日志维持原文。

繁简转换由 Dex CLI 单次启动、串流处理，依固定 OpenCC `s2twp`／`tw2sp` 设置运行范式、词组切分与有序转换，并共用至 APK 界面与 Dex 通知；数据版本见 `third_party/opencc-phrases/upstream.json`。改善「头发／发现」「干净／饼干」「皇后／后来」等字形选择，并保留项目用词。这是词组与地区用词转换，不是理解整句的翻译模型；Java 实作依固定设置运行，未嵌入 OpenCC 原生函数库。

正式脚本切回繁体时，另以该版本生成的完整行对照表还原已知差异；v1117 已在备用机验证 11 次往返 SHA-256 相同。用户自行修改或其他版本未收录的行不保证无损，一般文字与 conf 也不应用脚本还原规则。

切换语言及更新时，繁简转换会略过 `.conf` 文件，保留中文路径、帐密及多行设置值。设置注解由该备份／恢复入口下次启动时，使用目标语言的模板重新产生。

建置入口会自动生成词组索引与脚本还原表，CI 检查生成结果是否过期；词库在每个转换进程内只加载一次，不需外部词库或 JNI。

## 后端职责

Rust 负责配置的字面值解析、旧字段迁移与原子保存、远程地址追踪与帐密重填协调，以及诊断 tar 的锁定和原子更新。Dex 负责 Android 通知的文字、进度校正、节流与通知分类。Shell 保留备份／恢复流程、传输介接与设置模板；APK 保留原本界面。既有 conf、帐密重试／返回、地址记忆及单一诊断包的操作方式不变。

## 远程帐密与诊断

WebDAV 回传 401 或 SMB 明确认证拒绝时，前台操作会打开帐号、密码重填页。按「保存并重试」写回对应 conf，再重试连接预检；按「返回」停止本次操作。权限、路径与网络错误分开处理，不会自动重播上传或删除。背景模式需回到设置修正帐密。

同一工作服务阶段共用一份 `speed_debug_session_*.tar`，包内使用单一根目录及连续日志，不再为每次操作保留独立 run 子目录。快照与重试避免重复并入，JSON 保留最新有效内容及历史索引。关闭 APK 后接回仍属同一阶段；结束服务后重新启动才创建新包。每次安全收尾原子更新归档，失败保留原归档与待合并日志。

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

## APK 安装策略与恢复安全

- 目标 Android 用户的 Play 商店存在、激活且身分可确认时，优先使用 Play 安装者身分，不依 JSON 原始 installer 分流。数据目录或静默安装权限不足时不切换 Play UID；没有可用 Play 身分则使用普通 PM 安装。
- Play 混合 session 由每 App 一次的 Rust 协调器运行：以 Play UID 创建／提交，root 写入 APK。系统 PM 仍有子进程成本；不是 Java 安装器，也不是整批常驻安装 worker。
- 不再需要 `!play`；旧恢复清单前缀只作兼容性处理。JSON 安装来源字段仍可用于诊断，不是本次选择路径的依据。此功能不保证 `packageSource=STORE`、Play 授权、免登录或完整性认证。
- 保留路径、owner、UID/GID、文件描述符、逾时与 commit guard 检查。提交结果不明会回报状态 75，封锁本轮同用户／套件重试及其数据／AppState 恢复；只有明确失败才可依既有政策回退。重启脚本前先确认前次 session 结果。
- 提交期间可能暂时禁用 Android BackupManager 的全域自动还原，再依日志恢复；同一窗口内其他来源的安装也可能受影响，并非单一 App 隔离开关。
- 内部数据依目前套件 UID／seInfo 修复 ownership 与 SELinux；外部 data／obb 另走 Android 保存政策。终端宿主与无法安全停止的 App 仍受保护；从 Termux 自身运行时不恢复其宿主数据。
- 直接串流恢复会改动目标数据，没有整批回滚；失败可能已有部分内容写入。请保留独立备份，勿把「来源预检通过」当成恢复一定成功。

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
