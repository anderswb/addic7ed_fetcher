import tkinter as tk
from tkinter import ttk
from fnmatch import fnmatchcase

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
        tk.Tk.wm_title(self, "tkinter Test App")
        
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
        
        for F in (PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(PageOne)
        
    def show_frame(self, content):
        frame = self.frames[content]
        frame.tkraise()

class PageOne(tk.Frame):

    def updatelist(self, searchterm):
        print(searchterm)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label1 = ttk.Label(self, text="Select a show:")

        searchentry = ttk.Entry(self)
        searchentry.insert(0, '*')
        searchentry.bind("<Return>",(lambda event: PageOne.updatelist(self, searchentry.get())))


        label2 = ttk.Label(self, text="Search:")
        shows = fetchAndParse.getshows(self)

        scrollbar = tk.Scrollbar(self, orient="vertical")
        listbox1 = tk.Listbox(self, width=50, height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox1.yview)

        for show in shows:
            listbox1.insert(0, show[1])

        listbox1.insert(0,"123")

        button1 = ttk.Button(self, text="Go to page two",
                             command=lambda: controller.show_frame(PageTwo))

        label1.grid(row=0)
        searchentry.grid(row=1, sticky='ew')
        listbox1.grid(row=2, column=0, sticky='nsew')
        scrollbar.grid(row=2, column=1, sticky='nse')
        button1.grid(row=3)

        tk.Grid.grid_columnconfigure(self, 0, weight=1)
        tk.Grid.grid_rowconfigure(self, 2, weight=1)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Go to page one",
                             command=lambda: controller.show_frame(PageOne))
        button1.pack()

        
app = TkinterTestApp()
app.geometry("1000x500")
app.mainloop()
