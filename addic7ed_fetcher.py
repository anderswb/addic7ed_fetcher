import tkinter as tk
import subtitleselectionpage
import selectshowpage
from popupmessages import popupmsg


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
        filemenu.add_command(label="Save settings", command=lambda: popupmsg(self, 'Note', 'Not supported just yet!'))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        tk.Tk.config(self, menu=menubar)
        
        self.frames = {}
        
        for F in (selectshowpage.SelectShowPage, subtitleselectionpage.SubtitleSelectionPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(selectshowpage.SelectShowPage)
        
    def show_frame(self, content):
        frame = self.frames[content]
        frame.tkraise()

if __name__ == "__main__":
    app = TkinterTestApp()
    app.geometry("1000x500")
    app.mainloop()
