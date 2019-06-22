class MessageSocket:
    def __init__(self,VanillaSocket):
        self.s = VanillaSocket
        
    def msend(self,msg):
        mL = len(msg)
        msg = ("{:0>5}".format(mL)).encode()+msg.encode()
        totsent = 0
        while totsent<=mL:
            sent = self.s.send(msg[totsent:])
            if sent==0:
                raise RuntimeError("Socket connection is broken")
            totsent += sent
        return totsent
        
    def mrecv(self):
        chunks = []
        bytes_recv = 0
        while bytes_recv<5:
            chunk = self.s.recv(5-bytes_recv)
            if chunk == b'':
                raise RuntimeError("Socket connection is broken")
            chunks.append(chunk)
            bytes_recv += len(chunk)
        mL = int(b''.join(chunks))
        bytes_recv = 0
        while bytes_recv<mL:
            chunk = self.s.recv(min(mL-bytes_recv,2048))
            if chunk == b'':
                raise RuntimeError("Socket connection is broken")
            chunks.append(chunk)
            bytes_recv += len(chunk)
        return (b''.join(chunks))[5:].decode()

def genTriples(lis):
    l = len(lis)
    res = []
    for i in range(l-2):
        for j in range(i+1,l-1):
            for k in range(j+1,l):
                res += [[lis[i],lis[j],lis[k]]]
    return res
    
class Game:
    def __init__(self):
        self.board = [[" "," "," "],[" "," "," "],[" "," "," "]]
        self.pboard = [[" "," "," "],[" "," "," "],[" "," "," "]]
    
    def __str__(self):
        ll = "  0 1 2\n  -----\n"
        ll += "\n  -----\n".join([str(i)+":"+"|".join(self.board[i]) for i in range(3)])
        return ll
    
    def place(self,i,j,T,projective=False):
        if not projective:
            if self.board[i][j] == " ":
                self.board[i][j] = 1*T
            else:
                raise IndexError
        else:
            self.pboard = [[1*self.board[i][j] for j in range(3)] for i in range(3)]
            if self.pboard[i][j] == " ":
                self.pboard[i][j] = 1*T
            else:
                raise IndexError
            
    def win(self,projective=False):
        if not projective:
            b = self.board
        else:
            b = self.pboard
        XiL = genTriples([[i,j] for i in range(3) for j in range(3) if b[i][j]=="X"])
        for Xi in XiL:
            if (Xi[0][0]+Xi[1][0]+Xi[2][0])%3==0 and (Xi[0][1]+Xi[1][1]+Xi[2][1])%3==0:
                return "X"
        OiL = genTriples([[i,j] for i in range(3) for j in range(3) if b[i][j]=="O"])
        for Oi in OiL:
            if (Oi[0][0]+Oi[1][0]+Oi[2][0])%3==0 and (Oi[0][1]+Oi[1][1]+Oi[2][1])%3==4:
                return "O"
        return " "

if __name__=="__main__":
    g = Game()
    ii = 0
    t = ["X","O"]
    w = " "
    while w==" " and ii<9:
        print(g)
        s = input(t[ii%2]+"'s Turn. Type \"r,c\":").split(",")
        try:
            i,j = int(s[0]),int(s[1])
            g.place(i,j,t[ii%2])
            w = g.win()
            ii += 1
        except IndexError:
            input("Must use integers \"r,c\" of value 0, 1 or 2")
        except ValueError:
            input("Must use integers \"r,c\" of value 0, 1 or 2")
    print(g)
    print("Winner is: "+w)
        
        