import json
import sys
import os
import re
from tqdm import tqdm
from langdetect import detect
from concurrent.futures import ThreadPoolExecutor, as_completed

# JSONファイルを読み込む関数
def load_json(filename):
  with open(filename, 'r', encoding='utf-8') as f:
    return json.load(f)

# 言語を検出する関数
def detect_language(text):
  return detect(text)

# データをきれいにする関数
def clean_content(content):
  content = re.sub(r'<[^>]+>', '', content) # HTMLタグを削除
  content = re.sub(r':[a-zA-Z0-9_]+:', '', content) # 絵文字を削除
  content = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', '', content) # URLを削除
  content = re.sub(r'@[a-zA-Z0-9_]+', '', content) # メンションを削除
  content = re.sub(r'#', '', content) # ハッシュタグを削除
  content = content.strip() # 空白を削除
  content = content.replace('\n', '') # 改行を削除
  return content

# データが有効かどうかを判定する関数
def valid_content(content):
  return len(content) > 5

# データをJSONファイルに保存する関数
def save_json(data, path):
  basename, ext = os.path.splitext(os.path.basename(path))
  filename = os.path.join(os.path.dirname(path), f'{basename}_lang{ext}')
  with open(filename, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)
  return filename

def main():
  if len(sys.argv) < 2:
    print("使用方法: 引数にJSONファイルを指定してください。")
    return

  input_file = sys.argv[1]
  input_list = load_json(input_file)
  
  success = []

  def process_item(item):
    processed_data = []
    path = item.get('path')
    if not path:
      return None
    posts = load_json(path)
    for post in posts:
      content = post.get('content')
      if not content:
        continue
      content = clean_content(content)
      if not valid_content(content):
        continue
      try:
        lang = detect_language(content)
      except:
        continue
      post['language'] = lang
      processed_data.append(post)

    output_file = save_json(processed_data, path)
    return {
      'domain': item.get('domain'),
      'path': output_file,
      'posts': len(processed_data),
    }

  with ThreadPoolExecutor(max_workers=30) as executor:
    futures = []
    for item in input_list:
      futures.append(executor.submit(process_item, item))
    for future in tqdm(as_completed(futures), total=len(futures)):
      result = future.result()
      if result:
        success.append(result)

  save_json(success, input_file)

if __name__ == '__main__':
  main()
