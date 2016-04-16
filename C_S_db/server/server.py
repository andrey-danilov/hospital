import socket
import psycopg2
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

private = RSA.generate(2048)
f = open('../private.der','wb')
f.write(private.exportKey('PEM'))
f.close()



public = private.publickey()
print(public)
f = open('../public.der','wb')
f.write(public.exportKey('PEM'))
f.close()







con = None
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999
serversocket.bind((host, port))


serversocket.listen(5)

while True:
    clientsocket,addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))
    select=clientsocket.recv(1024)

    keya = RSA.importKey(open('../private.der').read())
    cipher = PKCS1_OAEP.new(keya)
    message = cipher.decrypt(select)
    print(message.decode('utf-8'))
    print('sdfsdf')


    print (select)

    try:
      con = psycopg2.connect(database='hospi', user='postgres' , password="1311")
      cur = con.cursor()
      #cur.execute(select)



      key = RSA.importKey(open('../public.der').read())
      cipher = PKCS1_OAEP.new(key)
      ciphertext = cipher.encrypt(select)

      clientsocket.send(ciphertext)

    except psycopg2.DatabaseError as e:
        clientsocket.send( e)

    finally:
      if con:
        con.close()
    clientsocket.close()