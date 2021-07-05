#database directory

import sys
import database
from database import Simpledb
phonefile = "telephone.txt"
db = Simpledb(phonefile)

def addCommand():
    print('Enter a name')
    name = input()
    print('Enter a phone')
    phone = input()
    if name and phone:
        db.insert(name, phone)
    else:
        print('You must enter a name and a phone.')

def findCommand():
    print('Enter a name')
    name = input()
    if name:
        phone = db.select_one(name)
        if phone:
            print(phone)
        else:
            print('Nothing found')
    else:
        print('You must enter a name.')
   

def deleteCommand():
    print('Enter a name')
    name = input()
    if name:
        found = db.delete(name)
        if not found:
            print('That name was not found.')
    else:
        print('You must enter a name.')
    

def updateCommand():
    print('Enter a name')
    name = input()
    if name:
        oldphone = db.select_one(name)
        if oldphone:
            print('Enter a phone')
            newphone = input()
            if newphone:
                db.update(name, newphone)
            else:
                print('You must enter a phone')

        else:
            print('Nothing found')
    else:
        print('You must enter a name')
        


while True:
    
    print('Choose a function:\n A - Add\n F - Find\n D - Delete\n U - Update\n Q - Quit\n')
    choice = input().upper()

    if choice.startswith('A'):
        addCommand()

    elif choice.startswith('F'):
        findCommand()

    elif choice.startswith('D'):
        deleteCommand()

    elif choice.startswith('U'):
        updateCommand()

    elif choice.startswith('Q'):
        sys.exit()

    else:
        print('You must choose one of the functions listed.\n')
