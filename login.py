#!/usr/bin/env python
import sys

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import hashlib
sg.change_look_and_feel('DarkAmber') 



credentials = {'username':'5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8', 'admin':'d033e22ae348aeb5660fc2140aec35850c4da997', 'maclain':'f798ddf054d3894403dc9c5e58c253be66defe4b'}


    
def PasswordMatches(a_hash, password):
    password_utf = password.encode('utf-8')
    sha1hash = hashlib.sha1()
    sha1hash.update(password_utf)
    password_hash = sha1hash.hexdigest()
    return password_hash == a_hash

def login_check(un,pw):
    for key in credentials:
        if(un == key and PasswordMatches(credentials[key], pw)):
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
            un.Close()
            return True
            
        elif not login_check(username, password) and ev1 in ('Login'):
            print('Invalid credentials provided. Please try again.')
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
    UsernameEnter()


if __name__ == '__main__':
	main()
