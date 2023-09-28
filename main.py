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
guiExportPath = ('')
guiVideoLink = ('')
guiOutputLocation = ('')
guiCheckbox = False

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

    with yt_dlp.YoutubeDL({'outtmpl': fr'{pathToExportYoutubeVideo}\%(title)s.%(ext)s'}) as ydl:
        ydl.download([theYoutubeVideoLink])
        filename = ydl.prepare_filename(ydl.extract_info(theYoutubeVideoLink, download=False))

    openFileLocation(guiCheckbox1, filename)

def InstagramDownload(instaLink, outputLocation, guiCheckbox1):
    cl = Client()
    outputLocation = str(pathlib.Path(outputLocation).absolute())
    mediaPk = int(cl.media_pk_from_url(instaLink))
    info = cl.media_info(str(mediaPk))
    mediaType = int(info.media_type)
    instaTitle = (info.caption_text).replace('\n', ' ')
    for i in range(len(forbiddenWindowsChractrs)):
        instaTitle = instaTitle.replace(forbiddenWindowsChractrs[i], ' ')

    if len(instaTitle) > 210:
        instaTitle = instaTitle[:210]
    if mediaType == 2:
        guiProgressBarText.configure(text="Downloading Instagram Video", text_color= 'white')
        cl.video_download(mediaPk, fileName=instaTitle, folder=outputLocation)
        openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle + '.mp4')



    elif mediaType == 1:
        guiProgressBarText.configure(text="Downloading Instagram Photo", text_color= 'white')
        cl.photo_download(mediaPk, fileName= instaTitle ,folder=outputLocation)
        openFileLocation(guiCheckbox1, outputLocation + '\\' + instaTitle + '.webp')

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
