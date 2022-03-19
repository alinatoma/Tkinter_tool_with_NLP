from tkinter import *
import tkinter.messagebox as MessageBox
import mysql.connector as mysql
from tkinter import ttk
import re
import pandas as pd
import numpy as np
from scipy.stats import randint
import seaborn as sns 
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings("ignore")
from PIL import ImageTk, Image

#Data
df = pd.read_csv("complaints.csv", sep=",")
df.shape

df1 = df[['Product', 'Consumer complaint narrative']].copy()
df1 = df1[pd.notnull(df1['Consumer complaint narrative'])]
df1.columns = ['Product', 'Consumer_complaint']
df1.shape
df2 = df1.sample(10000, random_state=1).copy()
df2.replace({'Product': 
             {'Credit reporting, credit repair services, or other personal consumer reports':'Credit card', 
              'Credit reporting': 'Credit card',
              'Credit card or prepaid card': 'Credit card',
              'Credit card': 'Credit card',
              'Prepaid card': 'Credit card',
              'Other financial service': 'Bank account or service',
              'Payday loan, title loan, or personal loan': 'Payday loan',      
              'Money transfer, virtual currency, or money service': 'Money transfer & virtual currency',
              'Consumer Loan': 'Vehicle loan or lease',
              'Bank account or service': 'Checking or savings account',
              'Money transfers': 'Money transfer & virtual currency',
              'Virtual currency': 'Money transfer & virtual currency'}}, 
              inplace= True)

#Remove X, {, }, /
df2['Consumer_complaint'] = df2['Consumer_complaint'].str.replace('X', '')
df2['Consumer_complaint'] = df2['Consumer_complaint'].str.replace('{', '')
df2['Consumer_complaint'] = df2['Consumer_complaint'].str.replace('}', '')
df2['Consumer_complaint'] = df2['Consumer_complaint'].str.replace('/', '')

#convert text to lower case
df2['Consumer_complaint'] = df2['Consumer_complaint'].apply(lambda x: ' '.join([i.lower() for i in x.split()]))

#Removing Punctuations
df2['Consumer_complaint'] = df2['Consumer_complaint'].str.replace(r'[^\w\s]',"")

#Removing stopwords
stop = stopwords.words('english')
df2['Consumer_complaint'] = df2['Consumer_complaint'].apply(lambda x: ' '.join([i for i in x.split() if i not in stop]))

df2['category_id'] = df2['Product'].factorize()[0]
category_id_df = df2[['Product', 'category_id']].drop_duplicates()

#Dictionaries for future use

category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'Product']].values)

tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5,ngram_range=(1, 2), stop_words='english')

features = tfidf.fit_transform(df2.Consumer_complaint).toarray()

labels = df2.category_id

N = 5
for Product, category_id in sorted(category_to_id.items()):
  features_chi2 = chi2(features, labels == category_id)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names())[indices]
  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]


X = df2['Consumer_complaint'] # Collection of documents
y = df2['Product'] # Target or the labels we want to predict (i.e., the 10 different complaints of products)

# X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.25,random_state = 0)

models = [
    LinearSVC(),
]

CV = 5
cv_df = pd.DataFrame(index=range(CV * len(models)))
    

#Predictions

X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                    test_size=0.25,
                                                    random_state = 0)

tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5,
                        ngram_range=(1, 2), 
                        stop_words='english')

fitted_vectorizer = tfidf.fit(X_train)
tfidf_vectorizer_vectors = fitted_vectorizer.transform(X_train)

model = LinearSVC().fit(tfidf_vectorizer_vectors, y_train)



def insert():
    complaint_id = e_complaint_id.get()
    date_complaint = e_date_complaint.get();
    name = e_name.get();
    surname = e_surname.get();
    email = check(e_email.get());
    complaint_text = e_complaint_text.get("1.0",'end-1c');
    product_category = e_product_category.get();
    company = e_company.get();
    state = e_state.get();
    zip_code = e_zip_code.get();
    submitted_via = e_submitted_via.get();

    if(date_complaint=="" or name=="" or surname=="" or complaint_text=="" or product_category=="" or company=="" or state=="" or zip_code=="" or submitted_via==""):
        MessageBox.showinfo("Insert Status", "All Fields are required")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database="complains")
        cursor = con.cursor()
        cursor.execute("insert into complains values('"+ complaint_id +"','"+ date_complaint +"','"+ name +"','"+ surname +"','"+ email +"',\
    '"+ complaint_text +"','"+ product_category +"','"+ company +"','"+ state +"','"+ zip_code +"','"+ submitted_via +"')")
        cursor.execute("commit");
        
        e_complaint_id.delete(0, 'end')
        e_date_complaint.delete(0, 'end')
        e_name.delete(0, 'end')
        e_surname.delete(0, 'end')
        e_email.delete(0, 'end')
        e_complaint_text.delete("1.0",'end-1c')
        e_product_category.delete(0, 'end')
        e_company.delete(0, 'end')
        e_state.delete(0, 'end')
        e_zip_code.delete(0, 'end')
        e_submitted_via.delete(0, 'end')
        MessageBox.showinfo("Insert Status", "Inserted Successfully"); 
        con.close()
 

def delete():
    if(e_complaint_id.get() == ""):
        MessageBox.showinfo("Delete Status", "Complaint id will be deleted")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database="complains")
        cursor = con.cursor()
        cursor.execute("delete from complains where complain_id='"+e_complaint_id.get() +"'")
        cursor.execute("commit");
        
        e_complaint_id.delete(0, 'end')
        e_date_complaint.delete(0, 'end')
        e_name.delete(0, 'end')
        e_surname.delete(0, 'end')
        e_email.delete(0, 'end')
        e_complaint_text.delete("1.0",'end-1c')
        e_product_category.delete(0, 'end')
        e_company.delete(0, 'end')
        e_state.delete(0, 'end')
        e_zip_code.delete(0, 'end')
        e_submitted_via.delete(0, 'end')
        MessageBox.showinfo("Delete Status", "Deleted Successfully"); 
        con.close()

def update():
    complaint_id = e_complaint_id.get()
    date_complaint = e_date_complaint.get();
    name = e_name.get();
    surname = e_surname.get();
    email = check(e_email.get());
    complaint_text = e_complaint_text.get("1.0",'end-1c');
    product_category = e_product_category.get();
    company = e_company.get();
    state = e_state.get();
    zip_code = e_zip_code.get();
    submitted_via = e_submitted_via.get();

    if(complaint_id=="" or date_complaint=="" or name=="" or surname=="" or complaint_text=="" or product_category=="" or company=="" or state=="" or zip_code=="" or submitted_via==""):
        MessageBox.showinfo("Update Status", "All Fields are required")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database="complains")
        cursor = con.cursor()
        cursor.execute("update complains set date_complain='"+ date_complaint +"', name='"+ name +"', surname='"+ surname +"', email='"+ email +"', complain_text='"+ complaint_text +"',\
        product_category='"+ product_category +"', company='"+ company +"', state='"+ state +"', zip_code='"+ zip_code +"', submitted_via='"+ submitted_via +"' where complain_id='"+ complaint_id +"'")
        cursor.execute("commit");
        
        e_complaint_id.delete(0, 'end')
        e_date_complaint.delete(0, 'end')
        e_name.delete(0, 'end')
        e_surname.delete(0, 'end')
        e_email.delete(0, 'end')
        e_complaint_text.delete("1.0",'end-1c')
        e_product_category.delete(0, 'end')
        e_company.delete(0, 'end')
        e_state.delete(0, 'end')
        e_zip_code.delete(0, 'end')
        e_submitted_via.delete(0, 'end')
        MessageBox.showinfo("Update Status", "Updated Successfully"); 
        con.close()    

def get():
    if(e_complaint_id.get() ==""):
        MessageBox.showinfo("Fetch status", "Complaint ID has to be filled in")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database="complains")
        cursor = con.cursor()
        cursor.execute("select * from complains where complain_id='"+ e_complaint_id.get() +"'")        
        rows = cursor.fetchall()

        e_complaint_id.delete(0, 'end')
        e_date_complaint.delete(0, 'end')
        e_name.delete(0, 'end')
        e_surname.delete(0, 'end')
        e_email.delete(0, 'end')
        e_complaint_text.delete("1.0",'end-1c')
        e_product_category.delete(0, 'end')
        e_company.delete(0, 'end')
        e_state.delete(0, 'end')
        e_zip_code.delete(0, 'end')
        e_submitted_via.delete(0, 'end')
        
        for row in rows:
            e_complaint_id.insert(0, row[0])
            e_date_complaint.insert(0, row[1])
            e_name.insert(0, row[2])
            e_surname.insert(0, row[3])
            e_email.insert(0, row[4])
            e_complaint_text.insert("1.0", row[5])
            e_product_category.insert(0, row[6])
            e_company.insert(0, row[7])
            e_state.insert(0, row[8])
            e_zip_code.insert(0, row[9])
            e_submitted_via.insert(0, row[10])
        MessageBox.showinfo("Get Status", "Get Successfully"); 
        con.close()

def open_main():
    complaint_form.destroy()
    import main

def text_classification():
    e_text_classification.config(text=model.predict(fitted_vectorizer.transform([e_complaint_text.get("1.0",'end-1c')])))

def get_response():
    if(e_complaint_id_response.get() == ""):
        MessageBox.showinfo("Fetch status", "Complaint ID has to be filled in Response Check section")
    else:
        con = mysql.connect(host="localhost", user="root", password="", database="complains")
        cursor = con.cursor()
        cursor.execute("select * from company_response where complain_id='"+ e_complaint_id_response.get() +"'")        
        rows = cursor.fetchall()

        e_complaint_id_response.delete(0, 'end')
        e_company_response.delete(0, 'end')
        e_response_details.delete("1.0",'end-1c')
        e_date_response.delete(0, 'end')
        
        for row in rows:
            e_complaint_id_response.insert(0, row[1])
            e_company_response.insert(0, row[2])
            e_response_details.insert("1.0", row[3])
            e_date_response.insert(0, row[4])
            MessageBox.showinfo("Fetch status", "Please check Response")
        if(e_complaint_id_response.get() == ""):
            MessageBox.showinfo("Fetch status", "Complaint ID was not processed")    
        else:
            con.close()

def clear_fields():
        e_complaint_id.delete(0, 'end')
        e_date_complaint.delete(0, 'end')
        e_name.delete(0, 'end')
        e_surname.delete(0, 'end')
        e_email.delete(0, 'end')
        e_complaint_text.delete("1.0",'end-1c')
        e_product_category.delete(0, 'end')
        e_company.delete(0, 'end')
        e_state.delete(0, 'end')
        e_zip_code.delete(0, 'end')
        e_submitted_via.delete(0, 'end')
        e_text_classification.config(text='Get Proposed Product Category')

def clear_fields_response():
        e_complaint_id_response.delete(0, 'end')
        e_company_response.delete(0, 'end')
        e_response_details.delete("1.0",'end-1c')
        e_date_response.delete(0, 'end')    

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

def check(email):
    if(re.search(regex, email)):
        return email
    else:
        MessageBox.showinfo("Email validation", "Email address is not valid")   


complaint_form = Tk()
complaint_form.geometry("1100x600");
complaint_form.title("Fill in a Complaint")

title_label = Label(complaint_form, text="Fill in a Complaint", font=("Helvetica", 16))
title_label.place(x=20, y=20)

complaint_id = Label(complaint_form, text='Enter Complaint ID:', font=('bold', 10))
complaint_id.place(x=20, y=70);

date_complaint = Label(complaint_form, text='Enter Date:', font=('bold', 10))
date_complaint.place(x=20, y=100);

name = Label(complaint_form, text='Enter Name:', font=('bold', 10))
name.place(x=20, y=130);

surname = Label(complaint_form, text='Enter Surname:', font=('bold', 10))
surname.place(x=20, y=160);

email = Label(complaint_form, text='Enter Email:', font=('bold', 10))
email.place(x=20, y=190);

complaint_text = Label(complaint_form, text='Enter Text:', font=('bold', 10))
complaint_text.place(x=20, y=220);

text_classification = Button(complaint_form, text="Run Classification Algorithm", font=("italic", 10), bg="white", command=text_classification)
text_classification.place(x=20, y=320)

product_category = Label(complaint_form, text='Enter Product Category:', font=('bold', 10))
product_category.place(x=20, y=370);

company = Label(complaint_form, text='Enter Company Name:', font=('bold', 10))
company.place(x=20, y=400);

state = Label(complaint_form, text='Enter State (2 digits):', font=('bold', 10))
state.place(x=20, y=430);

zip_code = Label(complaint_form, text='Enter Zip code (5 digits):', font=('bold', 10))
zip_code.place(x=20, y=460);

submitted_via = Label(complaint_form, text='Enter Submitted via:', font=('bold', 10))
submitted_via.place(x=20, y=490);

e_complaint_id = Entry()
e_complaint_id.place(x=210, y=70)

e_date_complaint = Entry()
e_date_complaint.place(x=210, y=100)

e_name = Entry()
e_name.place(x=210, y=130)

e_surname = Entry()
e_surname.place(x=210, y=160)

e_email = Entry()
e_email.place(x=210, y=190)

e_complaint_text = Text(complaint_form, height=5, width=40)
e_complaint_text.place(x=210, y=220)

e_text_classification = Label(complaint_form, text='Get Proposed Product Category', font=('bold', 10), width=40)
e_text_classification.place(x=210, y=320)

e_product_category = Entry(width=53)
e_product_category.place(x=210, y=370)

e_company = Entry()
e_company.place(x=210, y=400)

e_state = Entry()
e_state.place(x=210, y=430)

e_zip_code = Entry()
e_zip_code.place(x=210, y=460)

e_submitted_via = Entry()
e_submitted_via.place(x=210, y=490)

insert = Button(complaint_form, text="Insert", font=("italic", 10), bg="white", command=insert)
insert.place(x=100, y=550)

delete = Button(complaint_form, text="Delete", font=("italic", 10), bg="white", command=delete)
delete.place(x=170, y=550)

update = Button(complaint_form, text="Update", font=("italic", 10), bg="white", command=update)
update.place(x=240, y=550)

get = Button(complaint_form, text="Get", font=("italic", 10), bg="white", command=get)
get.place(x=310, y=550)

clear_fields = Button(complaint_form, text="Clear Fields", font=("italic", 10), bg="white", command=clear_fields)
clear_fields.place(x=360, y=550)

main = Button(complaint_form, text="Home", font=("italic", 10), bg="white", command=open_main)
main.place(x=450, y=20)

title_label = Label(complaint_form, text="Check Response", font=("Helvetica", 16))
title_label.place(x=580, y=20)

img = Image.open("Logo_fara_background.png")
img = img.resize((170,30), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(img)
logo_label = Label(complaint_form, image=logo)
logo_label.place(x=850, y=20)

complaint_id_response = Label(complaint_form, text='Enter Complaint ID:', font=('bold', 10))
complaint_id_response.place(x=580, y=150);

company_response = Label(complaint_form, text='Response category:', font=('bold', 10))
company_response.place(x=580, y=180);

response_details = Label(complaint_form, text='Response details:', font=('bold', 10))
response_details.place(x=580, y=210);

date_response = Label(complaint_form, text='Date of Response:', font=('bold', 10))
date_response.place(x=580, y=290);

e_complaint_id_response = Entry()
e_complaint_id_response.place(x=770, y=150)

e_company_response = Entry(width=40)
e_company_response.place(x=770, y=180)

e_response_details = Text(complaint_form, height=4, width=30)
e_response_details.place(x=770, y=210)

e_date_response = Entry()
e_date_response.place(x=770, y=290)

get_response = Button(complaint_form, text="Get Response", font=("italic", 10), bg="white", command=get_response)
get_response.place(x=580, y=100)

clear_fields_response = Button(complaint_form, text="Clear Fields", font=("italic", 10), bg="white", command=clear_fields_response)
clear_fields_response.place(x=770, y=100)

complaint_form.mainloop()
