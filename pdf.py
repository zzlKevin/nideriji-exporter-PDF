import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
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

# 读取日记条目的JSON数据
def read_diaries_json(file_path):
   with open(file_path, 'r', encoding='utf-8') as file:
       return json.load(file)
 
# 创建PDF文件
def create_pdf(diaries, file_name):
   # 创建PDF文档
   pdf = SimpleDocTemplate(file_name, pagesize=letter,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=72)
   
   # 为每篇日记创建段落
   flowables = []
   for entry in diaries:
       title = Paragraph(entry['title'], styles['diaryTitle'])
       mood = Paragraph(f'心情: {MOOD_DICT.get(entry["mood"], entry["mood"])}', styles['Chinese'])
       weather = Paragraph(f'天气: {WEATHER_DICT.get(entry["weather"], entry["weather"])}', styles['Chinese'])
       content = Paragraph(f'{entry["content"]}', styles['Chinese'])
       createddate = Paragraph(f'创建日期: {entry["createddate"]}', styles['Chinese'])
       modified_time = Paragraph(f'最后修改时间: {entry["ts"]}', styles['RightAlign'])
       created_time = Paragraph(f'创建时间: {entry["createdtime"]}', styles['Chinese'])
      
       if entry['title']:
         flowables.append(title)
       else:
         flowables.append(Paragraph(f'无题', styles['diaryTitle']))
       flowables.append(Spacer(1, 24))  # 添加更多的空间分隔日记
       flowables.append(createddate)
       flowables.append(created_time)
       if MOOD_DICT.get(entry["mood"]):
          flowables.append(mood)
       if WEATHER_DICT.get(entry["weather"]):
          flowables.append(weather)
       flowables.append(Spacer(1, 12))  # 添加一些空间
       flowables.append(content)
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
   # 读取JSON数据
   diaries = read_diaries_json(json_file_path)

   # 按日记日期升序排序
   sorted_diaries = sorted(diaries, key=lambda x: x['createddate'], reverse=False)
   
   # 让用户选择生成PDF的路径和文件名
   output_pdf_path = choose_output_pdf()
   print("选择生成PDF的路径和文件名")
   if not output_pdf_path:
         print("用户没有选择输出文件，程序退出。")
         return

   # 按日记日期升序排序
   sorted_diaries = sorted(diaries, key=lambda x: x['createddate'], reverse=False)
      
   # 生成PDF
   create_pdf(sorted_diaries, output_pdf_path)
 
if __name__ == '__main__':
   main()