import os
import sys
import configparser
import tkinter as tk
from tkinter import ttk

config = configparser.ConfigParser()
config.read_file(open('config.cfg'))

class Settings(tk.Tk):
    def __init__(self):
        super().__init__()
        
        fx_var = config.get('Options', 'fx_var')
        fy_var = config.get('Options', 'fy_var')
        outline = config.get('Options', 'outline')
        show_processed_image = config.get('Options', 'show_processed_image')
        enable_hotkey = config.get('Options', 'enable_hotkey')
        hotkey_shortcut = config.get('Options', 'hotkey_shortcut')
        rmb_on_tray = config.get('Options', 'rmb_on_tray')
        t_language = config.get('Options', 'language')
        t_config = config.get('Options', 't_config')
        t_path = config.get('Options', 't_path')
        
        self.attributes("-topmost", True)
        self.focus_force()
        self.resizable(False, False)
        self.iconbitmap('lib/screenshot-icon.ico')
        self.geometry("306x252")
        self.title("Settings")

        input_show_processed_image = tk.StringVar()
        input_fx_var = tk.StringVar()
        input_fy_var = tk.StringVar()
        input_outline = tk.StringVar()
        input_enable_hotkey = tk.StringVar()
        input_hotkey_shortcut = tk.StringVar()
        input_rmb_on_tray = tk.StringVar()
        input_t_language = tk.StringVar()
        input_t_config = tk.StringVar()
        input_t_path = tk.StringVar()

        input_fx_var.set(fx_var)
        input_fy_var.set(fy_var)
        input_outline.set(outline)
        input_show_processed_image.set(show_processed_image)
        input_enable_hotkey.set(enable_hotkey)
        input_hotkey_shortcut.set(hotkey_shortcut)
        input_rmb_on_tray.set(rmb_on_tray)
        input_t_language.set(t_language)
        input_t_config.set(t_config)
        input_t_path.set(t_path)

        def save():
            config.set("Options", "fx_var", input_fx_var.get())
            config.set("Options", "fy_var", input_fy_var.get())
            config.set("Options", "outline", input_outline.get())
            config.set("Options", "show_processed_image", input_show_processed_image.get())
            config.set("Options", "enable_hotkey", input_enable_hotkey.get())
            config.set("Options", "hotkey_shortcut", input_hotkey_shortcut.get())
            config.set("Options", "rmb_on_tray", input_rmb_on_tray.get())
            config.set("Options", "language", input_t_language.get())
            config.set("Options", "t_config", input_t_config.get())
            config.set("Options", "t_path", input_t_path.get())
            config.write(open("config.cfg", "w"))
            self.destroy()

        def close():
            self.destroy()

        def hotkey_field_disable():
            if input_enable_hotkey.get() == '0':
                hotkey_shortcut_entry.configure(state='disabled')
            else:
                hotkey_shortcut_entry.configure(state='normal')

        def restart():
            save()
            os.execl(sys.executable, '"{}"'.format(sys.executable), *sys.argv)

        outline_colors = ["white", "blue", "yellow", "red", "black", "green", "orange"]
        languages_list = ["eng", "rus", "eng+rus"]

        t_config_label = ttk.Label(self, text='Tesseract config', font=('calibre', 9,'normal'))
        t_config_list = ttk.Entry(self, textvariable=input_t_config, font=('calibre', 9,'normal'))

        fx_var_label = ttk.Label(self, text='Resize image X', font=('calibre', 9, 'normal'))
        fx_var_entry = ttk.Entry(self, textvariable=input_fx_var, font=('calibre', 9,'normal'))

        fy_var_label = ttk.Label(self, text='Resize image Y', font=('calibre', 9,'normal'))
        fy_var_entry = ttk.Entry(self, textvariable=input_fy_var, font=('calibre', 9,'normal'))

        outline_label = ttk.Label(self, text='Rectangle color', font=('calibre', 9,'normal'))
        outline_var_list = ttk.Combobox(self, values=outline_colors, textvariable=input_outline)

        t_language_label = ttk.Label(self, text = 'Recognizable languages', font=('calibre', 9,'normal'))
        t_language_list = ttk.Combobox(self, values=languages_list, textvariable=input_t_language)

        t_path_label = ttk.Label(self, text='* Tesseract path', font=('calibre', 9,'normal'))
        t_path_list = ttk.Entry(self, textvariable=input_t_path, font=('calibre', 9,'normal'))        

        hotkey_shortcut_entry = ttk.Entry(self, textvariable=input_hotkey_shortcut, font=('calibre', 9, 'normal'))
        enable_hotkey_cb = ttk.Checkbutton(self, text='* Enable hotkey', variable=input_enable_hotkey, command=hotkey_field_disable, onvalue=1, offvalue=0)
        hotkey_field_disable()

        rmb_on_tray_cb = ttk.Checkbutton(self, text='* Enable RMB on tray', variable=input_rmb_on_tray, onvalue=1, offvalue=0)

        show_processed_image_cb = ttk.Checkbutton(self, text='Show processed image', variable=input_show_processed_image, onvalue=1, offvalue=0)

        save_btn = ttk.Button(self, text='Save', command=save)
        close_btn = ttk.Button(self, text='Close', command=close)
        restart_btn = ttk.Button(self, text='Restart', command=restart)
        experimental_lable = ttk.Label(self, text='* Restart required', font=('calibre', 9))

        t_config_label.grid(row=0, column=0, sticky="w", padx=5, pady=1)
        t_config_list.grid(row=0, column=1, pady=1)

        fx_var_label.grid(row=1, column=0, sticky="w", padx=5, pady=1)
        fx_var_entry.grid(row=1, column=1, pady=1)
 
        fy_var_label.grid(row=2, column=0, sticky="w", padx=5)
        fy_var_entry.grid(row=2, column=1, pady=1)
  
        outline_label.grid(row=3, column=0, sticky="w", padx=5)
        outline_var_list.grid(row=3, column=1, pady=1)
 
        t_language_label.grid(row=4, column=0, sticky="w", padx=5)
        t_language_list.grid(row=4, column=1, pady=1)

        t_path_label.grid(row=5, column=0, sticky="w", padx=5, pady=1)
        t_path_list.grid(row=5, column=1, pady=1)
 
        enable_hotkey_cb.grid(row=6, column=0, sticky="w", padx=5)
        rmb_on_tray_cb.grid(row=7, column=0, sticky="w", padx=5)
        hotkey_shortcut_entry.grid(row=6, column=1, pady=1)
 
        show_processed_image_cb.grid(row=8, column=0, sticky="w", padx=5)
 
        save_btn.grid(row=10, column=1, sticky="w")
        close_btn.grid(row=10, column=1, sticky="e", padx=0)
        restart_btn.grid(row=10, column=0, sticky="w", padx=5)
        experimental_lable.grid(row=9, column=0, sticky="w", padx=5)