import os, requests
from github import Github, Auth
from requests import HTTPError
from shutil import make_archive, unpack_archive
from zhconv import convert

proj = "speed-backup"
my_repo = f"lingcraft/{proj}"
src_repo = "YAWAsau/backup_script"
old_repo = "Petit-Abba/backup_script_zh-CN"
token = Auth.Token(os.getenv("GITHUB_TOKEN"))


def main():
    version, description = get_latest()
    if version:
        simplify()
        upload(version, description)


def get_latest():
    release = Github().get_repo(src_repo).get_latest_release()
    if len(release.tag_name):
        for asset in release.assets:
            if download(asset.browser_download_url, asset.name):
                unpack_archive(asset.name, proj)
                os.remove(asset.name)
        return release.tag_name, convert(release.body, "zh-cn")
    else:
        return False, False


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


def simplify():
    for root, dirs, files in os.walk(proj):
        for file_name in list(filter(lambda e: e.endswith((".sh", ".conf")) or root.endswith("script"), files)):
            file = os.path.join(root, file_name)
            with open(file, "r", encoding="utf-8") as f:
                content = convert(f.read().replace(old_repo, my_repo), "zh-cn")
            os.remove(file)
            with open(convert(file, "zh-cn"), "w", encoding="utf-8", newline="\n") as f:
                f.write(content)


def upload(version, description):
    make_archive(proj, "zip", proj)
    repo = Github(auth=token).get_repo(my_repo)
    releases = list(filter(lambda x: x.tag_name == version, repo.get_releases()))
    if len(releases) == 0:
        release = repo.create_git_release(version, version, description, False, False, False)
        release.upload_asset(f"{proj}.zip", f"{proj}{version}.zip", "application/zip", f"{proj}{version}.zip")
    else:
        release = releases[0]
        for asset in release.get_assets():
            if download(asset.browser_download_url, asset.name):
                if os.path.getsize(f"{proj}.zip") != os.path.getsize(asset.name):
                    asset.delete_asset()
                    release.upload_asset(f"{proj}.zip", f"{proj}{version}.zip", "application/zip", f"{proj}{version}.zip")
                os.remove(asset.name)


if __name__ == "__main__":
    main()
