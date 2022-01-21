from pynput.mouse import Button, Controller
from tkinter import messagebox
import tkinter as tk
import pyautogui
import pyglet
import pynput
import ctypes
import sys
import os


def getpath(relative_path):
    # for pyinstaller onefile
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


HEIGHT = 100
WIDTH = 200

hack_running = False

mouse = Controller()

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


def PressKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008, 0,
                                           ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008 | 0x0002, 0,
                                           ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def EnR():
    ReleaseKeyPynput(0x02)


def keyshack():
    PressKeyPynput(0x02)
    root.after(25, EnR)
    if hack_running == True:
        root.after(200, keyshack)


scrnrex, scrnrey = pyautogui.size()


def mousehack():
    mouse.position = (scrnrex, scrnrey)
    mouse.click(Button.left, 1)
    if hack_running == True:
        root.after(200, mousehack)


def hack():
    if hack_running:
        keyshack()
        mousehack()


def quit():
    root.destroy()


def Start_stop():
    global hack_running
    if Startk['text'] == 'Start (F7)':
        hack_running = True
        hack()
        Startk.config(text='Stop (F7)')
    else:
        hack_running = False
        Startk.config(text='Start (F7)')


def press(key):
    if key == pynput.keyboard.Key.f7:
        Start_stop()


pynput.keyboard.Listener(on_press=press).start()

pyglet.font.add_file(getpath("Typo_Square_Regular_Demo.ttf"))
pyglet.font.add_file(getpath("cs_regular.ttf"))

root = tk.Tk()

root.title("BS2H")

root.iconbitmap(getpath('logo.ico'))

root.resizable(False, False)

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='black')
frame.place(relwidth=1, relheight=1)

cs_regular = pyglet.font.load('Counter-Strike', size=14)

Tittel = tk.Message(frame, text="BOXING SIMULATOR 2 HACK", bg='black', fg='white', font=("Counter-Strike", 14),
                    width='190', justify='center')
Tittel.place(relwidth='1')

messagebox.showinfo("Quick Info", "Thank you for downloading Boxing Simulator 2 Hack (V1.0)!")

Typo_Square_Regular_Demo = pyglet.font.load('Typo Square Regular Demo', size=13)

Startk = tk.Button(frame, text='Start (F7)', bg='white', font=("Typo Square Regular Demo", 13), command=Start_stop)
Startk.pack(side='top', pady='50')

Qut = tk.Button(root, text='QUIT', bg='white', font=("Typo Square Regular Demo", 13), command=quit)
Qut.pack(side='bottom')

pyglet.resource.reindex()

root.mainloop()
