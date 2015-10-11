import tkinter as tk
from tkinter import ttk

__author__ = 'Anders'


def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("{}x{}+{}+{}".format(size[0], size[1], int(x), int(y)))


def close(popup, parent_frame):
    parent_frame.attributes("-disabled", 0)
    popup.destroy()


def popupmsg(parent_frame, title, msg):
    popup = tk.Tk()
    popup.wm_title(title)
    popup.resizable(width=False, height=False)
    popup.attributes("-toolwindow", 1, "-topmost", 1)
    parent_frame.attributes("-disabled", 1)
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10, padx=10)
    b1 = ttk.Button(popup, text="OK", command=lambda: close(popup, parent_frame))
    b1.pack(pady=5)
    center(popup)
    popup.mainloop()
