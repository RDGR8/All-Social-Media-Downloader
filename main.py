import pathlib
import subprocess
import os
import ffmpeg
import moviepy.video.io.ffmpeg_tools
import yt_dlp
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

forbiddenWindowsChractrs = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
result = []
result2 = []
result3= []
guiExportPath = ('')
guiVideoLink = ('')
guiOutputLocation = ('')
guiCheckbox = False

randomNumber = str(random.randint(10000000,99999999))
#Defining functions


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    guiExportPath = filedialog.askdirectory()
    print(guiExportPath)
    guiOutputLocationEntry.delete(0, END)
    guiOutputLocationEntry.insert(0, guiExportPath)



def extractAudio(pathToVideo : str):
    guiProgressBar.set(0.15)
    guiProgressBarText.configure(text ="Converting Youtube Audio to a Usable Type")
    audio = AudioFileClip(pathToVideo)
    audio.write_audiofile((str(pathlib.Path(pathToVideo).absolute().parent))+'\\'+randomNumber+".mp3", logger = None)
    audio.close()

def openFileLocation(yesOrNo : bool, fileLocation):
    if yesOrNo == True:
        subprocess.run(f'explorer /select,"{fileLocation}"')


def YouTubeDownload(theYoutubeVideoLink, pathToExportYoutubeVideo, guiCheckbox1):

    subprocess.run(fr'yt-dlp.exe {theYoutubeVideoLink} --output {pathToExportYoutubeVideo}\%(title)s.%(ext)s')
    proc=subprocess.run(fr'yt-dlp.exe {theYoutubeVideoLink} --output {pathToExportYoutubeVideo}\%(title)s.%(ext)s --get-filename', stdout=subprocess.PIPE, encoding='utf-16', universal_newlines=True)

    print((proc.stdout))

    #print((((str(proc.stdout))[2:-3])))
    #print((str((proc.stdout))[2:-3])).replace(fr'\\', '\\')
    openFileLocation(guiCheckbox1, (((str(proc.stdout))[2:-3])).replace(fr'\\', '\\'))

    #subprocess.run('yt-dlp.exe', cwd=cu)

def InstagramDownload(instaLink, outputLocation, guiCheckbox1):
    cl = Client()
    outputLocation = (pathlib.Path(outputLocation).absolute())
    mediaPk = int(cl.media_pk_from_url(instaLink))
    mediaType = int(cl.media_info(str(mediaPk)).media_type)
    instaFormat = str(cl.media_info(str(mediaPk)).video_url)
    outputLocation = str(outputLocation)
    instaTitle = (cl.media_info(str(mediaPk)).caption_text).replace('\n', ' ')
    for i in range(len(forbiddenWindowsChractrs)):
        instaTitle = instaTitle.replace(forbiddenWindowsChractrs[i], ' ')

    if len(instaTitle) > 210:
        instaTitle = instaTitle[:210]
    if mediaType == 2:
        guiProgressBarText.configure(text="Downloading Instagram Video", text_color= 'white')
        cl.video_download(mediaPk, fileName=instaTitle, folder=outputLocation)
        openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle + '.mp4')
       # if '.mp4' in instaFormat:
        #    openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle +'.mp4')
        #elif '.mov' in instaFormat:
         #   openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle +'.mov')
        #elif '.gif' in instaFormat:
         #   openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle +'.gif')


    elif mediaType == 1:
        guiProgressBarText.configure(text="Downloading Instagram Photo", text_color= 'white')
        cl.photo_download(mediaPk, fileName= instaTitle ,folder=outputLocation)
        openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle + '.webp')
      #  if '.jpeg' in instaFormat:
       #     openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle +'.jpeg')
        #elif '.webp' in instaFormat:
         #   openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle +'.webp')
          #  print(outputLocation + '\\' + instaTitle +'.webp')
        #elif '.png' in instaFormat:
         #   openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle + '.png')
        #elif '.bmp' in instaFormat:
         #   openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle +'.bmp')
        #elif '.gif' in instaFormat:
         #   openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle +'.gif')

def guiStart():
    if 'youtube.com/' in (guiLinkEntry.get()) or  'youtu.be/' in (guiLinkEntry.get()):
        t = Thread(target=YouTubeDownload, args=(str(guiLinkEntry.get()), str(guiOutputLocationEntry.get()), bool(checkBox.get())), daemon=True)
        t.start()
    elif 'instagram.com/' in (guiLinkEntry.get()):
        t = Thread(target=InstagramDownload, args=(str(guiLinkEntry.get()), str(guiOutputLocationEntry.get()), bool(checkBox.get())), daemon=True)
        t.start()
    else:
        guiProgressBarText.configure(text="Invalid Link", text_color= 'red')

#GUI

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = customtkinter.CTk()
root.geometry('700x450')
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



guiOutputLocationButton = customtkinter.CTkButton(master=frame, height= 30, text ="Select Output Location", command=browse_button)
guiOutputLocationButton.pack(pady=5, padx=0)


guiStartButton = customtkinter.CTkButton(master=frame, height= 50, text="Start", command= guiStart)
guiStartButton.pack(pady=20, padx=10)

guiProgressBar =  customtkinter.CTkProgressBar(master= frame, orientation= HORIZONTAL, progress_color= '#3399FF')
guiProgressBar.set(0)
guiProgressBar.pack(pady=5, padx=10)

guiProgressBarText = customtkinter.CTkLabel(master= frame, text ="", font=("Arial", 15))
guiProgressBarText.pack(pady = 12, padx=10)


root.mainloop()
