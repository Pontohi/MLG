import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk,Image
import json
from os import walk

backgroundcoloreffect = "#708090"

f = []
for (_, _, filenames) in walk("./Scraped"):
    f.extend(filenames)
    break

approved = []

indexToUse = 0

root = tk.Tk()
root.title = "Validate"
topFrame = tk.Frame(root)
topFrame.configure(background=backgroundcoloreffect)
topFrame.pack()
bottomFrame = tk.Frame(root)
bottomFrame.configure(background=backgroundcoloreffect)
bottomFrame.pack(side='bottom')
def loadImage(path):
    im = Image.open(str(path))
    return im.resize((500, 500), Image.ANTIALIAS)
def loadAt(findex):
    img = loadImage("./Scraped/"+str(f[findex]))
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img
def verdict(choice,_event=None):
   global indexToUse
   if (choice): choiceStr = "Approved"
   else: choiceStr = "Denied"
   print(choiceStr+": "+f[indexToUse])
   if (choice): approved.append(f[indexToUse])
   f.pop(indexToUse)
   indexToUse+=1
   loadAt(indexToUse)
approve = lambda : verdict(True)
deny = lambda : verdict(False)
loadCurr = lambda :loadAt(indexToUse)
def on_closing():
    if messagebox.askyesno("Quit", "Do you want to quit?"):
        if messagebox.askyesno("Save", "Do you want to save your progress?"):
            print("Dumping links as JSON and exiting")
            with open('approved.json', 'w') as outfile:
                json.dump(approved, outfile)
        root.destroy()


root.bind('<Right>', func=lambda x: approve())
root.bind('<Left>', func=lambda  x: deny())

panel = tk.Label(root)
img = Image.open(str("./Scraped/" + f[len(f) - 1]))
img = img.resize((500, 500), Image.ANTIALIAS)
img = ImageTk.PhotoImage(img)
panel.configure(image=img, background =backgroundcoloreffect)
panel.pack(side = "bottom", fill = "both", expand = "yes")

approvebtn = tk.Button(bottomFrame, width = 30,  height = 2, text ="Approve", fg = "blue", command = approve)
denybtn = tk.Button(bottomFrame, width = 30, height = 2, text ="Deny", fg = "red", command = deny)
w = tk.LabelFrame(bottomFrame, width = 15, height = 0, highlightbackground = backgroundcoloreffect, highlightcolor = backgroundcoloreffect, highlightthickness = 0, bg = backgroundcoloreffect, bd = 0)

approvebtn.grid(column=2, row = 0)
w.grid(column=1, row=0)
denybtn.grid(column=0, row = 0)

root.protocol()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.geometry("600x600")
root.configure(background=backgroundcoloreffect)
root.after(0,loadCurr)
root.mainloop()
