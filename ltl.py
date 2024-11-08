import sys
import json
import os
from datetime import datetime
from mastodon import Mastodon
from misskey import Misskey
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Mastodon互換のソフトウェア名
MASTODON_SOFTWARE_NAMES = [
  'fedibird',
  'glitchcafe',
  'hometown',
  'mastodon',
  'akkoma',
  'pleroma',
  'friendica',
  'gotosocial',
  'mitra',
  'takahe',
]

# Misskey互換のソフトウェア名
MISSKEY_SOFTWARE_NAMES = [
  'cherrypick',
  'firefish',
  'foundkey',
  'iceshrimp',
  'meisskey',
  'misskey',
  'sharkey',
]

# 小文字に変換したソフトウェア名のセット
LOWER_MASTODON_SOFTWARE_NAMES = set(name.lower() for name in MASTODON_SOFTWARE_NAMES)
LOWER_MISSKEY_SOFTWARE_NAMES = set(name.lower() for name in MISSKEY_SOFTWARE_NAMES)

# JSONファイルにデータを保存
def save_json(data, domain):
  os.makedirs(f'local_timelines/{domain}', exist_ok=True)
  date_str = datetime.now().strftime('%Y%m%d%H%M%S')
  filename = f'local_timelines/{domain}/{date_str}.json'
  with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

# JSONファイルを読み込む
def load_json(filepath):
  with open(filepath, 'r', encoding='utf-8') as f:
    return json.load(f)

# Mastodonローカルタイムラインを取得して保存
def fetch_and_save_local_timeline(domain, software_name, posts_length):
  lower_software_name = software_name.lower()
  timelines = []
  err = ''
  
  try:
    if lower_software_name in LOWER_MASTODON_SOFTWARE_NAMES:
      mastodon = Mastodon(api_base_url=f'https://{domain}')
      num_fetched = 0
      max_id = None
      while num_fetched < posts_length:
        limit = min(40, posts_length - num_fetched)
        params = {'limit': limit}
        if max_id:
          params['max_id'] = max_id
        timeline_raw = mastodon.timeline_local(**params)
        if not timeline_raw:
          break
        for post in timeline_raw:
          timelines.append({
            'id': post.get('id'),
            'content': post.get('content'),
            'created_at': post.get('created_at').isoformat() if post.get('created_at') else None,
            'account': {
              'id': post.get('account', {}).get('id'),
              'display_name': post.get('account', {}).get('display_name'),
              'username': post.get('account', {}).get('username'),
            },
          })
        num_fetched += len(timeline_raw)
        max_id = timeline_raw[-1]['id'] - 1
    elif lower_software_name in LOWER_MISSKEY_SOFTWARE_NAMES:
      misskey = Misskey(domain)
      num_fetched = 0
      until_id = None
      while num_fetched < posts_length:
        limit = min(100, posts_length - num_fetched)
        params = {'limit': limit}
        if until_id:
          params['until_id'] = until_id
        timeline_raw = misskey.notes_local_timeline(**params)
        if not timeline_raw:
          break
        for note in timeline_raw:
          timelines.append({
            'id': note.get('id'),
            'content': note.get('text'),
            'created_at': note.get('createdAt'),
            'account': {
              'id': note.get('user', {}).get('id'),
              'display_name': note.get('user', {}).get('name'),
              'username': note.get('user', {}).get('username'),
            },
          })
        num_fetched += len(timeline_raw)
        until_id = timeline_raw[-1]['id']

  except Exception as e:
    err = e

  finally:
    filename = save_json(timelines, domain)
    return filename, err

def main():
  if len(sys.argv) < 2:
    print('使用方法: 引数にJSONファイルを指定してください。')
    return

  servers_file = sys.argv[1]
  servers = load_json(servers_file)
  error = []
  success = []

  # サーバーを処理する関数
  def process_server(server):
    domain = server.get('domain', '')
    software_name = server.get('software', {}).get('name', '')
    posts_length = 500

    # ローカルタイムラインを取得して保存
    filename, err = fetch_and_save_local_timeline(domain, software_name, posts_length)

    # エラーが発生した場合、エラーメッセージを返す
    if err:
      error.append({
        'domain': domain,
        'error': str(err),
      })
    else:
      success.append({
        'domain': domain,
        'path': filename,
      })

  # スレッドプールを使用して並列処理
  with ThreadPoolExecutor(max_workers=30) as executor:
    # サーバーごとに処理を実行し、エラーがあればリストに追加
    futures = [executor.submit(process_server, server) for server in servers]
    for future in tqdm(as_completed(futures), total=len(futures)):
      future.result()

  save_json(error, 'error')
  save_json(success, 'success')

if __name__ == '__main__':
  main()
