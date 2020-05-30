# coding=utf-8
# 斗地主的全部代码（正式用途） Version 1.2 (5.23) 版本说明：完整版
from treelib import Tree
from suijichupai import fakePlayer
import time
import math
import sys
import random
import copy


class Data:
    def __init__(self):
        self.enemyCard = []  # 所有在桌上的牌都不包含在 enemyCard 和 myCard 中
        self.myCard = []
        self.turn = 0  # 0 代表当前是自己出的牌； 1 代表是对方出的牌，每次建立新节点的时候根据其父节点是 0 还是 1 来判断自己是 0 还是 1
        self.cardOnBoard = []

    def if_one_wins(self):
        if len(self.enemyCard) == 0 or len(self.myCard) == 0:
            return True
        else:
            return False

    def set_enemyCard(self, lst):
        self.enemyCard = lst

    def get_enemyCard(self):
        return self.enemyCard

    def set_myCard(self, lst):
        self.myCard = lst

    def get_myCard(self):
        return self.myCard

    def set_cardOnBoard(self, lst):
        self.cardOnBoard = lst

    def get_cardOnBoard(self):
        return self.cardOnBoard

    def set_turn(self, n):
        self.turn = n

    def get_turn(self):
        return self.turn


class MCST(Tree):
    """
        AI player, use Monte Carlo Tree Search with UCB
    """

    def __init__(self, time=28):  # 这里的 node 是根节点，在初始化树之前要先建立 root 节点，root 节点的 identifier 设置为 0
        super().__init__()
        self.calculation_time = float(time)  # 最大运算时间
        self.confident = 3  # UCB中的常数
        self.simulations = 0  # 记录总模拟次数
        self.count = 1  # count 记录的是节点的名字

    def get_count(self):
        return self.count

    # UCB 是相对于其父节点的 本函数传入一个（子）节点，计算其相对于父节点的 UCB值
    def UCB(self, node):
        if node.tag == 0:  # 要注意，这里用none代表了0/0情况
            return sys.maxsize
        else:
            success_num = node.tag[0]
            total_num = node.tag[1]
            TOTAL_NUM = self.parent(node.identifier).tag[1]
            if self.parent(node.identifier).data.get_turn() == 1:  # 这里对应父节点显示当前是对方出的牌，轮到自己出牌的情况
                ucb = (success_num / total_num) + self.confident * math.sqrt(math.log(TOTAL_NUM) / total_num)
            else:
                ucb = ((total_num - success_num) / total_num) + self.confident * math.sqrt(math.log(TOTAL_NUM) / total_num)
        return ucb

    # 本函数传入一个节点，返回该节点的拥有最大 UCB 值的子节点
    def findUCBmax(self, node):  # 规定了在 tag 项放置[胜场, 总场次], Node是当前在判断的那个 subroot 节点
        nodelist = self.children(node.identifier)  # nodelist 中存放的是该节点的所有子节点
        maxUCB = 0
        node_maxUCB = None
        for subnode in nodelist:
            temp = self.UCB(subnode)
            if temp >= maxUCB:
                maxUCB = temp
                node_maxUCB = subnode
        return node_maxUCB  # 返回了UCB最大的那个node，实际中可能更关心这个node的具体属性

    # 本函数传入树，返回此时应该出的牌（一个列表）
    def get_action(self):
        begin = time.time()
        while time.time() - begin < self.calculation_time:
            self.simulation()  # 时间允许内，不断进行 simulation
        # 选择根节点的子节点中分母最大者，即被选择次数最多者。
        nodelist = self.children('root')
        move_node = None
        maxtotal = 0
        for node in nodelist:
            if node.tag[1] > maxtotal:
                maxtotal = node.tag[1]
                move_node = node
        move = move_node.data.get_cardOnBoard()  # 得到该节点所出的牌
        return move

    def rollout(self, node):  # 传入一个 tag 为 None 的 node，己方赢返回 1，己方输返回 0
        fakeplayer = fakePlayer()
        myhand = node.data.get_myCard()
        yourhand = node.data.get_enemyCard()
        cardOnTable = node.data.get_cardOnBoard()
        turn = - node.data.get_turn() + 1
        answer = fakeplayer.rollout(myhand, yourhand, cardOnTable, turn)
        return answer

    def extend(self, node):  # 目前的 extend 不返回值，是一个 void 函数，给传入的节点添上所有可能的子节点，如果已经运行到底，则什么也不做
        parentNode_identifier = node.identifier  # 被 extend 节点的 identifier
        parent_data = node.data  # 被 extend 节点的 data 类
        # possible_reactions 里装了所有当前 node 之下可能连接的出牌方式，每种可能出的牌放在一个子列表里，如 [[6, 7, 8], [ 10, J ,Q]]
        play = fakePlayer()
        # 若当前的 node 不是 pass，跟牌
        if parent_data.get_cardOnBoard():
            # 若当前的 node 是 enemy，我方跟牌
            if parent_data.get_turn() == 1:
                possible_reactions = play.gen(parent_data.get_myCard(), parent_data.get_cardOnBoard())
            # 若当前的 node 是 my，敌方跟牌
            else:
                possible_reactions = play.gen(parent_data.get_enemyCard(), parent_data.get_cardOnBoard())
        # 若当前的 node 是 pass，出牌
        else:
            # 若当前的 node 是 enemy，我方出牌
            if parent_data.get_turn() == 1:
                possible_reactions = play.chu(parent_data.get_myCard())
            # 若当前的 node 是 my，敌方出牌
            else:
                possible_reactions = play.chu(parent_data.get_enemyCard())

        # 第一种情况，当前的 node 是 enemy，即 parent_data.get_turn() == 1
        if parent_data.get_turn() == 1:
            for possible_reaction in possible_reactions:
                its_data = Data()  # 初始化并设立每个可能子节点的 data
                its_data.set_cardOnBoard(possible_reaction)

                # 设置 myCard 将出的牌删去
                parent_myCard = copy.deepcopy(parent_data.get_myCard())  # 父节点的 mycard
                for eachCard in possible_reaction:  # 需要将父节点的 mycard 中删去 possible_reaction 里出过的牌
                    parent_myCard.remove(eachCard)  # remove 方法本身就只能删去一个元素，所以不会将相同的牌全部删去
                its_data.set_myCard(parent_myCard)

                # 设置 enemyCard 直接继承
                parent_enemyCard = copy.deepcopy(parent_data.get_enemyCard())  # 父节点的 enemycard
                its_data.set_enemyCard(parent_enemyCard)

                # 设置当前子节点的出牌方
                its_data.set_turn(0)

                self.create_node(tag=0, identifier=str(self.get_count()), data=its_data, parent=parentNode_identifier)
                self.count = self.count + 1

        # 第二种情况，当前的 node 是 my，即 parent_data.get_turn() == 0
        elif parent_data.get_turn() == 0:
            for possible_reaction in possible_reactions:
                its_data = Data()  # 初始化并设立每个可能子节点的 data
                its_data.set_cardOnBoard(possible_reaction)

                # 设置 myCard 直接继承
                parent_myCard = copy.deepcopy(parent_data.get_myCard())  # 父节点的 mycard
                its_data.set_myCard(parent_myCard)

                # 设置 enemyCard，需要将父节点的 enemycard 中删去 possible_reaction 里出过的牌
                parent_enemyCard = copy.deepcopy(parent_data.get_enemyCard())
                for eachCard in possible_reaction:  # 需要将父节点的 mycard 中删去 possible_reaction 里出过的牌
                    parent_enemyCard.remove(eachCard)  # remove 方法本身就只能删去一个元素，所以不会将相同的牌全部删去
                its_data.set_enemyCard(parent_enemyCard)

                # 设置当前子节点的出牌方
                its_data.set_turn(1)

                self.create_node(tag=0, identifier=str(self.get_count()), data=its_data, parent=parentNode_identifier)
                self.count = self.count + 1

    def simulation(self):
        rootnode = self.get_node('root')
        currentnode = rootnode
        while not currentnode.is_leaf():
            currentnode = self.findUCBmax(currentnode)  # 如果不是 leaf，则取当前节点的所有子节点中 UCB 最大的，作为新的当前节点
        if currentnode.tag == 0:  # 对应访问次数为0
            result = self.rollout(currentnode)  # 传回一个 1 or 0
            currentnode.tag = [0, 0]
            while currentnode.identifier != 'root':  # 逐层往上，每一次都得到自己的parent，并更新它的tag
                currentnode.tag[0] += result
                currentnode.tag[1] += 1
                currentnode = self.parent(currentnode.identifier)
            rootnode.tag[0] += result  # 更新 root 节点的记录比分
            rootnode.tag[1] += 1
        else:  # 对应已经被访问过
            self.extend(currentnode)  # 这一步需要再商榷，目的是给出当前情况接下来所有可能情况，但是实现步骤必然需要接头后才能清楚xxx
            choicelist = self.children(currentnode.identifier)
            if len(choicelist) == 0:
                if not currentnode.data.enemyCard:
                    result = 0
                elif not currentnode.data.myCard:
                    result = 1
                else:
                    raise Exception("在simulation里明明双方手牌都没空但extend方法没奏效")
            else:
                i = random.randint(0, len(choicelist) - 1)  # 一个随机数
                currentnode = self.children(currentnode.identifier)[i]  # 随机选取一个子节点
                result = self.rollout(currentnode)  # 传回一个 1 or 0
            currentnode.tag = [0, 0]
            while currentnode.identifier != 'root':  # 逐层往上，每一次都得到自己的 parent，并更新它的tag
                currentnode.tag[0] += result
                currentnode.tag[1] += 1
                currentnode = self.parent(currentnode.identifier)
            rootnode.tag[0] += result  # 更新 root 节点的记录比分
            rootnode.tag[1] += 1
        self.simulations = self.simulations + 1
