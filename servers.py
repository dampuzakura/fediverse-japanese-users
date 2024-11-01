import requests
import json
import os
from datetime import datetime

# Fediverseサーバーの情報を取得する関数
def fetch_servers(limit=40, total=200):
  servers = [] # サーバーリストの初期化
  next_cursor = None # 次のカーソルの初期化

  while len(servers) < total:
    params = {'limit': limit} # リクエストパラメータの設定
    if next_cursor:
      params['cursor'] = next_cursor # 次のカーソルを追加

    # サーバー情報を取得
    response = requests.get('https://api.fedidb.org/v1/servers', params=params)

    if response.status_code != 200:
      # エラーが発生した場合は処理を終了
      print(f"データ取得エラー: {response.status_code}")
      break

    data = response.json()
    servers.extend(data['data']) # サーバーデータをリストに追加

    # 次のカーソルを取得
    next_cursor = data['meta'].get('next_cursor')
    if not next_cursor:
      # 次のカーソルがなければループを終了
      break

  return servers[:total] # 指定された総数までのサーバーデータを返す

# データをJSONファイルに保存する関数
def save_to_json(data):
  # 保存先ディレクトリを作成
  os.makedirs('servers', exist_ok=True)

  # 現在の日付を取得してファイル名を作成
  date_str = datetime.now().strftime('%Y%m%d%H%M%S')
  filename = f'servers/{date_str}.json'

  # JSONファイルに書き込み
  with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

def main():
  # サーバーデータを取得して保存
  server_data = fetch_servers(limit=40, total=2000) # サーバーデータを取得
  save_to_json(server_data) # サーバーデータをJSONに保存
  print(f"{len(server_data)}件のサーバーを取得して保存しました。") # 処理結果を出力

if __name__ == "__main__":
  main()
