# 常见问题与诊断

[返回首页](../README.md) · [使用指南](USER_GUIDE.md) · [设置参考](CONFIGURATION.md) · [常见问题](FAQ.md) · [架构说明](ARCHITECTURE.md)

## 日志与 debug

日常请在 App 的「运行日志」查看工作状态，可跟随最新或翻页回看；不需要打开终端追踪输出。背景同时会在 `log/` 保存兼容日志，例如：

```text
log/log_2026-07-25_21-40.txt
```

同时，完整诊断数据会打包到 speed_debug：

```text
/data/speed_debug/speed_debug_session_<工作阶段识别码>.tar
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

## 常见问题

### 为什么首页显示 SMB 2.0.2，而不是 3.1.1？

首页显示最近一次有效验证连接的协商结果。版本取决于客户端与服务器共同支持及允许的协定，并非固定显示最高设置值；SMB1 仍禁用。若没有明确协商回报，界面会标示未回报，脱机或设置变更后也不沿用旧版本。

### 为什么繁体的「脚本」变成「脚本」？

`s2twp` 包含台湾地区词汇转换，不只改字形。项目也保留少量指定用词，例如保存信息标签的繁体「硬盘」／简体「存储」。原始路径、识别码与不应翻译的数据保留原文。

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

## 目前核验范围

- 备份预估大小与实际打包大小分开核对，跳过、未知与失败项目分开处理；没有有效预扫计划的项目不能只靠数值相同判定通过。
- 恢复清单检查可发现缺档、类型、大小与链接等差异，不包含逐档内容哈希及完整 SELinux／ACL 验证。
- AppState／SSAID 核对通过后，仍需实际打开 App 确认数据与登录；系统、厂商及服务器限制不一定能由脚本还原。
- WebDAV 的串流耗时可能包含打包、压缩、网络、读取与守护收尾等待，小档显示的低速不能直接当成网络测速结果。
- 进程观察器与稳定等待不是原子性的「禁止所有新进程启动」保证。自订进程名称、ROM 政策及内核能力仍有限制。
- 备份封装未因这些安全检查而加密；HTTP 或 HTTPS 由远程设置决定。重要数据请另存独立备份。
- 性能数据及未采用方案见 [更新日志](../CHANGELOG.md)，单机微基准不代表所有 ROM 或完整备份／恢复的加速比例。
