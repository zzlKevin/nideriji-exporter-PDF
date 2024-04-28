<div align="center">
  <img id="nideriji-exporter" width="96" alt="nideriji-exporter" src="repository_icon/icon.png">
  <p>「 Nideriji Exporter - 导出你的日记！」新增导出PDF文件！保姆式操作</p>
</div>

[📚 简介](#-简介)

[📦 使用方式](#-使用方式)

[📦 exe打开即用](#-exe打开即用)

[⏳ 进度](#-进度)

[📌 注意事项](#-注意事项)

[🧑‍💻 贡献者](#-贡献者)

[🔦 声明](#-声明)

# 📚 简介

本脚本使用 你的日记 API 进行日记与图片的抓取，并导出 json 格式的日记和 json 格式与 jpg 格式的图片

由原版：https://github.com/Cierra-Runis/nideriji-exporter 修改
新增两个文件
pdf.py是输出纯文本pdf，没有图片。
imgpdf.py是输出带图片的日记PDF，
不需要修改代码
simhei.ttf为PDF生成中文提供字体支持

此分支为傻瓜式操作，不需要选择文件、文件夹路径，点击程序直接生成双方的两份日记：

根据exe名字的步骤依次执行
必须执行完   第一步：导出日记和图片.exe
才能执行 第二步：生成带图片的日记PDF.exe 和 第三步：生成纯文字PDF日记.exe

执行顺序：

 第一步：导出日记和图片.exe

（图片多的话会有点慢，必须等待到窗口运行完毕关闭为止）

第二步：生成带图片的日记PDF.exe

（图片多的话会有点慢，耐心等待）

第三步：生成纯文字PDF日记.exe


# 📦 使用方式

使用 `git clone https://github.com/zzlKevin/nideriji-exporter-PDF.git` 指令拉取本仓库至本地，运行 `nideriji_export.py` 并安指示输入帐号密码即可

先运行主体（nideriji_export.py），拿到图片和日记

然后再运行imgpdf.py，导出含图片的PDF

也可以运行pdf.py，导出只包含文字的pdf

报错需要运行的：

pip install reportlab

pip install Pillow

pip install tkinter

# 📦 exe打开即用

不需要Python环境，由 pyinstaller --onefile 打包为 exe

Windows可执行文件（.exe）：

https://smilelight.lanzouw.com/b030obn9da

密码:ez47

根据exe名字的步骤依次执行
必须执行完   第一步：导出日记和图片.exe
才能执行 第二步：生成带图片的日记PDF.exe 和 第三步：生成纯文字PDF日记.exe

执行顺序：

 第一步：导出日记和图片.exe

（图片多的话会有点慢，必须等待到窗口运行完毕关闭为止）

第二步：生成带图片的日记PDF.exe

（图片多的话会有点慢，耐心等待）

第三步：生成纯文字PDF日记.exe


.exported是文件夹名字

如果你的图片特别多，你的img文件夹中的json文件不要打开，否则会特别卡，那个是存储图片的json文件

存储日记的json在.exported\json\ 中

# ⏳ 进度

已完成，按需修改

# 📌 注意事项

- 图片拉取时可能会因连接超时而报错，请多次尝试即可

# 🧑‍💻 贡献者

<a href="https://github.com/Cierra-Runis/nideriji-exporter/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Cierra-Runis/nideriji-exporter" />
</a>

# 🧑‍💻 修改者

<a href="">
  <img src="https://avatars.githubusercontent.com/u/30650134?s=400&u=6bb953eb78e2ff9fe50cfc8b5798ebc336cacd30&v=4" />
</a>

# 🔦 声明

本脚本不会记录你的帐号和密码，请放心使用

由原版修改

