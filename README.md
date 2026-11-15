# SpeedBackup

Android 应用与数据备份工具，提供原生 App 界面、本地备份及 SMB／WebDAV 远程备份。

<p align="center">
 <a href="https://deepwiki.com/YAWAsau/backup_script"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki" /></a>
 <a href="https://github.com/YAWAsau/backup_script/stargazers"><img src="https://img.shields.io/github/stars/YAWAsau/backup_script?label=stars&style=flat-square" /></a>
 <a href="https://github.com/YAWAsau/backup_script/releases"><img src="https://img.shields.io/github/downloads/YAWAsau/backup_script/total?style=flat-square" /></a>
 <a href="https://github.com/YAWAsau/backup_script/releases/latest"><img src="https://img.shields.io/github/v/release/YAWAsau/backup_script?label=release&style=flat-square" /></a>
 <a href="https://choosealicense.com/licenses/gpl-3.0"><img src="https://img.shields.io/github/license/YAWAsau/backup_script?label=License&style=flat-square" /></a>
 <a href="https://t.me/yawasau_script"><img src="https://img.shields.io/badge/Follow-Telegram-blue.svg?logo=telegram&style=flat-square" /></a>
</p>

<p align="center">
  <a href="https://github.com/YAWAsau/backup_script/releases/latest">下载最新版</a> ·
  <a href="docs/USER_GUIDE.md">使用指南</a> ·
  <a href="docs/FAQ.md">常见问题</a> ·
</p>

## 特色

- **应用与数据**：批量备份／恢复 APK、Split APK、应用数据、OBB、自订文件夹及 Wi-Fi 设置。
- **应用状态**：支持 SSAID、权限、AppOps 与电池策略等状态的备份与恢复。
- **本地与远程**：支持 SMB／WebDAV、自动搜索设备及串流备份／恢复，减少本机暂存空间需求。
- **连接状态**：已保存连接先在背景验证；首页显示验证连接实际协商的 SMB 版本，脱机后清除旧值。
- **跳过未变更项目**：依版本、大小与状态纪录判断是否需要重新备份。
- **双界面风格**：Material／Miuix、深浅色、壁纸与液态玻璃，支持繁体／简体中文，切换时同步转换地区用词。
- **背景工作**：关闭画面后继续运行，重新启动可接回进度；提供日志、状态通知与除错包。


本仓库为**简体中文修正版**，对原脚本中**部分专有名词**进行了**修正**，脚本执行逻辑无任何修改，具体使用哪个版本请自行决定，**原版**可前往这里下载：
> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。

简体中文版使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。

## 开始使用

**需求：Android 9 以上、arm64 设备及 Root 权限（Magisk／KernelSU）。**

1. 从 [Releases](https://github.com/YAWAsau/backup_script/releases/latest) 下载完整手机运行包并解压。
2. 使用已取得 Root 权限的 MT 管理器或终端运行 `start.sh`，依提示进入 SpeedBackup App。
3. 在「设置 → 备份设置」选择备份位置与项目，保存后到功能页开始备份。

本地恢复请运行备份目录中的 `start.sh`；远程恢复可从 App 选择先下载或串流恢复。完整步骤见 [使用指南](docs/USER_GUIDE.md)。

更新前请让工作正常结束并退出脚本，使用同一发行包的完整工具。GitHub 自动产生的 **Source code** 压缩档是源代码，不能当作完整手机运行包。

## 文档

| 想了解的内容 | 文档 |
|---|---|
| 备份、恢复、远程连接、外观与更新 | [使用指南](docs/USER_GUIDE.md) |
| 高级设置字段 | [配置参考](docs/CONFIGURATION.md) |
| 常见问题、日志与核验范围 | [问题排查](docs/FAQ.md) |
| 后端分工、数据格式与兼容性 | [架构说明](docs/ARCHITECTURE.md) |

## 问题回报

请附上版本、重现步骤、截屏及 App 导出的 `speed_debug` 除错包。

- [GitHub Issues](https://github.com/YAWAsau/backup_script/issues)
- [Telegram 频道](https://t.me/yawasau_script)
- QQ 群：`976613477`
- 酷安：[@落叶凄凉TEL](http://www.coolapk.com/u/2277637)

## 鸣谢

感谢所有提供代码、想法、测试与文档协助的贡献者。

<details>
<summary>查看贡献者与贡献内容</summary>

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

</details>

第三方组件及授权见 [开源授权说明](docs/OPEN_SOURCE_LICENSES.md)。

## 支持与授权

如果 SpeedBackup 对你有帮助，欢迎 [赞助支持](https://paypal.me/YAWAsau?country.x=TW&locale.x=zh_TW)。

本项目采用 [GNU GPL v3.0](LICENSE)，第三方组件依各自授权条款提供。