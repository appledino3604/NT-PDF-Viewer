from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import messagebox
from tkPDFViewer import tkPDFViewer as pdf
import sys
import os
import fitz

window=Tk()
window.title("PDF viewer")
window.geometry("941x516")
# window.iconbitmap(r"C:\Users\Atharva\Downloads\PDFlogo.ico")

defaultzoom=72

status_frame=Frame(window)
status_frame.pack(side=BOTTOM, fill="x")

status_bar = Label(status_frame, text="                          ",   anchor=W, borderwidth=1)
status_bar.pack(side=LEFT, pady=(0,1),padx=(5))

status_sep_3=Separator(status_frame,orient=VERTICAL)
status_sep_3.pack(fill="y",side=LEFT,padx=(20))

s_grip=Sizegrip(status_frame)
s_grip.pack(side=RIGHT)

zoom_status = Label(status_frame, text="100%",   anchor=W, borderwidth=1)
zoom_status.pack(side=RIGHT, pady=(0,1) , padx=(5,20))

status_sep_1=Separator(status_frame,orient=VERTICAL)
status_sep_1.pack(fill="y",side=RIGHT,padx=(2))

pages = Label(status_frame, text="Pages: 0",   anchor=W, borderwidth=1)
pages.pack(side=RIGHT, pady=(0,1) , padx=(10))

status_sep_2=Separator(status_frame,orient=VERTICAL)
status_sep_2.pack(fill="y",side=RIGHT,padx=(2))

status_sep=Separator(window,orient=HORIZONTAL)
status_sep.pack(side=BOTTOM, fill="x")

stats = [0,0,0]
inputfile_state=[False]
# replace  with sys.argv
# sys.argv=["",r"C:\Users\Atharva\Documents\demon_slayer.pdf"]
if len(sys.argv)==2:
    
    if sys.argv[1].endswith(".pdf"):
        print(sys.argv[1])
       
        file=sys.argv[1]
        inputfile_pdfobj=pdf.ShowPdf()
        inputfile=inputfile_pdfobj.pdf_view(window,pdf_location=file,width=50,height=3508,bar=True,zoomDPI=82)
        inputfile.pack(fill="both",expand=1)

        # status_bar.config(text=sys.argv[1])
        status_bar.config(text=file)

        doc = fitz.open(file)
        page = len(doc)
        print(page)
        pages.config(text=f"Pages: {page}")

        stats[1]=inputfile
        inputfile_state[0]=True
        stats[2]=True #making sure the file is open
    else:
        messagebox.showerror("Error","Unable to open file.")
        exit()

menubar=Menu(window)
window.config(menu=menubar)

scroll=Scrollbar(window,orient="vertical")
v2 = None
def opendiag():
    global v2
    global path
    global zoom_level
    global zoom_label
    global  scroll
    
    path=filedialog.askopenfilename(title="Open a file",filetypes=[("PDF Files","*.pdf")])
    stats[0]=path #storing the path in first item of stats list

    status_bar.config(text=stats[0])
    zoom_label=100
    zoom_status.config(text=f"{zoom_label}%")
    
    doc = fitz.open(path)
    page = len(doc)
    print(page)
    pages.config(text=f"Pages: {page}")
    
    try:
        inputfile.destroy()
        pdfobj0.img_object_li.clear()
        
    except:
        pass

    if path:
        if v2:
            stats[1].destroy()
            
    pdfobj=pdf.ShowPdf()
    pdfobj.img_object_li.clear()

    v2=pdfobj.pdf_view(window,pdf_location=open(path,"r"),width=697,height=3508,bar=True,zoomDPI=82)
    v2.pack(fill="y")

    stats[2]=True #making sure the file is open
    print(path)    

    scroll.config(command=v2.yview)
    scroll.pack(side="right",fill="y")

    v2["yscrollcommand"]=scroll.set
    stats[1]=v2  #for v2 obeject

    inputfile_state[0]=False #True if file given by system is present or opened
    zoom_level=82 #reseting default zoomg
    return v2
   
 
zoom_dat=["0","0","0","0"]

v1 = pdf.ShowPdf()
zoom_label=100
zoom_level = 82

def zoom_func():
    global v2
    global zoom_level
    global zoom_label

    if not stats[2]:
        messagebox.showwarning("Zoom","Open a file in order to zoom")
        opendiag()
        return

    if v2: 
        v2.destroy()
         
    
    v2 = pdf.ShowPdf() 
    v2.img_object_li.clear()

    zoom_level=zoom_level+10
    zoom_label=zoom_label+10
    zoom_status.config(text=f"{zoom_label}%")


    if zoom.entrycget("Zoom out", "state") == "disabled": #check if the zoom out button was disabled
        zoom.entryconfig("Zoom out",state="normal")

    if zoom_level >= 122:
        zoom_level=122
        zoom.entryconfig("Zoom in",state="disabled")

    if inputfile_state[0] == True:
        file_location=sys.argv[1]
        inputfile.destroy()
    else:
        file_location=open(path,"r")

   
    v2=v2.pdf_view(window,pdf_location = file_location,zoomDPI=zoom_level,width=90,height=3508) 
    v2.pack(expand=1) 

    scroll.config(command=v2.yview)
    v2["yscrollcommand"]=scroll.set

    print("zoom in:", zoom_level)
    zoom_dat[0]=zoom_level #For relaying zoom information
    stats[1]=v2


def zoomout_func():
    global v2
    global zoom_level
    global zoom_label
    
    if not stats[2]:
        messagebox.showwarning("Zoom","Open a file in order to zoom")
        opendiag()
        return

    if v2: 
        v2.destroy()
        # creating object of ShowPdf from tkPDFViewer. 
    v2 = pdf.ShowPdf() 
    v2.img_object_li.clear()


    zoom_level=zoom_level-10
    zoom_label=zoom_label-10
    zoom_status.config(text=f"{zoom_label}%")

    if zoom.entrycget("Zoom in", "state") == "disabled": #Check if the  zoom button was disabled 
        zoom.entryconfig("Zoom in",state="normal")

    if zoom_level <= 52:
        zoom_level=52
        zoom.entryconfig("Zoom out",state="disabled")
        

    if inputfile_state[0] == True:
        file_location=sys.argv[1]
        inputfile.destroy()
    else:
        file_location=open(path,"r")
    
    v2=v2.pdf_view(window,pdf_location = file_location,zoomDPI=zoom_level,width=20,height=3508)
    v2.pack(fill="both",expand=1) 
    print("zoom out:", zoom_level)

    zoom_dat[0]=zoom_level
    stats[1]=v2
    

def print_file():
    scroll.set(0.37341772151898733,0.6119766309639727)
    pass



file=Menu(menubar, tearoff=False)
file.add_command(label="Open...              Ctrl+O",command=opendiag)
file.add_command(label="New window",command=print_file())
file.add_command(label="Print...",command=print_file)
file.add_separator()
file.add_command(label="Exit",command=window.destroy)
menubar.add_cascade(label="File",menu=file)

def fullscreen():
    window.attributes("-fullscreen",True)
    
def esc(event):
    window.attributes("-fullscreen",False)
window.bind("<Escape>",esc)


view=Menu(menubar,tearoff=False)
view.add_radiobutton(label="Dark theme")
view.add_radiobutton(label="Light theme")

zoom=Menu(view, tearoff=False)
zoom.add_command(label="Zoom in",command=zoom_func)
zoom.add_command(label="Zoom out",command=zoomout_func)
view.add_cascade(label="Zoom", menu=zoom)

view.add_separator()
view.add_command(label="Full screen",command=fullscreen)
menubar.add_cascade(label="View",menu=view)

# Keybindings
def help_menu_focus():
    print("ACE")
    menubar.focus_set()
    # menubar.entryconfigure("Help",state="enabled")
    menubar.entryconfigure('Help', accelerator='Alt-z')

window.bind("<Control-o>",lambda event:opendiag())
window.bind("<Control-O>",lambda event:opendiag())
window.bind("<Control-+>",lambda event:zoom_func())
window.bind("<Control-minus>",lambda event:zoomout_func())
window.bind("<MouseWheel>",lambda event: v2.yview_scroll(-int(event.delta/10),"units"))

window.bind("<F11>",lambda event:fullscreen())
window.bind("<h>",lambda event:help_menu_focus())


def about():
    messagebox.showinfo("About","PDF viewer  v1.2\nA Lightweight and simple PDF viewer for Windows.Powered by python, tkpdfviewer\nMissing functionality will be added in future realeses.\n\nAcknoledgements: Stack Overflow, Superuser, Other internet resources")

Help=Menu(menubar, tearoff=False)
Help.add_command(label="About",command=about)
menubar.add_cascade(label="Help",menu=Help)
# menubar.entryconfigure('Help', accelerator='Alt+z')



window.mainloop()



    
    
    







