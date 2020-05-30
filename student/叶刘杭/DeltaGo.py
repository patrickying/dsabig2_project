from MCST import Data, MCST


class Player:
    def __init__(self):
        self.name = "DeltaGo"
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
    
    def newGame(self, hand1, hand2, opponent):
        self.myHand = hand1
        self.yourHand = hand2
        self.opponent = opponent

    # 无用
    """def beat(self, t, yt):
        if len(t) == 1 and len(yt) == 1:
            return self.prec[t[0]] > self.prec[yt[0]]
        return not yt"""

    # t 是对方出的牌的列表
    def play(self, t):
        for c in t:
            self.yourHand.remove(c)
        if not self.myHand:
            return []
        root_data = Data()
        root_data.set_myCard(self.myHand)
        root_data.set_enemyCard(self.yourHand)
        root_data.set_cardOnBoard(t)
        root_data.set_turn(1)
        strategyTree = MCST()
        strategyTree.create_node(tag=None, identifier="root", data=root_data)
        strategyTree.extend(strategyTree.get_node("root"))
        strategyTree.get_node("root").tag = [0, 0]
        return strategyTree.get_action()

    def ack(self, t):
        #print("ack: {}".format(self.myHand))
        for c in t:
            self.myHand.remove(c)

    def teamName(self):
        return self.name

"""
Test
play = Player()
play.newGame(['10','J','Q','Q', 'Q', 'Q', 'K',"A"],['7','8','9','10','J','2','2'],"hahaha")
print(play.play(['7','8','9','10','J']))
play.newGame(['6','6','6','6','7'],['3','3','3','3','4'],"hahaha")
print(play.play(['3','3','3','3']))
"""