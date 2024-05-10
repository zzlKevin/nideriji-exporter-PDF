import os
import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image

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

def read_diaries_json(file_path):
   with open(file_path, 'r', encoding='utf-8') as file:
       return json.load(file)

def clean_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    return filename

def create_markdown(diaries, images_folder, output_folder):
   for entry in diaries:

      if entry.get('deleteddate') != 'None':
         continue

      title = clean_filename(entry['title']) if entry['title'] else ''
      filename = f"{entry['createddate']}_{title}.md" if title else f"{entry['createddate']}.md"
      filepath = os.path.join(output_folder, filename)

      os.makedirs(os.path.dirname(filepath), exist_ok=True)
      
      with open(filepath, 'w', encoding='utf-8') as file:
         file.write(f"---\n")
         file.write(f"created: {entry['createddate']}\n")
         file.write(f"updated: {entry['ts']}\n")
         file.write(f"mood: {MOOD_DICT.get(entry['mood'], entry['mood'])}\n")
         file.write(f"weather: {WEATHER_DICT.get(entry['weather'], entry['weather'])}\n")
         file.write(f"---\n\n")

         content_paragraphs = entry['content'].split('\n')
         for paragraph in content_paragraphs:
            if paragraph.startswith('[图'):
               img_key = paragraph[2:-1]
               print("正在加载图"+img_key)
               img_filename = f"图{img_key}.jpg"
               img_path = os.path.join(images_folder, img_filename)
               if os.path.exists(img_path):
                  file.write(f"\n![图{img_key}]({img_path})\n\n")
               else:
                  print(img_path+"不存在")
            else:
               file.write(f"{paragraph}\n")

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

def choose_output_folder():
  root = tk.Tk()
  root.withdraw()
 
  output_folder = filedialog.askdirectory(title="选择生成Markdown文件的文件夹")
  return output_folder

def main():
  print("选择日记JSON文件")
  json_file_path = choose_json_file()
  if not json_file_path:
      print("用户没有选择文件，程序退出。")
      return
 
  diaries = read_diaries_json(json_file_path)
 
  print("选择图片文件夹")
  images_folder = choose_images_folder()
  if not images_folder:
      print("用户没有选择文件夹，程序退出。")
      return
 
  print("选择生成Markdown文件的文件夹")
  output_folder = choose_output_folder()
  if not output_folder:
      print("用户没有选择输出文件夹，程序退出。")
      return

  sorted_diaries = sorted(diaries, key=lambda x: x['createddate'], reverse=False)
   
  create_markdown(sorted_diaries, images_folder, output_folder)
 
if __name__ == '__main__':
   main()