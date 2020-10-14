#Tic-Tac-Toe over LAN
#player1.py acts as the server
import socket
import random

board = [[' 1 ',' 2 ',' 3 '],[' 4 ',' 5 ',' 6 '],[' 7 ',' 8 ',' 9 ']]

player1M=[]
player2M=[]
players=[]
isFinished=False


def constructBoard():
    s='\nTablero\n'
    for row in board:
        s+=str(row)+'\n'
    s+='\n'
    return s

def printBoard():
    print ('\nTablero')
    for row in board:
        print (row)
    print ('\n') 

def piece(currentPlayer):
    piece='Null'
    if(currentPlayer==player1):
        piece=' X '
    else:
        piece=' O '
    return piece

def checkWinner(board,position,currentPlayer,sock):
    possibilities = [[1,4,7],[2,5,8],[3,6,9],[1,2,3],[4,5,6],[7,8,9],[1,5,9],[7,5,3]]

    if currentPlayer==player1:
        player1M.append(int(position))
        marks=0
        for column in possibilities:
            for element in column:
                if element in player1M:
                    marks+=1
                    if marks==3:
                        print (player1, ' es el ganador!\Gracias')
                        sock.send('%s es el ganador!\Gracias'%player1)
                        return True
            marks=0
    else:
        player2M.append(int(position))
        marks=0
        for column in possibilities:
            for element in column:
                if element in player2M:
                    marks+=1
                    if marks==3:
                        print (player2, ' es el ganador!\Gracias')
                        sock.send('%s es el ganador!\Gracias'%player2)
                        return True
            marks=0
    if len(player1M)+len(player2M)==9:
        print ('Hubo un empate!')
        sock.send('Hubo un empate!')
        return True
    return False

def changePlayer(currentPlayer):
    if(currentPlayer==player1):
        currentPlayer=player2
    else:
        currentPlayer=player1
    return currentPlayer

def theGame(location,sock,currentPlayer):
    position=str(location)
    if(int(position) in range(1,4)):
        try:
            board[0][board[0].index(' %s '%position)]=piece(currentPlayer)
            printBoard()
            sock.send(constructBoard())
        except:
            if currentPlayer==player2:
                sock.send('\nError en 1 de las 3 primeras posiciones')
            else:
                print ('\nError en 1 de las 3 primeras posiciones')

    elif int(position) in range(4,7):
        try:
            board[1][board[1].index(' %s '%position)]=piece(currentPlayer)
            printBoard()
            sock.send(constructBoard())
        except:
            if currentPlayer==player2:
                sock.send('\nError en 1 de las posiciones del medio')
            else:
                print ('\nError en 1 de las posiciones del medio')
    elif int(position) in range(7,10):
        try:
            board[2][board[2].index(' %s '%position)]=piece(currentPlayer)
            printBoard()
            sock.send(constructBoard())
        except:
            if currentPlayer==player2:
                sock.send('\nError en 1 de las 3 ultimas posiciones')
            else:
                print ('\nError en 1 de las 3 ultimas posiciones')
    else:
        if currentPlayer==player2:
            sock.send('Posicion fuera del rango!')
        else:
            print ('Posicion fuera del rango')

salir = False
opcion = 0
while not salir:
    print ('Juego de Tic-Tac-Toe!\n')
    print ('Menu de opciones:\n')
    print ('1- Jugador vs Jugador')
    print ('2- Jugador vs Maquina')
    print ('3- Salir\n')


    opcion = raw_input("Elige una opcion:")
 
    if opcion == "1":
        print ('\nUsted a elegido la opcion de Jugador vs Jugador')
        host = '192.168.0.8'

        s = socket.socket()
        port = 21217               
        s.bind((host, port))
        print ('\n\nEl juego esta corriendo en el puerto %s:%s esperando al Jugador 2'%(host,port))
        s.listen(1)
        sock, addr = s.accept()         
        while True:
            print ('El Jugador 2 se ha conectado!', addr)
            a="Se ha conectado correctamente a %s "%host
            sock.send(str(a))
            player2 = sock.recv(4096)
            player1="Jugador 1"
            players.append(player1)
            players.append(player2)
            play = '\nLobby\n%s vs. %s\n\n%s'%(player1,player2,constructBoard())
            print (play)
            sock.send(play)
            currentPlayer = random.choice(players)
            while isFinished==False:
                if currentPlayer==player1:
                    print ('\n\nEs tu turno. %s elige la posicion que deseas jugar'%player1)
                    sock.send("\n\nEs el turno de %s. Espera su jugada..."%player1)
                    position=raw_input()
                    theGame(position,sock,currentPlayer)
                    isFinished=checkWinner(board, position,currentPlayer,sock)
                    currentPlayer=changePlayer(currentPlayer)
                else:
                    print ("\n\nEs el turno de %s. Espera su jugada..."%player2)
                    sock.send("\n\nEs tu turno. %s elige la posicion que deseas jugar"%player2)
                    position=sock.recv(4096)
                    theGame(position,sock,currentPlayer)
                    isFinished=checkWinner(board, position,currentPlayer,sock)
                    currentPlayer=changePlayer(currentPlayer)
            break
        sock.close()
        salir = True
    elif opcion == "2":
        print ("Pendiente")
    elif opcion == "3":
        salir = True
    else:
        print ("Introduce un numero entre 1 y 2")
 
print ("Gracias por jugar")


