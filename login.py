import sys

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import hashlib
import datetime
import hashlib
import string
from pygrok import Grok
import time
from datetime import datetime as dt

#imports for database
import pymongo
import motor

client = pymongo.MongoClient("mongodb+srv://chapiiin:password20@cluster0-6dsmr.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.TBR
user = db.users


reg_users = {'_id':'temp'}

def IsAccount(un):
    ids = user.find()
    for key in ids:
        if un == key['_id']:
            return True
    return False


def AddAccount(un,pw):
    password_utf = pw.encode('utf-8')
    sha1hash = hashlib.sha1()
    sha1hash.update(password_utf)
    password_hash = sha1hash.hexdigest()
    reg_users.update({'_id':un})
    reg_users.update({'Password hash':password_hash})
    rez = user.insert_one(reg_users)
    return

def RemoveAccount(un):
    result1 = user.find({'_id':un})
    user.delete_one({'_id':un})

def PasswordReset(un, pw):
    RemoveAccount(un)
    AddAccount(un,pw)
    return


def PasswordMatches(a_hash, password):
    password_utf = password.encode('utf-8')
    sha1hash = hashlib.sha1()
    sha1hash.update(password_utf)
    password_hash = sha1hash.hexdigest()
    return password_hash == a_hash


def PrintAcc():
    for i in user.find():
        print(i['_id'])
        print(i['Password hash'])


def LoginCheck(un,pw):
    results = user.find()
    for key in results:
        if(un == key['_id'] and PasswordMatches(key['Password hash'], pw)):
            return True


def UserLogin():
    layout2 = [
        [sg.Text('Employee Login', size=(19,1), font ='Any 15')],
        [sg.Text('Username'), sg.Input(key='-username-', size = (20,1))],
        [sg.Text('Password'), sg.Input(key='-password-', size = (20,1), password_char='*')],
        [sg.T('', size =(6,1)), sg.Button('Login',bind_return_key=True), sg.Button('Exit')], 
    ]
    un = sg.Window('Employee', layout2,
                    auto_size_text = True,
                    text_justification='r',
                    grab_anywhere=False,
                    default_button_element_size=(3,1)
                   )


    while True:
        ev1, input = un.Read()
        if ev1 is None or ev1 == 'Exit':
            un.Close()
            break

             
        username = input['-username-']
        password = input['-password-']
        isAc = IsAccount(username)
        if LoginCheck(username, password) and ev1 in ('Login'):
            un.Close()
            return True
        
        if not LoginCheck(username, password) and ev1 in ('Login') and  not isAc:
            inval = [
                [sg.Text('This username does not have an account. Please try again.')],
                [sg.Button('Ok', bind_return_key=True)]
            ]
            err = sg.Window('Inccorect username or password', inval)
            while True:
                ev2, okay = err.Read()
                if ev2 in (None, 'Ok'):
                    err.Close()
                    break
                    
        if not LoginCheck(username, password) and ev1 in ('Login') and isAc:
            inval = [
                [sg.Text('Incorrect password. Please try again.')],
                [sg.Button('Ok', bind_return_key=True)]
            ]
            err = sg.Window('Inccorect username or password', inval)
            while True:
                ev2, okay = err.Read()
                if ev2 in (None, 'Ok'):
                    err.Close()
                    break


def main():
    UserLogin()
if __name__ == '__main__':
	main()
