'''
此版本为保姆式程序,目的是，运行了 nideriji_exporter.py 或者 nideriji_exporter.exe后,点击此程序直接生成双方的两份日记，而不需要选择文件路径
'''

import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image
import os

MOOD_DICT: dict = {
    'excited': '大笑',
    'tongue': '滑稽',
    'cool': '很酷',
    'devil': '生气的魔鬼',
    'happy': '开心',
    'poop': '一坨粑粑',
    'neutral': '平静',
    'sad': '失落',
    'dead': '原地去世',
    'normal': '正常',
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

# 主函数
def main():
 
  try:
    # 读取日记条目
    diaries1 = read_diaries_json('./.exported/json/diary1.json')
    # 按日记日期升序排序
    sorted_diaries1 = sorted(diaries1, key=lambda x: x['createddate'], reverse=False)
    images_folder1 = './.exported/img/diary1'
    output_pdf_path1 = './Imgdiary1.pdf'
    # 生成PDF
    create_pdf(sorted_diaries1, images_folder1, output_pdf_path1)
    print('生成自己的日记pdf完毕,尝试生成对方的日记pdf')
  except:
    print("没有呀？再试试对方的")
     
  try:
    diaries2 = read_diaries_json('./.exported/json/diary2.json')
    sorted_diaries2 = sorted(diaries2, key=lambda x: x['createddate'], reverse=False)
    images_folder2 = './.exported/img/diary2'
    output_pdf_path2 = './Imgdiary2.pdf'
    create_pdf(sorted_diaries2, images_folder2, output_pdf_path2)
    print('生成对方的日记pdf完毕')
  except:
    print("没有欸，可能你没有匹配")

  print("结束")
 
if __name__ == '__main__':
   main()