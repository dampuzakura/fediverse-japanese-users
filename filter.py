import json
import sys
import os

SOFTWARE_NAMES_TO_KEEP = [
  "Mastodon",
  "Pleroma",
  "Misskey",
  "Gotosocial",
  "Mitra",
  "Akkoma",
  "Cherrypick",
  "Fedibird",
  "Foundkey",
  "Meisskey",
  "Firefish",
  "Iceshrimp",
  "Sharkey",
]

def load_json(file_name):
  # JSONファイルを読み込む関数
  with open(file_name, 'r', encoding='utf-8') as file:
    return json.load(file)

def filter_servers(data, software_names):
  # 指定されたソフトウェア名に一致するサーバーをフィルタリングする関数
  return [
    server for server in data
    if server.get('software', {}).get('name') in software_names
  ]

def save_json(data, file_name):
  # データをJSONファイルに保存する関数
  with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

def main():
  # メイン処理
  if len(sys.argv) < 2:
    print("使用方法: 引数にJSONファイルを指定してください。")
    return
  input_file = sys.argv[1]
  data = load_json(input_file)
  filtered_data = filter_servers(data, SOFTWARE_NAMES_TO_KEEP)
  output_file = os.path.join(os.path.dirname(input_file), 'filtered_' + os.path.basename(input_file))
  save_json(filtered_data, output_file)

if __name__ == '__main__':
  main()