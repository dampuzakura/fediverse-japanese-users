import json
import sys
import os

# JSONファイルを読み込む関数
def load_json(file_name):
  with open(file_name, 'r', encoding='utf-8') as file:
    return json.load(file)

# フィルタリングしたデータからnameを抽出する関数
def extract_names(data):
  return [software.get('name') for software in data]

# データをJSONファイルに保存する関数
def save_json(data, file_name):
  with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

# メイン処理
def main():
  if len(sys.argv) < 2:
    print("使用方法: 引数にJSONファイルを指定してください。")
    return
  input_file = sys.argv[1]
  data = load_json(input_file)
  names = extract_names(data)
  base_name, ext = os.path.splitext(os.path.basename(input_file))
  output_file = os.path.join(os.path.dirname(input_file), f'{base_name}_names{ext}')
  save_json(names, output_file)

if __name__ == '__main__':
  main()
