from Tkinter import *
import sqlite3
import time

conn = sqlite3.connect( 'transactions.db' )
c = conn.cursor()

root = Tk()

#Initialize the Record table & set initial Amount = 0
c.execute("CREATE TABLE IF NOT EXISTS Record(DateTime TEXT, Amount REAL, Note TEXT, Balance REAL);")

def deposit():    
    global newBalance, amount
    #Call convertRaw function
    convertRaw()   
     
    #Add deposit value to the current balance and get current time
    amount = float( add.get() )        
    newBalance = amount + currentBalance    
    entryTime = time.ctime()
        
    #Call runSql to add a new entry to database
    runSql( "INSERT INTO Record VALUES( '{0}', '{1}', '{2}', '{3}' )".format( entryTime, amount, addNote.get(), newBalance ) )
    conn.commit()

    # Call showEntries to show updated list of transactions
    showEntries()

    cbEntry.delete( 0, END )
    cbEntry.insert( 0, newBalance )

    # Clear the deposit entries
    depEntry.delete( 0, END )
    dnEntry.delete( 0, END )

    return newBalance, amount
    

def withdrawl():
    # Call convertRaw to get balance from database
    convertRaw()
    # Setting global variables to 0 before assigning new values
    newBalance = 0
    amount = 0
    # Change amount to negative value and calculate newBalance
    amount = float( minus.get() ) * -1 
    newBalance = amount + currentBalance

    entryTime = time.ctime()
   
    #Call runSql to add a new entry to database
    runSql( "INSERT INTO Record VALUES( '{0}', '{1}', '{2}', '{3}' )".format( entryTime, amount, minusNote.get(), newBalance ) )
    conn.commit()

    showEntries()

    cbEntry.delete( 0, END )
    cbEntry.insert( 0, newBalance )   
    
    # Clear the withdrawl entries 
    witEntry.delete( 0, END )
    wnEntry.delete( 0, END )

    return newBalance, amount


# Function to change the memory location retrieved from database into a useful number
def convertRaw():
    global currentBalance    
    currentBalance = 0
    #Get current balance from database and change it into a useful number
    cb = c.execute( "SELECT SUM( Amount ) FROM Record" )    
    rawBalance = [ c.fetchone() ]          
    w = str( rawBalance )    
    x = w[ 2 : ( len( w ) - 3 ) ]    
    currentBalance = float( x )    

    return currentBalance


# Function to run sql command and then call showEntries()
def runSql( cmd ):
    x = c.execute( cmd )
    conn.commit()        
        
    
# Function to display the database
def showEntries():
    global entries
    ptBox.delete( 0, END )
    tranList = c.execute ( "SELECT DateTime, Amount, Note, Balance FROM Record WHERE Balance != 0 ORDER BY DateTime DESC" )
    entries = tranList.fetchall()
    for DateTime, Amount, Note, Balance in entries:
        ptBox.insert( END, 'NEW ENTRY', DateTime, Amount, Note, Balance, '----------' )


if "SELECT COUNT(*) FROM Record = 0":
    c.execute( "INSERT INTO Record VALUES( null, 0, 'Initialize', 0)" )

# Function to make GUI window
def makeWindow():

    global add, minus, addNote, minusNote, ptBox, cbEntry, depEntry, dnEntry, witEntry, wnEntry

    win = Toplevel( root )
    win.title( 'Bank Account Balance' )

    topFrame = Frame( win )
    topFrame.pack()

    #Current Balance Label and Entry
    cbLabel = Label( topFrame, text = 'Your Current Balance Is: ', padx = 3 )
    cbLabel.grid( row = 1, column = 0 )

    cbEntry = Entry( topFrame )
    cbEntry.grid( row = 1, column = 1 )

    #Button to add to balance, entry for doing it 
    depButton = Button( topFrame, text = 'Deposit', command = deposit )
    depButton.grid( row = 2, column = 0, padx = 5, pady = 2 )

    add = StringVar()
    depEntry = Entry( topFrame, textvariable = add )
    depEntry.grid( row = 2, column = 1, padx = 2  )

    #label and entry for deposit note    
    dnLabel = Label( topFrame, text = 'Deposit Note: ', padx = 5 )
    dnLabel.grid( row = 3, column = 0 )

    addNote = StringVar()
    dnEntry = Entry( topFrame, textvariable= addNote )
    dnEntry.grid( row = 3, column = 1, padx = 2  )

    #Button to withdraw, entry for doing it 
    witButton = Button( topFrame, text = 'Withdrawl', command = withdrawl )
    witButton.grid( row = 5, column = 0, padx = 5, pady = 2 )

    minus = StringVar()
    witEntry = Entry( topFrame, textvariable = minus )
    witEntry.grid( row = 5, column = 1, padx = 2  )

    #label and entry for withdrawl note    
    wnLabel = Label( topFrame, text = 'Withdrawl Note: ', padx = 5 )
    wnLabel.grid( row = 6, column = 0 )

    minusNote = StringVar()
    wnEntry = Entry( topFrame, textvariable = minusNote )
    wnEntry.grid( row = 6, column = 1, padx = 2  )


    bottomFrame = Frame( win )
    bottomFrame.pack()

    #label and listbox to display past transactions
    ptLabel = Label( bottomFrame, text = 'Past Transactions:', padx = 5, pady = 2 )
    ptLabel.grid( row = 8, column = 0, pady = 2 )    

    ptBox = Listbox( bottomFrame, width = 30, height = 12 )
    ptBox.grid( row = 9, column = 0, padx = 2 ) 
    
    scrollbar = Scrollbar( bottomFrame, orient = VERTICAL )
    scrollbar.grid( row = 9, column = 1, sticky = NS )
    scrollbar.configure( command = ptBox.yview )    

    ptBox.configure( yscrollcommand = scrollbar.set )
    
    return win


win = makeWindow()
win.mainloop()