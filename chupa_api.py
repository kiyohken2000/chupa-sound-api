import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from generate import get_random_chupa, generate_video

app = Flask(__name__)
CORS(app)

@app.route('/generate_random', methods=['POST'])
def generate_random():
  try:
    print('generate_random 関数の開始')

    # ここにランダム生成のロジックを追加
    random_output = get_random_chupa()

    # 結果の出力
    response = jsonify({'random_result': random_output})
    
    return response, 200

  except Exception as e:
    print('error', e)
    error_response = jsonify({'error': str(e)})
    
    return error_response, 500

@app.route('/generate_sound', methods=['POST'])
def generate_sound():
  try:
    print('generate_sound 関数の開始')
    
    # 受信したテキストを代入
    request_dict = request.get_json()
    received_text = str(request_dict['text'])
    print('受信したプロンプト', received_text)

    # ここに音声生成のロジックを追加
    video_base64 = generate_video(prompt=received_text)

    # 結果の出力
    response = jsonify({'video_result': "sound_output"})
    
    return response, 200

  except Exception as e:
    print('error', e)
    error_response = jsonify({'error': str(e)})
    
    return error_response, 500

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))