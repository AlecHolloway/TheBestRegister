import login
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

# imports for database
import pymongo
import motor
import pandas as pd

client = pymongo.MongoClient(
"mongodb+srv://chapiiin:password20@cluster0-6dsmr.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.TBR
user = db.users
transactions = db.transactions

def main():
    print()

def length(s):
    count = 0
    for i in s:
        count = count + 1
    return count


def Panel():
    layout0 = [
    [sg.Button('Add Account', size=(20, 1)), sg.Button('Delete Account', size=(20, 1))],
    [sg.Button('Reset Password', size=(20, 1)), sg.Button('Exit', size=(20, 1))]]

    window0 = sg.Window('Administrator Control Panel', layout0, default_button_element_size=(10, 1),
       auto_size_buttons=False)
    while True:
        event,value=window0.Read()
        if event is None or event == 'Exit':
            window0.Close()
            break

        if event == 'Add Account':
            layout2 = [
            [sg.Text('Username', size=(10,1)), sg.Input(key='-un-')],
            [sg.Text('Password', size=(10,1)), sg.Input(key='-pw1-')],
            [sg.Text('Confirm password', size=(20,1)), sg.Input(key='-pw2-')],
            [sg.Button('Submit', size=(10, 1)), sg.Button('Cancel', size=(10, 1))]]
            window2 = sg.Window('Add Account', layout2, auto_size_text = True,default_button_element_size=(10, 1), size=(512,120))
            addAcc = True
            while addAcc:
                event2, value2 = window2.Read()
                user2 = value2['-un-']
                pass21 = value2['-pw1-']
                pass22 = value2['-pw2-']
                unLength = length(user2)

                if event2 is None or event2 == 'Cancel':
                    window2.Close()
                    break
                if unLength < 1:
                    unval = [
                        [sg.Text('Invalid credentials provided. Please try again.')],
                        [sg.Button('Ok')]
                        ]
                    erro = sg.Window('Username or password cannot be null', unval)
                    nullName = True
                    while nullName:
                        ev2, okay = erro.Read()
                        if ev2 is None or ev2 == 'Ok':
                            erro.Close()
                            break
                            break
                if event2 == 'Submit' and pass21 == pass22 and unLength > 0:
                    login.AddAccount(user2, pass21)
                    layout21 = [
                        [sg.Text('User account has been created.')],
                        [sg.Button('Ok')]
                    ]
                    cre = sg.Window('Creation successful', layout21)
                    passwordsMatch = True
                    while passwordsMatch:
                        ev2, okay = cre.Read()
                        if ev2 is None or ev2 == 'Ok':
                            cre.Close()
                            break
                            break
                    window2.Close()
                    break
                if event2 == 'Submit' and pass21 != pass22:
                    inval = [
                        [sg.Text('Invalid credentials provided. Please try again.')],
                        [sg.Button('Ok')]
                    ]
                    err = sg.Window('Passwords did not match', inval)
                    passwordsMatch = False
                    while passwordsMatch:
                        ev2, okay = err.Read()
                        if ev2 is None or ev2 == 'Ok':
                            err.Close()
                            break
                            break
                    
        if event == 'Delete Account':
            layout3 = [[sg.Text('Enter the username of the account to be deleted', size=(50,1))],
            [sg.Input(key='-user-')],
            [sg.Button('Submit', size=(10,1),bind_return_key=True), sg.Button('Cancel', size=(10,1))]]
        
            window3 = sg.Window('Delete Account', layout3, default_button_element_size=(10,10))
            delAcc = True
            while delAcc:
                event3, value3 = window3.Read()
                user3 = value3['-user-']
                un3Len = length(user3)
                if event3 is None or event3 == 'Cancel':
                    window3.Close()
                    break
                if event3 == 'Submit' and un3Len != 0:
                    dele = [
                        [sg.Text('User account has been deleted.')],
                        [sg.Button('Ok')]
                    ]
                    login.RemoveAccount(user3)
                    deleted = sg.Window('Deletion successful', dele)
                    while True:
                        ev2, okay = deleted.Read()
                        if ev2 in (None, 'Ok'):
                            deleted.Close()
                            window3.Close()
                            break
                            break

                if event3 == 'Submit' and un3Len == 0:
                    inval = [
                            [sg.Text('Cannot delete nonexistent account. Please try again.')],
                            [sg.Button('Ok')]
                            ]
                    erd = sg.Window('Cannot delete nonexistent account. Please try again.', inval)
                    invalid_user = True
                    while invalid_user:
                        ev2, okay = erd.Read()
                        if ev2 is None or ev2 == 'Ok':
                            erd.Close()
                            break
                            break

        if event == 'Reset Password':
            layout4 = [[sg.Text('', size=(20, 1), font='Helvetica, 18')],
            [sg.T('', size=(7,1)),sg.Text('Username'), sg.Input(key='-un-')],
            [sg.T('',size=(4,1)),sg.Text('New password'), sg.Input(key='-pw1-')],
            [sg.Text('Confirm new password'), sg.Input(key='-pw2-')],

            [sg.Button('Submit', size=(10, 1), bind_return_key=True), sg.Button('Cancel', size=(10, 1))]]
            window4 = sg.Window('Password reset', layout4, default_button_element_size=(10, 10))
            resPass = True
            while resPass:
                event4, value4 = window4.Read()
                user4 = value4['-un-']
                pass41 = value4['-pw1-']
                pass42 = value4['-pw2-']
                resLen = length(user4)
                pasLen = length(pass41)
                if event4 is None or event4 == 'Cancel':
                    window4.Close()
                    break
                if event4 == 'Submit' and pass41 == pass42 and resLen != 0:
                    login.PasswordReset(user4, pass41)
                    layout41 = [
                        [sg.Text('Password has been reset.')],
                        [sg.Button('Ok')]
                    ]
                    re = sg.Window('Reset successful.', layout41)
                    while True:
                        ev4, okay = re.Read()
                        if ev4 is None or ev4 == 'Ok':
                            re.Close()
                            break
                            break
                    window4.Close()
                    break
                if event4 == 'Submit' and pass41 != pass42:
                    inval = [
                        [sg.Text('Invalid credentials provided. Please try again.')],
                        [sg.Button('Ok')]
                    ]
                    err = sg.Window('Passwords did not match', inval)
                    while True:
                        ev2, okay = err.Read()
                        if ev2 in (None, 'Ok'):
                            err.Close()
                            break

                if event4 == 'Submit' and resLen == 0 or pasLen == 0:
                    inval = [
                            [sg.Text('Cannot reset nonexistent account. Please try again.')],
                            [sg.T('', size=(15,1)),sg.Button('Ok')]
                            ]
                    erd = sg.Window('Cannot reset nonexistent account. Please try again.', inval)
                    invalid_user = True
                    while invalid_user:
                        ev2, okay = erd.Read()
                        if ev2 is None or ev2 == 'Ok':
                            erd.Close()
                            break
                            break
      
      
      

if __name__ == '__main__':
	main()
            
