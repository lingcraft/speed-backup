# 开源许可清单

「功能 → 开源许可」使用 Rust 内嵌的 `rust/src/open_source_licenses.json`。受保护的 `/api/licenses` 提供数据；APK 使用 Compose 原生卡片显示，外部浏览器打开项目网址。一般浏览器使用相同数据。

v1033 共 156 笔：134 个实际解析的 Maven 模块，以及 22 笔来源引用、设计参照与原生工具。涵盖 APK/WebUI、Dex 的直接及间接依赖，编译／注解处理项目另外标示。Rust 目前没有外部 Cargo 套件，标准函数库单独列出。设计参照不代表将对方完整程序库打包。

原有 cmd/keycheck 未附原作者与授权数据，界面明确标示「未记录」，并连到本项目的分发来源。部分原生工具未保留版本信息，不能将这些条目视为已补齐上游来源。现有授权原文与 NOTICE 仍保留于原有路径；此清单不取代它们。

## 更新依赖

1. 使用各项目原有 JDK／Android SDK，分别在 `webview` 与 `dex` 运行 Gradle：`gradlew -I <绝对路径>/ci/export_licenses.gradle exportLicenseCoordinates -PcatalogOut=<绝对输出路径>`。Dex 在非 ASCII 路径仍须 `-Pandroid.overridePathCheck=true`。
2. 运行 `python ci/generate_licenses.py --import-metadata <webview输出.json> <dex输出.json>`，从实际解析模块与 POM 产生 `third_party/licenses/resolved.json`。导出暂存含本机 POM 路径，不加入发行包。
3. 检查添加项目的作者、版本、授权与 HTTPS 项目网址；源代码引用与原生工具更新 `third_party/licenses/references.json`，再运行 `python ci/generate_licenses.py`。
4. 运行 `python ci/generate_licenses.py --check`、完整建置与仓库检查。依赖声明的 SHA-256 若改变，建置会要求重新导出，避免清单悄悄过期。

来源快照与产生器随干净源代码包交付。运行时不需连接下载许可清单。
