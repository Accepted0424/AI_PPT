import os
import re
import subprocess
import sys
import tkinter as tk
import random
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

def call_image_downloader(query,output_path):
    # 定义命令和参数
    command = [
        "python", "./Image-Downloader/image_downloader.py",
        "-e", "Bing",  # engine
        "-d", "api",  # driver
        "-n", "1",  # pic num
        "-j", "1",
        "-o", output_path, #output path
        f"\"{query}\""  # keyword
    ]
    # 执行命令
    stdout = subprocess.run(command, capture_output=True, text=True)
    pattern = r'(Bing_\d+\.(png|jpg|jpeg|bmp|gif))'
    match = re.search(pattern,stdout.stdout)
    file_name = match.group(0)
    return file_name

# 获取 Unsplash 图片的函数
def fetch_images(query):
    unsplash_access_key = "EHskG9CrYx-PQg6F4fWResn2qgSEDKLCh-npEo3mlTY"  # 替换为你的 Unsplash Access Key
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": unsplash_access_key,
        "per_page": 5,  # 控制返回的图片数量
    }
    response = requests.get(url, params=params)
    return response.json()["results"] if response.status_code == 200 else []


# 处理重名问题
def get_unique_filename(filepath):
    base, ext = os.path.splitext(filepath)
    counter = 1
    new_filepath = filepath

    while os.path.exists(new_filepath):
        # 如果文件已存在，增加一个数字后缀
        new_filepath = f"{base}_{counter}{ext}"
        counter += 1

    return new_filepath


def donwload_image_default(images, save_dir):
    random_image = random.choice(images)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    image_url = random_image['urls']['regular']  # get URL
    img_data = requests.get(image_url).content
    image = Image.open(BytesIO(img_data))

    save_path = os.path.join(save_dir, "random_image.jpg")  # 默认保存为 random_image.jpg
    save_path = get_unique_filename(save_path)  # 处理重名问题

    image.save(save_path)
    print(f"图片已保存到: {save_path}")
    return save_path


# 下载并保存图片
def download_image(image_url):
    # 选择保存路径
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
    if save_path:
        try:
            # 从URL获取图片内容
            img_response = requests.get(image_url)
            img = Image.open(BytesIO(img_response.content))
            img.save(save_path)
            messagebox.showinfo("成功", f"图片已保存到: {save_path}")
        except Exception as e:
            messagebox.showerror("错误", f"下载图片失败: {e}")


# 显示图片的函数
def display_images(images, image_frame):
    for widget in image_frame.winfo_children():
        widget.destroy()  # 清空当前显示的图片

    for image_data in images:
        image_url = image_data["urls"]["small"]
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))
        img.thumbnail((100, 100))  # 缩小图片尺寸
        tk_img = ImageTk.PhotoImage(img)

        # 使用 Label 显示图片
        image_label = tk.Label(image_frame, image=tk_img)
        image_label.image = tk_img  # 保存引用
        image_label.pack(side=tk.LEFT, padx=5, pady=5)

        # 下载按钮
        download_button = tk.Button(image_frame, text="下载", command=lambda url=image_url: download_image(url))
        download_button.pack(side=tk.LEFT, padx=5)


def getPic(query, mode):
    images = fetch_images(query)
    if mode == "default":
        img_path = donwload_image_default(images, "Pictures")
        return img_path
    elif mode == "user_select":
        # 创建主窗口
        root = tk.Tk()
        root.title("图片选择器")
        root.geometry("600x400")

        # 图片显示区域
        image_frame = tk.Frame(root)
        image_frame.pack(pady=10)

        # 直接搜索并显示图片
        display_images(images, image_frame)

        root.mainloop()

if __name__ == "__main__":
    query = "power law"
    path = "./picture/test"
    call_image_downloader(query,path)