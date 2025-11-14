import os, requests
from requests import HTTPError
from github import Github, Auth
from shutil import make_archive, unpack_archive
from zhconv import convert

auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
git = Github(auth=auth)
proj_name = "speed-backup"
my_repo = git.get_repo(f"lingcraft/{proj_name}")
src_repo = git.get_repo("YAWAsau/backup_script")
trans_dict = {
    # 脚本替换内容
    "shell_language=\"zh-TW\"": "shell_language=\"zh-CN\"",
    "萤幕": "屏幕",
    "备分": "备份",
    "使用者": "用户",
    "安装档": "安装包",
    "遗失": "丢失",
    # readme.md 替换内容
    "数据备份脚本": "数据备份脚本【简体中文版】",
    "安桌": "安卓",
    "支援": "支持",
    "backup_script.zip": "speed-backup.zip",
    "QQ组": "QQ群",
    "铭谢贡献": "感谢贡献者"
}
suffixes = (".sh", ".conf", "_List")
version, description, readme = "", "", ""


def main():
    get_latest_release()
    if version:
        simplify()
        upload()
        update_readme()


def get_latest_release():
    global version, description
    release = src_repo.get_latest_release()
    if len(release.tag_name):
        for asset in release.assets:
            if download(asset.browser_download_url, asset.name):
                unpack_archive(asset.name, proj_name)
        version, description = release.tag_name, convert(release.body, "zh-cn")


def download(url, name):
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(name, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
    except HTTPError:
        return False
    else:
        return True


def correct(content):
    for key, value in trans_dict.items():
        content = content.replace(key, value)
    return content


def simplify():
    for path, dir_names, file_names in os.walk(proj_name):
        for file_name in (file_name for file_name in file_names if file_name.endswith(suffixes)):
            file = os.path.join(path, file_name)
            with open(file, "r", encoding="utf-8") as f:
                content = correct(convert(f.read(), "zh-cn"))
            os.remove(file)
            with open(convert(file, "zh-cn"), "w", encoding="utf-8", newline="\n") as f:
                f.write(content)


def upload():
    make_archive(proj_name, "zip", proj_name)
    release = next((release for release in my_repo.get_releases() if release.tag_name == version), None)
    if release is None:
        release = my_repo.create_git_release(version, version, description, False, False, False)
    else:
        for asset in release.get_assets():
            if download(asset.browser_download_url, asset.name) and os.path.getsize(f"{proj_name}.zip") != os.path.getsize(asset.name):
                asset.delete_asset()
            else:
                return
    release.upload_asset(f"{proj_name}.zip", f"{proj_name}{version}.zip", "application/zip", f"{proj_name}{version}.zip")


def update_readme():
    global readme
    readme = correct(convert(src_repo.get_readme().decoded_content.decode(), "zh-cn"))
    readme_lines = readme.splitlines()
    start, end = 0, 0
    for index, line in enumerate(readme_lines):
        if "概述" in line:
            start = index + 5
        elif "优势" in line:
            end = index - 1
    readme = readme.replace("\n".join(readme_lines[start:end]), (
        "本仓库为简体中文修正版，对原脚本中部分繁体直接转换为简体的名词进行了修正，对于脚本的执行逻辑无任何修改，具体使用哪个版本请自行决定，**原版**可前往这里下载：\n"
        "> 原版：[backup_script](https://github.com/YAWAsau/backup_script) 。\n\n"
        "简体中文版使用 Github Action 自动构建，每小时执行1次，所以在原仓库发布新 release 后，不会立马更新简体版。"
    ))
    file = my_repo.get_readme()
    old_readme = file.decoded_content.decode()
    if readme != old_readme:
        my_repo.update_file(path=file.path, message="更新 README.md", content=readme, sha=file.sha)


if __name__ == "__main__":
    main()
