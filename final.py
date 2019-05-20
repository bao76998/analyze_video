from __future__ import unicode_literals
import moviepy.editor as mp
import os
import pytube
from googlesearch import search_videos
import youtube_dl
import urllib
import shutil
from os import path
import speech_recognition as sr
import re
import cv2
import numpy
import scenedetect
import os
import urllib.request
import json




cre = "AIzaSyCvvT_PUuE7uGTQ4PR5Y903UUGMrTJ7EO4"
maindir = path.dirname(path.realpath(__file__))
STATS_FILE_PATH = 'testpvideo.stats.csv'



def getinfo(url, folderdetails):
    id = getid(url)
    data = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/videos?part=id%2C+snippet&id="+id+"&key=" + cre).read()
    title = "Title: "+ json.loads(data)["items"][0]["snippet"]["title"] 
    author =  "\n\nAuthor: "+ json.loads(data)["items"][0]["snippet"]["channelTitle"]
    desb = "\n\nDescription: "+ json.loads(data)["items"][0]["snippet"]["description"] 
    publish = "\n\nPublished: " +json.loads(data)["items"][0]["snippet"]["publishedAt"] 
    detail = title + author + publish +desb  
    textfile = open(folderdetails+"/"+title[7:len(title)]+".txt","w")
    textfile.write(detail)
    textfile.close() 
    return detail

def getid(url):
    id = url[url.index("v=")+2:len(url)] 
    return id

def downloads(urls, dest):
    # for url in urls:
    #     print(url)
    #     yt = pytube.YouTube(url)
    #     yt.streams.first().download(dest)  # Download highest quality of video
    os.chdir(dest)
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
   
        
def search(key, n):
    founds = search_videos(key, stop=n)
    urls = []
    for url in founds:
        if url.startswith('https://www.youtube.com'):
            if url.startswith('https://www.youtube.com/channel'):
                urls = urls
            else:
                urls = urls + [url]
    return urls

def editFilename(filename):
    newname = re.sub('[^a-zA-Z0-9-_*.\s]', '', filename)
    newname = str.replace(newname," ","-")
    newname = str.replace(newname,"_","-")
    return newname
def trimFilename(path):
    for filename in os.listdir(path):
        dst = path + "/" + editFilename(filename)
        src = path +"/"+ filename  
        os.rename(src, dst) 

def video2Audio(folder_videos_dir, folder_audios_dir): 
    # use module moviepy
    for filename in os.listdir(folder_videos_dir):
        clip = mp.VideoFileClip(folder_videos_dir +"/"+ filename)
        clip.audio.write_audiofile(folder_audios_dir + "/" + filename[:-(len(filename)-filename.rfind("."))] + ".wav")

def splitVideo(path, folderAudiosSplitted):

    for filename in os.listdir(path):
        foldername = folderAudiosSplitted + '/' +filename[:-(len(filename)-filename.rfind("."))]
        os.makedirs(foldername)
        filedir = path+"/"+ filename
        cmd = "ffmpeg -i "+filedir + " -f segment -segment_time 10 -c copy "+foldername+"/out%03d.wav"
        os.system(cmd)

def recognize(sourceAudio,subfile, lg):
    r = sr.Recognizer()
    mysource = sr.AudioFile(sourceAudio)
    submain = ""
    with mysource as source:
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            audio = r.record(source)
            sub = r.recognize_google(audio, language = lg)
            submain = submain + " " + sub

        except sr.UnknownValueError:
            submain = submain
           
        except sr.RequestError:
            submain = submain
    textfile = open(subfile,"a")
    textfile.write(submain)
    textfile.close() 

def detect_scenes_cli(filepath, saveto):
    # option -j is export images with JPEG format
    detect(filepath)
    os.system('scenedetect -i ' + filepath + ' detect-content save-images -j -n 3 -o '+saveto) 

def detect(filename):

    # Create a video_manager point to video file testvideo.mp4. Note that multiple
    # videos can be appended by simply specifying more file paths in the list
    # passed to the VideoManager constructor. Note that appending multiple videos
    # requires that they all have the same frame size, and optionally, framerate.
    video_manager = VideoManager([filename])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)
    # Add ContentDetector algorithm (constructor takes detector options like threshold).
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()

    try:
        # If stats file exists, load it.
        if os.path.exists(STATS_FILE_PATH):
            # Read stats from CSV file opened in read mode:
            with open(STATS_FILE_PATH, 'r') as stats_file:
                stats_manager.load_from_csv(stats_file, base_timecode)

        start_time = base_timecode + 20     # 00:00:00.667
        end_time = base_timecode + 20.0     # 00:00:20.000
        # Set video_manager duration to read frames from 00:00:00 to 00:00:20.
        video_manager.set_duration(start_time=start_time, end_time=end_time)

        # Set downscale factor to improve processing speed (no args means default).
        video_manager.set_downscale_factor()

        # Start video_manager.
        video_manager.start()

        # Perform scene detection on video_manager.
        scene_manager.detect_scenes(frame_source=video_manager, end_time=end_time)


        # Obtain list of detected scenes.
        scene_list = scene_manager.get_scene_list(base_timecode)
        # Like FrameTimecodes, each scene in the scene_list can be sorted if the
        # list of scenes becomes unsorted.

        print('List of scenes obtained:')
        for i, scene in enumerate(scene_list):
            print('    Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
                i+1,
                scene[0].get_timecode(), scene[0].get_frames(),
                scene[1].get_timecode(), scene[1].get_frames(),))

        # We only write to the stats file if a save is required:
        if stats_manager.is_save_required():
            with open(STATS_FILE_PATH, 'w') as stats_file:
                stats_manager.save_to_csv(stats_file, base_timecode)

    finally:
        video_manager.release()
       
def Justdown(searchkey, stop):
    # input 
    search_key = searchkey
    n = stop
    
    # prepare something to store videos + audios
    index = 1
    while (os.path.isdir(maindir+"/videos/download"+str(index))): index=index+1
    folderVideos = maindir + "/videos/download"+str(index)
    folderAudios = maindir + "/audios/download"+str(index)
    os.mkdir(folderVideos)  
    os.mkdir(folderAudios)
    folderdetails = maindir + "/details/download"+str(index)
   
 


    # main process

    urls = search(search_key,int(n))
    
    downloads(urls,folderVideos)
    for url in urls:
        getinfo(url, folderdetails)

def mainprocess(searchkey, stop, language):
    # input 
    search_key = searchkey
    n = stop
    
    # prepare something to store videos + audios
    index = 1
    while (os.path.isdir(maindir+"/videos/download"+str(index))): index=index+1
    folderVideos = maindir + "/videos/download"+str(index)
    folderAudios = maindir + "/audios/download"+str(index)
    folderAudiosSplitted = maindir + "/splitted"
    if (os.path.isdir(maindir + "/splitted")): 
        shutil.rmtree(maindir + "/splitted")
    folderdetails = maindir + "/details/download"+str(index)
    os.mkdir(maindir + "/splitted")
    os.mkdir(folderdetails)
    os.mkdir(folderVideos)  
    os.mkdir(folderAudios)
    


    # main process

    urls = search(search_key,int(n))
    print(urls)
    downloads(urls,folderVideos)
    trimFilename(folderVideos)
    video2Audio(folderVideos,folderAudios)
    splitVideo(folderAudios,folderAudiosSplitted)
    for url in urls:
        getinfo(url, folderdetails)
    

    #SUBBING
    print("SUBBING... ")
    for folder in os.listdir(folderAudiosSplitted):
        subfile = folderAudios + "/" + folder + ".txt"
        for fileAudio in os.listdir(folderAudiosSplitted+"/"+folder):
            audioPath = folderAudiosSplitted+"/"+folder+"/"+fileAudio
            recognize(audioPath ,subfile, language)

    #DETECTSCENE
    for filename in os.listdir(folderVideos):
        os.makedirs(folderVideos+ '/' +filename[:-(len(filename)-filename.rfind("."))])
        saveto = folderVideos+ '/' +filename[:-(len(filename)-filename.rfind("."))]
        detect_scenes_cli(filename, saveto)

def mainprocessWithoutSub(searchkey, stop):
    # input 
    search_key = searchkey
    n = stop
    
    # prepare something to store videos + audios
    index = 1
    while (os.path.isdir(maindir+"/videos/download"+str(index))): index=index+1
    folderVideos = maindir + "/videos/download"+str(index)
    folderAudios = maindir + "/audios/download"+str(index)
    folderdetails = maindir + "/details/download"+str(index)
    # if (os.path.isdir(maindir + "/splitted")): 
    #     shutil.rmtree(maindir + "/splitted")
    # folderAudiosSplitted = maindir + "/splitted"
    # os.mkdir(maindir + "/splitted")
    os.mkdir(folderVideos)  
    os.mkdir(folderAudios)
    
    
    os.mkdir(folderdetails)
 


    # main process
    
    urls = search(search_key,int(n))
   
    downloads(urls,folderVideos)
    trimFilename(folderVideos)

    for url in urls:
        getinfo(url, folderdetails)
    # video2Audio(folderVideos,folderAudios)
    # splitVideo(folderAudios,folderAudiosSplitted)

   
    #DETECTSCENE
    for filename in os.listdir(folderVideos):
        saveto = folderVideos+ '/' + filename[:-(len(filename)-filename.rfind("."))]
        os.makedirs(folderVideos+ '/' + filename[:-(len(filename)-filename.rfind("."))])
        detect_scenes_cli(filename, saveto)


