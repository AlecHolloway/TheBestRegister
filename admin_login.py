#!/usr/bin/env python
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
admins = db.admins


reg_admins = {'_id':'temp'}


def AddAccount(un,pw):
    password_utf = pw.encode('utf-8')
    sha1hash = hashlib.sha1()
    sha1hash.update(password_utf)
    password_hash = sha1hash.hexdigest()
    reg_admins.update({'_id':un})
    reg_admins.update({'Password hash':password_hash})
    rez = admins.insert_one(reg_admins)
    return
	
def PasswordMatches(a_hash, password):
    password_utf = password.encode('utf-8')
    sha1hash = hashlib.sha1()
    sha1hash.update(password_utf)
    password_hash = sha1hash.hexdigest()
    return password_hash == a_hash


def AdminLoginCheck(un,pw):
    results = admins.find()
    for key in results:
        if(un == key['_id'] and PasswordMatches(key['Password hash'], pw)):
            print('you beautiful idiot, you did it')
            return True
			
   
   
def AdminLogin():
    layout2 = [
        [sg.Text('Administrator Login', size=(18,1), font ='Any 15')],
        [sg.Text('Username'), sg.Input(key='-username-', size = (20,1))],
        [sg.Text('Password'), sg.Input(key='-password-', size=(20,1), password_char='*')],
        [sg.T('', size =(6,1)),sg.Button('Login'), sg.Button('Exit')] 
    ]
    un = sg.Window('Username entry', layout2,
                    auto_size_text = True,
                    text_justification='r',
                    grab_anywhere=False)

    while True:
        ev1, input = un.Read()
        if ev1 in (None, 'Exit'):
            break

        username = input['-username-']
        password = input['-password-']
        #RemoveAccount('admin')
        if AdminLoginCheck(username, password) and ev1 in ('Login'):
            un.Close()
            return True
        
        elif not AdminLoginCheck(username, password) and ev1 in ('Login'):
            inval = [
                [sg.Text('Invalid credentials provided. Please try again.')],
                [sg.Button('Ok')]
            ]
            err = sg.Window('Inccorect username or password', inval)
            while True:
                ev2, okay = err.Read()
                if ev2 in (None, 'Ok'):
                    err.Close()
                    break
            

			
def main():
    AdminLogin()


if __name__ == '__main__':
	main()
