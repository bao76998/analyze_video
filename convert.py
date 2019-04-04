import os
from os import path
from pydub import AudioSegment
import moviepy.editor as mp

#convert .mp4 to .mp3
def convert(folder_videos_dir, folder_audios_dir):
	for filename in os.listdir(folder_videos_dir):
  		clip = mp.VideoFileClip(folder_videos_dir + filename)
  		clip.audio.write_audiofile(folder_audios_dir+ filename[:-4] +".mp3")
  		sound = AudioSegment.from_mp3(folder_audios_dir+  filename[:-4] + ".mp3" )
  		sound.export(folder_audios_dir+  filename[:-4], format="wav")

folder_audios = path.join(path.dirname(path.realpath(__file__)),"audios/")
folder_videos = path.join(path.dirname(path.realpath(__file__)),"videos/")
convert(folder_videos,folder_audios):
                                                       