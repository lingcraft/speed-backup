import os, requests, zhconv, zipfile
from github import Github, Auth

proj = "speed-backup"
my_repo = f"lingcraft/{proj}"
src_repo = "YAWAsau/backup_script"
token = Auth.Token(os.getenv("GITHUB_TOKEN"))


def main():
    version, description = download()
    if version:
        simplify()
        upload(version, convert(description))


def download():
    release = Github().get_repo(src_repo).get_latest_release()
    if len(release.tag_name):
        for asset in release.assets:
            with requests.get(asset.browser_download_url, stream=True) as r:
                r.raise_for_status()
                with open(asset.name, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                with zipfile.ZipFile(asset.name, "r") as f:
                    f.extractall(proj)
                os.remove(asset.name)
        return release.tag_name, release.body
    else:
        return False


def convert(content):
    return zhconv.convert(content, "zh-cn")


def simplify():
    for root, dirs, files in os.walk(proj):
        for file_name in list(filter(lambda e: e.endswith((".sh", ".conf")) or root.endswith("script"), files)):
            with open(os.path.join(root, file_name), "r", encoding="utf-8") as f:
                content = f.read()
            os.remove(os.path.join(root, file_name))
            with open(os.path.join(root, convert(file_name)), "w", encoding="utf-8", newline="\n") as f:
                f.write(convert(content))


def upload(version, description):
    with zipfile.ZipFile(f"{proj}.zip", "w") as f:
        for root, dirs, files in os.walk(proj):
            for file in files:
                f.write(os.path.join(root, file))
    git = Github(auth=token)
    repo = git.get_repo(my_repo)
    releases = list(filter(lambda x: x.tag_name == version, repo.get_releases()))
    if len(releases) == 0:
        release = repo.create_git_release(version, version, description, False, False, False)
        release.upload_asset(f"{proj}.zip", f"{proj}{version}.zip", "zip", f"{proj}{version}.zip")


if __name__ == "__main__":
    main()
