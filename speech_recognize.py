import speech_recognition as sr
import os

def subAudio(audio_dir):
	audio_filename = os.path.basename(audio_dir) 
	print(audio_filename)
	rec = sr.Recognizer()
	with sr.AudioFile(audio_dir) as source:
		audio = rec.record(source)
		text = rec.recognize_google(audio)
	try:
		print(text)
	except:
		print("failed")
	# os.system("touch "+audio_filename+"txt")
	# file = codecs.open(audio_filename+"txt",'w', encoding='utf-8') 
	# file.write(text) 
	# file.close() 
	# os.system("touch "+audio_filename+"txt")
	# file = codecs.open(audio_filename+"txt",'w',encoding='utf-8') 
	# file.write("Translate failed!") 
	# file.close() 

audios_folder = "./audios/"
# for filename in os.listdir(audios_folder):
# 	subAudio(audios_folder+filename)
subAudio('./videos/music.flac')