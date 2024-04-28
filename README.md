<div align="center">
  <img id="nideriji-exporter" width="96" alt="nideriji-exporter" src="repository_icon/icon.png">
  <p>「 Nideriji Exporter - 导出你的日记！」新增导出PDF文件！</p>
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
不需要修改代码,打开选择文件路径
simhei.ttf为PDF生成中文提供字体支持

无须选择的保姆式在分支master2

# 📦 使用方式

使用 `git clone https://github.com/zzlKevin/nideriji-exporter-PDF.git` 指令拉取本仓库至本地，运行 `nideriji_export.py` 并安指示输入帐号密码即可

先运行主体（nideriji_export.py），拿到图片和日记

然后再运行imgpdf.py，导出含图片的PDF

也可以运行pdf.py，导出只包含文字的pdf

打开后需要选择两到三个文件或文件路径：

1.选择图片文件夹

在 .exported\img 里选择你的图片文件夹(.exported\img\你的昵称)（建议将文件夹名字改为英文，不要有中文）

2.选择你的日记json文件

在 .exported\json\你的昵称 里选择你的日记json文件

3.设置导出的PDF名称、路径

pdf 导出路径、名称随意

报错需要运行的：

pip install reportlab

pip install Pillow

pip install tkinter

# 📦 exe打开即用

不需要Python环境，由 pyinstaller --onefile 打包为 exe

Windows可执行文件（.exe）：

https://smilelight.lanzouw.com/b030ob5f7c

密码：7nul

先运行nideriji_exporter.exe

输入邮箱，密码，等待数据抓取完毕

执行完毕后方可执行imgpdf.exe 导出含图片的PDF 或者 pdf.exe  导出只包含文字的pdf

同样的

打开后需要选择两到三个文件或文件路径：

1.选择图片文件夹

在 .exported\img 里选择你的图片文件夹(.exported\img\你的昵称)（建议将文件夹名字改为英文，不要有中文）

2.选择你的日记json文件

在 .exported\json\你的昵称 里选择你的日记json文件

3.设置导出的PDF名称、路径

pdf 导出路径、名称随意


.exported是文件夹名字

如果你的图片特别多，你的img文件夹中的json文件不要打开，否则会特别卡，那个是存储图片的json文件

存储日记的json在.exported\json\你的昵称中

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
新增两个文件
pdf.py是输出纯文本pdf，没有图片
imgpdf.py是输出带图片的日记PDF
不需要修改代码,打开选择文件路径
