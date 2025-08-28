# Backup_script 数据备份脚本（简体中文版）
[![Stars](https://img.shields.io/github/stars/YAWAsau/backup_script?label=stars)](https://github.com/YAWAsau)
[![Download](https://img.shields.io/github/downloads/YAWAsau/backup_script/total)](https://github.com/YAWAsau/backup_script/releases)
[![Release](https://img.shields.io/github/v/release/YAWAsau/backup_script?label=release)](https://github.com/YAWAsau/backup_script/releases/latest)
[![License](https://img.shields.io/github/license/YAWAsau/backup_script?label=License)](https://choosealicense.com/licenses/gpl-3.0)

## 概述

创作该脚本是为了使用户能够更加完整地**备份/恢复**应用数据，使用设备必须符合以下条件：`Android 8+`+`arm64`。

原版脚本现在已经支持根据执行环境自动转换为简体中文了，本仓库的存在意义已经不大了，发布的包和原版自动转换为简体后基本无差别，**原版**可前往这里下载：
> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。

PS. 简体版本使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。

## 优势

- 数据完整：在更换系统之后，原有的数据全部保留，无需重新登陆或者下载额外数据包。
- 易操作：简单几步即可备份应用完整数据！
- 限制少：不限制机型，可跨安卓版本。
- 功能强：可备份恢复`split apk`。
- 算法多：目前支持的压缩算法有 `tar(默认)` `lz4` `zstd`。
- 速度快：即使使用`zstd`压缩算法速率依旧快速（对比钛备份 swift）。

## 如何使用
`请认真阅读以下说明，以减少不必要的问题`

##### 推荐工具：[`MT管理器`](https://www.coolapk.com/apk/bin.mt.plus)，若使用`Termux`，则请勿使用`tsu`。

#### !!!以下操作皆须ROOT!!! ####

1. 首先将下载到的`数据备份脚本.zip`解压到任意目录后，可以看到以下几个文件与一个 目录：`生成应用列表.sh` `backup_settings.conf` `备份应用.sh` `tools` `备份自定义资料夹.sh` `终止脚本.sh` `警告! 不论备份或是恢复都必须保证tools的存在与完整性 否则脚本失效或是二进制调用失败`。

2. 然后执行`生成应用列表.sh`脚本，并等待脚本输出结束[[示意图]](https://raw.githubusercontent.com/YAWAsau/backup_script/0a08a49865fd9ec36d4fedd3e76ec68f841ff1d7/DCIM/Screenshot_20211230-185717_MT%E7%AE%A1%E7%90%86%E5%99%A8-01.jpeg)，再等待提示结束 [[示意图]](https://raw.githubusercontent.com/YAWAsau/backup_script/master/DCIM/Screenshot_20211230-190000_MT%E7%AE%A1%E7%90%86%E5%99%A8-01.jpeg) [[示意图]](https://raw.githubusercontent.com/YAWAsau/backup_script/master/DCIM/Screenshot_20211230-185941_MT%E7%AE%A1%E7%90%86%E5%99%A8-01.jpeg)，此时会在当前目录生成一个`appList.txt`，这就是你当前安装的所有第三方应用。

3. 现在打开生成的`appList.txt`，根据里面的提示操作后保存[[示意图]](https://github.com/Petit-Abba/backup_script_zh-CN//raw/main/File/Picture/3.png)，这样你就设置好了需要备份的软件。

4. 最后找到`backup_settings.conf`打开[[示意图]](https://raw.githubusercontent.com/YAWAsau/backup_script/master/DCIM/Screenshot_20211230-191248_MT%E7%AE%A1%E7%90%86%E5%99%A8-01.jpeg)，再打开`备份应用.sh`，等候备份结束。完成后会在当前目录生成一个以`Backup_压缩算法名`命名的资料夹，里面就是你的软件备份。把这个资料夹整个保持到其他位置，刷完机后复制回手机，直接在资料夹里找到`恢复备份.sh`即可恢复备份的所有数据，同样道理，里面也有个`appList.txt`，使用方法跟第3步骤一样，不需要还原的删除即可。

##### 附加说明：如何恢复 以下是关于恢复资料夹内的文件说明?
```
1. 找到恢复资料夹内的appList.txt打开 编辑列表 保存退出

2. 找到恢复备份.sh 给予root后等待脚本结束即可

3. 重新生成应用列表.sh可用于刷新appList.txt内的列表 使用时机为当你删除列表内的任何应用备份时,抑或者是恢复备份.sh提示列表错误时

4. 终止脚本.sh用于突然想要终止脚本或是意外操场时使用 同理备份资料夹也有一个，因为脚本无须后台特性不能使用常规手段终结，故此另外写了一个脚本终止
```
# 关于如何更新脚本？
- 目前有三种更新方法，有下列方式
- 1.手动将下载的备份脚本zip不解压缩直接放到脚本任意目录(不包括tools目录内)的任意地方执行任何脚本即可更新，脚本将提示
- 2.此备份的任何脚本在执行时均会联网检测脚本版本，当更新时会自己提示与下载，根据脚本提示操作的即可
- 3.将下载的压缩包不解压缩直接放在/storage/emulated/0/Download脚本自动检测更新，并按照提示操作即可

## 关于反馈
- 如果使用过程中出现问题，请携带截图并详细说明问题，建立 [issues](https://github.com/YAWAsau/backup_script/issues)。
- 酷安 @[落叶凄凉TEL](http://www.coolapk.com/u/2277637)
- QQ组 976613477
- TG https://t.me/backup_script

## 常见问题
```
Q1：批量备份大量提示失败怎么办？
A1：退出脚本，删除/data/backup_tools，再备份一次

Q2：批量恢复大量提示失败怎么办？
A2：退出脚本，按照上面同样操作。 如果还是错误，请建立issues，我帮你排除错误

Q3：微信/QQ 能不能完美备份&恢复数据？
A3：不能保证，有的人说不能有的人说能，所以备份会有提示。 建议用你信赖的备份软件针对微信/QQ再备份一次，以防丢失重要数据

Q4：为什么部分应用备份很久？ 例如王者荣耀、PUBG、原神、微信、QQ。
A4：因为连同软件数据包都给你备份了，例如原神数据包9GB+，当然久到裂开了，恢复也是同理，还要解压缩数据包
```

## 铭谢贡献
- 臭批老k([kmou424](https://github.com/kmou424))：提供部分与验证函数思路
- 屑老方([雄氏老方](http://www.coolapk.com/u/665894))：提供自动更新脚本方案
- 依心所言&情非得已c：提供appinfo替代aapt作为更高效的dump包名
- 胖子老陈(雨季骚年)
- XayahSuSuSu([XayahSuSuSu](https://github.com/XayahSuSuSu))：提供App支持
  `文档编辑：Petit-Abba, YuKongA`
