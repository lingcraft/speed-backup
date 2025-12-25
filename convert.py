import github, os, shutil, opencc

auth = github.Auth.Token(os.getenv("GITHUB_TOKEN"))
git = github.Github(auth=auth)
proj_name = "speed-backup"
my_repo = git.get_repo(f"lingcraft/{proj_name}")
src_repo = git.get_repo("YAWAsau/backup_script")
converter = opencc.OpenCC("tw2sp")
trans_dict = {
    "script": {  # 脚本修正
        "shell_language=\"zh-TW\"": "shell_language=\"zh-CN\"",
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
        "结束自身": "关闭自己"
    },
    "readme": {  # 自述修正
        "backup_script.zip": "speed-backup.zip",
        "数据备份脚本": "数据备份脚本【简体中文版】",
        "铭谢贡献": "感谢贡献者",
        "安桌": "安卓",
        "QQ组": "QQ群",
        "套用": "应用",
        "调试": "除错",
        "文档": "文件"
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
        shutil.unpack_archive(asset.name, proj_name)
        if os.path.isdir(proj_name):
            version, description = release.tag_name, convert(release.body)
            return True
    return False


def convert(content, dict_type="script"):
    content = converter.convert(content)
    for key, value in trans_dict.get(dict_type).items():
        content = content.replace(key, value)
    return content


def simplify():
    for path, dir_names, file_names in os.walk(proj_name):
        for file_name in (file_name for file_name in file_names if file_name.endswith(suffixes)):
            file = os.path.join(path, file_name)
            with open(file, "r", encoding="utf-8") as f:
                content = convert(f.read())
            os.remove(file)
            with open(convert(file), "w", encoding="utf-8", newline="\n") as f:
                f.write(content)


def upload():
    shutil.make_archive(proj_name, "zip", proj_name)
    release = next((release for release in my_repo.get_releases() if release.tag_name == version), None)
    if release is None:
        release = my_repo.create_git_release(version, version, description, False, False, False)
    else:
        assets = release.get_assets()
        if assets.totalCount > 0:
            asset = assets[0]
            asset.download_asset(asset.name, 8192)
            if os.path.getsize(f"{proj_name}.zip") != os.path.getsize(asset.name):
                asset.delete_asset()
            else:
                return
    release.upload_asset(f"{proj_name}.zip", f"{proj_name}{version}.zip", "application/zip", f"{proj_name}{version}.zip")


def update_readme():
    global readme
    readme = convert(src_repo.get_readme().decoded_content.decode(), "readme")
    readme_lines = readme.splitlines()
    start, end = 0, 0
    for index, line in enumerate(readme_lines):
        if "概述" in line:
            start = index + 5
        elif "优势" in line:
            end = index - 1
    readme = readme.replace("\n".join(readme_lines[start:end]), (
        "本仓库为**简体中文修正版**，对原脚本中部分繁体直接转换为简体的名词进行了修正，脚本执行逻辑无任何修改，具体使用哪个版本请自行决定，**原版**可前往这里下载：\n"
        "> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。\n\n"
        "简体中文版使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。"
    ))
    file = my_repo.get_readme()
    old_readme = file.decoded_content.decode()
    if readme != old_readme:
        my_repo.update_file(path=file.path, message="更新自述", content=readme, sha=file.sha)


if __name__ == "__main__":
    main()
