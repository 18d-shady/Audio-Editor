from pydub import AudioSegment 
from pydub.playback import play
from pydub import effects
import tkinter as tk
from tkinter import ttk, font
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from RangeSlider.RangeSlider import RangeSliderH 
from PIL import Image
from PIL import ImageTk
from pygame import mixer
import time
from datetime import datetime
import os


#AudioSegment.ffmpeg = "C:\FFmpeg\bin"
mixer.init()
file_index = 0
file_type = ['.wav', '.mp3', '.aac', '.m4a', '.wma', '.ogg']
selected = ''
sound = ''
togglePlay = 1
dura = 0
proportion = 0
counter = 0
toggleTrim = 0
volVar = 70
fadeVal1 = 0
fadeVal2 = 0
filtVar = 80
oldSpeedVar = 1.0
toogleHighlight = 0
speedDict = {}
volDict = {}
dictVar = 0

def homeWin(root):
    global selected
    # Add image file 
    #bgimg = tk.PhotoImage(file='homebg.ppm')
    #limg= tk.Label(root, image=bgimg)
    #limg.pack()
    #img = Image.open("homebg.png")
    #homebg = ImageTk.PhotoImage(img)

    #canvas = tk.Canvas(root, width=img.size[0]+20, height=img.size[1]+20)
    #canvas.create_image(10, 10, anchor=tk.NW, image=homebg)
    #canvas.pack(fill=tk.BOTH, expand=1)
    
    homepg = tk.Frame(root, bg = "black")
    homepg.pack(expand=True)

    HeadinFont = font.Font( family = "Comic Sans MS",  
                                 size = 20,  
                                 weight = "bold")

    buttonFont = font.Font( family = "Helvetica",  
                                 size = 15,  
                                 weight = "normal")

    tk.Label(root, text='Audio Editor', fg='#2b2929', bg="#bfafae", font=HeadinFont).place(x=20, y=20)
    btn = tk.Button(homepg, text = 'New Project', font=buttonFont, bd=1, width=15, height=2, bg="#2b2929", fg="white", command=lambda: changepage()) 
 
    # Set the position of button on the top of window.   
    btn.pack(side = 'top')

    uhomepg = tk.Frame(root, bg = "#2b2929")
    uhomepg.place(relx=0, rely=.7, relheight=.3, relwidth=1) 

    
def select_file():
    #1. M4A audio file type FLAC MP3 MP4 WAV WMA AAC OGG.
    filetypes = (('Audio Files', '.mp3 .wav .aac .m4a .wma .ogg'),)
    
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='C:/Music/',
        filetypes=filetypes)
    
    selected = filename
    print(selected)
    

    """
    showinfo(
        title='Selected File',
        message=filename
    )
    """
    return selected

def loadChanges(audio, sound):
    global dura, proportion, musicPos
    mixer.music.load(audio)
    mixer.music.play()
    mixer.music.pause()

    #get the sound duration and display it
    dura = sound.duration_seconds
    duration = time.strftime("%M:%S", time.gmtime(dura))
    tk.Label(menFrame, text=duration, bg="black", fg="white").grid(row=0, column=2, sticky='NW')#pack(side=tk.LEFT, pady=150)

    #return the bar to zzero
    proportion = 0
    musicPos.set(proportion)

def updateLabel():
    global labelFrame, dura, proportion

    #update the proprotion label
    try:
        lab = labelFrame.winfo_children()
    except tk.TclError:
        return

    for i in lab:
        i.place_configure(relx=proportion/100)
        i.configure(text=time.strftime("%M:%S", time.gmtime(proportion/100*dura)))

    root.after(100, updateLabel)
    
    
    


def apply():
    global extensionn, sound, newAudio, sounde, soundp, sounda

    #to add the sound back
    if soundp == '' and sounda != '':
        sound = sounde + sounda
    elif sounda == '' and soundp != '':
        sound = soundp + sounde
    elif soundp == '' and sounda == '':
        sound = sounde
    elif soundp != '' and sounda != '':
        sound = soundp + sounde + sounda
    #save the new trimmed audio as sound
    
    #os.remove(os.getcwd()+'/'+newAudio)
    mixer.music.unload()
    sound.export(newAudio, format='wav')

def arrangee(firstDura):
    global editpg, newAudio, highlighter, musicBar, sticks, dura

    try:
        #get the postion of the highlighted sound
        thewidth = float(highlighter.place_info()['relwidth'])
        #get the position of the highlighted clip
        delPos = float(highlighter.place_info()['relx'])
    except NameError:
        return
    except tk.TclError:
        return
        
    

    #get the end of the highlighted clip
    delPosend = delPos+thewidth
    print(delPosend)

    #get the percentage increase or decrease
    duraDiff = dura - firstDura
    duraChange = duraDiff/firstDura
    #the new scale after the deleted music
    newScale = 1 + duraChange

    for i in sticks:
        #get the relx position of each of the splits
        #relxx = float(i.place_info()['relx'])
        relxx = i.winfo_x()/musicBar.winfo_width()
        print(relxx)

        #if the stick is same as the end of the clip add the increase or decrease
        #else donot
        if relxx >= delPosend:
            #print(i.place_info()['relx'])
            i.place_configure(relx=(relxx+duraChange)/newScale)
        else:
            i.place_configure(relx=relxx/newScale)


def playy(toggleB=1):
    global selected, togglePlay, dura, proportion, musicPos

    #add a toogle that wont toggle unless the button is pressed
    #no matter how many times the function loops itself
    if toggleB == 0:
        if togglePlay == 0:
            togglePlay = 1
            mixer.music.pause()
        else:
            togglePlay = 0
            mixer.music.unpause()
            
            
    
    #increase the toggle when the music is playing and recall the function
    if togglePlay == 0:
        proportion += 1 #int(1/100 * dura)
        #root.update_idletasks()
        musicPos.set(proportion)
        
        #print(proportion)
        if proportion <= 100:
            root.after(int(1/100*dura*1000), playy)
        

def motion(event):
    global togglePlay, dura, proportion, musicPos, highlighter
    #check if the highlighter ison and remove it
    try:
        highlighter.destroy()
    except NameError:
        pass
    #reset the proportion
    proportion = (event.x / event.widget.winfo_width()) * 100
    musicPos.set(proportion)
    print(proportion)
    mixer.music.play(start=proportion/100*dura)
    if togglePlay == 1:
        mixer.music.pause()
        #togglePlay = 1
        #playy(0)
    #print(musicPos)
        
def removeHighlight(event):
    global toogleHighlight
    
    event.widget.destroy()
    toogleHighlight = 0
    
def highlight(event):
    global toogleHighlight, musicBar, highlighter, leftp, rightp, sticks, clickPos
    #to unhighlight if hilighted already
    #if highlighter in locals() or highlighter in globals():
    try:
        highlighter.destroy()
    except UnboundLocalError:
        pass
    except NameError:
        pass

    if toogleHighlight == 0:
        toogleHighlight = 1
            
        #get the position of the mouse onclick
        clickPos = event.x / event.widget.winfo_width()
        print(clickPos)
        #save all the splits in a list
        sticks = event.widget.winfo_children()
    
        #save all their positions in a list too
        #save the splits position before and after the click
        sticksPosmin = [i.winfo_x()/event.widget.winfo_width() for i in sticks if i.winfo_x()/event.widget.winfo_width() < clickPos ]
        sticksPosmax = [i.winfo_x()/event.widget.winfo_width() for i in sticks if i.winfo_x()/event.widget.winfo_width() > clickPos ]

        print(sticksPosmin, sticksPosmax)

        print(sticks)

        #find the left and right highlighting position
        try:
            leftp = min(sticksPosmin, key=lambda x:abs(x-clickPos))
        except ValueError:
            leftp = 0

        try:
            rightp = min(sticksPosmax, key=lambda x:abs(x-clickPos))
        except ValueError:
            rightp = 1
        print(leftp, rightp)

        #place the highlighter and then set it to remove once clicked
        highlighter = tk.Frame(musicBar, bg='', highlightthickness=2, highlightbackground='red')
        highlighter.place(relx=leftp, rely=.5, anchor="w", relwidth=rightp-leftp, relheight=1)
        highlighter.bind('<B1-Motion>', removeHighlight)
        highlighter.bind("<Button 1>", removeHighlight)
        highlightSounds()
    
    else:
        toogleHighlight = 0

        #save the begining seconds of split in a dictionary witht the values being the sounds
        #then sort the list
        #along with the list of the children of the musicBar

def highlightSounds():
    global leftp, rightp, sound, sounde, sounda, soundp, dura, leftPoint, rightPoint

    #this function is for when editing highlighted sounds

    try:
        #point = round(proportion/100*dura*1000)
        rightPoint = rightp*dura*1000
        leftPoint = leftp*dura*1000

        #slicing the sounds based on the highlighted for editing
        if leftp == 0 and rightp != 1:
            
            sounde = sound[0:rightPoint]
            sounda = sound[rightPoint:dura*1000]
            soundp = ''

        elif leftp != 0 and rightp != 1:
            sounde = sound[leftPoint:rightPoint]
            sounda = sound[rightPoint:dura*1000]
            soundp = sound[0:leftPoint]

        elif leftp != 0 and rightp == 1:
            sounde = sound[leftPoint:dura*1000]
            sounda = ''
            soundp = sound[0:leftPoint]

        elif leftp == 0 and rightp == 1:
            sounde =  sound
            sounda = ''
            soundp = ''

    #but if nothing is highlighted then select the full sound
    except NameError:
        sounde =  sound
        sounda = ''
        soundp = ''
        

    #create dictionaries for volume and for speed
    #change value of volume based on highlight
    recheckDict()

        
        
def splitAction():
    global proportion, musicBar

    #getting the seconds from the proportion of the progressbar
    #slicing the progress bar
    marker = tk.Frame(musicBar, width=1.5, bg='black')
    marker.place(relx=proportion/100, rely=.5, anchor="w", relheight=1)

    #now to the main splitting of the sounds
    #we do not actually need to split the sounds, we just need to split it when
    #we want to handle some part and then rejoin it at the end
    print(proportion)
    print(musicBar)

    
    
def trimAction():
    global editpg, toggleTrim, hSlider, sound, newAudio, sounde, dura

    if toggleTrim == 0:
        toggleTrim = 1
        #get the highlighted sound
        highlightSounds()
        #the double slider values
        hLeft = tk.DoubleVar(value = 0)  
        hRight = tk.DoubleVar(value = sounde.duration_seconds)
        #to input a double slider with two difffernt slide
        hSlider = RangeSliderH(menFrame, [hLeft, hRight], Width=400, Height=60, bgColor='black', font_color='white', font_size=8, min_val=0, max_val=sounde.duration_seconds, padX=52, bar_radius=5, valueSide='BOTTOM', suffix='s')
        hSlider.grid(row=0, column=1)
        #hSlider.forceValues([0, sounde.duration_seconds])
    #then trim it now
    elif toggleTrim == 1:
        toggleTrim = 0
        point1, point2 = hSlider.getValues()
        #start = round(point1/100*sounde.duration_seconds*1000)
        #end = round(point2/100*sounde.duration_seconds*1000)
        start = point1*1000
        end = point2*1000
        #print(start, end)
        sounde = sounde[start:end]
        
        #get the sound duration before you apply
        firstDura = dura
        apply()
        
        #load the music once again
        loadChanges(newAudio, sound)
        #arrange the clips because the duration has changed
        arrangee(firstDura)
        hSlider.destroy()

def duplicateAction():
    global sticks, sound, sounde, newAudio, highlighter, musicBar

    highlightSounds()
    sounde = sounde * 2

    try:
        #get the widthof the highlighted clip
        thewidth = float(highlighter.place_info()['relwidth'])
        
        #get the position of the highlighted clip
        dupliPos = float(highlighter.place_info()['relx'])

    except NameError:
        thewidth = 1
        dupliPos = 0
        
    except tk.TclError:
        return

    #get the end of the highlighted clip
    dupliPosend = dupliPos+thewidth
    print(dupliPosend)

    #the new scale after the highlighted clip has been duplicated
    newScale = 1 + thewidth
    try:
        for i in sticks:
            #get the relx position of each of the splits
            #relxx = float(i.place_info()['relx'])
            relxx = i.winfo_x()/musicBar.winfo_width()
            if relxx > dupliPosend:
                #print(i.place_info()['relx'])
                i.place_configure(relx=(relxx+thewidth)/newScale)
            else:
                i.place_configure(relx=relxx/newScale)
    except NameError:
        pass
    # check if it is the last clip
    if dupliPosend >= 1:
        dmarker = tk.Frame(musicBar, width=1.5, bg='black')
        dmarker.place(relx=1/newScale, rely=.5, anchor="w", relheight=1)

    else:
        dmarker = tk.Frame(musicBar, width=1.5, bg='black')
        dmarker.place(relx=(dupliPosend+thewidth)/newScale, rely=.5, anchor="w", relheight=1)
    
    
    apply()
        
    #load the music once again
    loadChanges(newAudio, sound)

def recheckDict():
    global oldvVar, sounde, volSlider, speedSlider, oldSpeedVar, dictVar

    if dictVar == 1:
        pass
    else:
        oldvVar = 70
        
        for keys in volDict:
            if volDict[keys] == sounde:
                oldvVar = keys
                
        volSlider.set(oldvVar)

        oldSpeedVar = 1.0

        #save the speeds in a dicionary and check to see if it has been saved already
        for keys in speedDict:
            if speedDict[keys] == sounde:
                oldSpeedVar = keys

        #print(oldSpeedVar)
        speedSlider.set(oldSpeedVar)
    
def volumeAction():
    global editpg, volVar, newAudio, sounde, oldvVar, volSlider

    volFrame = tk.Frame(editpl, bg='black', highlightthickness=1, highlightbackground='white')
    volFrame.grid(row=1, column=1, pady=10, padx=5)

    #tk.Label(volFrame, text="Volume", bg="black", fg="white").grid(row=0, column=0, sticky="NSWE")

    def donee():
        global sound, volVar, sounde, oldvVar, volSlider, dictVar
        #create a variable that controls the recheck volume function
        dictVar = 1
        #get the highlighted sound
        highlightSounds()
        print(volVar)
        volVar = volSlider.get()
        print(volVar)
        #increase or decrease the volume based on the previous volume value
        newVal = volVar - oldvVar
        sounde = sounde + newVal
        #add a new value into the dictionary
        volDict[volVar] = sounde
        print(volDict)

        apply()
        
        #load the music once again
        loadChanges(newAudio, sound)
        #volFrame.destroy()
        dictVar = 0
        

    done = tk.Button(volFrame, text="Done", bd=2, bg="black", fg="white", command=lambda: donee())
    done.grid(row=0, column=1, padx=10, sticky='NW')

    volSlider = tk.Scale(volFrame, from_=0, to=100, label="Volume", orient=tk.HORIZONTAL, length=300, fg='grey', bg='black', bd=0)
    volSlider.grid(row=0, column=0, sticky="NW")
    #create a variable that controls the recheck volume function

    #oldvVar = 70

    

def fadeAction():
    global sound, extensionn, fadeVal1, fadeVal2, newAudio

    fadeFrame = tk.Frame(editpl, bg='black', highlightthickness=1, highlightbackground='white')
    fadeFrame.grid(row=0, column=1, pady=10, padx=5, sticky=tk.W)

    #tk.Label(volFrame, text="Volume", bg="black", fg="white").grid(row=0, column=0, sticky="NSWE")

    def donef():
        global sound, fadeVal1, fadeVal2, sounde
        oldVar1 = fadeVal1
        oldVar2 = fadeVal2
        fadeVal1 = fadeSlider2.get()
        fadeVal2 = fadeSlider2.get()
        #get the highlighted sound
        highlightSounds()
        
        try:
            sounde = sounde.fade_in(fadeVal1*1000)
            sounde = sounde.fade_out(fadeVal2*1000)
        except TypeError:
            pass
            #fadeFrame.destroy()

        apply()
        
        #load the music once again
        loadChanges(newAudio, sound)
        #fadeFrame.destroy()
        

    done = tk.Button(fadeFrame, text="Done", bd=2, bg="black", fg="white", command=lambda: donef())
    done.grid(row=0, column=2, padx=10, sticky='NW')

    fadeSlider1 = tk.Scale(fadeFrame, from_=0, to=10, label="Fade In", orient=tk.HORIZONTAL, length=100, fg='grey', bg='black', bd=0)
    fadeSlider1.grid(row=0, column=0, padx=20, sticky="NW")
    fadeSlider1.set(fadeVal1)

    fadeSlider2 = tk.Scale(fadeFrame, from_=0, to=10, label="Fade Out", orient=tk.HORIZONTAL, length=100, fg='grey', bg='black', bd=0)
    fadeSlider2.grid(row=0, column=1, padx=20, sticky="NW")
    fadeSlider2.set(fadeVal2)
    
    
def filtAction():
    global sound, editpg, newAudio, filtVar

    filtFrame = tk.Frame(editpl, bg='black', highlightthickness=1, highlightbackground='white')
    filtFrame.grid(row=2, column=1, pady=10, padx=5)

    

    def donee():
        global sound, filtVar, sounde

        filtVar = filtSlider.get()
        
        #get the highlighted sound
        highlightSounds()

        #the two filters should be inverse of each other and have separate values
        sounde = sounde.high_pass_filter(filtVar+100)

        sounde = sounde.low_pass_filter((1/filtVar)*30000)

        apply()
        loadChanges(newAudio, sound)
    
        #filtFrame.destroy()
        

    done = tk.Button(filtFrame, text="Done", bd=2, bg="black", fg="white", command=lambda: donee())
    done.grid(row=0, column=1, padx=10, sticky='NW')

    filtSlider = tk.Scale(filtFrame, from_=0, to=100, label="Filter", orient=tk.HORIZONTAL, length=300, fg='grey', bg='black', bd=0)
    filtSlider.grid(row=0, column=0, sticky="NW")
    filtSlider.set(filtVar)

def overlayAction():
    global editpg, sound, extensionn, newAudio, newSoundo

    #get the sound from the file
    newSelected = select_file()
    try:
        newSoundo = AudioSegment.from_file(newSelected)
    except FileNotFoundError:
        return 
    

    overFrame = tk.Frame(editpl, bg='black', highlightthickness=1, highlightbackground='white')
    overFrame.grid(row=5, column=1)

    def finallydone():
        global sound, dura, newSoundo, newAudio, minSpin, secSpin, millSpin, checkVar

        #chose what minute seconds and milliseconds the song should start overlaying from
        mins = int(minSpin.get())
        mins = mins * 60

        secs = int(secSpin.get())
        mills = int(millSpin.get())

        overall = (mins + secs) * 10
        overall = (overall + mills) * 100

        #print(overall)
        #overlay the sound and then loop if the it is checked
        trimMain = sound[overall:dura*1000]
        if checkVar == 0:
            trimMain = trimMain.overlay(newSoundo)
        else:
            trimMain = trimMain.overlay(newSoundo, loop=True)
            
        untrimMain = sound[0:overall]
        sound = untrimMain + trimMain

        #instead of apply use the normal way because apply might not work
        #apply()
        mixer.music.unload()
        sound.export(newAudio, format='wav')
        loadChanges(newAudio, sound)
    
        overFrame.destroy()
        

    def donee():
        global newSoundo
        #trim the overlaying sound
        point1, point2 = hSlidero.getValues()
        start = point1*1000
        end = point2*1000
        #print(start, end)
        newSoundo = newSoundo[start:end]

        noooo()

    def noooo():
        global dura, minSpin, secSpin, millSpin, checkVar
        
        hSlidero.destroy()
        trimBt.destroy()
        noBt.destroy()

        
        tk.Label(overFrame, text='Choose What Seconds to Overlay From', bg="black", fg="white").grid(row=0, column=0)

        done = tk.Button(overFrame, text="Done", bd=2, bg="black", fg="white", command=lambda: finallydone())
        done.grid(row=0, column=1, padx=10, sticky='NW')

        overInner = tk.Frame(overFrame, bg='black')
        overInner.grid(row=1, column=0, pady=10)
        
        tk.Label(overInner, text='Minute: ', bg="black", fg="white").grid(row=0, column=0)
        mins = int(dura/60)
        minSpin = tk.Spinbox(overInner, from_=0, to=mins, width=5)
        minSpin.grid(row=0, column=1)

        tk.Label(overInner, text='Seconds: ', bg="black", fg="white").grid(row=0, column=2)
        secSpin = tk.Spinbox(overInner, from_=0, to=60, width=5)
        secSpin.grid(row=0, column=3)

        tk.Label(overInner, text='Milliseconds: ', bg="black", fg="white").grid(row=0, column=4)
        millSpin = tk.Spinbox(overInner, from_=0, to=10, width=5)
        millSpin.grid(row=0, column=5)

        checkVar = tk.IntVar()
        loopB = tk.Checkbutton(overFrame, text="Loop Overlayed Music when it finishes", variable=checkVar, onvalue=1, offvalue=0, bg='black', fg='white', selectcolor='black')
        loopB.grid(row=2, column=0)
        

    tk.Label(overFrame, text='Trim Sound?', bg="black", fg="white").grid(row=0, column=0)
    
    trimBt = tk.Button(overFrame, text="Trim", bd=2, bg="black", fg="white", command=lambda: donee())
    trimBt.grid(row=0, column=1, padx=10, sticky='NW')
    noBt = tk.Button(overFrame, text="No", bd=2, bg="black", fg="white", command=lambda: noooo())
    noBt.grid(row=0, column=2, padx=3, sticky='NW')
    #the double slider values
    hLefto = tk.DoubleVar(value = 0)  
    hRighto = tk.DoubleVar(value = newSoundo.duration_seconds)
    #to input a double slider with two difffernt slide
    hSlidero = RangeSliderH(overFrame, [hLefto, hRighto], Width=400, Height=60, bgColor='black', font_color='white', font_size=8, min_val=0, max_val=newSoundo.duration_seconds, padX=52, bar_radius=5, valueSide='BOTTOM', suffix='s')
    hSlidero.grid(row=1, column=0)
    #hSlidero.forceValues([0, newSoundo.duration_seconds])

    


def speed_change(sound, speed=1.0):
    # Manually override the frame_rate. This tells the computer how many
    # samples to play per second
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })

    # convert the sound with altered frame rate to a standard frame rate
    # so that regular playback programs will work right. They often only
    # know how to play audio at standard frame rate (like 44.1k)
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)

def speedAction():
    global sound, editpg, newAudio, speedVar, oldSpeedVar, aVar, sounde, speedSlider

    speedFrame = tk.Frame(editpl, bg='black', highlightthickness=1, highlightbackground='white')
    speedFrame.grid(row=4, column=1, pady=10, padx=5)

    

    def donee():
        global sound, speedVar, oldSpeedVar, aVar, sounde, dura, dictVar

        dictVar = 1
        #get the highlighted sound
        highlightSounds()
        speedVar = speedSlider.get()

        if oldSpeedVar != 1.0:
            #to return the speed get the inverse of old speedvar
            sounde = speed_change(sounde, 1/oldSpeedVar)
        
        #oldSpeedVar = speedVar

        if aVar == 0:
            if speedVar > 1:
                sounde = sounde.speedup(speedVar)
            else:
                sounde = speed_change(sounde, speedVar)
        else:
            sounde = speed_change(sounde, speedVar)
            
        speedDict[speedVar] = sounde
        print(speedDict)
        #get the sound duration before you apply
        firstDura = dura
        apply()
        loadChanges(newAudio, sound)
        #arrange the clips because the duration has changed
        arrangee(firstDura)
    
        #speedFrame.destroy()
        dictVar = 0
        

    done = tk.Button(speedFrame, text="Done", bd=2, bg="black", fg="white", command=lambda: donee())
    done.grid(row=0, column=1, padx=10, sticky='NW')

    speedVar = tk.DoubleVar()
    speedSlider = tk.Scale(speedFrame, from_=0.0, to=10.0, label="Speed", orient=tk.HORIZONTAL, tickinterval = 0.25, resolution=0.25, length=300, fg='grey', bg='black', bd=0)
    speedSlider.grid(row=0, column=0, sticky="NW")
    #oldSpeedVar = 1.0
    
    #print(sounde)

    
    
    aVar = tk.IntVar()
    alvinB = tk.Checkbutton(speedFrame, text="Alvin&Chipmunks Effect", variable=aVar, onvalue=1, offvalue=0, bg='black', fg='white', selectcolor='black')
    alvinB.grid(row=1, column=0)

def swapAction():
    global editpg, sound, newAudio, highlighter, musicBar, sticks, lspoint, rspoint

    #get the highlighted sound
    highlightSounds()

    try:
        #get the postion of the highlighted sound
        thewidth = float(highlighter.place_info()['relwidth'])
    except NameError:
        return
    except tk.TclError:
        return
        
    #get the position of the highlighted clip
    swapPos = float(highlighter.place_info()['relx'])

    #get the end of the highlighted clip
    swapPosend = swapPos+thewidth
    print(swapPosend)

    #get the former sounds
    lspoint = leftPoint
    rspoint = rightPoint

    # to use the delay function, we have to create a new function
    def swapAction2(thewidth, swapPos, swapPosend):
        global editpg, sound, dura, sounde, sounda, soundp, newAudio, highlighter, musicBar, sticks, leftPoint, rightPoint, lspoint, rspoint

        nextAction.destroy()
        #get the highlighted sound
        highlightSounds()

        
        try:
            #get the postion of the highlighted sound
            thewidth2 = float(highlighter.place_info()['relwidth'])
        except NameError:
            return
        except tk.TclError:
            return
        
        #get the position of the highlighted clip
        swapPos2 = float(highlighter.place_info()['relx'])

        #get the end of the highlighted clip
        swapPosend2 = swapPos2+thewidth2

        if swapPosend > swapPosend2:
            #get the former sounds
            if soundp == '' and sounda != '':
                sounde = sound[lspoint:rspoint]+sound[0:lspoint]+sound[rspoint:dura*1000]
            elif sounda == '' and soundp != '':
                pass
            elif soundp == '' and sounda == '':
                pass
            elif soundp != '' and sounda != '':
                sounde = sound[0:leftPoint]+sound[lspoint:rspoint]+sound[leftPoint:lspoint]+sound[rspoint:dura*1000]

        elif swapPosend < swapPosend2:
            #get the former sounds
            if soundp == '' and sounda != '':
                pass
            elif sounda == '' and soundp != '':
                sounde = sound[0:lspoint]+sound[rspoint:leftPoint]+sound[lspoint:rspoint]+sound[leftPoint:rightPoint]
            elif soundp == '' and sounda == '':
                pass
            elif soundp != '' and sounda != '':
                sounde = sound[0:lspoint]+sound[rspoint:leftPoint]+sound[lspoint:rspoint]+sound[leftPoint:rightPoint]+sound[rightPoint:dura*1000]

        soundp = ''
        sounda = '' 
        for i in sticks:
            #get the relx position of each of the splits
            #relxx = float(i.place_info()['relx'])
            relxx = i.winfo_x()/musicBar.winfo_width()

            #if swapping to the right
            if swapPosend > swapPosend2:
                if relxx == swapPosend2:
                    i.place_configure(relx=swapPos2+thewidth)
            
                elif relxx > swapPosend2 and relxx < swapPosend:
                    i.place_configure(relx=relxx+thewidth)
                    #for the last stick 
                    newRelxx = relxx+thewidth
                    if newRelxx == swapPosend:
                        i.place_configure(relx=swapPosend2+thewidth)
                    
            #if swapping to the left
            elif swapPosend < swapPosend2:
                #if the end one being swapped with is equal to 1
                if swapPosend2 >= 1:
                    dmarker = tk.Frame(musicBar, width=1.5, bg='black')
                    dmarker.place(relx=swapPos2, rely=.5, anchor="w", relheight=1)
                    if relxx > swapPosend and relxx < swapPosend2:
                        i.place_configure(relx=relxx-thewidth)
                    elif relxx == swapPosend:
                        i.destroy()
                        
                else:
                    if relxx == swapPosend2:
                        i.place_configure(relx=swapPos2)
        
                    elif relxx > swapPosend and relxx < swapPosend2:
                        i.place_configure(relx=relxx-thewidth)
                        
                    elif relxx == swapPosend:
                        i.place_configure(relx=swapPosend2)

        apply()
        loadChanges(newAudio, sound)

    nextAction = tk.Label(editpg, text='Click the clip where you want to put the highlighted clip in 3 seconds', bg="black", fg="white")
    nextAction.grid(row=2, column=0, pady=5)

    root.after(3000, lambda: swapAction2(thewidth, swapPos, swapPosend))


def delActions(event):
    delAction()

def delAction():
    global editpg, sound, sounde, sounda, soundp, newAudio, highlighter, musicBar, sticks

    #get the highlighted sound
    highlightSounds()

    #delete the highlighted sound
    if soundp == '' and sounda != '':
        sounde = sounda
    elif sounda == '' and soundp != '':
        sounde = soundp
    elif soundp == '' and sounda == '':
        pass
    elif soundp != '' and sounda != '':
        sounde = soundp +  sounda

    soundp = ''
    sounda = ''

    try:
        #get the postion of the highlighted sound
        thewidth = float(highlighter.place_info()['relwidth'])
    except NameError:
        return
    except tk.TclError:
        return
    
    #get the position of the highlighted clip
    delPos = float(highlighter.place_info()['relx'])

    #get the end of the highlighted clip
    delPosend = delPos+thewidth
    print(delPosend)

    #the new scale after the deleted music
    newScale = 1 - thewidth

    for i in sticks:
        #get the relx position of each of the splits
        #relxx = float(i.place_info()['relx'])
        relxx = i.winfo_x()/musicBar.winfo_width()
        print(relxx)
        if delPosend >= 1:
            if relxx == delPos:
                i.destroy()
                continue
        else:
            if relxx == delPosend:
                i.destroy()
                continue
            
        if relxx > delPosend:
            #print(i.place_info()['relx'])
            i.place_configure(relx=(relxx-thewidth)/newScale)
        else:
            i.place_configure(relx=relxx/newScale)

    apply()
    loadChanges(newAudio, sound)

    

def addAction():
    global editpg, sound, sounde, extensionn, newAudio, dura, highlighter, musicBar, sticks
    
    newSelected = select_file()
    
    try:
        addedSound = AudioSegment.from_file(newSelected)
    except FileNotFoundError:
        return 
    
    #get the highlighted sound
    highlightSounds()
    sounde = sounde + addedSound

    overallSeconds = addedSound.duration_seconds + dura
    print(overallSeconds)
    addedLent = addedSound.duration_seconds/overallSeconds
    #then compare it to the duraationof the songs
    addedLength = addedLent/(1-addedLent)
    
    #get the width of the songs from the seconds
    #get the widthof the highlighted clip
    try:
        thewidth = float(highlighter.place_info()['relwidth'])
        print(addedLength)

        #get the position of the highlighted clip
        addedPos = float(highlighter.place_info()['relx'])


    except NameError:
        thewidth = 1
        addedPos = 0
        
    except tk.TclError:
        return
        
    #get the end of the highlighted clip
    addedPosend = addedPos+thewidth
    print(addedPosend)

    #the new scale after the added music
    newScale = 1 + addedLength
        
    try:
        for i in sticks:
            #get the relx position of each of the splits
            #relxx = float(i.place_info()['relx'])
            relxx = i.winfo_x()/musicBar.winfo_width()
            if relxx > addedPosend:
                #print(i.place_info()['relx'])
                i.place_configure(relx=(relxx+addedLength)/newScale)
            else:
                i.place_configure(relx=relxx/newScale)
    except NameError:
        pass

    # check if it is the last clip
    if addedPosend >= 1:
        dmarker = tk.Frame(musicBar, width=1.5, bg='black')
        dmarker.place(relx=1/newScale, rely=.5, anchor="w", relheight=1)

    else:
        dmarker = tk.Frame(musicBar, width=1.5, bg='black')
        dmarker.place(relx=(addedPosend+addedLength)/newScale, rely=.5, anchor="w", relheight=1)
    


    apply()
    loadChanges(newAudio, sound)


def editWin(root):
    global pagenum, selected, editpg, labelFrame, labs, sound, editpl
    global file_type, file_index, dura, extensionn, musicBar, musicPos, newAudio, menFrame

    selected = select_file()
    #save the file extension for the final saving
    for exten in file_type:
        if exten in selected:
            file_index = file_type.index(exten)
            #print(file_index)
            extensionn = exten[1:]

    try:    
        sound = AudioSegment.from_file(selected, format=extensionn)
    except:
        pagenum = 3
        changepage()
        return
    
    #to save the edited files as the edition is going on
    newAudio = 'processing.wav'
    
    editpg = tk.Frame(root, bg='black')
    editpg.pack(anchor=tk.CENTER)

    save = tk.Button(editpg, text="Save", bg="green", fg="white", command=lambda: changepage())
    #save.pack(side=tk.TOP, anchor="e", padx=8, pady=20)
    #save.grid(row=0, column=10, padx=3, pady=20, sticky='NE')
    save.place(relx=.9, rely=.05)

    bacj = tk.Button(editpg, text="Back", bg="red", fg="white", command=lambda: backjj())
    #save.pack(side=tk.TOP, anchor="e", padx=8, pady=20)
    bacj.place(relx=.05, rely=.05)

    menFrame = tk.Frame(editpg, bg='black', width=420)
    menFrame.grid(row=0, column=0, padx=5, pady=(70, 0), sticky='WE')

    play = tk.Button(menFrame, text="Play", bd=2, bg="black", fg="white", command=lambda: playy(0))
    #play.pack(side=tk.LEFT, pady=150)
    play.grid(row=0, column=0, sticky='NW')

    mlFrame = tk.Frame(menFrame, bg='black', width=420)
    mlFrame.grid(row=0, column=1, padx=10, pady=3)
    
    mFrame = tk.Frame(mlFrame, bg='black')
    mFrame.grid(row=0, column=0)
    
    musicPos = tk.IntVar()
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("blue.Horizontal.TProgressbar", foreground='blue', background='blue')
    musicBar = ttk.Progressbar(mFrame, orient=tk.HORIZONTAL, maximum=100, length=400, mode='determinate', style='blue.Horizontal.TProgressbar')
    #musicBar.pack(side=tk.LEFT, padx=10, pady=150)
    musicBar.pack(side=tk.LEFT)
    musicBar.bind('<B1-Motion>', motion)
    musicBar.bind("<Button 1>", highlight)
    musicBar.config(variable=musicPos)

    labelFrame = tk.Frame(mlFrame, bg='black', width=400, height=20)
    labelFrame.grid(row=1, column=0)

    labs = tk.Label(labelFrame, text=time.strftime("%M:%S", time.gmtime(0*dura)), bg="black", fg="white")
    labs.place(relx=0, rely=.3, anchor="center")
    updateLabel()
    
    #to load the music and to write the duration
    loadChanges(selected, sound)


    editpl = tk.Frame(editpg, bg='black', highlightthickness=1, highlightbackground='white')
    editpl.grid(row=1, column=0, pady=(40, 0))
    
    splitB = tk.Button(editpl, text="Split", highlightthickness=1, highlightbackground='white', bg="black", fg="white", command=lambda: splitAction())
    #splitB.pack(side=tk.BOTTOM, padx=10, pady=300, anchor='w')
    splitB.grid(row=0, column=0, sticky=tk.W, padx=5)

    trimB = tk.Button(editpl, text="Trim", highlightthickness=1, highlightbackground='white', bg="black", fg="white", command=lambda: trimAction())
    #trimB.pack(side=tk.LEFT)
    trimB.grid(row=1, column=0, sticky=tk.W, padx=5)

    dupB = tk.Button(editpl, text="Duplicate", highlightthickness=1, highlightbackground='white', bg="black", fg="white", command=lambda: duplicateAction())
    #trimB.pack(side=tk.LEFT)
    dupB.grid(row=2, column=0, sticky=tk.W, padx=5)

    #fadeB = tk.Button(editpl, text="Fade", bd=0, bg="black", fg="white", command=lambda: fadeAction())
    #trimB.pack(side=tk.LEFT)
    #fadeB.grid(row=0, column=3, sticky=tk.W)
    fadeAction()

    #volB = tk.Button(editpl, text="Volume", bd=0, bg="black", fg="white", command=lambda: volumeAction())
    #trimB.pack(side=tk.LEFT)
    #volB.grid(row=0, column=4, sticky=tk.W)
    volumeAction()

    
    #filtB = tk.Button(editpl, text="Filter", bd=0, bg="black", fg="white", command=lambda: filtAction())
    #trimB.pack(side=tk.LEFT)
    #filtB.grid(row=0, column=5, sticky=tk.W)
    filtAction()
    
    overlayB = tk.Button(editpl, text="Overlay", highlightthickness=1, highlightbackground='white', bg="black", fg="white", command=lambda: overlayAction())
    #trimB.pack(side=tk.LEFT)
    overlayB.grid(row=5, column=1, sticky=tk.W, padx=5)

    #speedB = tk.Button(editpl, text="Speed", bd=0, bg="black", fg="white", command=lambda: speedAction())
    #trimB.pack(side=tk.LEFT)
    #speedB.grid(row=0, column=7, sticky=tk.W)
    speedAction()
    
    recheckDict()

    swapB = tk.Button(editpl, text="Swap", highlightthickness=1, highlightbackground='white', bg="black", fg="white", command=lambda: swapAction())
    #trimB.pack(side=tk.LEFT)
    swapB.grid(row=4, column=0, sticky=tk.W, padx=5)

    delB = tk.Button(editpl, text="Delete", highlightthickness=1, highlightbackground='white', bg="black", fg="white", command=lambda: delAction())
    delB.grid(row=5, column=0, sticky=tk.W, padx=5)

    addN = tk.Button(editpl, text="+", highlightthickness=1, highlightbackground='white', bg="red", fg="white", command=lambda: addAction())
    addN.grid(row=0, column=2, sticky=tk.NW, padx=5)

    root.bind('<Delete>', delActions)

def saveWin(root):
    global sound, extensionn
        
    savepg = tk.Frame(root, bg='black')
    savepg.pack(anchor=tk.CENTER)

    #save it according to the time now
    time_now = datetime.now().strftime('%Y%m%d%H%M%S')
    nameVar = tk.StringVar()
    name = tk.Entry(savepg, textvariable=nameVar)
    name.pack(anchor=tk.CENTER, pady=(70,10))
    nameVar.set('Exported'+time_now)

    #show all the existing file types in a spinbox
    extenVar = tk.StringVar()
    extenWidget = tk.Spinbox(savepg, values=file_type, textvariable=extenVar, width=5)
    extenWidget.pack()
    for i in file_type:
        if extensionn in i:
            extenVar.set(i)
    
    def done():
        nameVal = nameVar.get()
        extensionn = extenVar.get()
        extensionn = extensionn[1:]
        namePath = os.getcwd()+'\saved'
        if not os.path.exists(namePath):
            os.makedirs(namePath)
        nameVal = namePath+'/'+nameVal+'.'+extensionn
        sound.export(nameVal, format=extensionn)
        changepage()

    saveBut = tk.Button(savepg, text="Export", bd=2, bg="green", fg="white", command=lambda: done())
    saveBut.pack(pady=40)

    
def backjj():
    global pagenum
    pagenum = 3
    changepage()


def changepage():
    global pagenum, root
    for widget in root.winfo_children():
            widget.destroy()
    if pagenum == 1:
            pagenum = 2
            root['bg'] = 'black'
            editWin(root)
            

    elif pagenum == 2:
            pagenum = 3
            root['bg'] = 'black'
            saveWin(root)
            
            
    elif pagenum == 3:
            pagenum = 1
            root['bg'] = '#bfafae'
            homeWin(root)
            

            
#creating a window
pagenum = 1
root = tk.Tk()
#font.families()
root['bg'] = '#bfafae'
root.title("Audio Editor")
root.geometry("700x600")
root.resizable(True, True)
homeWin(root)
#select_file()

#call the function
root.mainloop()
