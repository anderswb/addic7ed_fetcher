import tkinter as tk
from tkinter import ttk
from fnmatch import fnmatch

from fetchandparse import fetchAndParse

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
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
        
        for F in (SelectShowPage, SubtitleSelectionPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(SelectShowPage)
        
    def show_frame(self, content):
        frame = self.frames[content]
        frame.tkraise()

class SelectShowPage(tk.Frame):

    def updatelist(self, searchterm):
        self.listbox1.delete(0, 'end')
        for show in self.shows:
            if fnmatch(show[1].lower(), searchterm.lower()):
                self.listbox1.insert(0, show[1])

    def nextpage(self, controller):
        selectedshowtitle = self.listbox1.get((self.listbox1.curselection()[0]))
        selectedshow = [self.shows[i] for i, v in enumerate(self.shows) if v[1] == selectedshowtitle][0]
        SubtitleSelectionPage.updatedisplay(self,selectedshow)
        controller.show_frame(SubtitleSelectionPage)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = ttk.Label(self, text="Select a show:")

        searchentry = ttk.Entry(self)
        searchentry.insert(0, '*')
        searchentry.bind("<Return>",(lambda event: self.updatelist(searchentry.get())))

        label2 = ttk.Label(self, text="Search:")
        self.shows = fetchAndParse.getshows(self)

        scrollbar = tk.Scrollbar(self, orient="vertical")
        self.listbox1 = tk.Listbox(self, width=50, height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox1.yview)
        self.updatelist('*')

        button1 = ttk.Button(self, text="Ok...",
                             command=lambda: self.nextpage(controller))

        label1.grid(row=0)
        searchentry.grid(row=1, sticky='ew', columnspan=2)
        self.listbox1.grid(row=2, column=0, sticky='nsew')
        scrollbar.grid(row=2, column=1, sticky='nse')
        button1.grid(row=3)

        tk.Grid.grid_columnconfigure(self, 0, weight=1)
        tk.Grid.grid_rowconfigure(self, 2, weight=1)


class SubtitleSelectionPage(tk.Frame):
    label1 = None
    notebook = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        SubtitleSelectionPage.label1 = ttk.Label(self, text="Unknown show")

        button1 = ttk.Button(self, text="Go to page one",
                             command=lambda: controller.show_frame(SelectShowPage))



        SubtitleSelectionPage.notebook = ttk.Notebook(self)

        SubtitleSelectionPage.label1.grid(row=0, column=0)
        SubtitleSelectionPage.notebook.grid(row=1, column=0, sticky='nsew')
        button1.grid(row=2, column=0)

        tk.Grid.grid_columnconfigure(self, 0, weight=1)
        tk.Grid.grid_rowconfigure(self, 1, weight=1)

    def updatedisplay(self, selectedshow):
        SubtitleSelectionPage.label1.config(text=selectedshow[1])
        seasons = fetchAndParse.getseasons(self, selectedshow[0])
        for eachseason in seasons:
            frame = ttk.Frame(SubtitleSelectionPage.notebook)
            SubtitleSelectionPage.notebook.add(frame, text="S{:02}".format(eachseason))


if __name__=="__main__":
    app = TkinterTestApp()
    app.geometry("1000x500")
    app.mainloop()
