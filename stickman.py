from PIL import Image, ImageTk
import tkinter as tk
import time,random,keyboard,pyautogui
import sys,threading
from tkinter import messagebox
import os,glob
import pygame
path = os.path.dirname(os.path.abspath(__file__))+'\\animations\\'
pygame.mixer.init()
root = tk.Tk()
frame = 1
animstate = 'sleep'
# Load the image file
img = Image.open(path + "idle/1.png")
sound = pygame.mixer.Sound(path + 'sounds\\bonk.mp3')
sound1 = pygame.mixer.Sound(path + 'sounds\\nokia.mp3')
sound2 = pygame.mixer.Sound(path + 'sounds\\vineboom.mp3')
sound3 = pygame.mixer.Sound(path + 'sounds\\sleep.mp3')
photo = ImageTk.PhotoImage(img)
# Make bouncing physics
w,h = pyautogui.size()
centerw,centerh = 0,0
speed = 1.5
xvel =0
yvel =0
x,y = random.randint(0,w-64),-700
w-=64+32
h-=85
heldmuch = 0
b = 1
def changeanim():
    global frame
    frames = len(glob.glob(path + animstate + '\\*.png'))
    if frame > frames:
        frame = 1
    photo = ImageTk.PhotoImage(file=path + animstate + '\\' + str(frame) + '.png')
    label.config(image=photo)
    label.image = photo
    frame += 1
    root.after(200,changeanim)
def bounce():
    global w,h,xvel,yvel,x,y,w,h,animstate,b
    if random.randint(0,400) == 0:
        m = random.randint(0,4)
        if m == 0:
            xvel = speed
        elif m == 1:
            xvel = 0
            b = random.randint(1,3)
            if b == 1:
                animstate = 'idle'
                sound2.play()
            elif b == 2:
                animstate = 'sleep'
            elif b == 3:
                animstate = 'dance'
            elif b > 3:
                if not pygame.mixer.Channel(0).get_busy():
                    sound1.play()
                animstate = 'phone'
        else:
            xvel = speed*-1
    if random.randint(0,500) == 0:
        if y > h-10 and x != 0:
            yvel -= 5
    x+=xvel
    y+=yvel
    if y < h-28:
        yvel += 0.05
        animstate = 'falling'
    # i dont know why doesnt it work
    #if yvel > 70:
    #    print('critical')
    #    yvel = 0
    else:
        yvel = 0
        if xvel > 0:
            animstate = 'walking_right'
        elif xvel < 0:
            animstate = 'walking_left'
        elif xvel == 0:
            if b == 3:
                animstate = 'dance'
            elif b == 0:
                animstate = 'bonk'
            elif b == 1:
                animstate = 'idle'
            elif b == 2:
                animstate = 'sleep'
                if not pygame.mixer.Channel(0).get_busy():
                    sound3.play()
            elif b > 3:
                animstate = 'phone'
    if x >= w or x <= 0:
        xvel*=-0.9
        x*=0.99
    root.geometry(f'64x64+{round(x)}+{round(y)}')
    if keyboard.is_pressed('m') and keyboard.is_pressed('l'):
        hold()
    if keyboard.is_pressed('p') and keyboard.is_pressed('l'):
        root.destroy()
        quit()
    root.after(10,bounce)
def hold():
    global x,y,yvel,xvel,heldmuch,centerh,centerw
    x,y = pyautogui.position()[0]-64,pyautogui.position()[1]-64
    yvel = (y-centerh)
    xvel = (x-centerw)
    heldmuch += 1
    if heldmuch > 1:
        centerw = x
        centerh = y
def bonk(*a):
    global b
    b = 0
    sound.play()
# Create the Label widget
label = tk.Label(root, image=photo, bg='white')
label.bind('<Button-1>', bonk)

# Set window properties
root.overrideredirect(True)
root.geometry("+0+0")
root.config(bg='white')
root.wm_attributes("-topmost", True)
#root.wm_attributes("-disabled", True)
root.wm_attributes("-transparentcolor", "white")


# Run physics
bounce()
changeanim()
# Pack the Label widget and run the mainloop
label.pack()
root.mainloop()
