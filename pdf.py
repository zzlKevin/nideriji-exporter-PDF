'''
此版本为保姆式程序,目的是，运行了 nideriji_exporter.py 或者 nideriji_exporter.exe后,点击此程序直接生成双方的两份日记，而不需要选择文件路径
'''

import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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

# 主函数
def main():
   try:
      diaries1 = read_diaries_json('./.exported/json/diary1.json')
      # 按日记日期升序排序
      sorted_diaries1 = sorted(diaries1, key=lambda x: x['createddate'], reverse=False)
      output_pdf_path1 = './diary1.pdf'
      # 生成PDF
      create_pdf(sorted_diaries1, output_pdf_path1)
      print('生成自己的日记pdf完毕,尝试生成对方的日记pdf')
   except:
    print("没有呀？再试试对方的")

   try:
    diaries2 = read_diaries_json('./.exported/json/diary2.json')   
    sorted_diaries2 = sorted(diaries2, key=lambda x: x['createddate'], reverse=False)
    output_pdf_path2 = './diary2.pdf'
    create_pdf(sorted_diaries2, output_pdf_path2)
    print('生成对方的日记pdf完毕')
   except:
    print("没有欸，可能你没有匹配")

      
   print("结束")

if __name__ == '__main__':
   main()