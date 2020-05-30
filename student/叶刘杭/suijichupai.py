import copy
import numpy
import re
import itertools

class fakePlayer:
    def __init__(self):
        self.name = "TeamOne"
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
        pass
    

    def seq(self, s): #返回一个已经化简、排序好的牌组的牌数和最大牌
        if self.prec[s[-1]] - self.prec[s[0]] + 1 == len(s): #诸如['J','Q','K','A','2']这种情况
            return (len(s), s[-1])
        elif self.prec[s[-1]] - self.prec[s[0]] == 12:  # loop 诸如['3','4','5','A','2']
            tail = -3 if s[-2] == 'A' else -2 # 既有A又有2还是只有2
            if self.prec[s[tail]] == len(s) + tail + 1:
                return (len(s), s[tail])
            else:
                return None
    

    def pattern(self, t): #t是一个出牌组，一个list类,该方法返回一个set，set[0]是t的牌型及数量，set[1]是该牌组的终止牌（最大牌）
        if not t:
            return None
        counter = dict((c, t.count(c)) for c in set(t)) #给出一个标注了t中不同点数的牌有多少张的字典，如：若t为['5','5','5','3']，则counter为{'5':3,'3':1}
        m = max(counter.values()) #判断t是一个什么类型的出牌，max的意义在于有效规避了三代一、三代二中一和二的干扰
        if m == 1:  # 单张或顺子
            s = self.seq(sorted(t, key=lambda x: self.prec[x]))
            if not s:
                return None
            if s[0] == 1 or s[0] > 4: #确认是单张（1张）或者顺子（大于等于5张）
                return ('single*{}'.format(s[0]), s[1]) # 对于['3'],返回（'single*1','3');对于['J','Q','K','A','2'],返回（’single*5','2');对于['3','4','5','A','2'],返回('single*5','3')
            else:
                return None
        if m == 2:  # 对子或连对
            for v in counter.values():
                if v != 2: #一大堆对子中出现了不是对子的东西
                    return None
            s = self.seq(sorted(counter.keys(), key=lambda x: self.prec[x]))
            if not s:
                return None
            return ('pair*{}'.format(s[0]), s[1]) #如['4','4','5','5','6','6'],counter为{'4':2,'5':2,'6':2},方法返回('pair*3','6')
        if m == 3:  #三同张或三顺（可能夹带）
            s = self.seq(sorted([k for k in counter if counter[k] == 3],
                                key=lambda x: self.prec[x]))
            if not s:
                return None
            aff = [counter[k] for k in counter if counter[k] < 3]   #用于判断夹带的牌型是否一致
            ptt = ''
            if not aff: #无夹带
                ptt = 'triple*{}'
            elif aff == [1] * s[0]: #三代一
                ptt = 'triple*{}+single'
            elif aff == [2] * s[0]: #三代二
                ptt = 'triple*{}+pair'
            else:
                return None
            return (ptt.format(s[0]), s[1])
        if m == 4:
            if len(counter) > 1:  # 没有连炸
                return None
            return ('bomb', t[0])
        return None


    def beat(self, t, yt):  #判断是否能压过
        t = self.pattern(t)
        yt = self.pattern(yt)
        return t[0] == yt[0] and self.prec[t[1]] > self.prec[yt[1]]
    

    def lipai(self,myHand): #返回一个理好的牌组，分别显示各种不同类型的牌有哪些
        myHand_counter = dict((c, myHand.count(c)) for c in set(myHand))
        myHand_sorted = {'炸弹':[],'三顺':[],'三张':[],'连对':[],'对子':[],'顺子':[],'单张':[]}
        
        for c in myHand_counter:
            if myHand_counter[c] == 4:
                myHand_sorted['炸弹'].append(c)
                myHand_sorted['三张'].append(c)
                myHand_sorted['对子'].append(c)
                myHand_sorted['单张'].append(c)
            elif myHand_counter[c] == 3:
                myHand_sorted['三张'].append(c)
                myHand_sorted['对子'].append(c)
                myHand_sorted['单张'].append(c)
            elif myHand_counter[c] == 2:
                myHand_sorted['对子'].append(c)
                myHand_sorted['单张'].append(c)
            else:
                myHand_sorted['单张'].append(c)
        myHand_sorted['炸弹'].sort(key=lambda x: self.prec[x])
        myHand_sorted['三张'].sort(key=lambda x: self.prec[x])
        myHand_sorted['对子'].sort(key=lambda x: self.prec[x])
        myHand_sorted['单张'].sort(key=lambda x: self.prec[x])
        
        triple = copy.deepcopy(myHand_sorted['三张'])
        for c in triple:
            j = 1
            while True:
                if self.prec[c] <= 11:
                    if self.prec[c] + j >= 14:
                        break
                    m = j
                else:
                    if self.prec[c] + j >= 14:
                        m = j - 13
                    else:
                        m = j
                if list(self.prec.keys())[list(self.prec.values()).index(self.prec[c] + m)] in triple:
                    lst = []
                    for k in range(0,j+1):
                        if triple.index(c) + k <= len(triple) - 1:
                            lst.append(triple[triple.index(c) + k])
                        else:
                            lst.append(triple[triple.index(c) + k - len(triple)])
                    myHand_sorted['三顺'].append(lst)
                    j = j + 1
                else:
                    break
        
        double = copy.deepcopy(myHand_sorted['对子'])
        for c in double:
            j = 1
            while True:
                if self.prec[c] <= 11:
                    if self.prec[c] + j >= 14:
                        break
                    m = j
                else:
                    if self.prec[c] + j >= 14:
                        m = j - 13
                    else:
                        m = j
                if list(self.prec.keys())[list(self.prec.values()).index(self.prec[c]+m)] in double:
                    lst = []
                    for k in range(0,j+1):
                        if double.index(c) + k <= len(double) - 1:
                            lst.append(double[double.index(c) + k])
                        else:
                            lst.append(double[double.index(c) + k - len(double)])
                    myHand_sorted['连对'].append(lst)
                    j = j + 1
                else:
                    break

        single = copy.deepcopy(myHand_sorted['单张'])
        if len(single) >= 5:
            for length in range(5,len(single)+1):
                for start in range(len(single)):
                    lst = []
                    if start + length <= len(single):
                        lst = copy.deepcopy(single[start:start+length])
                        if self.prec[lst[-1]] - self.prec[lst[0]] + 1 == len(lst):
                            myHand_sorted['顺子'].append(lst)
                    else:
                        if self.prec[single[start]] >= 12:
                            lst = copy.deepcopy(single[0:start+length-len(single)] + single[start:])
                            if self.prec[lst[-1]] - self.prec[lst[0]] == 12:
                                tail = -3 if lst[-2] == 'A' else -2
                                if self.prec[lst[tail]] == len(lst) + tail + 1:
                                    myHand_sorted['顺子'].append(lst)

        return myHand_sorted


    def gen(self,myHand,t):  #myhand为我手里的牌，t为对方刚出的牌
        cardOnTable = self.pattern(t)       
        myHand_sorted = self.lipai(myHand)
        legalOutput = []
        
        if cardOnTable[0] == 'bomb':    #对方出的是炸弹
            for c in myHand_sorted['炸弹']:
                if self.prec[c] > self.prec[cardOnTable[1]]:
                    legalOutput.append([c,c,c,c])
        else:
            for c in myHand_sorted['炸弹']:
                legalOutput.append([c,c,c,c])
            if re.match('\w+',cardOnTable[0]).group() == 'single':  #对方出的是单张或者顺子
                num = int(re.search('\d+',cardOnTable[0]).group())
                if num == 1:    #单张
                    for c in myHand_sorted['单张']:
                        if self.beat([c],t):
                            legalOutput.append([c])
                else:   #顺子
                    for c in myHand_sorted['顺子']:
                        if self.beat(c,t):
                            legalOutput.append(c)
            elif re.match('\w+',cardOnTable[0]).group() == 'pair':  #对方出的是对子或连对
                num = int(re.search('\d+',cardOnTable[0]).group())
                if num == 1:    #对子
                    for c in myHand_sorted['对子']:
                        if self.beat([c,c],t):
                            legalOutput.append([c,c])
                else:   #连对
                    for c in myHand_sorted['连对']:
                        if self.beat(c+c,t):
                            legalOutput.append(c+c)
            else:   #对方出的是三张或三顺
                num = int(re.search('\d+',cardOnTable[0]).group())
                if num == 1:    #三同张
                    ptt = re.search('\+\w+',cardOnTable[0])
                    if ptt == None: #无夹带
                        for c in myHand_sorted['三张']:
                            if self.beat([c,c,c],t):
                                legalOutput.append([c,c,c])
                    else:
                        if ptt.group() == '+single':    #三代一
                            for c in myHand_sorted['三张']:
                                for d in myHand_sorted['单张']:
                                    if c != d:
                                        if self.beat([c,c,c,d],t):
                                            legalOutput.append([c,c,c,d])
                        else:   #三代二
                            for c in myHand_sorted['三张']:
                                for d in myHand_sorted['对子']:
                                    if c != d:
                                        if self.beat([c,c,c,d,d],t):
                                            legalOutput.append([c,c,c,d,d])
                else:   #三顺
                    ptt = re.search('\+\w+',cardOnTable[0])
                    if ptt == None: #无夹带
                        for c in myHand_sorted['三顺']:
                            if self.beat(c+c+c,t):
                                legalOutput.append(c+c+c)
                    else:
                        if ptt.group() == '+single':    #三顺带一
                            for c in myHand_sorted['三顺']:
                                lst = itertools.combinations(myHand_sorted['单张'],len(c))
                                for d in lst:
                                    if list(set(c) & set(d)) == []:
                                        if self.beat(c+c+c+list(d),t):
                                            legalOutput.append(c+c+c+list(d))
                        else:   #三顺带二
                            for c in myHand_sorted['三顺']:
                                lst = itertools.combinations(myHand_sorted['对子'],len(c))
                                for d in lst:
                                    if list(set(c) & set(d)) == []:
                                        if self.beat(c+c+c+list(d)+list(d),t):
                                            legalOutput.append(c+c+c+list(d)+list(d))
    
        legalOutput.append([])
        return legalOutput


    def chu(self,myHand):
        myHand_sorted = self.lipai(myHand)
        legalOutput = []
        for c in myHand_sorted['炸弹']:
            legalOutput.append([c,c,c,c])
        for c in myHand_sorted['单张']:
            legalOutput.append([c])
        for c in myHand_sorted['顺子']:
            legalOutput.append(c)
        for c in myHand_sorted['对子']:
            legalOutput.append([c,c])
        for c in myHand_sorted['连对']:
            legalOutput.append(c+c)
        for c in myHand_sorted['三张']:
            legalOutput.append([c,c,c])
            for d in myHand_sorted['单张']:
                if d != c:
                    legalOutput.append([c,c,c,d])
            for d in myHand_sorted['对子']:
                if d != c:
                    legalOutput.append([c,c,c,d,d])
        for c in myHand_sorted['三顺']:
            legalOutput.append(c+c+c)
            lst1 = itertools.combinations(myHand_sorted['单张'],len(c))
            for d in lst1:
                if list(set(c) & set(d)) == []:
                    legalOutput.append(c+c+c+list(d))
            lst2 = itertools.combinations(myHand_sorted['对子'],len(c))
            for d in lst2:
                if list(set(c) & set(d)) == []:
                    legalOutput.append(c+c+c+list(d)+list(d))
        return legalOutput


    def chupai(self,myHand,t):
        outputList = []
        output = []
        if t == []:
            outputList = copy.deepcopy(self.chu(myHand))
            numpy.random.shuffle(outputList)
            #print('可以出',outputList)
            output = outputList[0]
        else:
            outputList = copy.deepcopy(self.gen(myHand,t))
            numpy.random.shuffle(outputList)
            #print('可以出',outputList)
            output = outputList[0]
        return output


    def rollout(self,myhand,yourhand,cardOnTable,turn):    #turn中，0表示我先出/跟牌，1表示对方先出/跟牌，最后返回我赢了没有
        myHand = copy.deepcopy(myhand)
        yourHand = copy.deepcopy(yourhand)
        if myHand != [] and yourHand != []:
            if turn == 0:
                # print('我的手牌：',myHand)
                output = self.chupai(myHand,cardOnTable)
                # print('我出',output)
                for c in output:
                    myHand.remove(c)
                return self.rollout(myHand,yourHand,output,1-turn)
            if turn == 1:
                # print('对方手牌：',yourHand)
                output = self.chupai(yourHand,cardOnTable)
                # print('对方出',output)
                for c in output:
                    yourHand.remove(c)
                return self.rollout(myHand,yourHand,output,1-turn)
        else:
            if myHand == []:
                # print('赢了')
                return 1
            else:
                # print('输了')
                return 0


