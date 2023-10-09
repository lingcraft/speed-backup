import os, requests, zhconv
from github import Github, Auth
from requests import HTTPError
from zipfile import ZipFile, ZIP_DEFLATED

proj = "speed-backup"
my_repo = f"lingcraft/{proj}"
src_repo = "YAWAsau/backup_script"
old_repo = "Petit-Abba/backup_script_zh-CN"
token = Auth.Token(os.getenv("GITHUB_TOKEN"))


def main():
    version, description = get_latest()
    if version:
        simplify()
        upload(version, convert(description))


def get_latest():
    release = Github().get_repo(src_repo).get_latest_release()
    if len(release.tag_name):
        for asset in release.assets:
            if download(asset.browser_download_url, asset.name):
                with ZipFile(asset.name, "r") as f:
                    f.extractall(proj)
                os.remove(asset.name)
        return release.tag_name, release.body
    else:
        return False


def download(url, name):
    with requests.get(url, stream=True) as r:
        try:
            r.raise_for_status()
            with open(name, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except HTTPError:
            return False


def convert(content):
    return zhconv.convert(content, "zh-cn")


def path(dir_path, file_name):
    return os.path.join(dir_path, file_name)


def size(name):
    return os.path.getsize(name)


def simplify():
    for root, dirs, files in os.walk(proj):
        for file_name in list(filter(lambda e: e.endswith((".sh", ".conf")) or root.endswith("script"), files)):
            with open(path(root, file_name), "r", encoding="utf-8") as f:
                content = f.read()
            os.remove(path(root, file_name))
            with open(path(root, convert(file_name)), "w", encoding="utf-8", newline="\n") as f:
                f.write(convert(content).replace(old_repo, my_repo))


def upload(version, description):
    with ZipFile(f"{proj}.zip", "w", ZIP_DEFLATED) as f:
        for root, dirs, files in os.walk(proj):
            for file in files:
                f.write(path(root, file))
    repo = Github(auth=token).get_repo(my_repo)
    releases = list(filter(lambda x: x.tag_name == version, repo.get_releases()))
    if len(releases) == 0:
        release = repo.create_git_release(version, version, description, False, False, False)
        release.upload_asset(f"{proj}.zip", f"{proj}{version}.zip", "zip", f"{proj}{version}.zip")
    else:
        release = releases[0]
        for asset in release.get_assets():
            if download(asset.browser_download_url, asset.name):
                if size(f"{proj}.zip") != size(asset.name):
                    asset.delete_asset()
                    release.upload_asset(f"{proj}.zip", f"{proj}{version}.zip", "zip", f"{proj}{version}.zip")
                os.remove(asset.name)


if __name__ == "__main__":
    main()
