import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import requests
import json
import os
import webbrowser
from datetime import datetime
import configparser  # 引入configparser模块

# 保存路径信息到配置文件
def save_path_config(path):
    config = configparser.ConfigParser()
    config['PATH'] = {'DownloadPath': path}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# 从配置文件中读取路径信息
def load_path_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'PATH' in config and 'DownloadPath' in config['PATH']:
        return config['PATH']['DownloadPath']
    else:
        return None

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def download_3d_model():
    code = code_entry.get()
    path = path_label["text"]

    has_url = 'https://pro.lceda.cn/api/eda/product/search'
    has_formdata = {
        'keyword': code,
        'needAggs': 'true',
        'url': '/api/eda/product/list',
        'currPage': '1',
        'pageSize': '10'
    }

    try:
        r0 = requests.post(has_url, data=has_formdata)
        json_data = r0.json()
        Data_ls = json_data['result']
        Data_ls2 = Data_ls['productList']
        Datas = Data_ls2[0]
        hasDevice = Datas['hasDevice']

        url = 'https://pro.lceda.cn/api/devices/searchByIds'
        formdata = {
            'uuids[]': hasDevice,
            'path': path
        }

        r1 = requests.post(url, data=formdata)
        json1_data = r1.json()
        Data1_ls = json1_data['result']
        Data1_ls2 = Data1_ls[0]
        Data1_ls3 = Data1_ls2['attributes']
        Model_id = Data1_ls3['3D Model']

        url2 = 'https://pro.lceda.cn/api/components/searchByIds?forceOnline=1'
        formdata2 = {
            'uuids[]': Model_id,
            'dataStr': 'yes',
            'path': path
        }

        r2 = requests.post(url2, data=formdata2)
        json2_data = r2.json()
        Data2_ls = json2_data['result']
        Data2_ls2 = Data2_ls[0]
        Data2_ls3 = Data2_ls2['dataStr']
        Data2_ls4 = json.loads(Data2_ls3)
        Model_id0 = Data2_ls4['model']

        download_url = "https://modules.lceda.cn/qAxj6KHrDKw4blvCG8QJPs7Y/" + Model_id0
        r3 = requests.get(download_url)
        demo = r3.text

        filename = f"{code}.step"  # 设置文件名为产品代码
        desktop_path = get_desktop_path()
        filepath = os.path.join(desktop_path, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(demo)

        now = datetime.now().strftime("%H:%M:%S")
        log_area.insert(tk.END, f"[{now}] {code}_3D模型下载成功！\n")
        log_area.see(tk.END)  # 将滚动条滚动到底部

    except Exception as e:
        now = datetime.now().strftime("%H:%M:%S")
        log_area.insert(tk.END, f"[{now}] 错误：请检查编号是否正确。\n")
        log_area.see(tk.END)  # 将滚动条滚动到底部

def set_path():
    selected_path = filedialog.askdirectory()
    if selected_path:
        path_label.config(text=selected_path)
        save_path_config(selected_path)  # 保存路径信息到配置文件

def about():
    about_window = tk.Toplevel(root)
    about_window.title("关于")
    about_window.geometry("300x200")

    text = tk.Text(about_window, wrap="word", padx=10, pady=10)
    text.pack(expand=True, fill="both")
    text.tag_configure("link", foreground="blue", underline=True)

    about_text = "嘉立创3D模型下载器\n版本：1.0\n作者：Jupiter\n\n\n\n"
    about_text += "更多信息请访问：https://github.com/zhutongxueya/JLC3DDownload"

    about_text +="\n\n\n\n代码来自于kulya97，感谢大佬 "

    text.insert("1.0", about_text)
    text.config(state="disabled")

    def on_link_click(event):
        about_window.destroy()  # 关闭当前窗口
        webbrowser.open("https://github.com/zhutongxueya/JLC3DDownload")  # 打开链接

    text.tag_bind("link", "<Button-1>", on_link_click)



# 创建主窗口
root = tk.Tk()
root.title("立创3D模型下载器")

# 设置窗口大小
window_width = 430
window_height = 290
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 设置窗口背景颜色
root.configure(bg="#f0f0f0")

# 创建输入框和标签
code_label = tk.Label(root, text="元器件编号:", bg="#f0f0f0", font=("Arial", 12))
code_label.grid(row=0, column=0, padx=(10, 5), pady=(20, 10), sticky="w")
code_entry = tk.Entry(root, font=("Arial", 12))
code_entry.insert(tk.END, "C8734")
code_entry.grid(row=0, column=1, padx=(0, 10), pady=(20, 10), sticky="ew")

# 创建下载按钮
download_button = tk.Button(root, text="下载3D模型", command=download_3d_model, bg="#4CAF50", fg="white", width=20, height=2)
download_button.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")

# 创建日志记录区域
log_area = scrolledtext.ScrolledText(root, width=40, height=10)
log_area.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# 创建路径标签
default_path = load_path_config() or get_desktop_path()  # 使用保存的路径或默认路径
path_label = tk.Label(root, text="下载路径: "+ default_path, bg="#f0f0f0")
path_label.grid(row=3, column=0, padx=10, pady=(5, 10), sticky="w")

# 创建菜单栏
menubar = tk.Menu(root)
root.config(menu=menubar)

# 创建菜单
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="修改下载路径", command=set_path)
file_menu.add_separator()
file_menu.add_command(label="退出", command=root.quit)

help_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="帮助", menu=help_menu)
help_menu.add_command(label="关于", command=about)

# 运行主循环
root.mainloop()
