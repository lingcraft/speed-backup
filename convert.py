import github, os, requests, zhconv, zipfile


def main():
    version = download()
    if version:
        convert()
        upload(version)


def download():
    url = f"https://api.github.com/repos/YAWAsau/backup_script/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        release = response.json()
        if "tag_name" in release:
            assets = release["assets"]
            tag = release["tag_name"]
            for asset in assets:
                file_url = asset["browser_download_url"]
                file_name = asset["name"]
                with requests.get(file_url, stream=True) as r:
                    r.raise_for_status()
                    with open(file_name, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                    with zipfile.ZipFile(file_name, "r") as f:
                        f.extractall("speed-backup")
                    os.remove(file_name)
            return tag
        else:
            return False


def convert():
    for root, dirs, files in os.walk("speed-backup"):
        for file_name in list(filter(lambda e: e.endswith((".sh", ".conf")) or root.endswith("script"), files)):
            with open(os.path.join(root, file_name), "r", encoding="utf-8") as f:
                content = f.read()
            os.remove(os.path.join(root, file_name))
            with open(os.path.join(root, zhconv.convert(file_name, "zh-cn")), "w", encoding="utf-8", newline="\n") as f:
                f.write(zhconv.convert(content, "zh-cn"))


def upload(version):
    with zipfile.ZipFile("speed-backup.zip", "w") as f:
        for root, dirs, files in os.walk("speed-backup"):
            for file in files:
                f.write(os.path.join(root, file))
    git = github.Github(auth=github.Auth.Token(os.getenv("GITHUB_TOKEN")))
    repo = git.get_repo("lingcraft/speed-backup")
    releases = list(filter(lambda x: x.tag_name == version, repo.get_releases()))
    if len(releases) == 0:
        release = repo.create_git_release(version, version, version, False, False, False)
        release.upload_asset("speed-backup.zip", f"speed-backup{version}.zip", "zip", f"speed-backup{version}.zip")


if __name__ == "__main__":
    main()
