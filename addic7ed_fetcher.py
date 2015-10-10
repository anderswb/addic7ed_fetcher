import tkinter as tk
from tkinter import ttk
import SubtitleSelectionPage
import SelectShowPage

def popupmsg(title, msg):
    popup = tk.Tk()
    popup.wm_title(title)
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10, padx=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack(pady=5)
    popup.mainloop()

class TkinterTestApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Addic7ed Fetcher")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg('Not supported just yet!'))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)
        
        self.frames = {}
        
        for F in (SelectShowPage.SelectShowPage, SubtitleSelectionPage.SubtitleSelectionPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(SelectShowPage.SelectShowPage)
        
    def show_frame(self, content):
        frame = self.frames[content]
        frame.tkraise()

if __name__=="__main__":
    app = TkinterTestApp()
    app.geometry("1000x500")
    app.mainloop()
