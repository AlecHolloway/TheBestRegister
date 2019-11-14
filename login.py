#!/usr/bin/env python
import sys

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import hashlib
sg.change_look_and_feel('DarkAmber') 



credentials = {'username':'password', 'admin':'admin', 'maclain':'admin', 'hayden':'hayden'}

def login_check(un,pw):
    for key in credentials:
        if(un == key and pw == credentials[key]):
            return True
                

def UsernameEnter():
    layout2 = [
        [sg.Text('Username entry screen', size=(30,1), font ='Any 15')],
        [sg.Text('Username'), sg.Input(key='-username-')],
        [sg.Text('Password'), sg.Input(key='-password-', password_char='*')],
        [sg.Button('Login'), sg.Button('Exit')] 
    ]
    un = sg.Window('Username entry', layout2,
                    auto_size_text = False,
                    text_justification='r',
                    grab_anywhere=False)

    while True:
        ev1, input = un.Read()
        if ev1 in (None, 'Exit'):
            break

             
        username = input['-username-']
        password = input['-password-']
            
        if login_check(username, password) and ev1 in ('Login'):
            print('Such a successful login')
            #open other window
            return True

    un.Close()
    



def main():
    UsernameEnter()


if __name__ == '__main__':
	main()