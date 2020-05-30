class Player:
    def __init__(self):
        self.name = "DuShen"
        self.prec = {}
        self.prec['3'] = 1
        self.prec['4'] = 2
        self.prec['5'] = 3
        self.prec['6'] = 4
        self.prec['7'] = 5
        self.prec['8'] = 6
        self.prec['9'] = 7
        self.prec['10'] = 8
        self.prec['J'] = 9
        self.prec['Q'] = 10
        self.prec['K'] = 11
        self.prec['A'] = 12
        self.prec['2'] = 13

    def newGame(self, hand1, hand2, opponent):
        self.myHand = self.order(hand1)
        self.yourHand = self.order(hand2)
        # self.opponent = self.order(opponent)
        self.opponent = opponent

    def is__danpai(self, t):  # 判断牌型t是否为顺子,t为列表
        if len(t) == 1:
            return t[0]
        else:
            return False

    def is__shunzi(self, t):  # 判断牌型t是否为顺子,t为列表
        if 'K' in t and '3' in t and "A" in t and '2' in t:
            return False
        prec = {}
        prec['2'] = 0
        prec['A'] = 0
        prec['K'] = 0
        prec['Q'] = 0
        prec['J'] = 0
        prec['10'] = 0
        prec['9'] = 0
        prec['8'] = 0
        prec['7'] = 0
        prec['6'] = 0
        prec['5'] = 0
        prec['4'] = 0
        prec['3'] = 0
        for i in t:
            prec[i] += 1
        current = '3'
        Found = False
        num = 0
        temp = 0
        for i in prec:
            previous = current
            current = i
            if prec[current] != 1 and prec[current] != 0:
                return False
            if prec[current] == 1 and prec[previous] == 0:
                temp += 1
            if prec[current] == 0:
                Found = False
            else:
                Found = True
            if Found:
                num += 1
        if temp == 0 or temp > 1:
            return False
        else:
            if num < 5:
                return False
            else:
                return True

    def is__liandui(self, t):  # 判断判断牌型t是否为连对（包括对子）
        if 'K' in t and '3' in t and "A" in t and '2' in t:
            return False
        prec = {}
        prec['2'] = 0
        prec['A'] = 0
        prec['K'] = 0
        prec['Q'] = 0
        prec['J'] = 0
        prec['10'] = 0
        prec['9'] = 0
        prec['8'] = 0
        prec['7'] = 0
        prec['6'] = 0
        prec['5'] = 0
        prec['4'] = 0
        prec['3'] = 0
        for i in t:
            prec[i] += 1
        current = '3'
        temp = 0
        for i in prec:
            previous = current
            current = i
            if prec[current] != 2 and prec[current] != 0:
                return False
            if prec[current] == 2 and prec[previous] == 0:
                temp += 1
        if temp == 0 or temp > 1:
            return False
        else:
            return True

    def is__liansantong0(self, t):  # 判断判断牌型t是否为普通连三同（包括普通三同）
        if 'K' in t and '3' in t and "A" in t and '2' in t:
            return False
        prec = {}
        prec['2'] = 0
        prec['A'] = 0
        prec['K'] = 0
        prec['Q'] = 0
        prec['J'] = 0
        prec['10'] = 0
        prec['9'] = 0
        prec['8'] = 0
        prec['7'] = 0
        prec['6'] = 0
        prec['5'] = 0
        prec['4'] = 0
        prec['3'] = 0
        for i in t:
            prec[i] += 1
        current = '3'
        temp = 0
        for i in prec:
            previous = current
            current = i
            if prec[current] != 3 and prec[current] != 0:
                return False
            if prec[current] == 3 and prec[previous] == 0:
                temp += 1
        if temp == 0 or temp > 1:
            return False
        else:
            return True

    def is__liansantong1(self, t):  # 判断判断牌型t是否为三带一连三同（包括三带一三同）
        self.main__list = []
        self.else__list = []
        prec = {}
        prec['2'] = 0
        prec['A'] = 0
        prec['K'] = 0
        prec['Q'] = 0
        prec['J'] = 0
        prec['10'] = 0
        prec['9'] = 0
        prec['8'] = 0
        prec['7'] = 0
        prec['6'] = 0
        prec['5'] = 0
        prec['4'] = 0
        prec['3'] = 0
        for i in t:
            prec[i] += 1
        current = '3'
        temp3 = 0
        temp1 = 0
        temp = 0
        if prec['K'] == 3 and prec['A'] == 3 and prec['2'] == 3 and prec['3'] == 3:
            return False
        for i in prec:
            previous = current
            current = i
            if prec[current] == 4 or prec[current] == 2:
                return False
            if prec[current] == 3:
                temp3 += 1
                self.main__list.append(current)
            elif prec[current] == 1:
                temp1 += 1
                self.else__list.append(current)
            if prec[current] == 3 and prec[previous] != 3:
                temp += 1
        if temp == 0 or temp > 1:
            return False
        elif temp1 != temp3:
            return False
        else:
            return True

    def is__liansantong2(self, t):  # 判断判断牌型t是否为三带二连三同（包括三带二三同）
        self.main__list = []
        self.else__list = []
        prec = {}
        prec['2'] = 0
        prec['A'] = 0
        prec['K'] = 0
        prec['Q'] = 0
        prec['J'] = 0
        prec['10'] = 0
        prec['9'] = 0
        prec['8'] = 0
        prec['7'] = 0
        prec['6'] = 0
        prec['5'] = 0
        prec['4'] = 0
        prec['3'] = 0
        for i in t:
            prec[i] += 1
        current = '3'
        temp3 = 0
        temp2 = 0
        temp = 0
        if prec['K'] == 3 and prec['A'] == 3 and prec['2'] == 3 and prec['3'] == 3:
            return False
        for i in prec:
            previous = current
            current = i
            if prec[current] == 4 or prec[current] == 1:
                return False
            if prec[current] == 3:
                temp3 += 1
                self.main__list.append(current)
            elif prec[current] == 2:
                temp2 += 1
                self.else__list.append(current)
            if prec[current] == 3 and prec[previous] != 3:
                temp += 1
        if temp == 0 or temp > 1:
            return False
        elif temp2 != temp3:
            return False
        else:
            return True

    def is__zhadan(self, t):  # 判断牌型t是否为炸弹
        if len(t) == 4:
            for i in range(1, 4):
                if t[i] != t[0]:
                    return False
            return True
        else:
            return False

    def beat(self, t1, t2):  # 判断t1牌型是否比t2大
        if len(t1) == len(t2):
            if len(t1) == 1:
                return self.prec[t1[0]] > self.prec[t2[0]]
            elif self.is__zhadan(t1):
                if self.is__zhadan(t2):
                    return self.prec[t1[0]] > self.prec[t2[0]]
                else:
                    return True
            elif self.is__shunzi(t1) and self.is__shunzi(t2):
                T1 = Shunzi(t1)
                T2 = Shunzi(t2)
                return T1.get__list__max() > T2.get__list__max()
            elif self.is__liandui(t1) and self.is__liandui(t2):
                T1 = Liandui(t1)
                T2 = Liandui(t2)
                return T1.get__list__max() > T2.get__list__max()
            elif self.is__liansantong0(t1) and self.is__liansantong0(t2):
                T1 = Liansantong0(t1)
                T2 = Liansantong0(t2)
                return T1.get__list__max() > T2.get__list__max()
            elif self.is__liansantong1(t1) and self.is__liansantong1(t2):
                T1 = Liansantong1(t1)
                T2 = Liansantong1(t2)
                return T1.get__list__max() > T2.get__list__max()
            elif self.is__liansantong2(t1) and self.is__liansantong2(t2):
                T1 = Liansantong2(t1)
                T2 = Liansantong2(t2)
                return T1.get__list__max() > T2.get__list__max()
            else:
                raise TypeError('牌型错误，无法比较大小')
        else:
            raise TypeError('牌型错误，无法比较大小')

    def order(self, t):  # 理牌(从小到大排列，如3,4,5,……,A,2)
        temp = []
        for item in t:
            temp.append([self.prec[item],item])
        for i in range(len(t)):
            for j in range(i+1,len(t)):
                if temp[i][0] > temp[j][0]:
                    temp[i], temp[j] = temp[j], temp[i]
        output = []
        for item in temp:
            output.append(item[1])
        return output

    def SortNum(self, t): # 牌型判断
        if self.is__danpai(t):
            return "danpai"
        elif self.is__shunzi(t):
            return "shunzi"
        elif self.is__liandui(t) and len(t)==2:
            return "duizi"
        elif self.is__liandui(t) and len(t)>2:
            return "liandui"
        elif self.is__liansantong0(t):
            return "liansantong0"
        elif self.is__liansantong1(t):
            return "liansantong1"
        elif self.is__liansantong2(t):
            return "liansantong2"
        elif self.is__zhadan(t):
            return "zhadan"
        else:
            raise TypeError('牌型错误')

#判断我手中是否有该牌型的牌（在不拆炸弹的情况下）
#返回能管上的最小的牌（str list）或空list
    def SortinmyHand(self, t):
        sort = self.SortNum(t)
        temp = []
        for item in self.myHand:
            temp.append(item)
        boomlist = list(set(self.BoominmyHand(temp)))  # 剔除炸弹
        for i in range(len(boomlist)):
            for j in range(4):
                temp.remove(boomlist[i])
        if sort == "danpai":
            while self.danpaiinmyHand(temp):
                if self.beat(self.danpaiinmyHand(temp),t):
                    return self.danpaiinmyHand(temp)
                else:
                    temp.remove(self.danpaiinmyHand(temp)[0])
            return []
        elif sort == "duizi":
            while self.duiziinmyHand(temp):
                if self.beat(self.duiziinmyHand(temp),t):
                    return self.duiziinmyHand(temp)
                else:
                    for item in self.duiziinmyHand(temp):
                        temp.remove(item)
            return []
        elif sort == "shunzi":
            while self.shunziinmyHand(temp,len(t)):
                if self.beat(self.shunziinmyHand(temp,len(t)),t):
                    return self.shunziinmyHand(temp,len(t))
                else:
                    tem = self.shunziinmyHand(temp,len(t))[0]
                    while self.shunziinmyHand(temp,len(t))[0] == tem:
                        temp.remove(tem)                   
            return []
        elif sort == "liandui":
            while self.lianduiinmyHand(temp,len(t)):
                if self.beat(self.lianduiinmyHand(temp,len(t)),t):
                    return self.lianduiinmyHand(temp,len(t))
                else:
                    tem = self.lianduiinmyHand(temp,len(t))[0]
                    temp.remove(tem)
                    temp.remove(tem)
            return []
        elif sort == "liansantong0":
            while self.liansantong0inmyHand(temp,len(t)):
                if self.beat(self.liansantong0inmyHand(temp,len(t)),t):
                    return self.liansantong0inmyHand(temp,len(t))
                else:
                    tem = self.liansantong0inmyHand(temp,len(t))[0]
                    temp.remove(tem)
                    temp.remove(tem)
                    temp.remove(tem)
            return []
        elif sort == "liansantong1":
            while self.liansantong1inmyHand(temp,len(t)):
                if self.beat(self.liansantong1inmyHand(temp,len(t)),t):
                    return self.liansantong1inmyHand(temp,len(t))
                else:
                    tem = self.liansantong1inmyHand(temp,len(t))[0]
                    temp.remove(tem)
                    temp.remove(tem)
                    temp.remove(tem)
            return []
        elif sort == "liansantong2":
            while self.liansantong2inmyHand(temp,len(t)):
                if self.beat(self.liansantong2inmyHand(temp,len(t)),t):
                    return self.liansantong2inmyHand(temp,len(t))
                else:
                    tem = self.liansantong2inmyHand(temp,len(t))[0]
                    temp.remove(tem)
                    temp.remove(tem)
                    temp.remove(tem)
            return []
#下面是一系列函数，用来判断手牌中有无该牌型的牌
#（可拆更高牌型，如手牌为["1","1","1"],danpaiinmyHand（）函数返回["1"]）
#如果有，返回该牌型中的最小牌，如返回["7","8","9","10","J"]
    def danpaiinmyHand(self, alist):
        if alist:
            return [alist[0]]
        else:
            return []

    def duiziinmyHand(self, alist):
        if alist:
            for i in range(len(alist)-1):
                pre = alist[i]
                nxt = alist[i+1]
                if pre == nxt:
                    return [pre,nxt]
            return []
        else:
            return []

    def shunziinmyHand(self, alist, length):
        temp = []
        for item in alist:
            if not item in temp:
                temp.append(item)
        if len(temp)<length:
            return []
        else:
            for i in range(len(temp)-length):
                if self.is__shunzi(temp[i:i+length]):
                    return temp[i:i+length]
            return []

    def lianduiinmyHand(self, alist, length):
        temp = []
        aset = list(set(alist))
        aset.sort(key = alist.index)  # 保证集合中元素的顺序与alist一致
        for item in aset:
            if alist.count(item)>=2:
                temp.append(item)
                temp.append(item)
        if len(temp)<length:
            return []
        else:
            for j in range(len(temp)-length):
                if self.is__liandui(temp[j:j+length]):
                    return temp[j:j+length]
            return []

    def liansantong0inmyHand(self, alist, length):
        l = length/3
        count = 0
        output = []
        aset = list(set(alist))
        aset.sort(key = alist.index)
        for item in aset:
            if alist.count(item) == 3:
                output.append(item)
                output.append(item)
                output.append(item)
                count = count + 1
                if count == l:
                    return output
        return []

    def liansantong1inmyHand(self, alist, length):
        l = length//4
        temp = []
        aset = list(set(alist))
        aset.sort(key = alist.index)
        for item in aset:
            if alist.count(item) == 3:
                temp.append(item)
                temp.append(item)
                temp.append(item)
        if len(temp)/3<l:
            return []
        else:
            output = temp[:3*l]
            temp2 = []
            for item in alist:
                temp2.append(item)
            for item in output:
                temp2.remove(item)
            for item in temp2:
                if len(output)<length:
                    if not item in output:
                        output.append(item)
                else:
                    return output
        return []

    def liansantong2inmyHand(self, alist, length):
        l = length//5
        temp = []
        aset = list(set(alist))
        aset.sort(key = alist.index)
        for item in aset:
            if alist.count(item) == 3:
                temp.append(item)
                temp.append(item)
                temp.append(item)
        if len(temp)/3<l:
            return []
        else:
            output = temp[:3*l]
            temp2 = []
            for item in alist:
                temp2.append(item)
            for item in output:
                temp2.remove(item)
            aset = list(set(temp2))
            aset.sort(key = temp2.index)
            for item in aset:
                if temp2.count(item)>=2:
                    output.append(item)
                    output.append(item)
                if len(output) == length:
                    return output
        return []
#手牌中“最大牌型”(不拆炸弹)
    def MaxmyHand(self): 
        temp = []
        for item in self.myHand:
            temp.append(item)
        boomlist = list(set(self.BoominmyHand(temp)))  # 剔除炸弹
        for i in range(len(boomlist)):
            for j in range(4):
                temp.remove(boomlist[i])
        if self.maxliansantong2inmyHand(temp):
            return self.maxliansantong2inmyHand(temp)
        elif self.maxliansantong1inmyHand(temp):
            return self.maxliansantong1inmyHand(temp)
        elif self.maxliansantong0inmyHand(temp):
            return self.maxliansantong0inmyHand(temp)
        elif self.maxshunziinmyHand(temp):
            return self.maxshunziinmyHand(temp)
        elif self.maxlianduiinmyHand(temp):
            return self.maxlianduiinmyHand(temp)
        elif self.duiziinmyHand(temp):
            return self.duiziinmyHand(temp)
        elif self.danpaiinmyHand(temp):
            return self.danpaiinmyHand(temp)
        else: # 手中只剩炸弹
            return self.BoominmyHand(self.myHand)

    def maxliansantong2inmyHand(self, alist):
        for length in range(len(alist)-len(alist)%5,4,-5):
            if self.liansantong2inmyHand(alist, length):
                return self.liansantong2inmyHand(alist, length)
        return []

    def maxliansantong1inmyHand(self, alist):
        for length in range(len(alist)-len(alist)%4,3,-4):
            if self.liansantong1inmyHand(alist, length):
                return self.liansantong1inmyHand(alist, length)
        return []

    def maxliansantong0inmyHand(self, alist):
        for length in range(len(alist)-len(alist)%3,2,-3):
            if self.liansantong0inmyHand(alist, length):
                return self.liansantong0inmyHand(alist, length)
        return []

    def maxshunziinmyHand(self, alist):
        for length in range(len(alist),4,-1):
            if self.shunziinmyHand(alist, length):
                return self.shunziinmyHand(alist, length)
        return []

    def maxlianduiinmyHand(self, alist):
        for length in range(len(alist)-len(alist)%2,3,-2):
            if self.lianduiinmyHand(alist,length):
                return self.lianduiinmyHand(alist,length)
        return []
#判断手中是否有炸弹（返回最小炸弹牌，如["2","2","2","2"]或空list）
    def BoominmyHand(self, alist):
        aset = list(set(alist))
        aset.sort(key = alist.index)
        for item in aset:
            if alist.count(item) == 4:
                return [item] * 4
        return []
# play函数
    def play(self, t):
        '''for item in t: 
            self.yourHand.remove(item)'''# 按现在的算法，不必设置yourHand变量
        if not t: # 对方管不上，出最多的牌（炸弹除外）
            output = []
            for item in self.MaxmyHand():  # 避免手牌仅有炸弹时出错
                output.append(item)
            # for item in output:
            #     self.myHand.remove(item)
            return output
        elif not self.BoominmyHand(self.myHand) or self.SortinmyHand(t): # 有可回应的牌（无论有无炸弹）
            output = self.SortinmyHand(t)
            # for item in output:
            #     self.myHand.remove(item)
            return output 
        else: # 有炸弹，无可回应的牌
            output = self.BoominmyHand(self.myHand)
            # for item in output:
            #     self.myHand.remove(item)
            return output 

    def ack(self, t):
        #print("ack: {}".format(self.myHand))
        for c in t:
            # print('a',str(c),t,self.myHand)
            self.myHand.remove(c)

    def teamName(self):
        return self.name


class Danpai(Player):
    def __init__(self, alist):
        if not Player().is__danpai(alist):
            raise TypeError('输入的列表不是单牌')
        self.mylist = alist
        self.length = len(alist)
        Player.__init__(self)

    def get__list__max(self):  # 返回最大牌
        return self.mylist[0]

class Shunzi(Player):
    def __init__(self, alist):
        a = Player()
        if not a.is__shunzi(alist):
            raise TypeError('输入的列表不是顺子')
        self.mylist = alist
        self.length = len(alist)
        Player.__init__(self)

    def get__list__max(self):  # 返回最大牌
        amax = 0
        if '2' in self.mylist and '3' in self.mylist:
            for i in self.mylist:
                if i != '2' and i != 'A':
                    amax = max(amax, self.prec[i])
        else:
            for i in self.mylist:
                amax = max(amax, self.prec[i])
        return amax


class Liandui(Player):
    def __init__(self, alist):
        a = Player()
        if not a.is__liandui(alist):
            raise TypeError('输入的列表不是连对')
        self.mylist = alist
        self.length = len(alist)
        Player.__init__(self)

    def get__list__max(self):  # 返回最大牌
        amax = 0
        if '2' in self.mylist and '3' in self.mylist:
            for i in self.mylist:
                if i != '2' and i != 'A':
                    amax = max(amax, self.prec[i])
        else:
            for i in self.mylist:
                amax = max(amax, self.prec[i])
        return amax


class Liansantong0(Player):
    def __init__(self, alist):
        a = Player()
        if not a.is__liansantong0(alist):
            raise TypeError('输入的列表不是普通连三同')
        self.mylist = alist
        self.length = len(alist)
        Player.__init__(self)

    def get__list__max(self):  # 返回最大牌
        amax = 0
        if '2' in self.mylist and '3' in self.mylist:
            for i in self.mylist:
                if i != '2' and i != 'A':
                    amax = max(amax, self.prec[i])
        else:
            for i in self.mylist:
                amax = max(amax, self.prec[i])
        return amax


class Liansantong1(Player):
    def __init__(self, alist):
        a = Player()
        if not a.is__liansantong1(alist):
            raise TypeError('输入的列表不是三带一连三同')
        self.mylist = alist
        self.length = len(alist)
        Player.__init__(self)
        Player.is__liansantong1(self, self.mylist)

    def get__list__max(self):  # 返回最大牌
        amax = 0
        if '2' in self.main__list and '3' in self.main__list:
            for i in self.main__list:
                if i != '2' and i != 'A':
                    amax = max(amax, self.prec[i])
        else:
            for i in self.main__list:
                amax = max(amax, self.prec[i])
        return amax


class Liansantong2(Player):
    def __init__(self, alist):
        a = Player()
        if not a.is__liansantong2(alist):
            raise TypeError('输入的列表不是三带二连三同')
        self.mylist = alist
        self.length = len(alist)
        Player.__init__(self)
        Player.is__liansantong2(self, self.mylist)

    def get__list__max(self):  # 返回最大牌
        amax = 0
        if '2' in self.main__list and '3' in self.main__list:
            for i in self.main__list:
                if i != '2' and i != 'A':
                    amax = max(amax, self.prec[i])
        else:
            for i in self.main__list:
                amax = max(amax, self.prec[i])
        return amax


class Zhadan(Player):
    def __init__(self, alist):
        a = Player()
        if not a.is__zhadan(alist):
            raise TypeError('输入的列表不是炸弹')
        self.mylist = alist
        self.length = len(alist)
        Player.__init__(self)

    def get__list__max(self):  # 返回最大牌
        return self.mylist[0]