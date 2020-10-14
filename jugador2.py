import socket             

print ('Juego de Tic-Tac-Toe!\nConectandose al servidor del jugador 1!')
host='192.168.0.8'

s = socket.socket() 
port = 21217               

s.connect((host, port))

print (s.recv(4096))
playername="Jugador 2"
s.send(playername)
print (s.recv(4096))
while True:
    data=s.recv(4096)
    if 'elige' in data:
        print (data)
        position=raw_input()
        s.send(position)
    else:
        print (data)

    if 'Gracias' in data:
        break

s.close()           
