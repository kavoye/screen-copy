import ctypes
import gc
import os
import re
import tkinter as tk
import winsound

import cv2
import keyboard
import pyperclip
import pystray._win32
import pytesseract
from PIL import Image, ImageEnhance, ImageGrab, ImageTk
from pystray import Icon as icon
from pystray import Menu as menu
from pystray import MenuItem as item
from settings import *

fx_var = config.getfloat('Options', 'fx_var')
fy_var = config.getfloat('Options', 'fy_var')
t_config = config.get('Options', 't_config')
t_language = config.get('Options', 'language')
t_path = config.get('Options', 't_path')
show_processed_image = config.getint('Options', 'show_processed_image')

pytesseract.pytesseract.tesseract_cmd = f"{t_path}"

class WindowGrab(tk.Tk):
    def __init__(self):
        super().__init__()

        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        w, h = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)
        self.configure(bg="black")
        self.geometry("%dx%d" % (w, h))
        self.withdraw()
        self.attributes('-topmost', True)
        self.iconbitmap('lib/screenshot-icon.ico')
        self.config(cursor='crosshair')

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        global image
        image = ImageGrab.grab(all_screens=True)
        bgimage = ImageEnhance.Brightness(image).enhance(0.6)
        self.image = ImageTk.PhotoImage(bgimage)
        self.photo = self.canvas.create_image(0, 0, image=self.image, anchor="nw")

        self.x, self.y = 0, 0
        self.rect, self.start_x, self.start_y = None, None, None
        self.deiconify()

        self.canvas.tag_bind(self.photo,"<ButtonPress-1>", self.on_button_press)
        self.canvas.tag_bind(self.photo,"<B1-Motion>", self.on_mouse_move)
        self.canvas.tag_bind(self.photo,"<ButtonRelease-1>", self.on_button_release)

    def on_button_press(self, event):
        outline = config.get('Options', 'outline')
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline=f'{outline}')

    def on_mouse_move(self, event):
        curX, curY = event.x, event.y
        crop_image = image.crop((self.start_x, self.start_y, curX, curY))
        trimage = ImageEnhance.Brightness(crop_image).enhance(1)
        self.canvas.image = ImageTk.PhotoImage(trimage)
        self.canvas.create_image(self.start_x, self.start_y, image=self.canvas.image, anchor='nw')
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
        self.canvas.lift(self.rect)

    def on_button_release(self, event):        
        bbox = self.canvas.bbox(self.rect)
        self.withdraw()
        self.new_image = ImageGrab.grab(bbox, all_screens=True)
        self.new_image.save("lib/processing_img.png","PNG")
        self.destroy()
        gc.collect()

        img = cv2.imread('lib/processing_img.png')
        img = cv2.resize(img, None, fx=fx_var, fy=fy_var, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if show_processed_image == 1:
            cv2.imshow('Processed image', img)

        tesseract_text = pytesseract.image_to_string(img, lang=t_language, config=f"{t_config}")
        re_tesseract_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', tesseract_text)
        pyperclip.copy(re_tesseract_text)
        
        winsound.MessageBeep()

def open_action():
    root = WindowGrab()
    root.overrideredirect(True)
    root.mainloop()

def settings():
    root = Settings()
    root.mainloop()

def tray():
    rmb_on_tray = config.get('Options', 'rmb_on_tray')
    enable_hotkey = config.getint('Options', 'enable_hotkey')
    hotkey_shortcut = config.get('Options', 'hotkey_shortcut')
    if enable_hotkey == 1:
        keyboard.add_hotkey(hotkey_shortcut, open_action)

    def exit_action():
        icon.visible = False
        icon.stop()
        os._exit(0)

    SEPARATOR = item('- - - -', None)
    image = Image.open("lib/screenshot-icon.ico")
    if rmb_on_tray == '0': 
        menu_item = menu(
                        item('Settings', settings),
                        item(SEPARATOR, None),
                        item('Exit', exit_action))
        icon = pystray.Icon("Screen Copy", image, "Screen Copy", menu_item)
    elif rmb_on_tray == '1':
        menu_item = menu(
                        item('Grab Area', open_action, default = True),
                        item('Settings', settings),
                        item(SEPARATOR, None),
                        item('Exit', exit_action))
        icon = pystray.Icon("Screen Copy", image, "Screen Copy", menu_item)
    icon.run()

if __name__ == "__main__":
    tray()