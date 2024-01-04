from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, Toplevel, Button, Tk, Menu

import pandas as pd
import os


def update(df, trv):
    trv.delete(*trv.get_children())
    for i in range(df.shape[0]):
        row = []
        for j in range(df.shape[1]):
            row.append(df.iloc[i][j])

        trv.insert('', 'end', values=row)


def search1():

    dfBooks = pd.read_csv('books.csv')
    df = dfBooks
    found = False

    q2 = str(q.get())

    for i in range(df.shape[0]):
        row = []
        for j in range(df.shape[1]):
            row.append(str(df.iloc[i][j]))

        if q2 in row:
            # print(row)
            temp0 = df.iloc[i][:]
            temp1 = pd.DataFrame(temp0)
            temp2 = temp1.transpose()
            print(temp2)

            found = True

        elif found == False:
            temp2 = pd.DataFrame()

        update(temp2, trv1)


def search2():

    dfBooksIssued = pd.read_csv('booksIssued.csv')
    df = dfBooksIssued
    found = False

    q2 = str(q.get())

    for i in range(df.shape[0]):
        row = []
        for j in range(df.shape[1]):
            row.append(str(df.iloc[i][j]))

        if q2 in row:
            # print(row)
            temp0 = df.iloc[i][:]
            temp1 = pd.DataFrame(temp0)
            temp2 = temp1.transpose()
            print(temp2)

            update(temp2, trv2)

            found = True

        elif found == False:
            temp2 = pd.DataFrame()

        update(temp2, trv2)


def searchall():
    search1()
    search2()


def clearall():
    opt()
    global dfBooks, dfBooksIssued
    update(dfBooks, trv1)
    update(dfBooksIssued, trv2)


def getrow(event):
    rowid = trv1.identify_row(event.y)
    item = trv1.item(trv1.focus())
    t1.set(item['values'][0])
    t2.set(item['values'][1])
    t3.set(item['values'][2])
    t4.set(item['values'][3])


def bgcolor():
    global Dark_Mode, Next_Mode, style, root, file, help

    if Dark_Mode == False:
        root['background'] = '#121212'
        Dark_Mode = True
        Next_Mode = 'Light'

        # Configure our treeview colors
        style.configure("Treeview",
                        background="#121212",
                        foreground="#ffffff",
                        rowheight=25,
                        fieldbackground="#121212",
                        font='georgia 12')

        style.configure("Treeview.Heading", background="#BB86FC",
                        foreground="#121212", relief="raised", font='Arial 12 bold')

        # Change selected color
        style.map('Treeview',
                  background=[('selected', '#03DAC5')],
                  foreground=[('selected', '#020202')])

        style.map('Treeview', font=[('selected', 'courier 12')])

        style.map('Treeview.Heading',
                  background=[('active', '#3700B3')],
                  foreground=[('active', '#FFFFFF')])

        # LabelFrame color change
        style.configure('TLabelframe', background='#121212',
                        foreground='white')
        style.configure('TLabelframe.Label',
                        background='#121212', foreground='white')
        style.configure('TButton', background='#242424', foreground='white')
        style.configure('TLabel', background='#121212', foreground='white')
        style.map('TButton', background=[('selected', '#BB86FC'), ('active', '#03DAC5')], foreground=[
                  ('selected', '#020202'), ('active', '#121212')])

        file.configure(bg='#121212', fg='#ffffff')
        help.configure(bg='#121212', fg='#ffffff')
        # style.configure('TEntry',background='#242424', foreground ='white' )

    else:
        root['background'] = '#ffffff'
        Dark_Mode = False
        Next_Mode = 'Dark'

        # Configure our treeview colors
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#000000",
                        rowheight=25,
                        fieldbackground="#ffffff")

        style.configure("Treeview.Heading", background="#6200EE",
                        foreground="#ffffff", relief="round")

        # Change selected color
        style.map('Treeview',
                  background=[('selected', '#03DAC6')],
                  foreground=[('selected', '#121212')])

        # LabelFrame color change
        style.configure('TLabelframe', background='#fdfdfd',
                        foreground='#000000')
        style.configure('TLabelframe.Label',
                        background='#ffffff', foreground='#000000')
        style.configure('TButton', background='#ffffff', foreground='#000000')
        style.configure('TLabel', background='#ffffff', foreground='#000000')

        file.configure(bg='#ffffff', fg='#121212')
        help.configure(bg='#ffffff', fg='#121212')
        # style.configure('TEntry',background='#ffffff', foreground ='#000000' )


def issue_book():

    global dfBooks, dfBooksIssued

    bookID = t1.get()

    idBook = dfBooks[dfBooks.bookID.astype(str) == bookID]

    if messagebox.askyesno('Confirm add', 'Are you sure you want to issue this book?'):
        if idBook.empty == False:

            avail = idBook[idBook.status.astype(str) == 'Available']
            if avail.empty == False:

                print('Available')
                issuedTo = t11.get()

                boolean_condition = (dfBooks.bookID.astype(str) == bookID)
                column_name = 'status'
                new_value = 'Issued'

                dfBooks.loc[boolean_condition, column_name] = new_value

                df3 = pd.DataFrame()

                df3['bookID'] = [bookID]
                df3['issuedTo'] = [issuedTo]

                print('\n Printing added data \n', df3, '\n')

                # dfBooksIssued = dfBooksIssued.append(df3)
                dfBooksIssued = pd.concat([dfBooksIssued, df3], ignore_index=True)

                dfBooks.to_csv('books.csv', index=False)
                dfBooksIssued.to_csv('booksIssued.csv', index=False)
            else:
                print('book already issued')
                messagebox.showerror("Error", "Book already issued")

        else:
            dfBooks = dfBooks.reset_index(drop=False)
            print('Book not available')

    clearall()


def add_new():

    global dfBooks

    bookid = t1.get()

    if not bookid == '':

        if messagebox.askyesno('Confirm add', 'Are you sure you want to add this book?'):
            idBook = dfBooks[dfBooks.bookID.astype(str) == bookid]
            if idBook.empty == True:

                bookID = t1.get()
                title = t2.get()
                auth = t3.get()
                status = 'Available'

                df2 = pd.DataFrame()

                df2['bookID'] = [bookID]
                df2['title'] = [title]
                df2['authers'] = [auth]
                df2['status'] = [status]

                print('\n Printing added data \n\n', df2, '\n')
                # dfBooks = dfBooks.append(df2)
                dfBooks = pd.concat([dfBooks, df2], ignore_index=True)
                dfBooks.to_csv('books.csv', index=False)

                # print(dfBooks)

                clearall()

        else:
            messagebox.showerror("Error", "Book id already exist")

    else:
        messagebox.showerror("Error", "Please enter book id.")


def delete_book():
    global dfBooks, dfBooksIssued

    bookid = t1.get()

    if messagebox.askyesno('Confirm delete', 'Are you sure you want to delete this book?'):
        idBook = dfBooks[dfBooks.bookID.astype(str) == bookid]
        if idBook.empty == False:

            dfBooks = dfBooks[dfBooks.bookID.astype(str) != bookid]
            dfBooksIssued = dfBooksIssued[dfBooksIssued.bookID.astype(
                str) != bookid]
            dfBooks.to_csv('books.csv', index=False)
            dfBooksIssued.to_csv('booksIssued.csv', index=False)

        else:
            print('error while deleting book', id)

        clearall()
    else:
        return True


def return_book():

    global dfBooks, dfBooksIssued

    bookID = t1.get()

    if messagebox.askyesno('Confirm return', 'Are you sure you want to return this book?'):

        idBook = dfBooks[dfBooks.bookID.astype(str) == bookID]
        if idBook.empty == False:
            issu = idBook[idBook.status.astype(str) == 'Issued']
            if issu.empty == False:

                print('Issued')

                boolean_condition = (dfBooks.bookID.astype(str) == bookID)
                column_name = 'status'
                new_value = 'Available'

                dfBooks.loc[boolean_condition, column_name] = new_value

                dfBooksIssued = dfBooksIssued[dfBooksIssued.bookID.astype(
                    str) != bookID]

                dfBooks.to_csv('books.csv', index=False)
                dfBooksIssued.to_csv('booksIssued.csv', index=False)

            else:
                print('book not issued')

        else:
            dfBooks = dfBooks.reset_index(drop=False)
            print('Book not available')

    clearall()


def opt():

    global dfBooks, dfBooksIssued

    if os.path.exists('books.csv') == True:
        dfBooks = pd.read_csv('books.csv')

    else:

        dfBooks = pd.DataFrame()

        dfBooks['bookID'] = []
        dfBooks['title'] = []
        dfBooks['authers'] = []
        dfBooks['status'] = []

        dfBooks.to_csv('books.csv', index=False)

        if os.path.exists('booksIssued.csv') == True:
            dfBooksIssued = pd.read_csv('booksIssued.csv')

        else:
            dfBooksIssued = pd.DataFrame()

            dfBooksIssued['bookID'] = []
            dfBooksIssued['issuedTo'] = []

            dfBooksIssued.to_csv('booksIssued.csv', index=False)


opt()

root = Tk()

menubar = Menu(root)
q = StringVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()
t4 = StringVar()
t11 = StringVar()
wrapper1 = ttk.LabelFrame(root, text='Books list')
wrapper2 = ttk.LabelFrame(root, text='Issued books list')
wrapper3 = ttk.LabelFrame(root, text='Search')
wrapper4 = ttk.LabelFrame(root, text='Edit Data')

wrapper1.pack(fill='both', expand='yes', padx=20, pady=10)
wrapper2.pack(fill='both', expand='yes', padx=20, pady=10)
wrapper3.pack(fill='both', expand='yes', padx=20, pady=10)
wrapper4.pack(fill='both', expand='yes', padx=20, pady=10)

Dark_Mode = False
Next_Mode = 'Dark'

# Add some style
style = ttk.Style()

# Pick a theme
style.theme_use("clam")

trv1 = ttk.Treeview(wrapper1, columns=(1, 2, 3, 4),
                    show='headings', height='6')
trv1.pack()

trv1.heading(1, text='Book ID')
trv1.heading(2, text='Title')
trv1.heading(3, text='Auther')
trv1.heading(4, text='Status')

trv1.bind('<Double 1>', getrow)

dfBooks = pd.read_csv('books.csv')

update(dfBooks, trv1)

trv2 = ttk.Treeview(wrapper2, columns=(1, 2), show='headings', height='6')
trv2.pack()

trv2.heading(1, text='Book ID')
trv2.heading(2, text='Issued To')

dfBooksIssued = pd.read_csv('booksIssued.csv')

update(dfBooksIssued, trv2)

# Menu bar

file = Menu(menubar, tearoff=0)
file.add_command(label=Next_Mode+" Mode", command=bgcolor)

file.add_separator()

file.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=file)

help = Menu(menubar, tearoff=0)
help.add_command(label="About")
menubar.add_cascade(label="Help", menu=help)

root.config(menu=menubar)

# Search Section

lbl = ttk.Label(wrapper3, text='Search')
lbl.pack(side=tk.LEFT, padx=10)
# lbl.place(relx=0.01,rely=0.01, relwidth=0.4,relheight=0.2)

end = Entry(wrapper3, textvariable=q)
end.pack(side=tk.LEFT, padx=6)
# end.place(relx=0.3,rely=0.01, relwidth=0.60,relheight=0.2)

btn1 = ttk.Button(wrapper3, text='Search', command=searchall)
# btn1.place(relx=0.3,rely=0.4, relwidth=0.40,relheight=0.2)
btn1.pack(side=tk.LEFT, padx=6)


btn2 = ttk.Button(wrapper3, text='Clear Search', command=clearall)
# btn2.place(relx=0.3,rely=0.7, relwidth=0.40,relheight=0.2)
btn2.pack(side=tk.LEFT, padx=6)

# User Data section

lbl11 = ttk.Label(wrapper4, text='Book ID')
lbl11.grid(row=0, column=0, padx=10, pady=4)
ent11 = ttk.Entry(wrapper4, textvariable=t1)
ent11.grid(row=0, column=1, padx=4, pady=4)

lbl12 = ttk.Label(wrapper4, text='Student Name')
lbl12.grid(row=0, column=3, padx=10, pady=4)
ent12 = ttk.Entry(wrapper4, textvariable=t11)
ent12.grid(row=0, column=4, padx=4, pady=4)

lbl21 = ttk.Label(wrapper4, text='Title')
lbl21.grid(row=1, column=0, padx=10, pady=4)
ent21 = ttk.Entry(wrapper4, textvariable=t2)
ent21.grid(row=1, column=1, padx=4, pady=4)

lbl31 = ttk.Label(wrapper4, text='Auther')
lbl31.grid(row=2, column=0, padx=10, pady=4)
ent31 = ttk.Entry(wrapper4, textvariable=t3)
ent31.grid(row=2, column=1, padx=4, pady=4)
'''
lbl41 = Label(wrapper4, text='Status')
lbl41.grid(row=3, column=0, padx=10, pady=4)
ent41 = Entry(wrapper4, textvariable=t4)
ent41.grid(row=3, column=1,padx=4, pady=4)
'''
up_btn = ttk.Button(wrapper4, text='Issue', command=issue_book)
add_btn = ttk.Button(wrapper4, text='Add', command=add_new)
delete_btn = ttk.Button(wrapper4, text='Delete', command=delete_book)
r_btn = ttk.Button(wrapper4, text='Return', command=return_book)

add_btn.grid(row=4, column=0, padx=2, pady=4)
up_btn.grid(row=6, column=0, padx=2, pady=4)
r_btn.grid(row=4, column=1, padx=2, pady=4)
delete_btn.grid(row=6, column=1, padx=2, pady=4)


root.title('My Library')
root.geometry('900x900')
root.mainloop()
