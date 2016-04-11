import socket
import psycopg2
import sys

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
    print (select)

    try:
      con = psycopg2.connect(database='ctock', user='postgres' , password="1311")
      cur = con.cursor()
      cur.execute(select)
      rows = cur.fetchall()
      print (rows)
      clientsocket.send(str(rows[0][0]))

    except psycopg2.DatabaseError, e:
        clientsocket.send( 'Error %s' % e)
      #sys.exit(1)
    finally:
      if con:
        con.close()
    clientsocket.close()