from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
from tkinter import ttk
from PIL import ImageTk, Image

def insert():
    response_id = e_response_id.get()
    complaint_id = e_complaint_id.get();
    company_response = e_company_response.get();
    response_details = e_response_details.get("1.0",'end-1c');
    date_response = e_date_response.get();

    if(complaint_id=="" or company_response=="" or response_details=="" or date_response==""):
        MessageBox.showinfo("Insert Status", "All Fields are required")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database="complains")
        cursor = con.cursor()
        cursor.execute("insert into company_response values('"+ response_id +"','"+ complaint_id +"','"+ company_response +"','"+ response_details +"','"+ date_response +"')")
        cursor.execute("commit");
        
        e_response_id.delete(0, 'end')
        e_complaint_id.delete(0, 'end')
        e_company_response.delete(0, 'end')
        e_response_details.delete("1.0",'end-1c')
        e_date_response.delete(0, 'end')
        MessageBox.showinfo("Insert Status", "Inserted Successfully"); 
        con.close()

def delete():
    if(e_response_id.get() == ""):
        MessageBox.showinfo("Delete Status", "Response id will be deleted")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database="complains")
        cursor = con.cursor()
        cursor.execute("delete from company_response where response_id='"+e_response_id.get() +"'")
        cursor.execute("commit");

        e_response_id.delete(0, 'end')
        e_complaint_id.delete(0, 'end')
        e_company_response.delete(0, 'end')
        e_response_details.delete("1.0",'end-1c')
        e_date_response.delete(0, 'end')
        MessageBox.showinfo("Delete Status", "Deleted Successfully"); 
        con.close()

def update():
    response_id = e_response_id.get()
    complaint_id = e_complaint_id.get();
    company_response = e_company_response.get();
    response_details = e_response_details.get("1.0",'end-1c');
    date_response = e_date_response.get();

    if(response_id=="" or complaint_id=="" or company_response=="" or response_details=="" or date_response==""):
        MessageBox.showinfo("Update Status", "All Fields are required")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database="complains")
        cursor = con.cursor()
        cursor.execute("update company_response set complain_id='"+ complaint_id +"', company_response='"+ company_response +"', response_details='"+ response_details +"',\
        date_response='"+ date_response +"' where response_id='"+ response_id +"'")
        cursor.execute("commit");
        
        e_response_id.delete(0, 'end')
        e_complaint_id.delete(0, 'end')
        e_company_response.delete(0, 'end')
        e_response_details.delete("1.0",'end-1c')
        e_date_response.delete(0, 'end')
        MessageBox.showinfo("Update Status", "Updated Successfully"); 
        con.close()       

def get():
    if(e_response_id.get() == ""):
        MessageBox.showinfo("Fetch status", "Response ID has to be filled in")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database="complains")
        cursor = con.cursor()
        cursor.execute("select * from company_response where response_id='"+ e_response_id.get() +"'")        
        rows = cursor.fetchall()

        e_response_id.delete(0, 'end')
        e_complaint_id.delete(0, 'end')
        e_company_response.delete(0, 'end')
        e_response_details.delete("1.0",'end-1c')
        e_date_response.delete(0, 'end')
                
        for row in rows:
            e_response_id.insert(0, row[0])
            e_complaint_id.insert(0, row[1])
            e_company_response.insert(0, row[2])
            e_response_details.insert("1.0", row[3])
            e_date_response.insert(0, row[4])
        MessageBox.showinfo("Get Status", "Get Successfully"); 
        con.close()

def clear_fields():
        e_response_id.delete(0, 'end')
        e_complaint_id.delete(0, 'end')
        e_company_response.delete(0, 'end')
        e_response_details.delete("1.0",'end-1c')
        e_date_response.delete(0, 'end')
    

def show1():
    con = mysql.connect(host="localhost", user="root", password="", database="complains")
    cursor = con.cursor()
    cursor.execute("select * from complains INNER JOIN company_response ON complains.complain_id = company_response.complain_id")
    rows = cursor.fetchall()
    list1.delete(0, list1.size())

    for row in rows:
        insertData = str(row[11])+' | '+str(row[0])+' | '+row[7]+' | '+row[6]+' | '+row[13]
        list1.insert(list1.size()+1, insertData)

    con.close()

def refresh():
    con = mysql.connect(host="localhost", user="root", password="", database="complains")
    cursor = con.cursor()
    cursor.execute("select * from complains INNER JOIN company_response ON complains.complain_id = company_response.complain_id where complains.company='"+company_options.get() +"'")
    rows = cursor.fetchall()
    list1.delete(0, list1.size())

    for row in rows:
        insertData = str(row[11])+' | '+str(row[0])+' | '+row[7]+' | '+row[6]+' | '+row[13]
        list1.insert(list1.size()+1, insertData)

    con.close()

def show2():
    con = mysql.connect(host="localhost", user="root", password="", database="complains")
    cursor = con.cursor()
    cursor.execute("select * from complains LEFT JOIN company_response ON complains.complain_id = company_response.complain_id WHERE company_response.complain_id IS NULL")
    rows = cursor.fetchall()
    list2.delete(0, list2.size())

    for row in rows:
        insertData = str(row[0])+' | '+row[7]+' | '+row[6]
        list2.insert(list2.size()+1, insertData)

    con.close()

def companies():
    con = mysql.connect(host="localhost", user="root", password="", database="complains")
    cursor = con.cursor()
    cursor.execute("select distinct company from complains INNER JOIN company_response ON complains.complain_id = company_response.complain_id ORDER BY company ASC")

    data = []
    for row in cursor.fetchall():
        data.append(row[0])
    return data

    con.close()

def select():
    value = list2.get(ACTIVE)
    e_complaint_id.insert(0, value.split(' ')[0])

def open_main():
    bank_form.destroy()
    import main
    
bank_form = Tk()
bank_form.geometry("900x600");
bank_form.title("Process_Complains")

title_label = Label(bank_form, text="Process a Complain", font=("Helvetica", 16))
title_label.place(x=20, y=20)

response_id = Label(bank_form, text='Enter Response ID:', font=('bold', 10))
response_id.place(x=20, y=70);

complaint_id = Label(bank_form, text='Enter Complain ID:', font=('bold', 10))
complaint_id.place(x=20, y=100);

company_response = Label(bank_form, text='Enter Response category:', font=('bold', 10))
company_response.place(x=20, y=130);

response_details = Label(bank_form, text='Enter Response details:', font=('bold', 10))
response_details.place(x=20, y=160);

date_response = Label(bank_form, text='Enter Date of Response:', font=('bold', 10))
date_response.place(x=20, y=240);

e_response_id = Entry()
e_response_id.place(x=200, y=70)

e_complaint_id = Entry()
e_complaint_id.place(x=200, y=100)

e_company_response = Entry()
e_company_response.place(x=200, y=130)

e_response_details = Text(bank_form, height=4, width=30)
e_response_details.place(x=200, y=160)

e_date_response = Entry()
e_date_response.place(x=200, y=240)

select = Button(bank_form, text="Select", font=("italic", 10), bg="white", command=select)
select.place(x=70, y=280)

insert = Button(bank_form, text="Insert", font=("italic", 10), bg="white", command=insert)
insert.place(x=140, y=280)

delete = Button(bank_form, text="Delete", font=("italic", 10), bg="white", command=delete)
delete.place(x=210, y=280)

update = Button(bank_form, text="Update", font=("italic", 10), bg="white", command=update)
update.place(x=280, y=280)

get = Button(bank_form, text="Get", font=("italic", 10), bg="white", command=get)
get.place(x=350, y=280)

clear_fields = Button(bank_form, text="Clear Fields", font=("italic", 10), bg="white", command=clear_fields)
clear_fields.place(x=410, y=280)

main = Button(bank_form, text="Home", font=("italic", 10), bg="white", command=open_main)
main.place(x=510, y=20)

select_company = Label(bank_form, text='Select a Company to see Solved Complains:', font=('bold', 10))
select_company.place(x=30, y=340);


company_options = ttk.Combobox(bank_form, value=companies())
company_options.current(0)
company_options.place(x=300, y=340)

img = Image.open("Logo_fara_background.png")
img = img.resize((170,30), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(img)
logo_label = Label(bank_form, image=logo)
logo_label.place(x=620, y=20)


list1 = Listbox(bank_form, width=140)
list1.place(x=30, y=380)
show1()

list2 = Listbox(bank_form, width=60)
list2.place(x=510, y=70)
show2()

refresh = Button(bank_form, text="Refresh", font=("italic", 10), bg="white", command=refresh)
refresh.place(x=460, y=340)

all_processed_complains = Button(bank_form, text="All Processed Complains", font=("italic", 10), bg="white", command=show1)
all_processed_complains.place(x=540, y=340)

bank_form.mainloop()
