import re
import subprocess


def call_image_downloader(query, output_path):
    # 定义命令和参数
    command = [
        "python", "./Image-Downloader/image_downloader.py",
        "-e", "Bing",  # engine
        "-d", "api",  # driver
        "-n", "1",  # pic num
        "-j", "1",
        "-o", output_path,  # output path
        f"\"{query}\""  # keyword
    ]
    # 执行命令
    stdout = subprocess.run(command, capture_output=True, text=True)
    pattern = r'(Bing_\d+\.(png|jpg|jpeg|bmp|gif))'
    match = re.search(pattern, stdout.stdout)
    file_name = match.group(0)
    return file_name


if __name__ == "__main__":
    query = "power law"
    path = "./picture/test"
    call_image_downloader(query, path)
