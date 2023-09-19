import os
import zhconv


def main():
    for root, dirs, files in os.walk("backup_script"):
        for file_name in list(filter(lambda e: e.endswith((".sh", ".conf")) or root.endswith("script"), files)):
            with open(os.path.join(root, file_name), "r", encoding="utf-8") as f:
                content = f.read()
            os.remove(os.path.join(root, file_name))
            with open(os.path.join(root, zhconv.convert(file_name, 'zh-cn')), "w", encoding="utf-8", newline="\n") as f:
                f.write(zhconv.convert(content, "zh-cn"))


if __name__ == "__main__":
    main()
