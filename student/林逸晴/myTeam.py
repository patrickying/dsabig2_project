import copy

def combinations(source0, n, nt):
    # 求n个三条所带的牌的所有组合
    # nt = 1 为三带一
    # nt = 2 为三带对
    source = copy.deepcopy(source0)
    l = list(source.keys())
    if len(l) == n:
        if all(source[i]>=nt for i in l):
            return [l]
        else:
            return []
    ans = []
    if n == 1:
        for i in l:
            if source[i]>=nt:
                ans.append([i])
        return ans
    source.pop(l[0])
    for each_list in combinations(source,n-1,nt):
        ans.append([l[0]]+each_list)
    for each_list in combinations(source,n,nt):
        ans.append(each_list)
    return ans

def comb_rep(l, n): #求可重复的所有组合
    r = []
    if n == 1:
        for c in l:
            if [c] not in r:
                r.append([c])
    elif n == len(l):
        r.append(l)
    else:
        for each_list in comb_rep(l[1:], n-1):
            if [l[0]] + each_list not in r:
                r.append([l[0]] + each_list)
        for each_list in comb_rep(l[1:], n):
            if each_list not in r:
                r.append(each_list)
    return r


class Player:
    def __init__(self):
        self.name = "myTeam"
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
        self.myHand = hand1
        self.yourHand = hand2
        self.opponent = opponent

    def seq(self, s):
        if self.prec[s[-1]] - self.prec[s[0]] + 1 == len(s):
            return (len(s), s[-1])
        elif self.prec[s[-1]] - self.prec[s[0]] == 12:  # loop
            tail = -3 if s[-2] == 'A' else -2
            if self.prec[s[tail]] == len(s) + tail + 1:
                return (len(s), s[tail])
            else:
                return None

    def pattern(self, t):
        if not t:
            return None
        counter = dict((c, t.count(c)) for c in set(t))
        m = max(counter.values())
        if m == 1:  # 单张或顺子
            s = self.seq(sorted(t, key=lambda x: self.prec[x]))
            if not s:
                return None
            if s[0] == 1 or s[0] > 4:
                return ('single*{}'.format(s[0]), s[1])
            else:
                return None
        if m == 2:  # 对子或连对
            for v in counter.values():
                if v != 2:
                    return None
            s = self.seq(sorted(counter.keys(), key=lambda x: self.prec[x]))
            if not s:
                return None
            return ('pair*{}'.format(s[0]), s[1])
        if m == 3:
            s = self.seq(sorted([k for k in counter if counter[k] == 3],
                                key=lambda x: self.prec[x]))
            if not s:
                return None
            aff = [counter[k] for k in counter if counter[k] < 3]
            ptt = ''
            if not aff:
                ptt = 'triple*{}'
            elif aff == [1] * s[0]:
                ptt = 'triple*{}+single'
            elif aff == [2] * s[0]:
                ptt = 'triple*{}+pair'
            else:
                return None
            return (ptt.format(s[0]), s[1])
        if m == 4:
            if len(counter) > 1:  # 没有连炸
                return None
            return ('bomb', t[0])
        return None

    def beat(self, t, yt):
        t = self.pattern(t)
        yt = self.pattern(yt)
        if not t:
            return False
        if not yt:
            return True
        if t[0] == 'bomb' and yt[0] != 'bomb':  # 炸弹盖过其他牌型
            return True
            # 牌型匹配且大于
        return t[0] == yt[0] and self.prec[t[1]] > self.prec[yt[1]]

    def get_all_solutions(self, t): #求所有能大过上家的牌组
        solutions = []
        myHand_v = [self.prec[c] for c in self.myHand]
        counter = dict((c, myHand_v.count(c)) for c in set(myHand_v))
        tp = self.pattern(t)
        if tp == None:
            for n in range(len(self.myHand)):
                r = comb_rep(self.myHand, n+1)
                solutions += r
            return solutions
        p = tp[0]
        v = tp[1]
        if p[0] == 's': #单牌或顺子
            n = int(p[7:])
            for c in counter:
                if c > self.prec[v]:
                    flag = 0
                    for i in range(n-1):
                        if c-i-1 not in counter:
                            flag = 1
                            break
                    if not flag and [c-i for i in range(n)] not in solutions:
                        solutions.append([c-i for i in range(n)])
        elif p[0] == 'p': #对子或连对
            n = int(p[5:])
            for c in counter:
                if c > self.prec[v]:
                    flag = 0
                    for i in range(n):
                        if c-i-1 not in counter or counter[c-i-1] < 2:
                            flag = 1
                            break
                    if not flag and [c-i for i in range(n) for j in range(2)] not in solutions:
                        solutions.append([c-i for i in range(n) for j in range(2)])
        elif p[0] == 't':  #三同张
            if '+' not in p:  #不带牌
                n = int(p[7:])
                for c in counter:
                    if c > self.prec[v]:
                        flag = 0
                        for i in range(n):
                            if c-i-1 not in counter or counter[c-i-1] < 3:
                                flag = 1
                                break
                        if not flag and [c-i for i in range(n) for j in range(3)] not in solutions:
                            solutions.append([c-i for i in range(n) for j in range(3)])
            else:  #三带一或三带对
                n = int(p[7:p.find('+')])
                if p[p.find('+')+1] == 's':
                    nt = 1
                else:
                    nt = 2
                for c in counter:
                    if c > self.prec[v]:
                        flag = 0
                        for i in range(n):
                            if c-i-1 not in counter or counter[c-i-1] < 3:
                                flag = 1
                                break
                        if not flag:
                            temp = [c-i for i in range(n) for j in range(3)]
                            counter_r = copy.deepcopy(counter)
                            for i in temp:
                                if i in counter_r:
                                    counter_r.pop(i)
                            ap = combinations(counter_r, n, nt)
                            if len(ap) == 0:
                                continue
                            for i in ap:
                                if temp+i not in solutions:
                                    solutions.append(temp+i)
        else: #炸弹
            for c in counter:
                if counter[c] == 4 and c > self.prec[v] and [c,c,c,c] not in solutions:
                    solutions.append([c,c,c,c])
        solutions_c = []
        for st in solutions:
            sol = [list(self.prec.keys())[list(self.prec.values()).index(i)] for i in st]
            solutions_c.append(sol)
        return solutions_c

    def try_act(self, t): #评估牌组
        myHand = copy.deepcopy(self.myHand)
        yourHand = copy.deepcopy(self.yourHand)
        if t != None:
            for c in t:
                myHand.remove(c)
        if len(myHand) == 0:
            return len(yourHand)
        opp = Player()
        opp.newGame(yourHand, myHand, self.teamName())
        t = opp.play(t)
        return -opp.try_act(t)

    def play(self, t): #返回最优方案
        solutions = self.get_all_solutions(t)
        if len(solutions) == 0:
            return []
        if len(solutions) == 1:
            return solutions[0]
        score = 0
        move = solutions[0]
        for sol in solutions:
            st = self.try_act(sol)
            if st > score:
                score = st
                move = sol
        return move

    def ack(self, t):
        #print("ack: {}".format(self.myHand))
        for c in t:
            self.myHand.remove(c)

    def teamName(self):
        return self.name
