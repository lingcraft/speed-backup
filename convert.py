from github import Github, Auth, UnknownObjectException
from opencc import OpenCC
from hashlib import sha256
from os import environ, path, remove, walk
from re import sub
from shutil import make_archive, rmtree, unpack_archive

auth = Auth.Token(environ["GITHUB_TOKEN"])
git = Github(auth=auth)
proj_name = "speed-backup"
my_repo = git.get_repo(f"lingcraft/{proj_name}")
src_repo = git.get_repo("YAWAsau/backup_script")
converter = OpenCC("tw2sp")
trans_dict = {
    "script": {  # 脚本修正
        "shell_language=\"zh-TW\"": "shell_language=\"zh-CN\"",
        "YAWAsau/backup_script": f"lingcraft/{proj_name}",
        "安装档": "安装包",
        "遗失": "丢失",
        "重新开机套用": "重启生效",
        "过世": "寄",
        "lock 档": "lock 文件",
        "文档": "文件",
        "单档": "单文件",
        "压缩档": "压缩文件",
        "损毁": "损坏",
        "意外断开": "连接断开",
        "尽速": "立即",
        "提升": "升级",
        "画面回报": "并反馈给",
        "杀死": "关闭",
        "结束自身": "关闭自己",
        "echoRgb \"脚本路径:$MODDIR": (
            "if [[ $SCRIPT_LANG = CN ]]; then\n"
            "    _l10n=\"$(printf '%s' \"$Device_name\" | _dex_exec_unfiltered com.xayah.dex.CCUtil t2s)\"\n"
            "    [[ -n $_l10n ]] && Device_name=\"$_l10n\"\n"
            "    _l10n=\"$(printf '%s' \"$DEVICE_NAME\" | _dex_exec_unfiltered com.xayah.dex.CCUtil t2s)\"\n"
            "    [[ -n $_l10n ]] && DEVICE_NAME=\"$_l10n\"\n"
            "    unset _l10n\n"
            "fi\n"
            "echoRgb \"脚本路径:$MODDIR"
        ),
        "IFS= read -r _GOOGLE_WELCOME_TEXT < \"$_out\" || true": (
            "IFS= read -r _GOOGLE_WELCOME_TEXT < \"$_out\" || true\n"
            "            if [[ $SCRIPT_LANG = CN && -n $_GOOGLE_WELCOME_TEXT ]]; then\n"
            "                _l10n=\"$(printf '%s' \"$_GOOGLE_WELCOME_TEXT\" | ts)\"\n"
            "                [[ -n $_l10n ]] && _GOOGLE_WELCOME_TEXT=\"$_l10n\"\n"
            "                unset _l10n\n"
            "            fi"
        ),
    },
    "readme": {  # 自述修正
        "backup_script.zip": f"{proj_name}.zip",
        "数据备份脚本": "数据备份脚本【简体中文版】",
        "铭谢贡献": "感谢贡献者",
        "安桌": "安卓",
        "QQ组": "QQ群",
        "套用": "应用",
        "调试": "除错",
        "文档说明": "文件说明",
        "设置档": "配置",
        "透过": "通过"
    }
}
suffixes = (".sh", ".conf", "_List")
version, description, readme = "", "", ""


def main():
    if get_latest_release():
        simplify()
        upload()
        update_readme()


def get_latest_release():
    global version, description
    release = src_repo.get_latest_release()
    if len(release.tag_name):
        asset = release.get_assets()[0]
        asset.download_asset(asset.name, 8192)
        unpack_archive(asset.name, proj_name)
        remove(asset.name)
        if path.isdir(proj_name):
            version, description = release.tag_name, convert(release.body)
            return True
    return False


def convert(content, dict_type="script"):
    content = converter.convert(content)
    for key, value in trans_dict.get(dict_type).items():
        content = content.replace(key, value)
    return content


def simplify():
    for file_path, _, file_names in walk(proj_name):
        for file_name in (file_name for file_name in file_names if file_name.endswith(suffixes)):
            file = path.join(file_path, file_name)
            with open(file, "r", encoding="utf-8") as f:
                content = convert(f.read())
            remove(file)
            with open(convert(file), "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
    update_hash()


def update_hash():
    file = path.join(proj_name, "tools", "tools.sh")
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    def refresh(match):
        name = match.group(1)
        tool = path.join(proj_name, "tools", name)
        if path.isfile(tool):
            return f"{name} {sha256(open(tool, "rb").read()).hexdigest()}"
        return match.group(0)

    with open(file, "w", encoding="utf-8", newline="\n") as f:
        f.write(sub(r"(?m)^(\S+) [0-9a-f]{64}$", refresh, content))


def upload():
    make_archive(proj_name, "zip", proj_name)
    rmtree(proj_name, True)
    try:
        release = my_repo.get_release(version)
    except UnknownObjectException:
        release = my_repo.create_git_release(version, version, description, False, False, False)
    assets = release.get_assets()
    name = f"{proj_name}{version}.zip"
    if assets.totalCount and assets[0].size == path.getsize(f"{proj_name}.zip"):
        return
    for asset in assets:
        asset.delete_asset()
    release.upload_asset(f"{proj_name}.zip", name, "application/zip", name)


def update_readme():
    global readme
    readme = convert(src_repo.get_readme().decoded_content.decode(), "readme")
    readme_lines = readme.splitlines()
    start_idx, insert_idx = None, None
    for index, line in enumerate(readme_lines):
        if "概述" in line:
            start_idx = index
            break
    if start_idx is not None:
        for index, line in enumerate(readme_lines[start_idx + 1:], start=start_idx + 1):
            if "##" in line:
                insert_idx = index
                if "---" in readme_lines[index - 2]:
                    insert_idx -= 2
                break
        if insert_idx is None:
            return
    if insert_idx is not None:
        content = [
            "本仓库为**简体中文修正版**，对原脚本中**部分专有名词**进行了**修正**，脚本执行逻辑无任何修改，具体使用哪个版本请自行决定，**原版**可前往这里下载：",
            "> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。",
            "",
            "简体中文版使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。",
            ""
        ]
        readme_lines[insert_idx:insert_idx] = content
    readme = "\n".join(readme_lines)
    file = my_repo.get_readme()
    old_readme = file.decoded_content.decode()
    if readme != old_readme:
        my_repo.update_file(path=file.path, message="更新自述", content=readme, sha=file.sha)


if __name__ == "__main__":
    main()
