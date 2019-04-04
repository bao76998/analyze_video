from googlesearch import search_videos
import pytube 
import os
from os import path
import moviepy.editor as mp
import speech_recognition as sr
import codecs
   

def downloads(url, dest):
	yt = pytube.YouTube(url)
	yt.streams.first().download(dest) #Download highest quality of video
	
	
def search(key, n):
  founds = search_videos(key, stop = n)
  urls = []
  for url in founds:
    if url.startswith('https://www.youtube.com'):
      if url.startswith('https://www.youtube.com/channel'):
        urls = urls
      else:
        urls = urls + [url]
  return urls

def convert(folder_videos_dir, folder_audios_dir):
  for filename in os.listdir(folder_videos_dir):
    clip = mp.VideoFileClip(folder_videos_dir + filename)
    clip.audio.write_audiofile(folder_audios_dir+  filename[:-4]  +".wav")

def subbing(folder_audios_dir):
  for filename in os.listdir(folder_audios_dir):
    subAudio(folder_audios_dir + filename)

def subAudio(audio_dir):
  audio_filename = os.path.basename(audio_dir)[:-3] 
  print(audio_filename)
  rec = sr.Recognizer()
  with sr.AudioFile(audio_dir) as source:
    audio = rec.record(source)
  try:
    text = rec.recognize_google(audio)
    print(text)
    # os.system("touch "+audio_filename+"txt")
    # file = codecs.open(audio_filename+"txt",'w', encoding='utf-8') 
    # file.write(text) 
    # file.close() 
  except:
    print("failed")
    # os.system("touch "+audio_filename+"txt")
    # file = codecs.open(audio_filename+"txt",'w',encoding='utf-8') 
    # file.write("Translate failed!") 
    # file.close() 

folder_audios = path.join(path.dirname(path.realpath(__file__)),"audios/")
folder_videos = path.join(path.dirname(path.realpath(__file__)),"videos/")

# folder_audios = "./audios/"
# folder_videos = "./videos/"


# print('Nhập tên videos cần tìm: ')
# search_key = input()
# urls = search(str(search_key),5)
# print(urls)

# for url in urls:
#   downloads(url,folder_videos)

convert(folder_videos, folder_audios)
subbing(folder_audios)

    
