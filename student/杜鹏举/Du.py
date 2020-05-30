class Player:
    def __init__(self):
        self.name = "Du&Zhou"

    def getVal(self, cards):
        vals = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4, '8': 5, '9': 6, '10': 7, 'J': 8, 'Q': 9, 'K': 10, 'A': 11, '2': 12}
        for i, card in enumerate(cards):
            cards[i] = vals[card]


    def getCard(self, vals):
        cards = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
        ans = []
        for val in vals:
            ans.append(cards[val])
        return ans

# 获得顺子
    def getSeq(self, cards, length, size, num):
        ans = []
        seq = []
        if len(cards) >= length * num:
            for card in list(set(cards)):
                if ((len(seq) == 0 and card > size and card < 12 and cards.count(card) >= num) or
                        (len(seq) != 0 and seq[-1] + 1 == card and card < 12 and cards.count(card) >= num)):
                    seq = seq + [card] * num
                else:
                    seq = [card]
                if len(seq) == length * num:
                    pattern = -1
                    if num == 1:
                        pattern = length + 2
                    elif num == 2:
                        pattern = length + 13
                    elif num == 3:
                        pattern = length + 24
                    ans.append({'c': copy.deepcopy(seq), 'p': pattern, 's': seq[0]})
                    seq = seq[num:]
        return ans


# 获得飞机带翅膀
    def getPlane(self, cards, length, size):
        ans = []
        seq = []
        if len(cards) >= length * 4:
            for card in list(set(cards)):
                if ((len(seq) == 0 and card > size and card < 12 and cards.count(card) >= 3) or
                        (len(seq) != 0 and seq[-1] + 1 == card and card < 12 and cards.count(card) >= 3)):
                    seq = seq + [card] * 3
                else:
                    seq = []
                if len(seq) == length * 3:
                    cardBs = list(set(cards) - set(seq))
                    for case in list(combinations(cardBs, length)):
                        newSeq = seq + list(case)
                        ans.append({'c': newSeq, 'p': length + 24, 's': seq[0]})
                    seq = seq[3:]
        return ans


# 枚举可能的下一步
    def getNextMove(self, cards, pattern, size):
        moves = []
    # 炸弹
        if pattern != 0:
            for card in set(cards):
                if cards.count(card) == 4:
                    moves.append({'c': [card] * 4, 'p': 100, 's': card})
    # 单个牌
        if pattern == -1 or pattern == 2:
            for card in set(cards):
                if card > size:
                    moves.append({'c': [card], 'p': 2, 's': card})
    # 对子牌
        if pattern == -1 or pattern == 3:
            for card in set(cards):
                if cards.count(card) >= 2 and card > size:
                    moves.append({'c': [card] * 2, 'p': 3, 's': card})
    # 三张牌
        if pattern == -1 or pattern == 4:
            for card in set(cards):
                if cards.count(card) >= 3 and card > size:
                    moves.append({'c': [card] * 3, 'p': 4, 's': card})
    # 三带一
        if pattern == -1 or pattern == 5:
            for card in set(cards):
                if cards.count(card) >= 3 and card > size:
                    for cardB in set(cards):
                        if card != cardB:
                            moves.append({'c': [card] * 3 + [cardB], 'p': 5, 's': card})
    # 三带二
        if pattern == -1 or pattern == 6:
            for card in set(cards):
                if cards.count(card) >= 3 and card > size:
                    for cardB in set(cards):
                        if card != cardB and cards.count(cardB) >= 2:
                            moves.append({'c': [card] * 3 + [cardB] * 2, 'p': 6, 's': card})
    # 单顺子
        if pattern == -1:
            for length in range(5, 13):
                moves = moves + self.getSeq(cards, length, -1, 1)
        if pattern >= 7 and pattern <= 12:
            moves = moves + self.getSeq(cards, pattern - 2, size, 1)
    # 双顺子
        if pattern == -1:
            for length in range(2, 13):
                moves = moves + self.getSeq(cards, length, -1, 2)
        if pattern >= 15 and pattern <= 25:
            moves = moves + self.getSeq(cards, pattern - 13, size, 2)
    # 没有三顺子
    # if pattern == -1:
    # for length in range(2, 13):
    # moves = moves + getSeq(cards, length, -1, 3)
    # if pattern >= 26 and pattern <= 36:
    # moves = moves + getSeq(cards, pattern - 24, size, 3)
    # 飞机带翅膀
        if pattern == -1:
            for length in range(2, 7):
                moves = moves + self.getPlane(cards, length, -1)
        if pattern >= 28 and pattern <= 32:
            moves = moves + self.getPlane(cards, pattern - 24, size)

    # 四带两张单牌
        if pattern == -1 or pattern == 33:
            for card in set(cards):
                if cards.count(card) >= 4 and card > size:
                    cardBs = list(set(cards) - set([card]))
                    for case in list(combinations(cardBs, 2)):
                        moves.append({'c': [card] * 4 + list(case), 'p': 31, 's': card})
    # 四带两个对子
        if pattern == -1 or pattern == 34:
            for card in set(cards):
                if cards.count(card) >= 4 and card > size:
                    cardBs = list(set(cards) - set([card]))
                    for case in list(combinations(cardBs, 2)):
                        flag = True
                        for element in list(case):
                            if cards.count(element) < 2:
                                flag = False
                                break
                        if flag:
                            moves.append({'c': [card] * 4 + list(case) * 2, 'p': 32, 's': card})
    # 不出
        if pattern != -1:
            moves.append({'c': [], 'p': -1, 's': -1})
        return moves


# 从 list 中删掉另一个 list
    def removeElements(self, listA, listB):
        for element in listB:
            listA.remove(element)


    def newGame(self, hand1, hand2, opponent):
        self.myhand = hand1
        self.getVal(self.myhand)
        self.yourhand = hand2
        self.opponent = opponent


# moves中'c'记录牌的数值和数量；'p'记录牌的大小，每一种牌大小用一个数值代替用作后面比较：炸弹为100，单张为2，对牌为3，三张为4，三带一为5，\
# 三带二为6,单顺子中按张数从5张到12张，分别为7-14;双顺子（连对）从3344最小，到33-AA最大，分别为15-25；飞机带翅膀26-30；四带两单31；四带两对32
# 's'记录是哪张牌

# 主体
    def play(self, t):
        # 使用数值代替牌面
        movesA = self.getNextMove(self.myhand, -1, -1)
        if t == []:
            for i, move in enumerate(movesA):
                if 1 < move['p'] <= 30:
                    result = move
            return self.getCard(result['c'])
        else:
            self.getVal(t)
            movesB = self.getNextMove(t, -1, -1)
            for i, move in enumerate(movesB):
                if move['p'] == 100:
                    needtodefeat = move
                    break
                else:
                    needtodefeat = move
            for i, move in enumerate(movesA):
                if move['p'] == needtodefeat['p']:
                    if move['s'] > needtodefeat['s']:
                        return self.getCard(move['c'])
                        break

    def ack(self, t):
        # 使用数值代替牌面
        # print(self.myhand,t)
        self.getVal(t)
        movesA = self.getNextMove(self.myhand, -1, -1)
        if t == []:
            for i, move in enumerate(movesA):
                if 1 < move['p'] <= 30:
                    result = move
            self.removeElements(self.myhand, result['c'])
        else:
            movesB = self.getNextMove(t, -1, -1)
            for i, move in enumerate(movesB):
                if move['p'] == 100:
                    needtodefeat = move
                    break
                else:
                    needtodefeat = move

            for i, move in enumerate(movesA):
                if move['p'] == needtodefeat['p']:
                    if move['s'] > needtodefeat['s']:
                        self.removeElements(self.myhand, move['c'])
                        break
    def teamName(self):
        return self.name