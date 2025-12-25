# Backup_script 数据备份脚本【简体中文版】
[![Stars](https://img.shields.io/github/stars/YAWAsau/backup_script?label=stars)](https://github.com/YAWAsau)
[![Download](https://img.shields.io/github/downloads/YAWAsau/backup_script/total)](https://github.com/YAWAsau/backup_script/releases)
[![Release](https://img.shields.io/github/v/release/YAWAsau/backup_script?label=release)](https://github.com/YAWAsau/backup_script/releases/latest)
[![License](https://img.shields.io/github/license/YAWAsau/backup_script?label=License)](https://choosealicense.com/licenses/gpl-3.0)
[![Channel](https://img.shields.io/badge/Follow-Telegram-blue.svg?logo=telegram)](https://t.me/yawasau_script)

## 概述

创作该脚本是为了使用户能够更加完整地**备份/恢复**应用数据，
支持设备必须符合以下条件：`Android 8+`+`arm64`。

本仓库为简体中文修正版，对原脚本中部分繁体直接转换为简体的名词进行了修正，对于脚本的执行逻辑无任何修改，具体使用哪个版本请自行决定，**原版**可前往这里下载：
> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。

简体中文版使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。

## 优势

- 数据完整：在更换系统之后，原有的数据全部保留，无需重新登陆或者下载额外数据包。
- 支持备份SSAID 可完美备份LINE
- 支持备份应用权限 可备份运行时权限与ops权限
- 易操作：简单几步即可备份应用完整数据！
- 限制少：不限制机型，可跨安卓版本。
- 功能强：可备份恢复`split apk`。
- 算法多：目前支持的压缩算法有 `tar(默认)`
- `zstd`。
- 速度快：即使使用`zstd`压缩算法速率依旧快速（对比钛备份 swift backup）。
- 脚本自带tools完整性效验与压缩包效验
## 如何使用
`请认真阅读以下说明，以减少不必要的问题`

##### 推荐工具：[`MT管理器`](https://www.coolapk.com/apk/bin.mt.plus)，若使用`Termux`，则请勿使用`tsu`。

#### !!!以下操作皆须ROOT!!! ####

1. 首先将下载到的脚本解压到任意目录后，可以看到以下目录结构 警告! 不论备份或是恢复都必须保证tools的存在与完整性 否则脚本失效或是二进制调用失败。

`这是脚本结构与说明`
```
speed-backup.zip
│
├── tools
│       ├── Device_List
│       ├── bc
│       ├── busybox
│       ├── classes.dex
│       ├── cmd             
│       ├── jq                
│       ├── find              
│       ├── keycheck         
│       ├── soc.json
│       ├── tar
│       ├── tools.sh
│       ├── zip
│       └── zstd
├── backup_settings.conf         <--- 脚本默认行为设置
└── start.sh          <--- 运行脚本
```

2. 然后运行`start.sh`脚本音量键选择生成应用列表，等待脚本输出提示结束，此时会在当前目录生成一个`appList.txt`，这就是你当前安装的所有第三方应用(脚本会屏蔽预装应用，可于backup_settings.conf设置需要备份包名)。

3. 现在打开生成的`appList.txt`，根据里面的提示操作后保存，这样你就设置好了需要备份的软件。

4. 最后找到`backup_settings.conf`打开后根据提示设置保存，再打开`start.sh`，音量键选择备份应用，备份结束完成后会在当前目录生成一个以`Backup_压缩算法名`命名的文件夹，里面就是你的软件备份。把这个文件夹整个保持到其他位置，刷完机后拷贝回手机，直接运行`Backup_压缩算法名/start.sh`即可恢复备份的所有数据，同样道理，里面也有个`appList.txt`，使用方法跟第3步骤一样，不需要还原的删除即可，另外进去备份好的文件夹找到单独应用文件夹有个 backup.sh and recover.sh可以单独备份与恢复脚本。

5. 脚本运行过程中请留意红色字眼提示有无任何错误，并且使用恢复脚本时留意恢复结束后是否提示应用存在ssaid，假设提示存在ssaid请在恢复后立刻重启已便应用ssaid,假设恢复ssaid后立刻打开应用会导致ssaid应用失败，因为Android会产生一个新的saaid，如此会导致应用卡白屏或是提示需要登录，ssaid是判断应用是否换过环境与设备的判断之一，保持一致可以减少诸如提示异地登录或是需要重新登录验证的方法。


 ##### 附加说明：如何恢复 以下是关于恢复文件夹内的文件说明?

1. 找到恢复文件夹内的appList.txt打开 编辑列表 保存退出

2. 找到start.sh 给予root音量键选择恢复备份后等待脚本结束即可

3. start.sh的重新生成应用列表功能可用于刷新appList.txt内的列表 使用时机为当你删除列表内的任何应用备份时,抑或者是恢复备份提示列表错误时

4. start.sh的终止脚本功能用于突然想要终止脚本或是意外操作时使用 同理备份也有一个，因为脚本无须后台特性不能使用常规手段终结，故此另外写了一个终止


# 关于如何更新脚本？
- 目前有三种更新方法，有下列方式
- 1.手动将下载的备份脚本zip不解压缩直接放到脚本任意目录(不包括tools目录内)的任意地方运行任何脚本即可更新，脚本将提示
- 2.此备份的任何脚本在运行时均会联网检测脚本版本，当更新时会自己提示与下载，根据脚本提示操作的即可(conf update=1时生效),脚本联网仅作为检查更新用途，无任何非法操作亦或是下发格机
- 3.将下载的压缩包不解压缩直接放在/storage/emulated/0/Download脚本自动检测更新，并按照提示操作即可
- 4.在QQ群内下载的脚本不解压缩脚本会自己检测更新

## 关于反馈
- 如果使用过程中出现问题，请携带截屏并详细说明问题，创建 [issues](https://github.com/YAWAsau/backup_script/issues)。
- 酷安 @[落叶凄凉TEL](http://www.coolapk.com/u/2277637)
- QQ群 976613477 很少上 尽量来TG
- TG https://t.me/yawasau_script

## 答疑
- 一个shell脚本内为什么有dex?
- dex用来实现脚本难以实现的目的，目前saaid备份恢复，备份恢复运行时权限与ops权限，下载与访问GitHub api来检查脚本更新，列出用户应用名称与包名，繁体转简体均为dex的功能，感谢[Android-DataBackup](https://github.com/XayahSuSuSu/Android-DataBackup) by [XayahSuSuSu](https://github.com/XayahSuSuSu)

## 常见问题

Q1：批量备份大量提示失败怎么办？
A1：退出脚本，删除/data/backup_tools，再备份一次

Q2：批量恢复大量提示失败怎么办？
A2：退出脚本，按照上面同样操作。 如果还是错误，请创建issues，我帮你排除错误

Q3：微信/QQ 能不能完美备份&恢复数据？
A3：不能保证，有的人说不能有的人说能，所以备份会有提示。 建议用你信赖的备份软件针对微信/QQ再备份一次，以防丢失重要数据

Q4：为什么部分应用备份很久？ 例如王者荣耀、PUBG、原神、微信、QQ。
A4：因为连同软件数据包都给你备份了，例如原神数据包9GB+，当然久到裂开了，恢复也是同理，还要解压缩数据包

Q5:脚本每次备份都是全新备份吗？
A5;脚本备份时会比对上次备份时的备份SIZE大小 如果有差异就备份,反之忽略备份节省时间

备份脚本耗费了我大量时间与精力 如果你觉得好用，可以捐赠XD
.(https://paypal.me/YAWAsau?country.x=TW&locale.x=zh_TW))


## 感谢贡献者
- 臭批老k([kmou424](https://github.com/kmou424))：提供部分与验证函数思路
- 屑老方([雄氏老方](http://www.coolapk.com/u/665894))：提供自动更新脚本方案
- 胖子老陈(雨季骚年)
- XayahSuSuSu([XayahSuSuSu](https://github.com/XayahSuSuSu))：提供App支持,dex支持

`文件编辑：Petit-Abba, YuKongA`
