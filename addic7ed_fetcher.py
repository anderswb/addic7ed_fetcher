from controller import Controller

import tkinter as tk
import subtitleselectionpage
import selectshowpage


class TkinterTestApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.updatetitle()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        for F in (selectshowpage.SelectShowPage, subtitleselectionpage.SubtitleSelectionPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(selectshowpage.SelectShowPage)
        
    def show_frame(self, content):
        frame = self.frames[content]
        frame.updatedisplay()
        frame.tkraise()

if __name__ == '__main__':
    c = Controller()
    c.run()
