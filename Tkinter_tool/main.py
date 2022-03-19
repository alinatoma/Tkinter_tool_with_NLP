from tkinter import *
import tkinter.messagebox as MessageBox
from tkhtmlview import HTMLLabel
from PIL import ImageTk, Image


root = Tk()
root.geometry("500x450");
root.title("Complaint_management_tool")

title_label = Label(root, text="Select your Form", font=("Helvetica", 16))
title_label.place(x=20, y=20)

img = Image.open("Logo_fara_background.png")
img = img.resize((170,30), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(img)
logo_label = Label(root, image=logo)
logo_label.place(x=250, y=20)

def open_complaint():
    root.destroy()
    import complaint

def login_bank():
    root.destroy()
    import login_bank


open_complaint = Button(root, text="Fill in a Complaint", font=("italic", 10), bg="white", command=open_complaint)
open_complaint.place(x=20, y=80)

login_bank = Button(root, text="Login Bank", font=("italic", 10), bg="white", command=login_bank)
login_bank.place(x=20, y=140)

check_statistics = HTMLLabel(root, html="<a href='http://127.0.0.1:8050/'>Dashboard</a>")
check_statistics.pack(pady=200, padx=20)

root.mainloop()
