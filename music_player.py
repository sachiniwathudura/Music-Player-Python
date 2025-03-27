import pygame
import tkinter as tkr
from tkinter.filedialog import askdirectory, askopenfilename
import os, eyed3, datetime, io
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from itertools import count, cycle
from mutagen import File
from mutagen.id3 import ID3

music_player = Tk()
music_player.title("Mp3 Player")
music_player.geometry("450x600")
window_color = '#eeeeee'
music_player.configure(bg=window_color)
widgetcolor = window_color
global status
global prev
global n
global directory
n = 0


def rounded_img(ims):
    blur_radius = 0
    offset = 4
    back_color = Image.new(ims.mode, ims.size, color=widgetcolor)
    offset = blur_radius * 2 + offset
    mask = Image.new("L", ims.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle(((offset, offset), (ims.size[0] - offset, ims.size[1] - offset)), 20, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
    img_round = Image.composite(ims, back_color, mask)
    return img_round



def get_detail(selected_entry):
    global song_detail, duration
    if not selected_entry:
        print("Error: get_detail called with empty filename")
        song_detail = "No Song Selected"  # Set a default value
        duration = "00:00:00"
        return

    try:
        audiofile = eyed3.load(selected_entry)
    except Exception as e:
        print(f"Error loading file with eyed3: {e}")
        song_detail = "Error Loading Song"  # Set a default value
        duration = "00:00:00"
        return

    try:
        duration = str(datetime.timedelta(seconds=int(audiofile.info.time_secs)))
    except Exception:
        duration = '00:00:00'
    try:
        Stitle = audiofile.tag.title
        Sartist = audiofile.tag.artist
    except Exception:
        song_detail = selected_entry.replace('.mp3', '')
    else:
        if Stitle is None or Sartist is None:
            song_detail = selected_entry
        else:
            song_detail = Sartist + ' - ' + Stitle



def get_thumb(activemp3):
    global newimg, directory
    if not activemp3:
        return None

    try:
        song_loc = os.path.join(directory, activemp3)
        mp3file = ID3(song_loc)
        artwork = mp3file.get("APIC:").data
        img = Image.open(io.BytesIO(artwork))
        img = img.resize((256, 256), resample=Image.LANCZOS)
    except Exception:
        newimg = None
    else:
        newimg = rounded_img(img)
        newimg = ImageTk.PhotoImage(newimg)
        return newimg



currdir = os.path.abspath(os.path.curdir)
img0 = Image.open(currdir + "\\files\\oie_trans.gif")
img0 = img0.resize((256, 256), Image.LANCZOS)
coverart = ImageTk.PhotoImage(img0)
img1 = Image.open(currdir + "\\files\\button_black_play.png")
img1 = img1.resize((66, 66), Image.LANCZOS)
play_icon = ImageTk.PhotoImage(img1)
img2 = Image.open(currdir + "\\files\\button_black_stop.png")
img2 = img2.resize((50, 50), Image.LANCZOS)
stop_icon = ImageTk.PhotoImage(img2)
img3 = Image.open(currdir + "\\files\\button_black_pause.png")
img3 = img3.resize((66, 66), Image.LANCZOS)
pause_icon = ImageTk.PhotoImage(img3)
img4 = Image.open(currdir + "\\files\\button_black_previous.png")
img4 = img4.resize((50, 50), Image.LANCZOS)
prev_icon = ImageTk.PhotoImage(img4)
img5 = Image.open(currdir + "\\files\\button_black_next.png")
img5 = img5.resize((50, 50), Image.LANCZOS)
next_icon = ImageTk.PhotoImage(img5)
img6 = Image.open(currdir + "\\files\\button_black_load.png")
img6 = img6.resize((50, 50), Image.LANCZOS)
load_icon = ImageTk.PhotoImage(img6)
status = 'DEFAULT'
Frame0 = tkr.Frame(music_player, width=600, height=600, bg=widgetcolor)
Frame0.grid(row=1, sticky='nesw', padx=88, pady=6)
Frame11 = tkr.Frame(music_player, width=600, height=100, bg=widgetcolor)
Frame11.grid(row=2, sticky='nesw', padx=80, pady=3)
Frame1 = tkr.Frame(music_player, width=600, height=100, bg=widgetcolor)
Frame1.grid(row=3, sticky='nesw', padx=5, pady=3)
Frame2 = tkr.Frame(music_player, width=600, height=100, bg=widgetcolor)
Frame2.grid(row=4, sticky='nesw', pady=3, padx=60)
Frame3 = tkr.Frame(music_player, width=600, height=100, bg=widgetcolor)
Frame3.grid(row=5, sticky='nesw', pady=3, padx=3)
song_list = []
directory = os.popen('echo %userprofile%').read().replace('\n', '') + '\\Downloads'
os.chdir(directory)
for files in os.listdir():
    if files[-3:] == 'mp3':
        song_list.append(files)



def dbl_click(event):
    global song_detail, duration, status

    stop()
    Button1['image'] = pause_icon
    activemp3 = play_list.get(tkr.ACTIVE)
    if activemp3:  # Check if activemp3 is not empty
        pygame.mixer.music.load(activemp3)
        get_detail(activemp3)
        newimg = get_thumb(activemp3)
        var.set(song_detail)
        var1.set(duration)
        marquee_set(song_detail)
        lbl.unload()
        if newimg is None:
            lbl.load(currdir + '\\files\\mp3animtion256.gif')
        else:
            lbl['image'] = newimg
        pygame.mixer.music.play()
        status = 'PLAYED'
    else:
        print("Error: dbl_click called with no song selected")



play_list = tkr.Listbox(Frame3, width='49', height='9', font="Helvetica 12 bold", bg="#1581bf", fg="white",
                         selectbackground='#11469c', selectforeground='#000000', activestyle='none',
                         selectmode=tkr.SINGLE)
play_list.grid(row=4)
play_list.bind('<Double-1>', dbl_click)
prev = play_list.get(tkr.ACTIVE)
for item in song_list:
    pos = 0
    play_list.insert(pos, item)
    pos += 1
play_list.selection_clear(0, END)
play_list.selection_set(first=0)
play_list.see(0)
play_list.activate(0)



def load_folder():
    global directory
    play_list.delete(0, END)
    song_list = []
    directory = askdirectory()
    if directory:
        os.chdir(directory)
        for files in os.listdir():
            if files[-3:] == 'mp3':
                song_list.append(files)
        for item in song_list:
            pos = 0
            play_list.insert(pos, item)
            pos += 1
    else:
        print("Error: No directory selected")

def add_songs():
    global directory
    file_names = askopenfilename(initialdir=directory, title="Select Song", filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")), multiple=True)
    if file_names:
        for file_name in file_names:
            # Get only the filename, not the full path
            file_name_only = os.path.basename(file_name)
            if file_name_only not in play_list.get(0, END):
                song_list.append(file_name_only)
                pos = 0
                play_list.insert(pos, file_name_only)
    else:
        print("Error: No files selected")



pygame.mixer.init()
song_end = False



def play_next_auto():
    global song_end, status
    if pygame.mixer.music.get_busy():
        song_end = False
    else:
        song_end = True
        if status == 'PLAYED' or status == 'UNPAUSED':
            stop()
            Next()
    music_player.after(1000, play_next_auto)



def marquee_set(song_name):
    canvas.itemconfigure("marquee", text=song_name)



def shift():
    global canvas, fps
    x1, y1, x2, y2 = canvas.bbox("marquee")
    if (x2 < 0 or y1 < 0):
        x1 = canvas.winfo_width()
        y1 = canvas.winfo_height() // 2
        canvas.coords("marquee", x1, y1)
    else:
        canvas.move("marquee", -2, 0)
    canvas.after(1000 // fps, shift)



def play():
    play_next_auto()
    global status, curr, prev, n, newimg
    n += 1
    activemp3 = play_list.get(tkr.ACTIVE)

    curr = activemp3
    print(prev, '<####>', curr)
    print('Count : ', n)
    get_thumb(activemp3)
    get_detail(activemp3)
    if n == 1:
        Button1['image'] = pause_icon
        if activemp3: #check
            pygame.mixer.music.load(activemp3)
            var.set(song_detail)
            var1.set(duration)
            marquee_set(song_detail)
            lbl.unload()
            if newimg is None:
                lbl.load(currdir + '\\files\\mp3animtion256.gif')
            else:
                lbl['image'] = newimg
            pygame.mixer.music.play()
            status = 'PLAYED'
        else:
            print("error: nothing to play")
    elif status == 'PLAYED' or status == 'UNPAUSED':
        Button1['image'] = play_icon
        pygame.mixer.music.pause()
        lbl.unload()
        if newimg is None:
            lbl.load(currdir + '\\files\\mp3fixed256.gif')
        else:
            lbl['image'] = newimg
        status = 'PAUSED'
    elif status == 'PAUSED' and curr == prev:
        Button1['image'] = pause_icon
        pygame.mixer.music.unpause()
        lbl.unload()
        if newimg is None:
            lbl.load(currdir + '\\files\\mp3animtion256.gif')
        else:
            lbl['image'] = newimg
        status = 'UNPAUSED'
    elif status == "STOPPED" or curr != prev:
        Button1['image'] = pause_icon
        if activemp3: #check
            pygame.mixer.music.load(activemp3)
            var.set(song_detail)
            var1.set(duration)
            marquee_set(song_detail)
            lbl.unload()
            if newimg is None:
                lbl.load(currdir + '\\files\\mp3animtion256.gif')
            else:
                lbl['image'] = newimg
            pygame.mixer.music.play()
            status = 'PLAYED'
        else:
            print("error: nothing to play")
    prev = curr
    print(status)




def stop():
    lbl.load(currdir + '\\files\\mp3fixed256.gif')
    Button1['image'] = play_icon
    global status
    pygame.mixer.music.stop()
    status = 'STOPPED'
    print(status)



def Next():
    play_next_auto()
    global status, newimg
    pygame.mixer.music.stop()
    next_mp3 = ''
    for index in play_list.curselection():
        next_mp3 = play_list.get(index + 1)
        if not next_mp3:
            next_mp3 = play_list.get(0)
            play_list.selection_clear(first=index)
            play_list.selection_set(first=0)
            play_list.see(0)
            play_list.activate(0)
        else:
            play_list.selection_clear(first=index)
            play_list.selection_set(first=index + 1)
            play_list.see(index + 1)
            play_list.activate(index + 1)
        break #important
    if next_mp3:
        get_detail(next_mp3)
        Button1['image'] = pause_icon
        var.set(song_detail)
        var1.set(duration)
        marquee_set(song_detail)
        newimg = get_thumb(next_mp3)
        lbl.unload()
        if newimg is None:
            lbl.load(currdir + '\\files\\mp3animtion256.gif')
        else:
            lbl['image'] = newimg
        status = 'PLAYED'
        print('Next & Play')
        pygame.mixer.music.load(next_mp3)
        pygame.mixer.music.play()
    else:
        print("error: no next song")
        

def Prev():
    play_next_auto()
    global status, newimg
    pygame.mixer.music.stop()
    prev_mp3 = ''
    list_size = play_list.size()
    for index in play_list.curselection():
        prev_mp3 = play_list.get(index - 1)
        if not prev_mp3:
            prev_mp3 = play_list.get(list_size - 1)
            play_list.selection_clear(first=index)
            play_list.selection_set(first=list_size - 1)
            play_list.see(list_size - 1)
            play_list.activate(list_size - 1)
        else:
            play_list.selection_clear(first=index)
            play_list.selection_set(first=index - 1)
            play_list.see(index - 1)
            play_list.activate(index - 1)
        break #important
    if prev_mp3:
        get_detail(prev_mp3)
        Button1['image'] = pause_icon
        var.set(song_detail)
        var1.set(duration)
        marquee_set(song_detail)
        newimg = get_thumb(prev_mp3)
        lbl.unload()
        if newimg is None:
            lbl.load(currdir + '\\files\\mp3animtion256.gif')
        else:
            lbl['image'] = newimg
        status = 'PLAYED'
        print('Prev & Play')
        pygame.mixer.music.load(prev_mp3)
        pygame.mixer.music.play()
    else:
        print("error: no prev song")



class ImageLabel(tkr.Button):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []
        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)
        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100
        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)




lbl = ImageLabel(Frame0, width=256, height=256, highlightthickness=0, relief=FLAT, bd=0, bg=widgetcolor)
lbl.grid(row=1, padx=10)
lbl.load(currdir + '\\files\\sound-8563_256.gif')
var1 = tkr.StringVar()
Label1 = tkr.Label(Frame11, font=("Helvetica 12 bold"), textvariable=var1, bg=widgetcolor)
Label1.grid(row=1, padx=110)
Button1 = tkr.Button(Frame2, text="", image=play_icon, bg=widgetcolor, borderwidth=0)
Button1['command'] = play
Button1.grid(row=2, column=3, padx=5)
Button2 = tkr.Button(Frame2, text="", image=stop_icon, command=stop, bg=widgetcolor, borderwidth=0)
Button2.grid(row=2, column=5, padx=5)
Button3 = tkr.Button(Frame2, text="", image=prev_icon, command=Prev, bg=widgetcolor, borderwidth=0)
Button3.grid(row=2, column=2, padx=12)
Button4 = tkr.Button(Frame2, text="", image=next_icon, command=Next, bg=widgetcolor, borderwidth=0)
Button4.grid(row=2, column=4, padx=5)
Button5 = tkr.Button(Frame2, text="", image=load_icon, command=load_folder, bg=widgetcolor, borderwidth=0)
Button5.grid(row=2, column=1, padx=5)
Button6 = tkr.Button(Frame2, text="Add Songs", command=add_songs, bg=widgetcolor, borderwidth=0)  # Add Button
Button6.grid(row=2, column=6, padx=5)
var = tkr.StringVar()
canvas = Canvas(Frame1, bg=widgetcolor, highlightthickness=0)
canvas.grid(row=1)
text_var = ''
text = canvas.create_text(0, -2000, text=text_var, font=('consolas', 20, 'bold'), fill='#460157', tags=("marquee",),
                    anchor='w')
x1, y1, x2, y2 = canvas.bbox("marquee")
width = x2 - x1
height = y2 - y1
canvas['width'] = '440'
canvas['height'] = height
fps = 40
shift()
marquee_set('Python Music Player')
var1.set('00:00:00')
music_player.mainloop()

