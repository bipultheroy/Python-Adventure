import os
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import time
import threading
from pygame import mixer
from mutagen.mp3 import MP3
from tkinter import ttk
from ttkthemes import ThemedTk

root = ThemedTk(theme="radiance")

statusbar = ttk.Label(root, text="Welcome to Pymusic", relief=SUNKEN, anchor=W, font='Times 15 bold')
statusbar.pack(side=BOTTOM, fill=X)

# Create a menubar
menubar = Menu(root)
root.config(menu=menubar)


def browse_file():
    global file_path
    file_path = filedialog.askopenfilename()
    add_to_playlist(file_path)

# playlist - contains the full path + filename
# playlistbox - contains just the filename

playlist = []


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, file_path)
    index += 1


# Create submenu
submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Pymusic', 'This is the simplest music player using python.')


submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="Update")
submenu.add_command(label="About us", command=about_us)

mixer.init()  # initializing the mixer

root.title("PyMusic")
root.iconbitmap(r'E:\Python-Adventure\icon\Pymusic.ico')
# root.geometry('500x500')
root.resizable(0, 0)

lengthlabel = ttk.Label(root, text='Music Length : --:--')
lengthlabel.place(relx=.5, rely=.5,anchor='center')
lengthlabel.pack(pady=5)

currtimelabel = ttk.Label(root, text='Current time : --:--', relief=GROOVE)
currtimelabel.pack(pady=5)

leftframe = Frame(root)
leftframe.pack(side='left', padx=30, pady=30)

playlistbox = Listbox(leftframe)
playlistbox.pack()

rightframe = Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

addbutton = ttk.Button(leftframe, text="+ Add", command=browse_file)
addbutton.pack(side='left')

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)


delbutton = ttk.Button(leftframe, text="- Del", command=del_song)
delbutton.pack(side='left')


# show music details
def show_music_details(playsong):
    filedata = os.path.splitext(playsong)

    if filedata[1] == '.mp3':
        audio = MP3(playsong)
        totallength = audio.info.length
    else:
        a = mixer.Sound(playsong)
        totallength = a.get_length()

    # div = total_length/60, mod = totallength % 60
    mins, secs = divmod(totallength, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Music Length: " + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(totallength,))
    t1.start()


def start_count(t):
    global paused
    currenttime = 0
    # mixer.music.get_busy() - Returns false when press stop
    while currenttime <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(currenttime, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currtimelabel['text'] = "Current time: " + ' - ' + timeformat
            time.sleep(1)
            currenttime += 1


# play the music
def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music resumed"
        paused = False
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            playit = playlist[selected_song]
            mixer.music.load(playit)
            mixer.music.play()
            statusbar['text'] = "Music is playing" + ' ' + os.path.basename(playit)
            show_music_details(playit)
        except:
            tkinter.messagebox.showerror('Invalid File',
                                         "You haven't selected a file or the file format is not supported!")


paused = False


# Pause the music
def pause_music():
    global paused
    paused = True
    mixer.music.pause()
    statusbar['text'] = "Music paused"


# stop the music
def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music stopped"


# Pause the music
def rewind_music():
    play_music()
    statusbar['text'] = "Music rewind"


muted = False


# Mute the music
def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        volumebutton.configure(image=volume_icon)
        volume.set(70)
        muted = False

    else:  # mute the music
        mixer.music.set_volume(0)
        volumebutton.configure(image=mute_icon)
        volume.set(0)
        muted = True


# control volume
def set_vol(val):
    # pygame has 0 as minimum and 1 as maximum volume
    vol = float(val) / 100
    mixer.music.set_volume(vol)


middleframe = Frame(rightframe)
middleframe.pack(pady=30, padx=30)

play_icon = PhotoImage(file='E:\Python-Adventure\controller\play.png')
playbutton = ttk.Button(middleframe, image=play_icon, command=play_music)
playbutton.grid(row=0, column=0, padx=10)

stop_icon = PhotoImage(file='E:\Python-Adventure\controller\stop.png')
stopbutton = ttk.Button(middleframe, image=stop_icon, command=stop_music)
stopbutton.grid(row=0, column=1, padx=10)

pause_icon = PhotoImage(file='E:\Python-Adventure\controller\pause.png')
pausebutton = ttk.Button(middleframe, image=pause_icon, command=pause_music)
pausebutton.grid(row=0, column=2, padx=10)

bottomframe = Frame(rightframe)
bottomframe.pack()

rewind_icon = PhotoImage(file='E:\Python-Adventure\controller\_rewind.png')
rewindbutton = ttk.Button(bottomframe, image=rewind_icon, command=rewind_music)
rewindbutton.grid(row=0, column=0)

mute_icon = PhotoImage(file='E:\Python-Adventure\controller\mute.png')
volume_icon = PhotoImage(file='E:\Python-Adventure\controller/volume.png')
volumebutton = ttk.Button(bottomframe, image=volume_icon, command=mute_music)
volumebutton.grid(row=0, column=1, padx=10)

volume = ttk.Scale(bottomframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
volume.set(70)  # Default volume
mixer.music.set_volume(0.7)
volume.grid(row=0, column=2, pady=15, padx=10)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
