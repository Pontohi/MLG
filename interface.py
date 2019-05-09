from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import numpy as np
import threading
cprocess = np.array([False,False,False,False])
processMap = ["Scraping ImSorryJon", "Scraping Garfield Strips", "Loading Scraped Data","Training the Network"]
import queue
def trainModel():
    tdirs = []
    if bool(sorryVar.get()): tdirs.append("ImSorryJon")
    if bool(dailyVar.get()): tdirs.append("DailyGarf")
    if bool(stripVar.get()): tdirs.append("Strips")
    if (len(tdirs)>0):
        runCommand("train.py --tdirs "+" ".join(tdirs),3)
        print(tdirs)
    else:
        messagebox.showinfo("Error","No datasets selected")
root = Tk()
root.title("Algarfieithm Simplified Scripting Homolingual Operating (super)Leveled Executor")

nb = ttk.Notebook(root)
nb.grid()
f1 = Frame(nb)
nb.add(f1, text="Scrape")
f2 = Frame(nb)
nb.add(f2, text="Train")
nb.select(f2)
nb.enable_traversal()

Label(f1, width = 0, height = 1,).grid(row=0,column=0)
Button(f1,width = 30, text="Scrape all datasets",command=lambda: runCommand("loadScrape.py",2)).grid(row=1,column=0,columnspan=3)
Label(f1, width = 0, height = 1,).grid(row=2,column=0)

Label(f2, width = 0, height = 1,).grid(row=0,column=0)
dailyVar = IntVar()
Checkbutton(f2, text="Use DailyGarf", variable=dailyVar).grid(row=0, column=0,columnspan=1)
stripVar = IntVar()
Checkbutton(f2, text="Use Garf Strips", variable=stripVar).grid(row=0, column=1,columnspan=1)
sorryVar = IntVar()
Checkbutton(f2, text="Use ImSorryJon", variable=sorryVar).grid(row=0, column=2,columnspan=1)
Button(f2,width = 30, text="Train Network on /r/Imsorryjon",command=trainModel).grid(row=3,column=0,rowspan=2)
Label(f2, width = 0, height = 1,).grid(row=4,column=0)

status=Label(f1,text="No process started")
status.grid(row=3,column=0)

status2=Label(f2,text="No process started")
status2.grid(row=5,column=0)

def rCArchetpye(command,i):
    global cprocess
    os.system(command)
    cprocess[i] = False

def runCommand(fname,i):
    global cprocess
    if not (i<2 and cprocess[2]) and not (i == 2 and np.any(cprocess[:2])) and not cprocess[i]:
        cprocess[i] = True
        nT = threading.Thread(target=rCArchetpye,args=("python "+fname,i))
        nT.start()
    else:
        messagebox.showinfo("Error","This instruction is not compatible with currently running processes. Wait for these to finish.")
    
def updateStatus():
    if (not np.any(cprocess)):
        newStatus = "No process started"
    else:
        processes = []
        for d in range(len(cprocess)):
            if (cprocess[d]): processes.append(processMap[d])
        newStatus="Processes: "+(", ".join(processes))
    status.configure(text=newStatus)
    status2.configure(text=newStatus)
    root.after(500,updateStatus)

root.after(0,updateStatus)
root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
root.mainloop()