import time
output = ''
Visit ={}

'''
playerClass
'''
def GetVal(c):
    if c=='10' or c=='T':
        return 7
    if c=='J':
        return 8
    if c=='Q':
        return 9
    if c=='K':
        return 10
    if c=='A':
        return 11
    if c=='2':
        return 12
    return int(c)-3
def SetChar(x):
    if x<=6:
        return str(3+x)
    if x==7:
        return 'T'
    if x==8:
        return 'J'
    if x==9:
        return 'Q'
    if x==10:
        return 'K'
    if x==11:
        return 'A'
    if x==12:
        return '2'
def changerOut(s):
    li = []
    for i in list(s):
        if i=='T':
            li.append('10')
        else:
            li.append(i)
    return li
def toNow(li):
    temp = [0]*16
    Now = ''
    for i in li:
        temp[GetVal(i)]+=1
    for i in range(4,0,-1):
        for j in range(13):
            if temp[j]==i:
                for w in range(i):
                    Now = Now + SetChar(j)
    return Now
class timerecorder:
    def __init__(self):
        self.t = 0
    def refresh(self):
        self.t = time.time()
class player:
    def __init__(self):
        self.a = [0]*16
        self.cnt = 0
        self.CanThree = False
        self.CanBoom = False
        self.CanMS = False
        self.CanMC = False
        self.CanM3 = False
    def out(self):
        for i in range(16):
            for j in range(self.a[i]):
                print(SetChar[i],end = '')
        print()
    def CanPlaySingle(self,x):
        return self.a[x]>=1
    def CanPlayCouple(self,x):
        return self.a[x]>=2
    def CanPlayThree(self,x):
        return self.a[x]>=3
    def CanPlayBoom(self,x):
        return self.a[x]>=4
    def CanPlayMoreSingle(self,l,r):
        if l>r and 14-l+r>=5:
            if l<11:
                return False
            for i in range(l,13):
                if not self.CanPlaySingle(i):
                    return False
            for i in range(0,r+1):
                if not self.CanPlaySingle(i):
                    return False
            return True
        elif r-l<4 or r>12:
            return False
        for i in range(l,r+1):
            if not self.CanPlaySingle(i):
                return False
        return True
    def CanPlayMoreCouple(self,l,r):
        if l>r and 14-l+r>=2:
            if l<11:
                return False
            for i in range(l,13):
                if not self.CanPlayCouple(i):
                    return False
            for i in range(0,r+1):
                if not self.CanPlayCouple(i):
                    return False
            return True
        if r-l<1 or r>12:
            return False
        for i in range(l,r+1):
            if not self.CanPlayCouple(i):
                return False
        return True
    def CanPlayMoreThree(self,l,r):
        if l>r and 14-l+r>=2:
            if l<11:
                return False
            for i in range(l,13):
                if not self.CanPlayThree(i):
                    return False
            for i in range(0,r+1):
                if not self.CanPlayThree(i):
                    return False
            return True
        if r-l<1 or r>12:
            return False
        for i in range(l,r+1):
            if not self.CanPlayThree(i):
                return False
        return True
    def CanPlay3Single(self,x,y):
        if x==y:
            return False
        return self.CanPlayThree(x) and self.CanPlaySingle(y)
    def CanPlay3Couple(self,x,y):
        if x==y:
            return False
        return self.CanPlayThree(x) and self.CanPlayCouple(y)
    def CanPlayM3Single(self,l,r,pix):
        if l>r:
            if l<11:
                return False
            for i in pix:
                if not self.CanPlaySingle(i):
                    return False
            pls = 14-l+r
            w = list(pix)+list(range(l,13))+list(range(0,r+1))
            if len(set(w))!=pls*2:
                return False
            return self.CanPlayMoreThree(l,r)
        for i in pix:
            if not self.CanPlaySingle(i):
                return False
        pls = r-l+1
        w = list(pix)+list(range(l,r+1))
        if len(set(w))!=pls*2:
            return False
        return self.CanPlayMoreThree(l,r)
    def CanPlayM3Couple(self,l,r,pix):
        if l>r:
            if l<11:
                return False
            for i in pix:
                if not self.CanPlayCouple(i):
                    return False
            pls = 14-l+r
            w = list(pix)+list(range(l,13))+list(range(0,r+1))
            if len(set(w))!=pls*2:
                return False
            return self.CanPlayMoreThree(l,r)

        for i in pix:
            if not self.CanPlayCouple(i):
                return False
        pls = r-l+1
        w = list(pix)+list(range(l,r+1)) if pls>0 else list(pix)+list(range(l,13))+list(range(0,r+1))
        if len(set(w))!=pls*2:
            return False
        return self.CanPlayMoreThree(l,r)
    def PlaySingle(self,x):
        self.a[x] -= 1
        self.cnt -= 1
    def PlayCouple(self,x):
        self.a[x] -= 2
        self.cnt -= 2
    def PlayThree(self,x):
        self.a[x] -= 3
        self.cnt -= 3
    def PlayBoom(self,x):
        self.a[x] -= 4
        self.cnt -= 4
    def PlayMoreSingle(self,l,r):
        if r>l:
            for i in range(l,r+1):
                self.PlaySingle(i)
        else:
            for i in range(l,13):
                self.PlaySingle(i)
            for i in range(0,r+1):
                self.PlaySingle(i)
    def PlayMoreCouple(self,l,r):
        if r>l:
            for i in range(l,r+1):
                self.PlayCouple(i)
        else:
            for i in range(l,13):
                self.PlayCouple(i)
            for i in range(0,r+1):
                self.PlayCouple(i)
    def PlayMoreThree(self,l,r):
        if r>l:
            for i in range(l,r+1):
                self.PlayThree(i)
        else:
            for i in range(l,13):
                self.PlayThree(i)
            for i in range(0,r+1):
                self.PlayThree(i)
    def Play3Single(self,x,y):
        self.PlayThree(x)
        self.PlaySingle(y)
    def Play3Couple(self,x,y):
        self.PlayThree(x)
        self.PlayCouple(y)
    def PlayM3Single(self,l,r,pix):
        for i in pix:
            self.PlaySingle(i)
        self.PlayMoreThree(l,r)
    def PlayM3Couple(self,l,r,pix):
        for i in pix:
            self.PlayCouple(i)
        self.PlayMoreThree(l,r)
    def empty(self):
        return self.cnt==0
    def Hash(self):
        res = 0
        for i in range(0,16):
            res = res<<2|self.a[i]
        return res
    def GetMin(self):
        for i in range(0,16):
            if self.a[i]:
                return i
    def GetMax(self):
        for i in range(13,-1,-1):
            if self.a[i]:
                return i
        return -1
    def ResetCan(self):
        self.CanThree = False
        self.CanBoom = False
        self.CanMS = False
        self.CanMC = False
        self.CanM3 = False
        for i in range(16):
            if self.CanPlayThree(i):
                self.CanThree = True
            if self.CanPlayBoom(i):
                self.CanBoom = True
        for i in range(8):
            if self.CanPlayMoreSingle(i,i+4):
                self.CanMS = True
        for i in range(2,4):
            if self.CanPlayMoreSingle(9+i,i):
                self.CanMS = True
        for i in range(12):
            if self.CanPlayMoreCouple(i,i+1):
                self.CanMC = True
            if self.CanPlayMoreThree(i,i+1):
                self.CanM3 = True
        if self.CanPlayMoreCouple(12,0):
            self.CanMC = True
        if self.CanPlayMoreThree(12,0):
            self.CanM3 = True
    def read(self):
        self.a = [0]*16
        self.cnt = 0
        s = input()
        self.cnt = len(s)
        for i in range(self.cnt):
            self.a[GetVal(s[i])] += 1
        self.ResetCan()
    def replace(self,origplayer):
        self.a = origplayer.a[:]
        self.cnt = origplayer.cnt
        self.CanThree = origplayer.CanThree
        self.CanBoom = origplayer.CanBoom
        self.CanMS = origplayer.CanMS
        self.CanMC = origplayer.CanMC
        self.CanM3 = origplayer.CanM3

'''
helper
'''
def Out_Single(x):
    global output
    output = output + '{}'.format(SetChar(x))
def Out_Couple(x):
    global output
    output = output + '{}{}'.format(SetChar(x),SetChar(x))
def Out_Three(x):
    global output
    output = output + '{}{}{}'.format(SetChar(x),SetChar(x),SetChar(x))
def Out_Boom(x):
    global output
    output = output + '{}{}{}{}'.format(SetChar(x),SetChar(x),SetChar(x),SetChar(x))
def Out_3Single(x,y):
    Out_Three(x)
    Out_Single(y)
def Out_3Couple(x,y):
    Out_Three(x)
    Out_Couple(y)
def Out_MS(l,r):
    if r>l:
        for i in range(l,r+1):
            Out_Single(i)
    else:
        for i in range(l,13):
            Out_Single(i)
        for i in range(0,r+1):
            Out_Single(i)
def Out_MC(l,r):
    if r>l:
        for i in range(l,r+1):
            Out_Couple(i)
    else:
        for i in range(l,13):
            Out_Couple(i)
        for i in range(0,r+1):
            Out_Couple(i)
def Out_M3(l,r):
    if r>l:
        for i in range(l,r+1):
            Out_Three(i)
    else:
        for i in range(l,13):
            Out_Three(i)
        for i in range(0,r+1):
            Out_Three(i)
def Out_M3Single(l,r,pix):
    Out_M3(l,r)
    for i in pix:
        Out_Single(i)
def Out_M3Couple(l,r,pix):
    Out_M3(l,r)
    for i in pix:
        Out_Couple(i)
def Is_Empty(s):
    return s=='*'
def Is_Single(s):
    return len(s)==1 and s!='*'
def Is_Couple(s):
    return len(s)==2 and s[0]==s[1]
def Is_Three(s):
    return len(s)==3 and s[0]==s[1]==s[2]
def Is_Boom(s):
    return len(s)==4 and s[0]==s[1]==s[2]==s[3]
def Is_3Single(s):
    return len(s)==4 and s[0]==s[1]==s[2] and s[2]!=s[3]
def Is_3Couple(s):
    return len(s)==5 and s[0]==s[1]==s[2] and s[2]!=s[3] and s[3]==s[4]
def Is_MS(s):
    l = len(s)
    if l<5:
        return False
    if s[0]=='3' and s[-1]=='2':
        count = 2
        for i in range(1,l):
            if GetVal(s[i-1])+1!=GetVal(s[i]):
                break
            else:
                count+=1
        for i in range(l-1,-1,-1):
            if GetVal(s[i-1])+1!=GetVal(s[i]):
                break
            else:
                count+=1
        if count>=5:
            return True
        else:
            return False
    else:
        for i in range(1,l):
            if GetVal(s[i-1])+1!=GetVal(s[i]):
                return False
        return True
def Is_MC(s):
    l = len(s)
    if l < 4:
        return False
    if s[0]=='3' and s[-1]=='2':
        temp = [0]*13
        max = 1
        for i in list(s):
            temp[GetVal(i)]+=1
            if temp[GetVal(i)]>max:
                max = temp[GetVal(i)]
        if max==2:
            return True
        else:
            return False
    else:
        for i in range(1,l,2):
            if s[i] != s[i-1]:
                return False
        for i in range(2,l,2):
            if GetVal(s[i-1])+1 != GetVal(s[i]):
                return False
        return True
def Is_M3(s):
    l = len(s)
    if l<6:
        return False
    if s[0]==3 and s[-1]=='2':
        temp = [0]*13
        for i in list(s):
            temp[GetVal(i)]+=1
        for i in temp:
            if i==1 or i==2:
                return False
            return True
        else:
            return False
    else:
        for i in range(2,l,3):
            if not(s[i]==s[i-1]==s[i-2]):
                return False
        for i in range(3,l,3):
            if GetVal(s[i-1])+1 != GetVal(s[i]):
                return False
        return True
def Is_M3Single(s):
    l = len(s)
    if l<8:
        return False
    if l%4!=0:
        return False
    pls = l//4
    return Is_M3(s[:3*l])
def Is_M3Couple(s):
    l = len(s)
    if l<10:
        return False
    if l%5!=0:
        return False
    pls = l//5
    return Is_M3(s[:3*l])
    
'''
main
'''
def Play_Boom(a,b,last,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt,['',0,0,0]
    if b.empty():
        return -1*a.cnt,['',0,0,0]
    _a = player()
    _a.replace(a)
    cardload = ['',0,0,0]
    if a.CanBoom:
        for i in range(last+1,13):
            if a.CanPlayBoom(i):
                a.PlayBoom(i)
                a.ResetCan()
                now = Play_Boom(b,a,i,False,True,-beta,-alpha,depth+1)[0]
                if now!=-27 and (-now > alpha or (now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'Boom'
                    cardload[1] = i
                a.replace(_a)
                if beta<=alpha:
                    return -27,cardload
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
        if beta<=alpha:
            return -27,cardload
    if cardload[0]=='Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27,cardload
    else:
        return alpha,cardload
def Play_Single(a,b,last,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt
    if b.empty():
        return -1*a.cnt
    _a = player()
    _a.replace(a)
    cardload = ['',0,0]
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,False,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and cardload[0]==''):
            alpha = temp[0]
            cardload = temp[1]
        if beta<=alpha:
            return -27
    for i in range(last+1,13):
        if a.CanPlaySingle(i):
            a.PlaySingle(i)
            now = Play_Single(b,a,i,False,True,-beta,-alpha,depth+1)
            if now!=-27 and (-now > alpha or (-now==alpha and cardload[0]=='')):
                alpha = -now
                cardload[0] = 'Single'
                cardload[1] = i
            a.replace(_a)
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
            cardload[0] = ''
        if beta<=alpha:
            return -27
    if cardload[0] == 'Single' and fir:
        Out_Single(cardload[1])
    if cardload[0] == 'Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27
    else:
        return alpha
def Play_Couple(a,b,last,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt
    if b.empty():
        return -1*a.cnt
    _a = player()
    _a.replace(a)
    cardload = ['',0,0]
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,False,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and cardload[0]==''):
            alpha = temp[0]
            cardload = temp[1]
        if beta<=alpha:
            return -27
    for i in range(last+1,13):
        if a.CanPlayCouple(i):
            a.PlayCouple(i)
            now = Play_Couple(b,a,i,False,True,-beta,-alpha,depth+1)
            if now!=-27 and (-now > alpha or (-now==alpha and cardload[0]=='')):
                alpha = -now
                cardload[0] = 'Couple'
                cardload[1] = i
            a.replace(_a)
            if beta<=alpha:
                return -27
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
            cardload[0] = ''
        if beta<=alpha:
            return -27
    if cardload[0] == 'Couple' and fir:
        Out_Couple(cardload[1])
    if cardload[0] == 'Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27
    else:
        return alpha
def Play_Three(a,b,last,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt
    if b.empty():
        return -1*a.cnt
    _a = player()
    _a.replace(a)
    cardload = ['',0,0]
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,False,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and cardload[0]==''):
            alpha = temp[0]
            cardload = temp[1]
        if beta<=alpha:
            return -27
    if a.CanThree:
        for i in range(last+1,13):
            if a.CanPlayThree(i):
                a.PlayThree(i)
                a.ResetCan()
                now = Play_Three(b,a,i,False,True,-beta,-alpha,depth+1)
                if now!=-27 and (-now > alpha or (-now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'Three'
                    cardload[1] = i
                a.replace(_a)
                if beta<=alpha:
                    return -27
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
            cardload[0] = ''
        if beta<=alpha:
            return -27
    if cardload[0]=='Three' and fir:
        Out_Three(cardload[1])
    if cardload[0] == 'Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27
    else:
        return alpha
def Play_3Single(a,b,last,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt
    if b.empty():
        return -1*a.cnt
    _a = player()
    _a.replace(a)
    cardload = ['',0,0]
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,False,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and cardload[0]==''):
            alpha = temp[0]
            cardload = temp[1]
        if beta<=alpha:
            return -27
    for i in range(last+1,13):
        if a.CanThree:
            if a.CanPlayThree(i):
                for j in range(15):
                    if a.CanPlay3Single(i,j):
                        a.Play3Single(i,j)
                        a.ResetCan()
                        now = Play_3Single(b,a,i,False,True,-beta,-alpha,depth+1)
                        if now!=-27 and (-now > alpha or (-now==alpha and cardload[0]=='')):
                            alpha = -now
                            cardload[0] = '3Single'
                            cardload[1] = i
                            cardload[2] = j
                        a.replace(_a)
                        if beta<=alpha:
                            return -27
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
            cardload[0] = ''
        if beta<=alpha:
            return -27
    if cardload[0] == '3Single' and fir:
        Out_3Single(cardload[1],cardload[2])
    if cardload[0] == 'Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27
    else:
        return alpha
def Play_3Couple(a,b,last,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt
    if b.empty():
        return -1*a.cnt
    _a = player()
    _a.replace(a)
    cardload = ['',0,0]
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,False,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and cardload[0]==''):
            alpha = temp[0]
            cardload = temp[1]
        if beta<=alpha:
            return -27
    for i in range(last+1,13):
        if a.CanThree:
            if a.CanPlayThree(i):
                for j in range(15):
                    if a.CanPlay3Couple(i,j):
                        a.Play3Couple(i,j)
                        a.ResetCan()
                        now = Play_3Couple(b,a,i,False,True,-beta,-alpha,depth+1)
                        if now!=-27 and (-now > alpha or (-now==alpha and cardload[0]=='')):
                            alpha = -now
                            cardload[0] = '3Couple'
                            cardload[1] = i
                            cardload[2] = j
                        a.replace(_a)
                        if beta<=alpha:
                            return -27
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
            cardload[0] = ''
        if beta<=alpha:
            return -27
    if cardload[0] == '3Couple' and fir:
        Out_3Couple(cardload[1],cardload[2])
    if cardload[0] == 'Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27
    else:
        return alpha
def Play_MS(a,b,l,r,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt
    if b.empty():
        return -1*a.cnt
    _a = player()
    _a.replace(a)
    cardload = ['',0,0]
    pls = r-l
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,False,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and cardload[0]==''):
            alpha = temp[0]
            cardload = temp[1]
        if beta<=alpha:
            return -27
    if a.CanMS and pls > 0:
        for i in range(l+1,12-pls):
            if a.CanPlayMoreSingle(i,i+pls):
                a.PlayMoreSingle(i,i+pls)
                a.ResetCan()
                now = Play_MS(b,a,i,i+pls,False,True,-beta,-alpha,depth+1)
                if now!=-27 and (-now > alpha or (-now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'MS'
                    cardload[1] = i
                    cardload[2] = i+pls
                a.replace(_a)
                if beta<=alpha:
                    return -27
    if a.CanMS and pls<0:
        pls = 13-l+r
        for i in range(l+1,13):
            if a.CanPlayMoreSingle(i,i+pls-13):
                a.PlayMoreSingle(i,i+pls-13)
                a.ResetCan()
                now = Play_MS(b,a,i,i+pls-13,False,True,-beta,-alpha,depth+1)
                if now!=-27 and (-now > alpha or (-now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'MS'
                    cardload[1] = i
                    cardload[2] = i+pls-13
                a.replace(_a)
                if beta<=alpha:
                    return -27
        for i in range(0,13-pls):
            if a.CanPlayMoreSingle(i,i+pls):
                a.PlayMoreSingle(i,i+pls)
                a.ResetCan()
                now = Play_MS(b,a,i,i+pls,False,True,-beta,-alpha,depth+1)
                if now!=-27 and (-now > alpha or (-now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'MS'
                    cardload[1] = i
                    cardload[2] = i+pls
                a.replace(_a)
                if beta<=alpha:
                    return -27
    if a.CanMS and pls==0:
        if a.CanPlayMoreSingle(0,12):
            a.PlayMoreSingle(0,12)
            a.ResetCan()
            now = Play_MS(b,a,0,12,False,True,-beta,-alpha,depth+1)
            if now!=-27 and (-now > alpha or (-now==alpha and cardload[0]=='')):
                alpha = -now
                cardload[0] = 'MS'
                cardload[1] = 0
                cardload[2] = 12
            a.replace(_a)
            if beta<=alpha:
                return -27
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
            cardload[0] = ''
        if beta<=alpha:
            return -27
    if cardload[0] == 'MS' and fir:
        Out_MS(cardload[1],cardload[2])
    if cardload[0] == 'Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27
    else:
        return alpha
def Play_MC(a,b,l,r,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt
    if b.empty():
        return -1*a.cnt
    _a = player()
    _a.replace(a)
    cardload = ['',0,0]
    pls = r-l
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,False,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and cardload[0]==''):
            alpha = temp[0]
            cardload = temp[1]
        if beta<=alpha:
            return -27
    if a.CanMC and pls>0:
        for i in range(l+1,12-pls):
            if a.CanPlayMoreCouple(i,i+pls):
                a.PlayMoreCouple(i,i+pls)
                a.ResetCan()
                now = Play_MC(b,a,i,i+pls,False,True,-beta,-alpha,depth+1)
                if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'MC'
                    cardload[1] = i
                    cardload[2] = i+pls
                a.replace(_a)
                if beta<=alpha:
                    return -27
    if a.CanMC and pls<0:
        pls = 13-l+r
        for i in range(l+1,13):
            if a.CanPlayMoreCouple(i,i+pls-13):
                a.PlayMoreCouple(i,i+pls-13)
                a.ResetCan()
                now = Play_MC(b,a,i,i+pls,False,True,-beta,-alpha,depth+1)
                if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'MC'
                    cardload[1] = i
                    cardload[2] = i+pls-13
                a.replace(_a)
                if beta<=alpha:
                    return -27
        for i in range(0,13-pls):
            if a.CanPlayMoreCouple(i,i+pls):
                a.PlayMoreCouple(i,i+pls)
                a.ResetCan()
                now = Play_MC(b,a,i,i+pls,False,True,-beta,-alpha,depth+1)
                if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'MC'
                    cardload[1] = i
                    cardload[2] = i+pls
                a.replace(_a)
                if beta<=alpha:
                    return -27
    if a.CanMC and pls==0:
        if a.CanPlayMoreCouple(0,12):
            a.PlayMoreCouple(0,12)
            a.ResetCan()
            now = Play_MC(b,a,0,12,False,True,-beta,-alpha,depth+1)
            if now!=-27 and (-now > alpha or (-now==alpha and cardload[0]=='')):
                alpha = -now
                cardload[0] = 'MC'
                cardload[1] = 0
                cardload[2] = 12
            a.replace(_a)
            if beta<=alpha:
                return -27
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
            cardload[0] = ''
        if beta<=alpha:
            return -27
    if cardload[0] == 'MC' and fir:
        Out_MC(cardload[1],cardload[2])
    if cardload[0] == 'Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27
    else:
        return alpha
def Play_M3(a,b,l,r,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt
    if b.empty():
        return -1*a.cnt
    _a = player()
    _a.replace(a)
    cardload = ['',0,0]
    pls = r-l
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,False,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and cardload[0]==''):
            alpha = temp[0]
            cardload = temp[1]
        if beta<=alpha:
            return -27
    if a.CanM3 and pls>0:
        for i in range(l+1,12-pls):
            if a.CanPlayMoreThree(i,i+pls):
                a.PlayMoreThree(i,i+pls)
                a.ResetCan()
                now = Play_M3(b,a,i,i+pls,False,True,-beta,-alpha,depth+1)
                if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'M3'
                    cardload[1] = i
                    cardload[2] = i+pls
                a.replace(_a)
                if beta<=alpha:
                    return -27
    if a.CanM3 and pls<0:
        pls = 13-l+r
        for i in range(l+1,13):
            if a.CanPlayMoreThree(i,i+pls-13):
                a.PlayMoreThree(i,i+pls-13)
                a.ResetCan()
                now = Play_M3(b,a,i,i+pls,False,True,-beta,-alpha,depth+1)
                if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'M3'
                    cardload[1] = i
                    cardload[2] = i+pls-13
                a.replace(_a)
                if beta<=alpha:
                    return -27
        for i in range(0,13-pls):
            if a.CanPlayMoreThree(i,i+pls):
                a.PlayMoreThree(i,i+pls)
                a.ResetCan()
                now = Play_M3(b,a,i,i+pls,False,True,-beta,-alpha,depth+1)
                if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                    alpha = -now
                    cardload[0] = 'M3'
                    cardload[1] = i
                    cardload[2] = i+pls
                a.replace(_a)
                if beta<=alpha:
                    return -27
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
            cardload[0] = ''
        if beta<=alpha:
            return -27
    if cardload[0] == 'M3' and fir:
        Out_M3(cardload[1],cardload[2])
    if cardload[0] == 'Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27
    else:
        return alpha
def Play_M3Single(a,b,l,r,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt
    if b.empty():
        return -1*a.cnt
    _a = player()
    _a.replace(a)
    cardload=['',0,0,0]
    pls = r-l
    if pls<0:
        pls = 13-l+r
        l -= 13
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,False,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and cardload[0]==''):
            alpha = temp[0]
            cardload = temp[1]
        if beta<=alpha:
            return -27
    if a.CanM3:
        for i in range(l+1,12-pls):
            right = i+pls-13 if i+pls>12 else i+pls
            if a.CanPlayMoreThree(i,right):
                if pls==1:
                    for j1 in range(15):
                        for j2 in range(15):
                            temp = j1,j2
                            if i<0:
                                i+=13
                            if a.CanPlayM3Single(i,right,temp):
                                a.PlayM3Single(i,right,temp)
                                a.ResetCan()
                                now = Play_M3Single(b,a,i,right,False,True,-beta,-alpha,depth+1)
                                if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                                    alpha = -now
                                    cardload[0] = 'M3Single'
                                    cardload[1] = i
                                    cardload[2] = right
                                    cardload[3] = j1,j2
                                a.replace(_a)
                                if beta<=alpha:
                                    return -27
                elif pls==2:
                    for j1 in range(15):
                        for j2 in range(15):
                            for j3 in range(15):
                                temp = j1,j2,j3
                                if i<0:
                                    i+=13
                                if a.CanPlayM3Single(i,right,temp):
                                    a.PlayM3Single(i,right,temp)
                                    a.ResetCan()
                                    now = Play_M3Single(b,a,i,right,False,True,-beta,-alpha,depth+1)
                                    if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                                        alpha = -now
                                        cardload[0] = 'M3Single'
                                        cardload[1] = i
                                        cardload[2] = right
                                        cardload[3] = j1,j2,j3
                                    a.replace(_a)
                                    if beta<=alpha:
                                        return -27
                elif pls==3:
                    for j1 in range(15):
                        for j2 in range(15):
                            for j3 in range(15):
                                for j4 in range(15):
                                    temp = j1,j2,j3,j4
                                    if i<0:
                                        i+=13
                                    if a.CanPlayM3Single(i,right,temp):
                                        a.PlayM3Single(i,right,temp)
                                        a.ResetCan()
                                        now = Play_M3Single(b,a,i,right,False,True,-beta,-alpha,depth+1)
                                        if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                                            alpha = -now
                                            cardload[0] = 'M3Single'
                                            cardload[1] = i
                                            cardload[2] = right
                                            cardload[3] = j1,j2,j3,j4
                                        a.replace(_a)
                                        if beta<=alpha:
                                            return -27
                elif pls==4:
                    for j1 in range(15):
                        for j2 in range(15):
                            for j3 in range(15):
                                for j4 in range(15):
                                    for j5 in range(15):
                                        temp = j1,j2,j3,j4,j5
                                        if i<0:
                                            i+=13
                                        if a.CanPlayM3Single(i,right,temp):
                                            a.PlayM3Single(i,right,temp)
                                            a.ResetCan()
                                            now = Play_M3Single(b,a,i,right,False,True,-beta,-alpha,depth+1)
                                            if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                                                alpha = -now
                                                cardload[0] = 'M3Single'
                                                cardload[1] = i
                                                cardload[2] = right
                                                cardload[3] = j1,j2,j3,j4,j5
                                            a.replace(_a)
                                            if beta<=alpha:
                                                return -27
                elif pls==5:
                    for j1 in range(15):
                        for j2 in range(15):
                            for j3 in range(15):
                                for j4 in range(15):
                                    for j5 in range(15):
                                        for j6 in range(15):
                                            temp = j1,j2,j3,j4,j5,j6
                                            if i<0:
                                                i+=13
                                            if a.CanPlayM3Single(i,right,temp):
                                                a.PlayM3Single(i,right,temp)
                                                a.ResetCan()
                                                now = Play_M3Single(b,a,i,right,False,True,-beta,-alpha,depth+1)
                                                if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                                                    alpha = -now
                                                    cardload[0] = 'M3Single'
                                                    cardload[1] = i
                                                    cardload[2] = right
                                                    cardload[3] = j1,j2,j3,j4,j5,j6
                                                a.replace(_a)
                                                if beta<=alpha:
                                                    return -27
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
            cardload[0] = ''
        if beta<=alpha:
            return -27
    if cardload[0] == 'M3Single' and fir:
        Out_M3Single(cardload[1],cardload[2],cardload[3])
    if cardload[0] == 'Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27
    else:
        return alpha           
def Play_M3Couple(a,b,l,r,fir,ok,alpha = -27,beta = 27,depth = 0):
    global newA,newB
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt
    if b.empty():
        return -1*a.cnt
    _a = player()
    _a.replace(a)
    cardload=['',0,0,0]
    pls = r-l
    if pls<0:
        pls = 13-l+r
        l -= 13
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,False,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and cardload[0]==''):
            alpha = temp[0]
            cardload = temp[1]
        if beta<=alpha:
            return -27
    if a.CanM3:
        for i in range(l+1,12-pls):
            right = i+pls-13 if i+pls>12 else i+pls
            if a.CanPlayMoreThree(i,right):
                if pls==1:
                    for j1 in range(15):
                        for j2 in range(15):
                            temp = j1,j2
                            if i<0:
                                i+=13
                            if a.CanPlayM3Couple(i,right,temp):
                                a.PlayM3Couple(i,right,temp)
                                a.ResetCan()
                                now = Play_M3Couple(b,a,i,right,False,True,-beta,-alpha,depth+1)
                                if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                                    alpha = -now
                                    cardload[0] = 'M3Couple'
                                    cardload[1] = i
                                    cardload[2] = right
                                    cardload[3] = j1,j2
                                a.replace(_a)
                                if beta<=alpha:
                                    return -27
                elif pls==2:
                    for j1 in range(15):
                        for j2 in range(15):
                            for j3 in range(15):
                                temp = j1,j2,j3
                                if i<0:
                                    i+=13
                                if a.CanPlayM3Couple(i,right,temp):
                                    a.PlayM3Couple(i,right,temp)
                                    a.ResetCan()
                                    now = Play_M3Couple(b,a,i,right,j3,False,True,-beta,-alpha,depth+1)
                                    if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                                        alpha = -now
                                        cardload[0] = 'M3Couple'
                                        cardload[1] = i
                                        cardload[2] = right
                                        cardload[3] = j1,j2,j3
                                    a.replace(_a)
                                    if beta<=alpha:
                                        return -27
                elif pls==3:
                    for j1 in range(15):
                        for j2 in range(15):
                            for j3 in range(15):
                                for j4 in range(15):
                                    temp = j1,j2,j3,j4
                                    if i<0:
                                        i+=13
                                    if a.CanPlayM3Couple(i,right,temp):
                                        a.PlayM3Couple(i,right,temp)
                                        a.ResetCan()
                                        now = Play_M3Couple(b,a,i,right,False,True,-beta,-alpha,depth+1)
                                        if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                                            alpha = -now
                                            cardload[0] = 'M3Couple'
                                            cardload[1] = i
                                            cardload[2] = right
                                            cardload[3] = j1,j2,j3,j4
                                        a.replace(_a)
                                        if beta<=alpha:
                                            return -27
                elif pls==4:
                    for j1 in range(15):
                        for j2 in range(15):
                            for j3 in range(15):
                                for j4 in range(15):
                                    for j5 in range(15):
                                        temp = j1,j2,j3,j4,j5
                                        if i<0:
                                            i+=13
                                        if a.CanPlayM3Couple(i,right,temp):
                                            a.PlayM3Couple(i,right,temp)
                                            a.ResetCan()
                                            now = Play_M3Couple(b,a,i,right,False,True,-beta,-alpha,depth+1)
                                            if now!=-27 and (-now>alpha or (-now==alpha and cardload[0]=='')):
                                                alpha = -now
                                                cardload[0] = 'M3Couple'
                                                cardload[1] = i
                                                cardload[2] = right
                                                cardload[3] = j1,j2,j3,j4,j5
                                            a.replace(_a)
                                            if beta<=alpha:
                                                return -27
    if ok:
        temp = -1*PLAY(b,a,False,-beta,-alpha,depth+1)[0]
        if temp>alpha and temp!=27:
            alpha = temp
            cardload[0] = ''
        if beta<=alpha:
            return -27
    if cardload[0] == 'M3Couple' and fir:
        Out_M3Couple(cardload[1],cardload[2],cardload[3])
    if cardload[0] == 'Boom' and fir:
        Out_Boom(cardload[1])
    if (not ok) and (cardload[0]==''):
        return -27
    else:
        return alpha
def PLAY(a,b,fir = False,alpha = -27,beta = 27,depth = 0):
    global Visit
    global output
    if depth > depthLimit or time.time()-startTime.t>timeLimit:
        return b.cnt-a.cnt,[]
    h = a.Hash(),b.Hash()
    if b.empty():
        Visit[h] = (-1*a.cnt,''),''
        return -1*a.cnt,[]
    cardload = ''
    slen = 0
    playmode = ''
    if h in Visit:
        if fir:
            output = Visit[h][1]
        return Visit[h][0],changerOut(Visit[h][1])
    if a.CanBoom:
        temp = Play_Boom(a,b,-1,True,False,alpha,beta,depth+1)
        if temp[0]>alpha or (temp[0]==alpha and playmode==''):
            alpha = temp[0]
            cardload = 'Boom'
            playmode = output
        output = ''
        if beta<=alpha:
            return -27,changerOut(playmode)
    if a.CanMS:
        for i in range(9,-1,-1):
            temp = Play_MS(a,b,8-i,-1,True,False,alpha,beta,depth+1)
            if temp>alpha or (temp==alpha and playmode==''):
                alpha = temp
                cardload = 'MS'
                slen = 5+i
                playmode = output
            output = ''
            if beta<=alpha:
                return -27,changerOut(playmode)
        temp = Play_MS(a,b,0,0,True,False,alpha,beta,depth+1)
        if temp>alpha or (temp==alpha and playmode==''):
            alpha = temp
            cardload = 'MS'
            slen = 0
            playmode = output
        output = ''
        if beta<=alpha:
            return -27,changerOut(playmode)
    if a.CanMC:
        for i in range(11,-1,-1):
            temp = Play_MC(a,b,11-i,-1,True,False,alpha,beta,depth+1)
            if temp>alpha or (temp==alpha and playmode==''):
                alpha = temp
                cardload = 'MC'
                slen = 2+i
                playmode = output
            output = ''
            if beta<=alpha:
                return -27,changerOut(playmode)
        temp = Play_MC(a,b,0,0,True,False,alpha,beta,depth+1)
        if temp>alpha or (temp==alpha and playmode==''):
            alpha = temp
            cardload = 'MC'
            slen = 0
            playmode = output
        output = ''
        if beta<=alpha:
            return -27,changerOut(playmode)
    if a.CanM3:
        for i in range(12,0,-1):
            temp = Play_M3(a,b,-1+i,-1,True,False,alpha,beta,depth+1)
            if temp>alpha or (temp==alpha and playmode==''):
                alpha = temp
                cardload = 'M3'
                slen = 14-i
                playmode = output
            output = ''
            if beta<=alpha:
                return -27,changerOut(playmode)
            temp = Play_M3Single(a,b,-1+i,-1,True,False,alpha,beta,depth+1)
            if temp>alpha or (temp==alpha and playmode==''):
                alpha = temp
                cardload = 'M3Single'
                slen = 14-i
                playmode = output
            output = ''
            if beta<=alpha:
                return -27,changerOut(playmode)
            temp = Play_M3Couple(a,b,-1+i,-1,True,False,alpha,beta,depth+1)
            if temp>alpha or (temp==alpha and playmode==''):
                alpha = temp
                cardload = 'M3Couple'
                slen = 14-i
                playmode = output
            output = ''
            if beta<=alpha:
                return -27,changerOut(playmode)
    if a.CanThree:
        temp = Play_Three(a,b,-1,True,False,alpha,beta,depth+1)
        if temp>alpha or (temp==alpha and playmode==''):
            alpha = temp
            cardload = 'Three'
            playmode = output
        output = ''
        if beta<=alpha:
            return -27,changerOut(playmode)
        temp = Play_3Single(a,b,-1,True,False,alpha,beta,depth+1)
        if temp>alpha or (temp==alpha and playmode==''):
            alpha = temp
            cardload = '3Single'
            playmode = output
        output = ''
        if beta<=alpha:
            return -27,changerOut(playmode)
        temp = Play_3Couple(a,b,-1,True,False,alpha,beta,depth+1)
        if temp>alpha or (temp==alpha and playmode==''):
            alpha = temp
            cardload = '3Couple'
            playmode = output
        output = ''
        if beta<=alpha:
            return -27,changerOut(playmode)
    temp = Play_Couple(a,b,-1,True,False,alpha,beta,depth+1)
    if temp>alpha or (temp==alpha and playmode==''):
        alpha = temp
        cardload = 'Couple'
        playmode = output
    output = ''
    if beta<=alpha:
        return -27,changerOut(playmode)
    temp = Play_Single(a,b,-1,True,False,alpha,beta,depth+1)
    if temp>alpha or (temp==alpha and playmode==''):
        alpha = temp
        cardload = 'Single'
        playmode = output
    output = ''
    if beta<=alpha:
        return -27,changerOut(playmode)
    Visit[h] = (alpha,playmode)
    if fir:
        output = playmode
    return alpha,changerOut(playmode)

'''
connector
'''
newA = player()
newB = player()
startTime = timerecorder()
depthLimit = 30
timeLimit = 29.99
class PlayerInterface:
    def teamName(self):
        return 'Liu_Chengwu'
    def ack(self,t):
        for i in t:
            newA.PlaySingle(GetVal(i))
        newA.ResetCan()
    def newGame(self,hand1,hand2,opponent):
        global Visit
        global newA,newB
        self.a = player()
        self.b = player()
        self.a.a = [0]*16
        self.a.cnt = len(hand1)
        for i in hand1:
            self.a.a[GetVal(i)] += 1
        self.a.ResetCan()
        self.b.a = [0]*16
        self.b.cnt = len(hand2)
        for i in hand2:
            self.b.a[GetVal(i)] += 1
        self.b.ResetCan()
        newA.replace(self.a)
        newB.replace(self.b)
    def play(self,t):
        global newA,newB
        global output
        self.a.replace(newA)
        self.b.replace(newB)
        global Visit
        startTime.refresh()
        Visit.clear()
        alpha = -self.a.cnt-1
        beta = self.b.cnt+1-len(t)
        depth = 0
        if t==[]:
            PLAY(self.a,self.b,True,alpha,beta,depth+1)
            temp = output
            output = ''
            return changerOut(temp)
        for i in t:
            self.b.PlaySingle(GetVal(i))
        self.b.ResetCan()
        newB.replace(self.b)
        now = toNow(t)
        if Is_Single(now):
            if Play_Single(self.a,self.b,GetVal(now[0]),False,False,alpha,beta,depth+1)<Play_Single(self.a,self.b,GetVal(now[0]),False,True,alpha,beta,depth+1):
                return []
            else:
                Play_Single(self.a,self.b,GetVal(now[0]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        if Is_Couple(now):
            if Play_Couple(self.a,self.b,GetVal(now[0]),False,False,alpha,beta,depth+1)<Play_Couple(self.a,self.b,GetVal(now[0]),False,True,alpha,beta,depth+1):
                return []
            else:
                Play_Couple(self.a,self.b,GetVal(now[0]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        if Is_Three(now):
            if Play_Three(self.a,self.b,GetVal(now[0]),False,False,alpha,beta,depth+1)<Play_Couple(self.a,self.b,GetVal(now[0]),False,True,alpha,beta,depth+1):
                return []
            else:
                Play_Three(self.a,self.b,GetVal(now[0]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        if Is_Boom(now):
            if Play_Boom(self.a,self.b,GetVal(now[0]),False,False,alpha,beta,depth+1)[0]<Play_Boom(self.a,self.b,GetVal(now[0]),False,True,alpha,beta,depth+1)[0]:
                return []
            else:
                Play_Boom(self.a,self.b,GetVal(now[0]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        if Is_3Single(now):
            if Play_3Single(self.a,self.b,GetVal(now[0]),False,False,alpha,beta,depth+1)<Play_3Single(self.a,self.b,GetVal(now[0]),False,True,alpha,beta,depth+1):
                return []
            else:
                Play_3Single(self.a,self.b,GetVal(now[0]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        if Is_3Couple(now):
            if Play_3Couple(self.a,self.b,GetVal(now[0]),False,False,alpha,beta,depth+1)<Play_3Couple(self.a,self.b,GetVal(now[0]),False,True,alpha,beta,depth+1):
                return []
            else:
                Play_3Couple(self.a,self.b,GetVal(now[0]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        if Is_MS(now):
            if Play_MS(self.a,self.b,GetVal(now[0]),GetVal(now[-1]),False,False,alpha,beta,depth+1)<Play_MS(self.a,self.b,GetVal(now[0]),GetVal(now[-1]),False,True,alpha,beta,depth+1):
                return []
            else:
                Play_MS(self.a,self.b,GetVal(now[0]),GetVal(now[-1]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        if Is_MC(now):
            if Play_MC(self.a,self.b,GetVal(now[0]),GetVal(now[-1]),False,False,alpha,beta,depth+1)<Play_MC(self.a,self.b,GetVal(now[0]),GetVal(now[-1]),False,True,alpha,beta,depth+1):
                return []
            else:
                Play_MC(self.a,self.b,GetVal(now[0]),GetVal(now[-1]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        if Is_M3(now):
            if Play_M3(self.a,self.b,GetVal(now[0]),GetVal(now[-1]),False,False,alpha,beta,depth+1)<Play_M3(self.a,self.b,GetVal(now[0]),GetVal(now[-1]),False,True,alpha,beta,depth+1):
                return []
            else:
                Play_M3(self.a,self.b,GetVal(now[0]),GetVal(now[-1]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        if Is_M3Single(now):
            if Play_M3Single(self.a,self.b,GetVal(now[0]),GetVal(now[(len(now)/4*3)-1]),False,False,alpha,beta,depth+1)<Play_M3Single(self.a,self.b,GetVal(now[0]),GetVal(now[(len(now)/4*3)-1]),False,True,alpha,beta,depth+1):
                return []
            else:
                Play_M3Single(self.a,self.b,GetVal(now[0]),GetVal(now[(len(now)/5*3)-1]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        if Is_M3Couple(now):
            if Play_M3Couple(self.a,self.b,GetVal(now[0]),GetVal(now[(len(now)/5*3)-1]),False,False,alpha,beta,depth+1)<Play_M3Couple(self.a,self.b,GetVal(now[0]),GetVal(now[(len(now)/5*3)-1]),False,True,alpha,beta,depth+1):
                return []
            else:
                Play_M3Couple(self.a,self.b,GetVal(now[0]),GetVal(now[(len(now)/4*3)-1]),True,False,alpha,beta,depth+1)
                temp = output
                output = ''
                return changerOut(temp)
        return []