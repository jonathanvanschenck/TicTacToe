import socket
import classes
import varbs

if __name__=='__main__':
    # Setup server
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((varbs.HOST, varbs.PORT))
    ss.listen(2)
    # Get first player
    conn1, addr1 = ss.accept()
    s1 = classes.MessageSocket(conn1)
    s1.msend('You play X, waiting for additional player...')
    # Get second player
    conn2, addr2 = ss.accept()
    s2 = classes.MessageSocket(conn2)
    s2.msend('You play O, beginning game...')
    s1.msend('beginning game...')
    # Setup game
    sL = [s1,s2]
    char = ["X","O"]
    g = classes.Game()
    turn = 0
    turnO = 0
    w = ' '
    while turn<9 and w==' ':
        turnO = 1*turn
        for s in sL:
            s.msend(g.__str__())
        sL[(turn+1)%2].msend(char[turn%2]+"'s Turn. Waiting response...")
        while turn==turnO:
            sL[(turn)%2].msend(char[turn%2]+"'s Turn. Type \"r,c\"")
            response = sL[(turn)%2].mrecv()
            try:
                ss = response.split(",")
                i,j = int(ss[0]),int(ss[1])
                g.place(i,j,char[turn%2])
                w = g.win()
                turn += 1
            except IndexError:
                sL[(turn)%2].msend("Must use integers \"r,c\" of value 0, 1 or 2")
            except ValueError:
                sL[(turn)%2].msend("Must use integers \"r,c\" of value 0, 1 or 2")
    for s in sL:
        s.msend(g.__str__())
        s.msend("Winner is: "+w)
        s.msend("term")
        s.s.close()
    ss.close()