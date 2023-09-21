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
#Defining functions
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
    audio.close()






#GUI

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('1000x500')
root.resizable(0,0)
root.title('All Social Media Downloader')
#root.after(201, lambda :root.iconbitmap("./youtubeWhiteLogo.ico"))

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand =False)

label = customtkinter.CTkLabel(master= frame, text ="All Social Media Downloader", font=("Arial", 24))
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

    instaLink
    instaInfo = str(cl.media_info(cl.media_pk_from_url(instaLink)))
    if 'media_type=1' in instaInfo:
        cl.photo_download(cl.media_pk_from_url(instaLink))

    elif 'media_type=2' in instaInfo:
        cl.video_download(cl.media_pk_from_url(instaLink))


    #if guiCheckbox1 == True:
    #    subprocess.run(f'explorer /select,"{outputLocation}/{youtubeVideo.title}.mp4"')

def YouTubeDownload(theYoutubeVideoLink : str, pathToExportYoutubeVideo, guiCheckbox1):


    #Defining the main variables
    pathToExportYoutubeVideo = str(pathlib.Path(pathToExportYoutubeVideo).absolute())

    #Downloading the YouTube Video
    guiProgressBar.set(0.05)
    guiProgressBarText.configure(text ="Downloading YouTube Video")
    YouTube(theYoutubeVideoLink).streams.filter(adaptive=True, file_extension= 'mp4').order_by('resolution').last().download(pathToExportYoutubeVideo, filename=randomNumber + '.mp4')
    guiProgressBar.set(0.1)
    guiProgressBarText.configure(text ="Downloading YouTube Audio")
    YouTube(theYoutubeVideoLink).streams.filter(file_extension= 'mp4').last().download(pathToExportYoutubeVideo, filename=randomNumber + '_audio.mp4')

    #Defining youtubeVideo for the usage of youtubeVideo.title and for refrencing paths
    youtubeVideo = YouTube(theYoutubeVideoLink)
    youtubeVideoAbsloutePath = (pathToExportYoutubeVideo+'\\'+randomNumber+'.mp4')
    youtubeAudioAbsloutePath = (pathToExportYoutubeVideo+'\\'+randomNumber+'_audio.mp4')


    extractAudio(youtubeAudioAbsloutePath)
    #Extracting the mp3 file from the mp4 audio file (yes, an mp4 audio file)
    guiProgressBar.set(0.15)
    guiProgressBarText.configure(text ="Converting Youtube Audio to a Usable Type")
    audio = AudioFileClip(youtubeAudioAbsloutePath)
    audio.write_audiofile((str(pathlib.Path(youtubeVideoAbsloutePath).absolute().parent))+'\\'+randomNumber+".mp3", logger = None)
    audio.close()

    os.remove(youtubeAudioAbsloutePath)
    youtubeAudioAbsloutePath = (pathToExportYoutubeVideo+'\\'+randomNumber+'.mp3')

    guiProgressBar.set(0.70)
    videoWithoutSound = VideoFileClip(youtubeVideoAbsloutePath)
    videoWithSound = videoWithoutSound.set_audio(AudioFileClip(youtubeAudioAbsloutePath))

    #Getting the bitrate of the originial video
    bit_rate =int((os.path.getsize(youtubeVideoAbsloutePath)/1000000)/((videoWithoutSound.duration/60)*0.0075))
    bit_rate = str(bit_rate*1000)

    #Creating the final video
    guiProgressBarText.configure(text ="Getting the Final Video")
    videoWithSound.write_videofile(pathToExportYoutubeVideo + '\\' + randomNumber + youtubeVideo.title + '.mp4', bitrate= bit_rate, verbose= False, logger = None)
    guiProgressBar.set(1)
    guiProgressBarText.configure(text = "Finished!")

    #deleting variables so at the end the program would be able to delete files that are not needed anymore
    videoWithoutSound.close()
    videoWithSound.close()
    del youtubeAudioAbsloutePath
    os.remove(youtubeVideoAbsloutePath)
    os.remove(youtubeAudioAbsloutePath)

    #path = (fr'{pathToExportYoutubeVideo}\{youtubeVideo.title}.mp4')

    #Open the final video file in windows explorer
    if guiCheckbox1 == True:
        subprocess.run(f'explorer /select,"{pathToExportYoutubeVideo}/{youtubeVideo.title}.mp4"')




def guiStart():
    if 'youtube.com/' in (guiLinkEntry.get()) or  'youtu.be' in (guiLinkEntry.get()):
        t = Thread(target=YouTubeDownload, args=(str(guiLinkEntry.get()), str(guiOutputLocationEntry.get()), bool(checkBox.get())), daemon=True)
        t.start()
    elif 'instagram.com/' in (guiLinkEntry.get()):
        t = Thread(target=InstagramDownload, args=(str(guiLinkEntry.get()), str(guiOutputLocationEntry.get()), bool(checkBox.get())), daemon=True)
        t.start()

guiStartButton = customtkinter.CTkButton(master=frame, height= 50, text="Start", command= guiStart)
guiStartButton.pack(pady=20, padx=10)

guiProgressBar =  customtkinter.CTkProgressBar(master= frame, orientation= HORIZONTAL, progress_color= '#3399FF')
guiProgressBar.set(0)
guiProgressBar.pack(pady=5, padx=10)

guiProgressBarText = customtkinter.CTkLabel(master= frame, text ="", font=("Arial", 15))
guiProgressBarText.pack(pady = 12, padx=10)


root.mainloop()
