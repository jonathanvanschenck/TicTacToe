import socket
import classes
import varbs

if __name__=='__main__':
    s = classes.MessageSocket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    s.s.connect((varbs.HOST, varbs.PORT))
    msg = s.mrecv()
    while msg!="term":
        print(msg)
        if "Type" in msg:
            coords = input("?")
            s.msend(coords)
        msg = s.mrecv()