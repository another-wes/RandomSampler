import tkinter, tkinter.constants, tkinter.filedialog, tkinter.messagebox, os, pyaudio, random, sys, time, wave
from pygame import mixer
class SamplerWindow(tkinter.Frame):

  def __init__(self, root):

    tkinter.Frame.__init__(self, root)
    # options for buttons
    button_opt = {'fill': tkinter.constants.BOTH, 'padx': 5, 'pady': 5}
    self.sounds=[]
    self.stream=None
    self.directory=""
    self.file=""
    # define buttons
    tkinter.Button(self, text='Select Root Directory', command=self.askdirectory).pack(**button_opt)
    #tkinter.Button(self, text='Load Your Own Sound', command=self.askopenfile).pack(**button_opt) No reason
    #tkinter.Button(self, text='Save Something?', command=self.asksaveasfile).pack(**button_opt)   No current purpose
    tkinter.Button(self, text='Random Sample', command=self.randomsound).pack(**button_opt)
    tkinter.Button(self, text='Preview Sample', command=self.previewsound).pack(**button_opt)
    tkinter.Button(self, text='Stop Preview', command=self.stoppreview).pack(**button_opt)
    #weird text stuff
    fileName = tkinter.StringVar()
    self.yourFile = tkinter.Entry(root, textvariable=fileName)
    self.yourFile.grid(column=0,row=0,sticky='EW')
    self.yourFile.update()
    self.yourFile.focus_set()
    self.yourFile.pack(padx = 20, pady = 20,anchor='n')
    self.yourFile.place(y = 100, x = 20, width = 720, height = 22)
    #weird text stuff ends
    # define options for opening or saving a file
    self.file_opt = options = {}
    options['defaultextension'] = '.wav'
    options['filetypes'] = [('mp3 files', '.mp3'), ('wav files', '.wav')]
    options['initialdir'] = 'C:\\Program Files (x86)\Image-Line\FL Studio 10\Data\Patches\Packs\Legacy\HipHop'
    options['initialfile'] = 'HIP_Hat_6.wav'
    options['parent'] = root
    options['title'] = 'The Selector'

    # This is only available on the Macintosh, and only when Navigation Services are installed.
    #options['message'] = 'message'

    # if you use the multiple file version of the module functions this option is set automatically.
    #options['multiple'] = 1

    # defining options for opening a directory
    self.dir_opt = options = {}
    options['initialdir'] = 'C:\\Program Files (x86)\Image-Line\FL Studio 10\Data\Patches\Packs\Legacy'
    options['mustexist'] = True
    options['parent'] = root
    options['title'] = 'This is a title'
    self.playing = 0 #0=none; 1=wav; 2=mp3

  def askopenfile(self):
    self.file=tkinter.filedialog.askopenfilename(mode='r', **self.file_opt)
    return self.file

  def previewsound(self):
    if len(self.file)>3:
        if self.file.endswith(".wav"):
            self.playing = 1
            sound = wave.open(self.file)
            p = pyaudio.PyAudio()
            chunk = 1024
            self.stream = p.open(format =
                p.get_format_from_width(sound.getsampwidth()),
                channels = sound.getnchannels(),
                rate = sound.getframerate(),
                output = True)
            data = sound.readframes(chunk)
            while data != '':
                self.stream.write(data)
                data = sound.readframes(chunk)
            self.stream.stop_self.stream()
            self.playing = 0
            self.stream.close()
            p.terminate()
        elif self.file.endswith(".mp3"):
            self.playing=2
            mixer.init()
            mixer.music.load(self.file)
            mixer.music.play()
            
  def stoppreview(self):
    if self.playing==1:
        self.stream.stop_self.stream()
        self.stream.close()
        p.terminate()
    elif self.playing==2:
        mixer.music.stop()

  def asksaveasfile(self):
    return tkinter.filedialog.asksaveasfile(mode='w', **self.file_opt)

  def randomsound(self):
    if (len(self.sounds)==0): tkinter.messagebox.showinfo("Error", "Directory Not Selected")
    else:
        self.yourFile.delete(0, tkinter.constants.END)
        self.file=random.choice(self.sounds) # get filename
        self.yourFile.insert(tkinter.constants.INSERT, self.file)
        print(self.file)

  def askdirectory(self):
    """Returns a selected directoryname."""
    name = tkinter.filedialog.askdirectory(**self.dir_opt)
    sounds=[]
    for root in [x[0] for x in os.walk(name)]:
        for filename in os.listdir(root):
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                sounds.append(os.path.abspath(root)+"\\"+filename)
    self.directory=name
    self.sounds=sounds 
    print("Directory:",name)
    return name

if __name__=='__main__':
  root = tkinter.Tk()
  root.geometry('760x300')
  root.update()
  SamplerWindow(root).pack()
  root.mainloop()
