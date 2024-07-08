from gradio_client import Client
import os
import datetime
import ffmpeg
import base64

def get_random_chupa():
	client = Client("votepurchase/sbv2_chupa_demo")
	result = client.predict(
		api_name="/get_random_text"
	)
	print('chupa_text', result)
	return result

def get_audio_duration(audio_path):
	probe = ffmpeg.probe(audio_path)
	audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
	if audio_stream:
		return float(audio_stream['duration'])
	return 0

def create_video(image_path, audio_path, output_path):
	audio_duration = get_audio_duration(audio_path)

	input_image = ffmpeg.input(image_path, loop=1, t=audio_duration)
	input_audio = ffmpeg.input(audio_path)

	(
		ffmpeg
		.concat(input_image, input_audio, v=1, a=1)
		.output(output_path,
						vcodec='libx264',
						acodec='aac',
						audio_bitrate='192k',
						ab='192k',
						ar='44100',
						strict='experimental',
						video_bitrate='1000k',
						r=30,  # フレームレート
						pix_fmt='yuv420p')
		.overwrite_output()
		.global_args('-loglevel', 'info')  # ログレベルを info に設定
		.run(capture_stdout=True, capture_stderr=True)
	)

def generate_sound(prompt):
	client = Client("votepurchase/sbv2_chupa_demo")
	result = client.predict(
		model_name="chupa_1",
		model_path="model_assets/chupa_1/chupa_1spk_e1000_s194312.safetensors",
		text=prompt,
		language="JP",
		sdp_ratio=1,
		noise_scale=0.6,
		noise_scale_w=0.8,
		length_scale=1,
		line_split=True,
		split_interval=0.5,
		speaker="1",
		api_name="/tts_fn"
	)
	# 元のファイルパスを取得
	original_path = result[1]
	# タイムスタンプを生成（例：20240705_123456）
	timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	# 新しいファイル名を生成（例：20240705_123456.wav）
	new_filename = f"{timestamp}.wav"
	# 現在の.pyファイルのディレクトリを取得
	current_directory = os.path.dirname(os.path.abspath(__file__))
	# 新しいファイルパスを生成
	new_path = os.path.join(current_directory, new_filename)
	# ファイルをコピーして名前を変更
	with open(original_path, 'rb') as f_in, open(new_path, 'wb') as f_out:
		f_out.write(f_in.read())
	print(f"音声が保存されました: {new_path}")
	# 元のファイルを削除
	os.remove(original_path)
	
	return new_path

def encode_base64(output_path):
	with open(output_path, 'rb') as video_file:
		video_data = video_file.read()
		video_base64 = base64.b64encode(video_data).decode('utf-8')

		return video_base64

def generate_video(prompt):
	# 現在の.pyファイルのディレクトリを取得
	current_directory = os.path.dirname(os.path.abspath(__file__))
	# PNGファイルのパス
	image_path = os.path.join(current_directory, 'base_image.png')
	# WAVファイルのパス
	audio_path = generate_sound(prompt)
	# タイムスタンプを生成（例：20240705_123456）
	timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	# MP4ファイルのパス
	output_path = os.path.join(current_directory, f"{timestamp}.mp4")
	# 動画を作成
	create_video(image_path, audio_path, output_path)
	# base64エンコード
	video_base64 = encode_base64(output_path)
	# 音声を削除
	os.remove(audio_path)
	# 動画ファイルを削除
	os.remove(output_path)

	return video_base64