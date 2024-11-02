import json
import sys
import os

# 保持するソフトウェア名のリスト
SOFTWARE_NAMES_TO_KEEP = [
  # Misskeyフォーク
  "cherrypick",
  "firefish",
  "foundkey",
  "iceshrimp",
  "meisskey",
  "misskey",
  "sharkey",

  # Mastodonフォーク
  "fedibird",
  "glitchcafe",
  "hometown",
  "mastodon",

  # Pleromaフォーク
  "akkoma",
  "pleroma",

  # Mastodon互換のソフトウェア
  "friendica",
  "gotosocial",
  "mitra",
  "takahe",
]

# JSONファイルを読み込む関数
def load_json(file_name):
  with open(file_name, 'r', encoding='utf-8') as file:
    return json.load(file)

# 指定されたソフトウェア名に一致するサーバーをフィルタリングする関数
def filter_servers(data, software_names):
  lower_software_names = set(name.lower() for name in software_names)
  return [
    server for server in data
    if server.get('software', {}).get('name', '').lower() in lower_software_names
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
  output_file = os.path.join(os.path.dirname(input_file), f'{base_name}_filtered{ext}')
  save_json(filtered_data, output_file)
  print(f"{len(filtered_data)}件のサーバーを抽出して保存しました。")

if __name__ == '__main__':
  main()
