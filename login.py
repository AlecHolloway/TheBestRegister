import sys

if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg
    
import hashlib

def UsernameEnter():
    access = False

    layout = [
        [sg.Text('Username entry screen', size=(30,1), font ='Any 15')],
        [sg.Text('Username'), sg.Input(key='-username-')],
        [sg.Text('Password'), sg.Input(key='-password-')],
        [sg.Button('Login'), sg.Button('Exit')]
    ]
    window = sg.Window('Username entry', layout,
                auto_size_text = False,
                #text_justification='l',
                #default_element_size(10,1),
                grab_anywhere=False)

    while True:
        event, values = window.Read()
          
        username = values['-username-']
        password = values['-password-']
        
        if event in (None, 'Exit'):
            break
        if event in ('Login'):
            access = True
        
        if username == 'admin' and password == 'admin' and access == True:
                print('Login Successful')
                window.Close()
                return access

    window.Close()
    
    
def main():
    UsernameEnter()


if __name__ == '__main__':
	main()