import json
import sys
import os

# 保持するソフトウェア名のリスト
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

# JSONファイルを読み込む関数
def load_json(file_name):
  with open(file_name, 'r', encoding='utf-8') as file:
    return json.load(file)

# 指定されたソフトウェア名に一致するサーバーをフィルタリングする関数
def filter_servers(data, software_names):
  return [
    server for server in data
    if server.get('software', {}).get('name') in software_names
  ]

# データをJSONファイルに保存する関数
def save_json(data, file_name):
  with open(file_name, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

def main():
  if len(sys.argv) < 2:
    print("使用方法: 引数にJSONファイルを指定してください。")
    return
  input_file = sys.argv[1]
  data = load_json(input_file)
  filtered_data = filter_servers(data, SOFTWARE_NAMES_TO_KEEP)
  base_name, ext = os.path.splitext(os.path.basename(input_file))
  output_file = os.path.join(os.path.dirname(input_file), f'server/{base_name}_filtered{ext}')
  save_json(filtered_data, output_file)

if __name__ == '__main__':
  main()
