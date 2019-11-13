#!/usr/bin/env python
import sys

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
import hashlib


def main():

    def UsernameEnter():
        layout2 = [
            [sg.Text('Username entry screen', size=(30,1), font ='Any 15')],
            [sg.Text('Username'), sg.Input(key='-username-')],
            [sg.Text('Password'), sg.Input(key='-password-')],
        ]
        un = sg.Window('Username entry', layout2,
                        auto_size_text = False,
                        #text_justification='l',
                        #default_element_size(10,1),
                        return_keyboard_events=True,
                        grab_anywhere=False)

        while True:
            ev1, input = un.Read()
            if ev1 is None:
                break
              
            username = input['-username-']
            password = input['-password-']
            
            if username == 'admin' and password == 'admin':
                print('you logged in')
                break
            
    UsernameEnter()   


if __name__ == '__main__':
	main()