from tkinter import *
import tkinter.messagebox as MessageBox

login_bank = Tk()
login_bank.geometry("300x300");
login_bank.title("Login_Form")

title_label = Label(login_bank, text="Bank Login", font=("Helvetica", 16))
title_label.place(x=20, y=20)

def login():
    user = e_user.get()
    password = e_password.get()

    if(user=="" and password==""):
        MessageBox.showinfo("Login input", "Please fill in User and Password")

    elif(user=="Admin" and password=="123"):
        login_bank.destroy()
        import bank_form

    else:
        MessageBox.showinfo("Login input", "Incorrect User and Password")

user = Label(login_bank, text='User:', font=('bold', 10))
user.place(x=20, y=80);

password = Label(login_bank, text='Password:', font=('bold', 10))
password.place(x=20, y=110);

e_user = Entry()
e_user.place(x=100, y=80)

e_password = Entry()
e_password.place(x=100, y=110)
e_password.config(show="*")

login = Button(login_bank, text="Login", font=("italic", 10), bg="white", command=login)
login.place(x=50, y=170);

login_bank.mainloop()
