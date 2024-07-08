import requests
import json
import base64

# APIにリクエストを送信
url = "https://chupa-api-omc3n2et7a-an.a.run.app/generate_sound"
payload = {"text": "やっぱり……ゆりこ……いろけ……やべえよ……せんきょ……そくほう……みながら……しこってる"}
headers = {"Content-Type": "application/json"}

try:
  response = requests.post(url, json=payload, headers=headers)
  response.raise_for_status()  # エラーレスポンスの場合、例外を発生させる
except requests.exceptions.RequestException as e:
  print(f"APIリクエストエラー: {e}")

try:
  data = response.json()
  video_base64 = data['video_result']
  # Base64文字列の先頭100文字を表示
  print("Base64エンコードされた動画データの先頭100文字:")
  print(video_base64[:100])
  print("...")  # 省略を示すために追加
except (json.JSONDecodeError, KeyError) as e:
  print(f"JSONパースエラー: {e}")
  print(f"レスポンス: {response.text}")

# Base64デコードしてMP4ファイルとして保存
output_file = "output.mp4"
try:
  with open(output_file, "wb") as f:
    f.write(base64.b64decode(video_base64))
  print(f"動画を {output_file} に保存しました。")
except Exception as e:
  print(f"ファイル保存エラー: {e}")