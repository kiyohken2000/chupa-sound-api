from generate import generate_video, get_random_chupa

def generate_chupa_sound():
  text = get_random_chupa()
  video_base64 = generate_video(prompt=text)
  print(video_base64)