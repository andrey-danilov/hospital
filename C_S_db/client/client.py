import socket
from tkinter import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
key = RSA.importKey(open('../private.der').read())
cipher = PKCS1_OAEP.new(key)



def leftclick(event):
    name = None
    select = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 9999
    s.connect((host, port))
    name = listbox1.get("active")
    select =("SELECT * FROM public.people ")

    print (select)
    key = RSA.importKey(open('../public.der').read())
    cipher = PKCS1_OAEP.new(key)
    select = cipher.encrypt(select.encode('utf-8'))
    print(select)
    s.send(select)
    names = s.recv(1024)
    message = cipher.decrypt(names)
    print(message.decode('utf-8'))
    print (names)
    s.close()
    text1.insert(1.0, names)
    name = None
    names=None

def window_deleted():

    root.quit()
root=Tk()
root.title('title')
root.geometry('600x400+300+200')
root.protocol('WM_DELETE_WINDOW', window_deleted)
root.resizable(True, False)
button1=Button(root,text='ok',bg='black',fg='red',font='arial 14' )
button1.pack(side="top")
button1.bind('<Button-1>', leftclick)
listbox1=Listbox(root,width = 5, height = 10 ,selectmode=EXTENDED)
list1=["AMD","Intel"]
for i in list1:
    listbox1.insert(END,i)
listbox1.pack(side="top")

text1=Text(root,height=50,width=50,font='Arial 14',wrap=WORD)
text1.pack(side="left")
root.mainloop()
