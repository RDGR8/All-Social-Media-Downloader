import pathlib
import yt_dlp
from moviepy.editor import *
import customtkinter
from tkinter import filedialog
from tkinter import *
from threading import Thread
from instagrapi import Client
from win32comext.shell import shell, shellcon
import pythoncom

forbiddenWindowsChractrs = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
guiExportPath = ('')
guiVideoLink = ('')
guiOutputLocation = ('')
guiCheckbox = False

#Defining functions

pythoncom.CoInitialize()


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    guiExportPath = filedialog.askdirectory()
    print(guiExportPath)
    guiOutputLocationEntry.delete(0, END)
    guiOutputLocationEntry.insert(0, guiExportPath)





def openFileLocation(yesOrNo : bool, fileLocation):
    if yesOrNo == True:

        path = os.path.dirname(fileLocation).replace('/', '\\')
        files = [os.path.basename(fileLocation)]
        folder_pidl = shell.SHILCreateFromPath(path, 0)[0]
        desktop = shell.SHGetDesktopFolder()
        shell_folder = desktop.BindToObject(folder_pidl, None, shell.IID_IShellFolder)
        name_to_item_mapping = dict(
            [(desktop.GetDisplayNameOf(item, shellcon.SHGDN_FORPARSING | shellcon.SHGDN_INFOLDER), item) for item in
             shell_folder])
        to_show = []
        for file in files:
            if file in name_to_item_mapping:
                to_show.append(name_to_item_mapping[file])
            # else:
            # raise Exception('File: "%s" not found in "%s"' % (file, path))

        shell.SHOpenFolderAndSelectItems(folder_pidl, to_show, 0)



def my_hook(d):
    if d['status'] == 'finished':
        guiProgressBarText.configure(text="Done Downloading\n"+os.path.basename(d['filename']), text_color='white')
    if d['status'] == 'downloading':
        guiProgressBarText.configure(text=d['_speed_str']+'\nETA '+d['_eta_str'], text_color='white')
        guiProgressBar.set((float(d['_percent_str'].replace('%', '')))/100)

def YouTubeDownload(theYoutubeVideoLink, pathToExportYoutubeVideo, guiCheckbox1):
    with yt_dlp.YoutubeDL({'outtmpl': fr'{pathToExportYoutubeVideo}\%(title)s.%(ext)s', 'progress_hooks' : [my_hook]}) as ydl:
        filename = ydl.prepare_filename(ydl.extract_info(theYoutubeVideoLink, download=True))

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
        t = Thread(target=YouTubeDownload, args=(str(guiLinkEntry.get()), str(guiOutputLocationEntry.get().replace('/', '\\')), bool(checkBox.get())), daemon=True)
        t.start()
    elif 'instagram.com/' in (guiLinkEntry.get()):
        t = Thread(target=InstagramDownload, args=(str(guiLinkEntry.get()), str(guiOutputLocationEntry.get().replace('/', '\\')), bool(checkBox.get())), daemon=True)
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

guiProgressBarText = customtkinter.CTkLabel(master= frame, text ="", font=("Arial", 13), wraplength=530)
guiProgressBarText.pack(pady = 12, padx=10)


root.mainloop()
