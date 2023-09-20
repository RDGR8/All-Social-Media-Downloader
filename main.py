import pathlib
import subprocess
import os
import ffmpeg
import moviepy.video.io.ffmpeg_tools
from pytube import YouTube
import random
from moviepy.editor import *
import shlex
import json
import customtkinter
from tkinter import filedialog
from tkinter import *
import tkinter
from tkinter.ttk import *
from threading import Thread
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from instagrapi import Client
from instagrapi.types import StoryMention, StoryMedia, StoryLink, StoryHashtag

result = []
result2 = []
result3= []
guiExportPath = ('')
guiVideoLink = ('')
guiOutputLocation = ('')
guiCheckbox = False

randomNumber = str(random.randint(10000000,99999999))
def downloadYoutubeVideo(url: str, exportPath : str):
    guiProgressBar.set(0.05)
    guiProgressBarText.configure(text ="Downloading YouTube Video")
    YouTube(url).streams.filter(adaptive=True, file_extension= 'mp4').order_by('resolution').last().download(exportPath, filename=randomNumber + '.mp4')
    guiProgressBar.set(0.1)
    guiProgressBarText.configure(text ="Downloading YouTube Audio")
    YouTube(url).streams.filter(file_extension= 'mp4').last().download(exportPath, filename=randomNumber + '_audio.mp4')

def extractAudio(pathToVideo : str):
    guiProgressBar.set(0.15)
    guiProgressBarText.configure(text ="Converting Youtube Audio to a Usable Type")
    audio = AudioFileClip(pathToVideo)
    audio.write_audiofile((str(pathlib.Path(pathToVideo).absolute().parent))+'\\'+randomNumber+".mp3", logger = None)






#GUI

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('1000x500')
root.resizable(0,0)
root.title('YouTube Video Music Remover')
#root.after(201, lambda :root.iconbitmap("./youtubeWhiteLogo.ico"))

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand =False)

label = customtkinter.CTkLabel(master= frame, text ="YouTube Video Music Remover", font=("Arial", 24))
label.pack(pady = 20, padx=10)

guiLinkEntry = customtkinter.CTkEntry(master= frame, width= 300, placeholder_text="Enter Link")
guiLinkEntry.pack(pady=5, padx=10)
guiOutputLocationEntry = customtkinter.CTkEntry(master= frame, width= 300, placeholder_text="Output Location")
guiOutputLocationEntry.pack(pady=12, padx=10)

checkBox=customtkinter.CTkCheckBox(master = frame, text="Open File Location When Done")
checkBox.pack(pady=5, padx=10)

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    guiExportPath = filedialog.askdirectory()
    print(guiExportPath)
    guiOutputLocationEntry.delete(0, END)
    guiOutputLocationEntry.insert(0, guiExportPath)

guiOutputLocationButton = customtkinter.CTkButton(master=frame, height= 30, text ="Select Output Location", command=browse_button)
guiOutputLocationButton.pack(pady=5, padx=0)

def InstagramDownload(instaLink, outputLocation, guiCheckbox1):
    cl = Client()
    # cl.login(USERNAME, PASSWORD)

    instaLink = 'https://www.instagram.com/p/CaKbKV5DQlH/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA=='
    instaInfo = str(cl.media_info(cl.media_pk_from_url(instaLink)))
    if 'media_type=1' in instaInfo:
        cl.photo_download(cl.media_pk_from_url(instaLink))

    elif 'media_type=2' in instaInfo:
        cl.video_download(cl.media_pk_from_url(instaLink))

def YouTubeDownload(videoLink : str, outputLocation, guiCheckbox1):


    #Defining the main variables
    theYoutubeVideoLink = (videoLink)
    print(theYoutubeVideoLink)
    pathToExportYoutubeVideo = str(pathlib.Path(outputLocation).absolute())
    print(pathToExportYoutubeVideo)

    downloadYoutubeVideo(theYoutubeVideoLink, pathToExportYoutubeVideo)

    #Defining youtubeVideo for the usage of youtubeVideo.title
    youtubeVideo = YouTube(theYoutubeVideoLink)
    youtubeVideoAbsloutePath = (pathToExportYoutubeVideo+'\\'+randomNumber+'.mp4')
    youtubeAudioAbsloutePath = (pathToExportYoutubeVideo+'\\'+randomNumber+'_audio.mp4')

    #subprocess.run(f'ffmpeg -i "{youtubeAudioAbsloutePath}" "{pathToExportYoutubeVideo}\\{randomNumber}.mp3"',shell=True)

    extractAudio(youtubeAudioAbsloutePath)
    extractedAudioPath = (pathToExportYoutubeVideo+'\\'+randomNumber+'.mp3')
    #audioClipDuration = AudioFileClip(pathToExportYoutubeVideo+'\\'+randomNumber+'.mp3')
    #audioClipDuration = audioClipDuration.duration
    #count = 0
    #if audioClipDuration <= 0:
    #    print('The video is less or equal to 300 seconds')
#
 #   else:
  #      duration_of_clip = 240  # in seconds, duration of final audio clip
   #     src_duration = int(audioClipDuration)  # in seconds, the duration of the original audio
    #    guiProgressBar.set(0.20)
     #   guiProgressBarText.configure(text ="Splitting Audio Files into bits")
      #  for i in range(0, src_duration, duration_of_clip):
       #     ffmpeg_extract_subclip(extractedAudioPath, i, i + duration_of_clip,
        #                    targetname=pathToExportYoutubeVideo+'\\'+randomNumber+f'_{count}.mp3')
#
 #           result.append(pathToExportYoutubeVideo+'\\'+randomNumber+f'_{count}.mp3')
  #          count += 1
#
 #   audioClips = result

    #!C:\Users\Rashid Ahmed\PycharmProjects\YoutubeMusicRemover311\MDX23\Miniconda
    #exec(open("./MDX23/inference.py").read())
    #path = str(pathlib.Path('./MDX23/Miniconda/Python.exe').absolute())
    #arg2 = ('-r'+(pathToExportYoutubeVideo))
    #arg3 = ('--overlap_large'+' 0.6')
    #arg4 = ('--overlap_small'+' 0.5')
    #arg5 = ('--chunk_size'+'250000')
    #increaseAmount = float(1/len(audioClips))
    #increaseAmount = 0.4*increaseAmount
    #count = 1
    #for i in range(len(audioClips)):
#
 #       guiProgressBarText.configure(text =str("Separating Music from file Number "+str(count)))
  #      arg1 = ('-i' + (audioClips[i]))
   #     subprocess.run([path, "./MDX23/inference.py", arg1, arg2, '--single_onnx', '--only_vocals'], shell=False)   #stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    #    result2.append(audioClips[i].replace(randomNumber+f'_{i}.mp3', randomNumber+f'_{i}_vocals.wav'))
     #   result3.append(audioClips[i].replace(randomNumber+f'_{i}.mp3', randomNumber+f'_{i}_instrum.wav'))
      #  increaseAmount1 =float((float(guiProgressBar.get()))+increaseAmount)
       # guiProgressBar.set(increaseAmount1)
        #count += 1
#
    #audioClipsVocals = result2
    #audioClipsInstrum = result3
    #clips = [AudioFileClip(c) for c in audioClipsVocals]
    #guiProgressBarText.configure(text ="Merging Audio Files Together")
    #audioWithoutMusic = concatenate_audioclips(clips)
    guiProgressBar.set(0.70)
    videoWithMusic = VideoFileClip(str(pathlib.Path(pathToExportYoutubeVideo + "/" + randomNumber + ".mp4").absolute()))
    extractedAudioPath = AudioFileClip(extractedAudioPath)
    videoWithoutMusic = videoWithMusic.set_audio(extractedAudioPath)
    pathToExportYoutubeVideo = str(pathlib.Path(pathToExportYoutubeVideo).absolute())


    bit_rate =int((os.path.getsize(youtubeVideoAbsloutePath)/1000000)/((videoWithMusic.duration/60)*0.0075))
    bit_rate = str(bit_rate*1000)
    print(bit_rate)
    print(bit_rate)
    guiProgressBarText.configure(text ="Getting the Final Video")
    print(pathToExportYoutubeVideo + '\\' + randomNumber + '_vocal.mp4')
    print(videoWithoutMusic)
    videoWithoutMusic.write_videofile(pathToExportYoutubeVideo + '\\' + randomNumber + '_vocal.mp4', bitrate= bit_rate, verbose= False, logger = None)
    guiProgressBar.set(1)
    guiProgressBarText.configure(text = "Finished!")


    videoWithMusic.close()
    videoWithoutMusic.close()
    del extractedAudioPath
    path = (fr'{pathToExportYoutubeVideo}\{randomNumber}_vocal.mp4')

    if guiCheckbox1 == True:
        subprocess.run(f'explorer /select,"{path}"')




def guiStart():
    if 'youtube.com/' in (guiLinkEntry.get()) or  'youtu.be' in (guiLinkEntry.get()):
        t = Thread(target=YouTubeDownload, args=(str(guiLinkEntry.get()), str(guiOutputLocationEntry.get()), bool(checkBox.get())), daemon=True)
        t.start()
    elif 'instagram.com/' in (guiLinkEntry.get()):
        t = Thread(target=YouTubeDownload, args=(str(guiLinkEntry.get()), str(guiOutputLocationEntry.get()), bool(checkBox.get())), daemon=True)
        t.start()

guiStartButton = customtkinter.CTkButton(master=frame, height= 50, text="Start", command= guiStart)
guiStartButton.pack(pady=20, padx=10)

guiProgressBar =  customtkinter.CTkProgressBar(master= frame, orientation= HORIZONTAL, progress_color= '#3399FF')
guiProgressBar.set(0)
guiProgressBar.pack(pady=5, padx=10)

guiProgressBarText = customtkinter.CTkLabel(master= frame, text ="", font=("Arial", 15))
guiProgressBarText.pack(pady = 12, padx=10)






root.mainloop()
