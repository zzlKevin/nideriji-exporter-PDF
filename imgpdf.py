import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog

MOOD_DICT: dict = {
    'excited': '大笑',
    'tongue': '大笑',
    'cool': '开心',
    'devil': '生气',
    'happy': '开心',
    'poop': '大哭',
    'neutral': '一般',
    'sad': '失落',
    'dead': '我死',
    'normal': '一般',
}

WEATHER_DICT: dict = {
    'lightning-rainy': '闪电-下雨',
    'pouring': '暴雨',
    'snow': '下雪',
    'snowy': '大雪',
    'cloudy': '多云',
    'sunny': '晴朗',
    'rainy': '下雨',
    'fog': '雾霾',
    'windy': '大风',
    'hail': '冰雹',
}

# 注册中文字体
pdfmetrics.registerFont(TTFont('SimHei', 'simHei.ttf'))  # 确保你有这个字体文件
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='diaryTitle', fontName='SimHei', fontSize=18, alignment=1, bold=True))
styles.add(ParagraphStyle(name='Chinese', fontName='SimHei', fontSize=12))
styles.add(ParagraphStyle(name='RightAlign', fontName='SimHei', fontSize=12, alignment=2))
styles.add(ParagraphStyle(name='Center', fontName='SimHei', fontSize=12, alignment=1))  #居中的图片数字样式
# 读取日记条目的JSON数据
def read_diaries_json(file_path):
   with open(file_path, 'r', encoding='utf-8') as file:
       return json.load(file)
 

# 创建PDF文件
def create_pdf(diaries, images_folder, file_name):
   # 创建PDF文档
   pdf = SimpleDocTemplate(file_name, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
   
   # 为每篇日记创建段落，并插入图片
   flowables = []
   for entry in diaries:
      title = Paragraph(entry['title'], styles['diaryTitle'])
      mood = Paragraph(f'心情: {MOOD_DICT.get(entry["mood"], entry["mood"])}', styles['Chinese'])
      weather = Paragraph(f'天气: {WEATHER_DICT.get(entry["weather"], entry["weather"])}', styles['Chinese'])
      createddate = Paragraph(f'创建日期: {entry["createddate"]}', styles['Chinese'])
      # deleteddate = Paragraph(f'删除日期: {entry["deleteddate"]}', styles['Chinese'])
      modified_time = Paragraph(f'最后修改时间: {entry["ts"]}', styles['RightAlign'])
      created_time = Paragraph(f'创建时间: {entry["createdtime"]}', styles['Chinese'])
      
      if entry['title']:
         flowables.append(title)
      else:
         flowables.append(Paragraph(f'无题', styles['diaryTitle']))
      flowables.append(Spacer(1, 24))  # 添加更多的空间分隔日记
      flowables.append(createddate)
      # flowables.append(deleteddate)
      flowables.append(created_time)
      if MOOD_DICT.get(entry["mood"]):
          flowables.append(mood)
      if WEATHER_DICT.get(entry["weather"]):
          flowables.append(weather)
      flowables.append(Spacer(1, 12))  # 添加一些空间

      # 解析content中的图片标记，并插入图片
      content_paragraphs = entry['content'].split('\n')
      for paragraph in content_paragraphs:
            if paragraph.startswith('[图'):
               # 提取图片标记，例如'[图525]'中的'525'
               img_key = paragraph[2:-1]  # 格式为'[图标记]'
               print("正在加载图"+img_key)
               # 构建图片文件路径
               img_filename = f"图{img_key}.jpg"
               img_path = os.path.join(images_folder, img_filename)
               if os.path.exists(img_path):
                  image = Image.open(img_path)
                  image = image.resize((image.width // 5, image.height // 5), Image.Resampling.LANCZOS)
                  # 获取PDF框架的大小
                  frame_width = pdf.width - pdf.leftMargin - pdf.rightMargin
                  frame_height = pdf.height - pdf.topMargin - pdf.bottomMargin
                  
                  # 计算图像缩放因子，保持宽高比
                  scale = min(frame_width / image.width, frame_height / image.height)
                  if scale > 1:  # 如果缩放因子大于1，则不需要放大，直接使用原始尺寸
                        scale = 1
                  
                  # 调整图像大小
                  new_width = image.width * scale
                  new_height = image.height * scale
                  
                  rl_image = RLImage(img_path, width=new_width, height=new_height)
                  # 图片可能需要居中，可以使用Spacer来调整位置
                  # flowables.append(Spacer(1, (frame_height - new_height) / 2))  # 临时Spacer，确保图片垂直居中
                  flowables.append(Spacer(1, 12))  # 添加一些空间
                  flowables.append(rl_image)
                  flowables.append(Paragraph(f'[图{img_key}]', styles['Center']))
                  flowables.append(Spacer(1, 12))  # 添加一些空间

            else:
               flowables.append(Paragraph(paragraph, styles['Chinese']))
   
      flowables.append(Spacer(1, 12))  # 添加一些空间
      flowables.append(modified_time)
      flowables.append(Spacer(1, 24))  # 添加更多的空间分隔日记
      flowables.append(Spacer(1, 24))  # 添加更多的空间分隔日记
      
   print("准备输出pdf")
   # 构建PDF文档
   pdf.build(flowables)
   print("输出完毕")

def choose_json_file():
  root = tk.Tk()
  root.withdraw()  # 隐藏主窗口
 
  # 使用 filedialog.askopenfilename 来让用户选择文件
  json_file_path = filedialog.askopenfilename(title="选择日记JSON文件", filetypes=[("JSON files", "*.json")])
  return json_file_path

def choose_images_folder():
   root = tk.Tk()
   root.withdraw()  # 隐藏主窗口
 
   # 使用 filedialog.askdirectory 来让用户选择文件夹
   images_folder = filedialog.askdirectory(title="选择图片文件夹")
   return images_folder

def choose_output_pdf():
  root = tk.Tk()
  root.withdraw()  # 隐藏主窗口
 
  # 使用 filedialog.asksaveasfilename 来让用户选择保存文件的位置和名称
  # 设置文件类型为 PDF 文件
  output_pdf_path = filedialog.asksaveasfilename(title="选择生成PDF的路径和文件名", filetypes=[("PDF files", "*.pdf")])
  return output_pdf_path

# 主函数
def main():
  # 让用户选择JSON文件
  print("选择日记JSON文件")
  json_file_path = choose_json_file()
  if not json_file_path:
      print("用户没有选择文件，程序退出。")
      return
 
  # 读取日记条目
  diaries = read_diaries_json(json_file_path)
 
  # 让用户选择图片文件夹
  print("选择图片文件夹")
  images_folder = choose_images_folder()
  if not images_folder:
      print("用户没有选择文件夹，程序退出。")
      return
 
  # 让用户选择生成PDF的路径和文件名
  output_pdf_path = choose_output_pdf()
  print("选择生成PDF的路径和文件名")
  if not output_pdf_path:
      print("用户没有选择输出文件，程序退出。")
      return

  # 按日记日期升序排序
  sorted_diaries = sorted(diaries, key=lambda x: x['createddate'], reverse=False)
   
  # 生成PDF
  create_pdf(sorted_diaries, images_folder, output_pdf_path)
 
if __name__ == '__main__':
   main()