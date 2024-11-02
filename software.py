import requests
import json
import os
from datetime import datetime

# ソフトウェアの情報を取得する関数
def fetch_software():
  software_list = []

  response = requests.get('https://api.fedidb.org/v1/software')

  if response.status_code != 200:
    print(f"データ取得エラー: {response.status_code}")
    return

  data = response.json()
  software_list.extend(data)

  return software_list

# データをJSONファイルに保存する関数
def save_json(data):
  os.makedirs('software', exist_ok=True)

  date_str = datetime.now().strftime('%Y%m%d%H%M%S')
  filename = f'software/{date_str}.json'

  with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

def main():
  software_data = fetch_software()
  save_json(software_data)
  print(f"{len(software_data)}件のソフトウェアを取得して保存しました。")

if __name__ == "__main__":
  main()
