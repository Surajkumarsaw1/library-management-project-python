# importing library
import pandas as pd
import os
'''
import numpy as np
import matplotlib.pyplot as plt
'''

class Library:
    
    def __init__(self, dfBooks, dfBooksIssued):
    
        self.dfBooks = dfBooks
        self.dfBooksIssued = dfBooksIssued

    # addBook.py

    def addBook(self):

        bookID = str(input('Enter book id : '))
        title = str(input('Enter title of book : '))
        auth = str(input('Enter auther name : '))
        status = 'Available'

        df2 = pd.DataFrame()

        df2['bookID']=[bookID]
        df2['title']=[title]
        df2['authers']=[auth]
        df2['status']=[status]

        #df2 = df2.set_index('bookID')

        print('\n Printing added data \n\n',df2,'\n') 
        self.dfBooks = dfBooks.append(df2)
        self.dfBooks.to_csv('books.csv',index=False)

        #print(dfBooks)
        
    # viewBooks.py
    def viewBooks(self):
        print(self.dfBooks)
        
    # delete.py

    def delBook(self):
        bookid = str(input('Enter book id to delete : '))

        idBook = self.dfBooks[self.dfBooks.bookID.astype(str) == bookid]
        if idBook.empty == False :

            #print(self.dfBooks[self.dfBooks.bookID.astype(str) == bookid])
            self.dfBooks = self.dfBooks[self.dfBooks.bookID.astype(str) != bookid]
            self.dfBooks.to_csv('books.csv',index=False)

        else:
            print('error while deleting book',id)
            
    def viewIssuedBooks(self):
        print(self.dfBooksIssued)


    def issuebook(self):

        bookID = str(input('Enter book id : '))

        idBook = self.dfBooks[self.dfBooks.bookID.astype(str) == bookID]
        if idBook.empty == False :

            #bookID = str(input('Enter book id : '))

            avail = idBook[idBook.status.astype(str) == 'Available']
            if avail.empty == False :

                print('Available')
                issuedTo = str(input('Issue To : '))

                boolean_condition = (self.dfBooks.bookID.astype(str) == bookID)
                column_name = 'status'
                new_value = 'Issued'

                self.dfBooks.loc[boolean_condition, column_name] = new_value

                df3 = pd.DataFrame()

                df3['bookID']=[bookID]
                df3['issuedTo']=[issuedTo]

                print('\n Printing added data \n',df3,'\n') 
                self.dfBooksIssued = self.dfBooksIssued.append(df3)

                self.dfBooks.to_csv('books.csv',index=False)
                self.dfBooksIssued.to_csv('booksIssued.csv',index=False)

            else:
                print('book already issued')

        else:
            self.dfBooks = self.dfBooks.reset_index(drop=False)
            print('Book not available')
            
    def returnBook(self):

        bookID = str(input('Enter book id : '))

        idBook = self.dfBooks[self.dfBooks.bookID.astype(str) == bookID]
        if idBook.empty == False :

            #bookID = str(input('Enter book id : '))

            issu = idBook[idBook.status.astype(str) == 'Issued']
            if issu.empty == False :

                print('Issued')

                boolean_condition = (self.dfBooks.bookID.astype(str) == bookID)
                column_name = 'status'
                new_value = 'Available'

                self.dfBooks.loc[boolean_condition, column_name] = new_value

                self.dfBooksIssued = self.dfBooksIssued[self.dfBooksIssued.bookID.astype(str) != bookID]

                self.dfBooks.to_csv('books.csv',index=False)
                self.dfBooksIssued.to_csv('booksIssued.csv',index=False)

            else:
                print('book not issued')

        else:
            dfBooks = dfBooks.reset_index(drop=False)
            print('Book not available')


if __name__ == '__main__':
                
    while True:
        
        if os.path.exists('books.csv') == True :
            dfBooks = pd.read_csv('books.csv')
        else:

            dfBooks = pd.DataFrame()

            dfBooks['bookID']=[]
            dfBooks['title']=[]
            dfBooks['authers']=[]
            dfBooks['status']=[]

            #dfBooks = dfBooks.set_index('bookID') 

            dfBooks.to_csv('books.csv',index=False)
            #print(dfBooks)

        if os.path.exists('booksIssued.csv') == True :
            dfBooksIssued = pd.read_csv('booksIssued.csv')

        else:
            dfBooksIssued = pd.DataFrame()

            dfBooksIssued['bookID']=[]
            dfBooksIssued['issuedTo']=[]

            #dfBooksIssued = dfBooksIssued.set_index('bookID')

            dfBooksIssued.to_csv('booksIssued.csv',index=False)
            #print(dfBooksIssued)

        lib = Library(dfBooks,dfBooksIssued)


        print('1. Add book')
        print('2. Show books table')
        print('3. Delete book')
        print('4. Issue book')
        print('5. Show Issued books table')
        print('6. return book')
        print('7. Exit')

        x = str(input('Enter your choice : '))
        
        os_info = os.uname().sysname
        try:
            if os_info == 'Windows':
                os.system('cls')
            elif os_info == 'Linux':
                os.system('clear')
        except:
            pass

        print('You entered ' + x)
        print('\n')
        
        if x == str(1):
            lib.addBook()
        elif x == str(2):
            lib.viewBooks()
        elif x == str(3):
            lib.delBook()
        elif x == str(4):
            lib.issuebook()
        elif x == str(5):
            lib.viewIssuedBooks()
        elif x == str(6):
            lib.returnBook()
        elif x == str(7):
            break 
        else:
            print('Please give valid input')
    quit()
    exit()
