# ecoding=utf-8
import time
from dealer import Dealer

# 牌号和值的对应映射
values = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, '10': 7,
          'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
cards = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']


def getVal(cards):  # 牌名->牌值
    ans = []
    for card in cards:
        ans.append(values[card])
    return ans


def getCard(vals):  # 牌值->牌名
    ans = []
    for val in vals:
        ans.append(cards[val])
    return ans


class Player:
    def __init__(self):
        self.opponent = None
        self.hand1 = None
        self.hand2 = None

    def teamName(self):
        return '朔风烈'

    def newGame(self, hand1, hand2, opponent):
        """
        hand1:自己手里的牌，比如：['A','A','2'],字母大写
        hand2:对方手里的牌
        opponent:对手名称
        """
        self.opponent = opponent
        me, oppo = getVal(hand1), getVal(hand2)
        me.sort()
        oppo.sort()
        self.hand1, self.hand2 = me, oppo

    def play(self, t):
        """
        打牌的过程，输入对手的牌，输出自己的对策，都是list[str]格式
        []表示自己先手或者对方pass
        return:自己出的牌，需要能压住t
        """
        h1 = Hand(self.hand1)
        h2 = Hand(self.hand2)
        t = getVal(t)
        playlist = h1.generatePlayList(t)
        for val in t:
            self.hand2.remove(val)
        if playlist == [[]]:  # 利用分支因子进行评估
            return []
        else:  # 深度评估
            eTree = Tree(h1, h2, t)
            buildTree(eTree, -100, 100, 0, deptheval(len(playlist)))
            toPlay = findT(eTree)
            return getCard(toPlay)

    def ack(self, t):
        t = getVal(t)
        for c in t:
            self.hand1.remove(c)


class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.valence = {i: 0 for i in range(13)}
        self.defineValence()
        # 在初始化的时候，先对每个号码进行估价。

    # get系列，在手牌堆里寻找所要求的的牌型
    def getSingle(self, card):
        '''
        获得单牌。
        '''
        if self.cards.count(card) in [1, 2, 3] or \
                (self.cards.count(card) == 4 and len(self.cards) <= 15):
            return [card]
        else:
            return None

    def getPair(self, card):
        '''
        获得对子。
        '''
        if self.cards.count(card) in [2, 3] or \
                (self.cards.count(card) == 4 and len(self.cards) <= 15):
            return [card, card]
        else:
            return None

    def getTriple(self, card):
        '''
        获得三同张。
        '''
        if self.cards.count(card) == 3 or \
                (self.cards.count(card) == 4 and len(self.cards) <= 15):
            return [card, card, card]
        else:
            return None

    def getTripleWithSingle(self, card):
        '''
        获得三带一。这里带的那一张单牌是自动选出的，为所有单牌中价最低的那张。注意带的那张牌和三同张的牌号不同。
        '''
        c = self.getTriple(card)

        if c:
            plusList = self.playSingle(-1)
            if not plusList:
                return None
            elif plusList[0][0] == card:
                # 注意 带的牌不能和三同张的一样。况且我在得到pluslist的时候并没有把三同张的牌删掉。
                # 就有可能，你只有三个九 但是plusList的第一个元素是[9]，这么出就错了。
                # 这个时候你就要出plusList的第二个元素，作为一个alternative。
                # 但是你plusList没有第二个元素呢？那你就别出了。
                if len(plusList) == 1:
                    return None
                else:
                    plus = plusList[1]
            else:
                plus = plusList[0]
            return c + plus
        else:
            return None

    def getTripleWithPair(self, card):
        '''
        获得三带二。带的那个对子也是自动选出的，是所有对子里头价最低的那个。
        '''
        c = self.getTriple(card)
        plusList = self.playPair(-1)
        if c:
            if not plusList:
                return None
            elif plusList[0][0] == card:
                if len(plusList) == 1:
                    return None
                else:
                    plus = plusList[1]
            else:
                plus = plusList[0]
            return c + plus
        else:
            return None

    def getSeq(self, size, beginning):
        '''
        获得顺子
        :param size: 想要得到的顺子的长度
        :param beginning: 顺子的第一张牌(可能是A23456...J）
        '''
        sum = 0
        seq = []
        if beginning <= 13 - size or beginning >= 11:
            for i in range(size):
                cnt = self.cards.count((beginning + i) % 13)
                if cnt == 4:  # 如果里面有炸弹，舍弃
                    return None
                sum += cnt
                seq.append((beginning + i) % 13)
            if len(self.cards) > 10 and 2 * sum // size > 3:  # 如果单张牌都有超过1.5的数目（平均），那么舍弃
                return None
            if set(self.cards) > set(seq):
                return seq
            return None

    def getSeqPair(self, size, beginning):
        '''
        获得连对
        :param size: 输入对子的长度
        :param beginning: 输入对子的最小牌号
        '''
        seqPair = []
        if beginning <= 13 - size or beginning >= 11:
            for i in range(size):
                if self.getPair((beginning + i) % 13):
                    seqPair.extend(self.getPair((beginning + i) % 13))
                else:
                    return None
            return seqPair

    def getSeqTriple(self, size, beginning):
        '''
        获得连三
        :param size: 输入连三的长度
        :param beginning: 输入连三的最小牌号
        '''
        seqTriple = []
        if beginning <= 13 - size or beginning >= 11:
            for i in range(size):
                if self.getTriple((beginning + i) % 13):
                    seqTriple.extend(self.getTriple((beginning + i) % 13))
                else:
                    return None
            return seqTriple

    def getSeqTripleWithSingle(self, size, beginning):
        '''
        获得连三带一。输出的形式是[x,x,x,y,a,a,a,b]这样的
        要有拆散一些整牌的觉悟，以达到出更多牌的目的
        '''
        plusList = self.playSingle(-1)
        output = []
        blist = []
        for i in range(size):
            c = self.getTriple((beginning + i) % 13)
            if c:
                output += c
            else:
                return None
        alist = list(set(output))
        for i in alist:
            if [i] in plusList:
                plusList.remove([i])

        if len(alist) > len(plusList):
            return None
        else:
            for i in range(len(alist)):
                blist.extend([alist[i], alist[i], alist[i],
                              plusList[i][0]])
            return blist

    def getSeqTripleWithPair(self, size, beginning):
        '''
        获得连三带二。基本同连三带一那个算法。
        要有拆散一些整牌的觉悟，以达到出更多牌的目的。
        '''
        plusList = self.playPair(-1)
        output = []
        blist = []
        for i in range(size):
            c = self.getTriple((beginning + i) % 13)
            if c:
                output += c
            else:
                return None
        alist = list(set(output))
        for i in alist:
            if [i, i] in plusList:
                plusList.remove([i, i])
        if len(alist) > len(plusList):
            return None
        else:
            for i in range(len(alist)):
                blist.extend([alist[i], alist[i], alist[i],
                              plusList[i][0], plusList[i][0]])
            return blist

    def getBomb(self, card):
        '''
        获得炸弹。
        '''
        if self.cards.count(card) >= 4:
            return [card, card, card, card]
        else:
            return None

    # play系列，根据对方的牌来输出可能方案
    def playSingle(self, t):
        '''
        出单牌。根据对方的牌，给出自己的出牌方案。
        :param t: 对方单牌的牌号
        :return: 可能的出牌方案，按照牌的价值来排序。价低的放在前面，先考虑。毕竟一般不希望把好牌拆了。
        '''
        solution = []
        for i in range(t + 1, 13):
            c = self.getSingle(i)
            if c:
                solution.append(c)
        return self.sortSolution(solution)

    def playPair(self, t):
        '''
        出对子。根据对方的牌，给出自己的出牌方案。
        :param t: 对方对子的牌号
        :return: 出牌方案。按照牌的价值排序。
        '''
        solution = []
        for i in range(t + 1, 13):
            c = self.getPair(i)
            if c:
                solution.append(c)
        return self.sortSolution(solution)

    def playTriple(self, t):
        '''
        出三张。
        '''
        solution = []
        for i in range(t + 1, 13):
            c = self.getTriple(i)
            if c:
                solution.append(c)
        return self.sortSolution(solution)

    def playTripleWithSingle(self, t):
        '''
        出三带一。带的那一张牌自己生成了。
        '''
        solution = []
        for i in range(t + 1, 13):
            c = self.getTripleWithSingle(i)
            if c:
                solution.append(c)
        return self.sortSolution(solution)

    def playTripleWithPair(self, t):
        '''
        出三带二。
        '''
        solution = []
        for i in range(t + 1, 13):
            c = self.getTripleWithPair(i)
            if c:
                solution.append(c)
        return self.sortSolution(solution)

    def playSeq(self, t, size):
        '''
        出顺子，可能出现A2345
        '''
        solution = []
        if t != -1 and t < 11 and t + size > 12:
            return []
        if -1 < t < 11:
            for i in range(t + 1, 14 - size):
                c = self.getSeq(size, i)
                if c:
                    solution.append(c)
        elif t > 10 or t == -1:
            for i in range(14 - size):
                c = self.getSeq(size, i)
                if c:
                    solution.append(c)
            if t == -1:
                for i in [11, 12]:
                    c = self.getSeq(size, i)
                    if c:
                        solution.append(c)
            elif t == 11:
                c = self.getSeq(size, 12)
                if c:
                    solution.append(c)

        return self.sortSolution(solution)

    def playSeqPair(self, t, size):
        '''
        出连对，可能出现AA2233等
        '''
        solution = []
        if t != -1 and t < 11 and t + size > 12:
            return []
        if -1 < t < 11:
            for i in range(t + 1, 14 - size):
                c = self.getSeqPair(size, i)
                if c:
                    solution.append(c)
        elif t > 10 or t == -1:
            if size == 2 and t == 11:
                return []
            for i in range(14 - size):
                c = self.getSeqPair(size, i)
                if c:
                    solution.append(c)
            if t == -1:
                for i in [11, 12]:
                    c = self.getSeqPair(size, i)
                    if c:
                        solution.append(c)
            elif t == 11:
                c = self.getSeqPair(size, 12)
                if c:
                    solution.append(c)
        return self.sortSolution(solution)

    def playSeqTriple(self, t, size):
        '''
        出连三，可能出现AAA222333等
        '''
        solution = []
        if t != -1 and t < 11 and t + size > 12:
            return []
        if -1 < t < 11:
            for i in range(t + 1, 14 - size):
                c = self.getSeqTriple(size, i)
                if c:
                    solution.append(c)
        elif t > 10 or t == -1:
            if size == 2 and t == 11:
                return []
            for i in range(14 - size):
                c = self.getSeqTriple(size, i)
                if c:
                    solution.append(c)
            if t == -1:
                for i in [11, 12]:
                    c = self.getSeqTriple(size, i)
                    if c:
                        solution.append(c)
            elif t == 11:
                c = self.getSeqTriple(size, 12)
                if c:
                    solution.append(c)
        return self.sortSolution(solution)

    def playSeqTripleWithSingle(self, t, size):
        '''
        出连三带一。
        '''
        solution = []
        if t != -1 and t < 11 and t + size > 12:
            return []
        if -1 < t < 11:
            for i in range(t + 1, 14 - size):
                c = self.getSeqTripleWithSingle(size, i)
                if c:
                    solution.append(c)
        elif t > 10 or t == -1:
            if size == 2 and t == 11:
                return []
            for i in range(14 - size):
                c = self.getSeqTripleWithSingle(size, i)
                if c:
                    solution.append(c)
            if t == -1:
                for i in [11, 12]:
                    c = self.getSeqTripleWithSingle(size, i)
                    if c:
                        solution.append(c)
            elif t == 11:
                c = self.getSeqTripleWithSingle(size, 12)
                if c:
                    solution.append(c)
        return self.sortSolution(solution)

    def playSeqTripleWithPair(self, t, size):
        '''
        出连三带二。可能出现2225533344
        '''
        solution = []
        if t != -1 and t < 11 and t + size > 12:
            return []
        if -1 < t < 11:
            for i in range(t + 1, 14 - size):
                c = self.getSeqTripleWithPair(size, i)
                if c:
                    solution.append(c)
        elif t > 10 or t == -1:
            if size == 2 and t == 11:
                return []
            for i in range(14 - size):
                c = self.getSeqTripleWithPair(size, i)
                if c:
                    solution.append(c)
            if t == -1:
                for i in [11, 12]:
                    c = self.getSeqTripleWithPair(size, i)
                    if c:
                        solution.append(c)
            elif t == 11:
                c = self.getSeqTripleWithPair(size, 12)
                if c:
                    solution.append(c)
        return self.sortSolution(solution)

    def playBomb(self, t):
        '''
        出炸弹
        '''
        solution = []
        for i in range(t + 1, 13):
            c = self.getBomb(i)
            if c:
                solution.append(c)
        return self.sortSolution(solution)

    def playFree(self):
        '''
        自由出牌
        :return: 把所有出牌方案都给你输出一遍。然后其实只会输出前八种打法。
        '''
        solution = []
        for i in range(13, 1, -1):
            solution += self.playSeqTripleWithPair(-1, i)
            solution += self.playSeqTripleWithSingle(-1, i)

        for i in range(13, 1, -1):
            solution += self.playSeqPair(-1, i)
        for i in range(13, 4, -1):
            solution += self.playSeq(-1, i)

        solution += self.playTripleWithPair(-1)
        solution += self.playTripleWithSingle(-1)
        solution += self.playPair(-1)
        solution += self.playSingle(-1)
        solution += self.playBomb(-1)
        return solution[:8]

    # “高手经验”系列，为了给输出方案列表一个更好的排序方式。
    def defineValence(self):
        '''
        单牌价值为1，对子2，连对3，顺子4，三张5，连三张6，炸弹7。没这张牌就0
        '''
        for i in range(13):
            if i not in self.cards:
                self.valence[i] = 0
            elif self.getBomb(i):
                self.valence[i] = 7
            elif self.getSeqTriple(2, i) \
                    or self.getSeqTriple(2, i - 1):
                self.valence[i] = 6
            elif self.getTriple(i):
                self.valence[i] = 5
            elif self.is_it_inside_a_Seq(i):
                self.valence[i] = 4
            elif self.getSeqPair(2, i) \
                    or self.getSeqPair(2, i - 1):
                self.valence[i] = 3
            elif self.getPair(i):
                self.valence[i] = 2
            elif self.getSingle(i):
                self.valence[i] = 1

    def is_it_inside_a_Seq(self, card):
        '''
        上面那个估价函数的辅助。判断一张牌是不是在一个顺子里头
        '''
        for i in range(card - 4, card + 1):
            if self.getSeq(5, i):
                return True
        return False

    def sortSolution(self, solution):
        '''
        将play***方法得到的solution进行一个大概的排序
        :param solution: solution列表
        :return: 排序之后的solution列表，并且只输出前四种。
        '''
        solution.sort(key=lambda x: self.valence[x[0]])
        return solution[:4]

    # 实际操作只要用到最后两个。根据对方出的牌生成备选方案列表 + 删除打出的牌
    def generatePlayList(self, t):
        '''
        生成一个方案列表。形式为[[],[0,0,0,..],[a,b,...],...]。第一个空列表表示过。
        :param p: 对方出的牌t
        :return: 出牌列表playlist
        '''
        d = Dealer('version1')
        p = d.pattern(getCard(t))
        if not p:
            playlist = self.playFree()
        else:
            # p形如 ('triple*3+single', '3')
            playlist = []
            pattern = p[0].split('+')
            if pattern[0] == 'bomb':  # 炸弹的话没有标size
                t = values[p[1]]
                playlist += self.playBomb(t)
            else:
                size = int(pattern[0][-1])
                t = (values[p[1]] - size + 1) % 13  # 这一串牌的初始牌。老师给的那个返回的是终止牌，我们的代码用的是初始牌。
                if len(pattern) == 1:
                    if size == 1:
                        if pattern[0][:-2] == 'triple':
                            playlist += self.playTriple(t)
                        elif pattern[0][:-2] == 'pair':
                            playlist += self.playPair(t)
                        elif pattern[0][:-2] == 'single':
                            playlist += self.playSingle(t)
                    else:
                        if pattern[0][:-2] == 'triple':
                            playlist += self.playSeqTriple(t, size)
                        elif pattern[0][:-2] == 'pair':
                            playlist += self.playSeqPair(t, size)
                        elif pattern[0][:-2] == 'single':
                            playlist += self.playSeq(t, size)
                if len(pattern) == 2:
                    if size == 1:
                        if pattern[0][:-2] == 'triple' and pattern[1] == 'pair':
                            playlist += self.playTripleWithPair(t)
                        elif pattern[0][:-2] == 'triple' and pattern[1] == 'single':
                            playlist += self.playTripleWithSingle(t)
                    else:
                        if pattern[0][:-2] == 'triple' and pattern[1] == 'pair':
                            playlist += self.playSeqTripleWithPair(t, size)
                        elif pattern[0][:-2] == 'triple' and pattern[1] == 'single':
                            playlist += self.playSeqTripleWithSingle(t, size)
                playlist += self.playBomb(-1)
            playlist += [[]]
        return playlist[:8]


class Tree:
    def __init__(self, hand1, hand2, t, layer=- 1):
        self.hand1 = hand1  # 牌从hand1中出
        self.hand2 = hand2  # 上一次的出牌方剩下的牌为hand2。
        self.t = t  # t:上一次出的牌，即需要应对的牌。
        self.score = 0
        self.child = []
        self.layer = layer  # 层数，-1为偶，1为奇

    def getHand1(self):
        return self.hand1

    def getHand2(self):
        return self.hand2

    def getT(self):
        return self.t

    def getLayer(self):
        return self.layer

    def insertChild(self, childTree):
        self.child.append(childTree)

    def getChild(self):
        return self.child

    def setScore(self, newscore):
        self.score = newscore

    def getScore(self):
        return self.score


def buildTree(eTree, alpha, beta, depth, maxdepth):
    start = time.time()
    if eTree.getHand1().cards and eTree.getHand2().cards and depth < maxdepth:  # 不是叶节点
        playlist = eTree.getHand1().generatePlayList(eTree.getT())  # 所有出牌方法。（注：这里默认如果对方出[]，我方将不会出[])
        for playChoice in playlist:
            end = time.time()
            if int(end - start) > 27:
                break
            newList = eTree.getHand1().cards.copy()
            for card in playChoice:
                newList.remove(card)  # 把hand1中决定出出的牌删去
            # 建子树，记得两个hand交换顺序
            childTree = Tree(eTree.getHand2(), Hand(newList), playChoice, (-1) * eTree.getLayer())
            eTree.insertChild(childTree)

            if eTree.layer == -1:
                alpha = max(alpha, buildTree(childTree, alpha, beta, depth + 1, maxdepth))
                toReturn = alpha
                if beta <= alpha:
                    break
            else:
                beta = min(beta, buildTree(childTree, alpha, beta, depth + 1, maxdepth))
                toReturn = beta
                if beta <= alpha:
                    break
        eTree.setScore(toReturn)
        return toReturn

    else:  # 对当前迭代树的叶节点，直接返回评估的分数
        # TODO:评估函数可优化
        eTree.setScore((len(eTree.getHand1().cards) - len(eTree.getHand2().cards)) * eTree.getLayer())
        return eTree.getScore()


def findT(eTree):  # 找出第1层（根节点的下一层）中得分最高的节点的t（出牌方法）
    maxScore = -120
    ToPlay = []
    for child in eTree.getChild():
        childScore = child.getScore()
        if childScore > maxScore:
            ToPlay = child.getT()
            maxScore = childScore
    return ToPlay


# 评估迭代深度的函数
def deptheval(b):
    return 15 - b // 4
