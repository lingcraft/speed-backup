# 配置参考

[返回首页](../README.md) · [使用指南](USER_GUIDE.md) · [设置参考](CONFIGURATION.md) · [常见问题](FAQ.md) · [架构说明](ARCHITECTURE.md)

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
