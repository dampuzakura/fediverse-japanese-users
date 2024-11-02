import requests
import json
import os
from datetime import datetime

# Fediverseサーバーの情報を取得する関数
def fetch_servers(limit=40, total=40):
  servers = []
  next_cursor = None

  while len(servers) < total:
    params = {'limit': limit}
    if next_cursor:
      params['cursor'] = next_cursor

    response = requests.get('https://api.fedidb.org/v1/servers', params=params)

    if response.status_code != 200:
      print(f"データ取得エラー: {response.status_code}")
      break

    data = response.json()
    servers.extend(data['data'])

    next_cursor = data['meta'].get('next_cursor')
    if not next_cursor:
      break

  return servers[:total]

# データをJSONファイルに保存する関数
def save_json(data):
  os.makedirs('servers', exist_ok=True)

  date_str = datetime.now().strftime('%Y%m%d%H%M%S')
  filename = f'servers/{date_str}.json'

  with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

def main():
  server_data = fetch_servers(limit=40, total=2000)
  save_json(server_data)
  print(f"{len(server_data)}件のサーバーを取得して保存しました。")

if __name__ == "__main__":
  main()
