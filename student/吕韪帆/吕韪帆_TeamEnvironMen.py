# Big2 version_1.4
# Team EnvironMen
import copy
from functools import reduce
from itertools import combinations
card2num = {'A': 14, '2': 15, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
num2card = {0: None, 1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A', 15: '2'}
card2num_1 = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}


class Player:
    def teamName(self):
        return 'EnvironMen'

    def newGame(self, hand1, hand2, opponent='Player'):
        self.mycard = sorted(hand1, key=lambda x: card2num[x])
        self.opponentcard = sorted(hand2, key=lambda x: card2num[x])

    def play(self, t=[]):
        for x in t:
            self.opponentcard.remove(x)
        op = playable(t, self.mycard)
        op1 = playable([], self.mycard)
        op2 = playable([], self.opponentcard)
        draw = []
        begin = copy.deepcopy(self.mycard)
        if t:
            priority = False
            if is_sol_end(op2):
                draw = find_max_value(op, self.mycard, self.opponentcard, 2, priority)
            else:
                draw = find_max_value(op, self.mycard, self.opponentcard, 1, priority)
        else:
            priority = True
            if find_str_2(op, self.mycard):
                draw = find_str_2(op, self.mycard)[0]
            else:
                pre_draw = []
                if find_A_pattern(op, self.mycard):
                    pre_draw += find_A_pattern(op, self.mycard)
                if find_str_1(op, self.mycard):
                    pre_draw += find_str_1(op, self.mycard)
                if find_distr_1(op, self.mycard):
                    pre_draw += find_distr_1(op, self.mycard)
                if pre_draw:
                    draw = pre_find_max_value(pre_draw)
                else:
                    if is_sol_end(op2):
                        draw = find_max_value(op, self.mycard, self.opponentcard, 2, priority)
                    else:
                        draw = find_max_value(op, self.mycard, self.opponentcard, 1, priority)
        return draw

    def ack(self, t=[]):
        for x in t:
            self.mycard.remove(x)


def pattern(play):  # 判断牌型,返回一个元组
    counter = [play.count(num2card[i]) if i >= 3 else 0 for i in range(16)]
    if counter[3] == counter[15] and not (3 in counter and (counter[3] == 2 or counter[3] == 1)) and counter[3] != 0:
        counter = [play.count(num2card[i]) if i <= 13 else 0 for i in range(16)]
    if 4 in counter:  # 如果输入中包含四张(bomb)
        if len(play) == 4:  # 而且没有其他牌
            return (1, 0, counter.index(4))  # 返回(1//指炸弹,0//不需要牌型值,牌面)
        else:
            return None  # 牌型不合法
    if 3 in counter:  # 否则如果输入中包含三张
        num3 = counter.count(3)  # 三张的组数
        num2 = counter.count(2)  # 带两张的组数
        num1 = counter.count(1)  # 带一张的组数
        for i in range(num3):  # 确定三张是否相连
            if counter[counter.index(3) + i] != 3:  # 如果不相连
                return None  # 牌型不合法
        if 2 in counter:  # 如果带了两张
            if num2 != num3 or 1 in counter:
                return None
        if 1 in counter:  # 如果带了一张
            if num1 != num3:
                return None
        return (0, (0, num1, num2, num3), counter.index(3))  # 返回(0//指普通牌,(0,num1,num2,num3)//分别是占位符、一张、两张、三张的组数,连三张最小牌的牌面)
    if 2 in counter:  # 下面基本同理
        num2 = counter.count(2)
        for i in range(num2):
            if counter[counter.index(2) + i] != 2:
                return None
        if 1 in counter:
            return None
        return (0, (0, 0, num2, 0), counter.index(2))
    if 1 in counter:
        num1 = counter.count(1)
        if 1 < num1 < 5:
            return None
        for i in range(num1):
            if counter[counter.index(1) + i] != 1:
                return None
        return (0, (0, num1, 0, 0), counter.index(1))
    return (-1, 0, 0)  # 如果是空牌组,那么返回(-1,0,0)


def findBroken(card):  # 寻找碎牌(非顺单张、非连二张),返回一个列表[None,[碎单张牌号],[碎对子牌号]]
    counter = [card.count(num2card[i]) for i in range(16)]
    minnum = 1
    maxlen = 0
    connected = []
    while minnum < 16 and maxlen < 5:
        for i in range(16 - minnum):
            if counter[minnum + i] < 1 or minnum + i == 16:
                maxlen = i
                break
        if maxlen >= 5:
            connected += [(minnum + i) for i in range(maxlen)]
            minnum += maxlen
            break
        else:
            minnum += 1
    while minnum < 16 and maxlen < 5:
        for i in range(16 - minnum):
            if counter[minnum + i] < 1 or minnum + i == 16:
                maxlen = i
                break
        if maxlen >= 5:
            connected += [(minnum + i) for i in range(maxlen)]
            minnum += maxlen
            break
        else:
            minnum += 1
    broken = [None, [], []]
    broken1 = set()
    broken2 = set()
    for i in range(16):
        if counter[i] == 1 and i not in connected:
            broken1.add(num2card[i])
        if counter[i] == 2:
            if (i == 3 or counter[i - 1] != 2) and (i == 15 or counter[i + 1] != 2):
                broken2.add(num2card[i])
    broken[1] = sorted([card2num[x] for x in broken1])
    broken[2] = sorted([card2num[x] for x in broken2])
    return broken


def playableForEmpty(mycard):
    result = []
    counter = [mycard.count(num2card[i]) if i >= 3 else 0 for i in range(16)]
    broken = findBroken(mycard)
    for i in range(16):  # 单张
        if counter[i] == 1:
            result.append([num2card[i]])
    for i in range(16):  # 两张
        if counter[i] == 2:
            result.append([num2card[i] for _ in range(2)])
    for i in range(16):  # 三张
        if counter[i] == 3:
            result.append([num2card[i] for _ in range(3)])
    counter = [mycard.count(num2card[i]) for i in range(16)]
    for x in range(16):  # 连二
        for i in range(16 - x):
            if counter[x + i] < 2:
                maxnum = i
                break
        if maxnum >= 2:
            for i in range(2, maxnum + 1):
                result.append(reduce(lambda t, j: t + [num2card[x + j]] * 2, range(i), []))
    for x in range(16):  # 连三
        for i in range(16 - x):
            if counter[x + i] < 3:
                maxnum = i
                break
        if maxnum >= 2:
            for i in range(2, maxnum + 1):
                result.append(reduce(lambda t, j: t + [num2card[x + j]] * 3, range(i), []))

    for x in range(16):  # 顺子
        for i in range(16 - x):
            if counter[x + i] < 1:
                maxnum = i
                break
        if maxnum >= 5:
            for i in range(5, maxnum + 1):
                result.append([num2card[x + j] for j in range(i)])

    temp = []
    for i in range(16):  # 连三带
        for j in range(16 - i):
            if counter[i + j] < 3:
                maxnum = j
                break
        if maxnum >= 1:
            for j in range(1, maxnum + 1):
                temp.append((i, j))
    for x in temp:
        t = [y for y in broken[1]]
        if len(broken[1]) >= x[1]:
            for y in (combinations(t, x[1])):
                result.append(reduce(lambda t, i: t + [num2card[x[0] + i]] * 3, range(x[1]), []) + reduce(lambda t, i: t + [num2card[i]], y, []))
        t = [y for y in broken[2]]
        if len(broken[2]) >= x[1]:
            for y in (combinations(t, x[1])):
                result.append(reduce(lambda t, i: t + [num2card[x[0] + i]] * 3, range(x[1]), []) + reduce(lambda t, i: t + [num2card[i]] * 2, y, []))
    for i in range(16):  # 炸弹
        if counter[i] == 4:
            result.append([num2card[i] for _ in range(4)])
    return result


def playable(t, mycard):
    counter = [mycard.count(num2card[i]) if i >= 3 else 0 for i in range(16)]
    playedPattern = pattern(t)
    assert playedPattern, str(t)
    if playedPattern[0] == -1:
        return playableForEmpty(mycard)
    if playedPattern[0] == 1:  # 炸弹
        return [[num2card[x]] * 4 for x in range(playedPattern[2], 16) if counter[x] == 4]
    result = [[num2card[x]] * 4 for x in range(16) if counter[x] == 4]
    if playedPattern[0] == 0:
        if playedPattern[1][3] > 0:  # (连)三
            joint = 2 if playedPattern[1][2] else 1 if playedPattern[1][1] else 0  # 带牌
            num3 = playedPattern[1][3]
            temp = [x for x in range(playedPattern[2] + 1, 17 - num3) if False not in map(lambda i: counter[x + i] >= 3, range(num3))]  # 所有(连)三
            if joint:
                for x in temp:
                    t = [y for y in range(16) if counter[y] >= joint and y not in range(x, x + num3)]
                    for y in (combinations(t, num3)):
                        result.append(reduce(lambda t, i: t + [num2card[x + i]] * 3, range(num3), []) + reduce(lambda t, i: t + [num2card[i]] * joint, y, []))
                return result
            return result + [reduce(lambda t, i: t + [num2card[x + i]] * 3, range(num3), []) for x in temp]
        if playedPattern[1][2] > 0:
            num2 = playedPattern[1][2]
            temp = [x for x in range(playedPattern[2] + 1, 17 - num2) if False not in map(lambda i: counter[x + i] >= 2, range(num2))]
            return result + [reduce(lambda t, i: t + [num2card[x + i]] * 2, range(num2), []) for x in temp]
        if playedPattern[1][1] > 0:
            num1 = playedPattern[1][1]
            temp = [x for x in range(playedPattern[2] + 1, 17 - num1) if False not in map(lambda i: counter[x + i] >= 1, range(num1))]
            return result + [[num2card[x + i] for i in range(num1)] for x in temp]
    return []


def pre_find_max_value(pre_draw):  #  提到过优先寻找一些特定的牌型，这个函数和下面的函数可以在找到了多个特定牌型之后决定哪一手优先打
    draw = pre_draw[0]
    maxvalue = 0
    for each in pre_draw:
        value = pre_count_value(each)
        if value >= maxvalue:
            maxvalue = value
            draw = each
    return draw


def pre_count_value(t):
    value = 0
    if pattern(t)[1][3] >= 2:
        value += 20
        value += 15 - pattern(t)[2]
    if pattern(t)[1][1] >= 5:
        value += 15
        value += 15 - pattern(t)[2]
    if pattern(t)[1][2] >= 2:
        value += 15 - pattern(t)[2]
    return value


def find_str_num(op):  # 计算顺子的数量，但是实际上用的时候只有：有顺子和没顺子的区别
    num = 0
    for e in op:
        p = pattern(e)
        if p[0] == 0:
            if p[1][1] >= 5:
                num += 1
    return num


def find_A_pattern(op, cards):  #寻找这些牌型：不需要拆牌的顺子，连对
    draw_list = []
    for each in op:
        begin = copy.deepcopy(cards)
        after = remove(each, begin)
        pure = True
        for i in each:
            if i in after:
                pure = False
                break
        if pure:
            p = pattern(each)
            if p and p[0] == 0:
                if p[1][2] >= 2 and p[2] <= 12:
                    draw_list.append(each)
                elif p[1][1] >= 5:
                    draw_list.append(each)
    return draw_list


def find_str_1(op, cards):  # 寻找牌型：拆牌数量不多的顺子，大概5拆2,6拆2都是可以接受的
    draw_list = []
    for e in op:
        p = pattern(e)
        begin = copy.deepcopy(cards)
        after = remove(e, begin)
        help_set = set(after)
        if p and p[0] == 0:
            if p[1][1] >= 5:
                count = 0
                for i in e:
                    if i in help_set:
                        count += 1
                if len(e) - count > count:
                    draw_list.append(e)
    return draw_list


def find_distr_1(op, cards):  # 找到只需要拆一个三张的3连对。这里不用担心把边上的三张拆开，因为前面已经找过纯的连对，这里没有这样的情况
    draw_list = []
    for e in op:
        p = pattern(e)
        begin = copy.deepcopy(cards)
        after = remove(e, begin)
        if p and p[0] == 0:
            if p[1][2] >= 3 and p[2] <= 12:
                count = 0
                if e[0] in after or e[len(e) - 1] in after:
                    count += 2
                i = 2
                while i <= len(e) - 3:
                    if e[i] in after:
                        count += 1
                    i += 2
                if count <= 1:
                    draw_list.append(e)
    return draw_list


def find_str_2(op, cards):  # 寻找重叠的顺子，避免把中间的连对优先打掉，留下一堆单牌
    draw_list = []
    str_list = []
    distr_list = []
    for e in op:
        p = pattern(e)
        if p and p[0] == 0:
            if p[1][1] >= 5:
                str_list.append(e)
            if p[1][2] >= 2:
                distr_list.append(e)
    if len(str_list) >= 2:
        for e in str_list:
            help_list = copy.deepcopy(str_list)
            help_list.remove(e)
            e_set = set(e)
            for i in help_list:
                i_set = set(i)
                for x in distr_list:
                    x_set = set(x)
                    if x_set == e_set.intersection(i_set):
                        new_set = i_set.union(e_set)
                        begin = copy.deepcopy(cards)
                        after = remove(e, begin)
                        end = remove(i, after)
                        count = 0
                        for each in new_set:
                            if each in end:
                                count += 1
                        if count <= 1:
                            draw_list.append(e)
                            draw_list.append(i)
                            return draw_list
    return draw_list


def remove(t, begin):  # 辅助功能
    for i in t:
        begin.remove(i)
    return begin


def find_max_value(op, cards1, cards2, k, x):  # 最大价值寻找
    max_value = 0
    draw = []
    for each in op:
        vl = value_count(each, cards1, cards2, k, x)
        if vl > max_value:
            max_value = vl
            draw = each
    return draw


def smallAndBig(mycard, op):
    mycard1 = list(mycard)
    op1 = list(op)
    mycounter = [mycard1.count(num2card[i]) if i >= 3 else 0 for i in range(16)]
    opcounter = [op1.count(num2card[i]) if i >= 3 else 0 for i in range(16)]
    # 当一方只剩单双张的时候，比如对方只剩单双张，那我方只要有先手，顺子，三张都可以直接打出
    mysmallsin = []
    mybigsin = []
    mysinmax = 0
    opsinmax = 15  # 如果对方没有单牌，相当于占有一定优势，
    mysinmin = 0
    opsinmin = 0
    for i in range(15, 0, -1):
        if mycounter[i] == 1:
            mysinmax = i
            break
    for i in range(15, 0, -1):
        if opcounter[i] == 1:
            opsinmax = i
            break
    for i in range(15):
        if mycounter[i] == 1:
            mysinmin = i
            break
    for i in range(15):
        if opcounter[i] == 1:
            opsinmin = i
            break
    # 如果最大的单牌在我方，那么我方所有比对方最大单牌大的单牌都是大牌；
    # 如果最小的单牌在我方，那么我方所有比对方最小单牌小的都是小牌
    if mysinmax >= opsinmax:
        for i in range(opsinmax, mysinmax + 1):
            if mycounter[i] == 1:
                mybigsin.append([num2card[i]])
    if mysinmin <= opsinmin:
        for i in range(mysinmin, opsinmin + 1):
            if mycounter[i] == 1:
                mysmallsin.append([num2card[i]])

    mysmallcp = []
    mybigcp = []
    mycpmax = 0
    opcpmax = 0
    mycpmin = 0
    opcpmin = 0
    for i in range(15, 0, -1):
        if mycounter[i] == 2:
            mycpmax = i
            break
    for i in range(15, 0, -1):
        if opcounter[i] == 2:
            opcpmax = i
            break
    for i in range(15):
        if mycounter[i] == 2:
            mycpmin = i
            break
    for i in range(15):
        if opcounter[i] == 2:
            opcpmin = i
            break
    # 如果最大的对牌在我方，那么比对方最大对牌大的是大牌，比我方最大单牌大的，也可以是大牌，即可以考虑拆，不建议直接打出
    if mycpmax >= opcpmax or mycpmax > mysinmax:
        for i in range(min(opcpmax, max(opsinmax, mysinmax)), mycpmax + 1):
            if mycounter[i] == 2:
                mybigcp.append([num2card[i]] * 2)
                # mybigcp.append(num2card[i])
    if mycpmax >= opsinmax:
        for i in range(opsinmax, mycpmax + 1):
            if mycounter[i] == 2:
                mybigsin.append([num2card[i]])
                mybigsin.append([num2card[i]])
    if mycpmin <= opcpmin:
        for i in range(mycpmin, opcpmin + 1):
            if mycounter[i] == 2:
                mysmallcp.append([num2card[i]] * 2)
                # mysmallcp.append(num2card[i])

    result = [mybigsin, mysmallsin, mybigcp, mysmallcp]
    return result


def value_count(t, card1, card2, k, x):  # 价值计算
    value = k * len(t)
    set_help = set(t)
    p = pattern(t)
    if p and p[0] == 1 and not x:
        value += 3 + 20 / len(card1)
    elif p and p[0] == 0:
        if len(t) == 1:
            if not playable(t, card2):
                value += 30 / (len(set(card2)))
            if 12 - card2num[t[0]] > 0:
                value += 12 - card2num[t[0]]
        else:
            if len(t) == 2:
                if 12.5 - card2num[t[0]] > 0:
                    value += 12.5 - card2num[t[0]]
            elif p[1][3] == 1:
                if len(t) > 3:
                    value += 13 - card2num[t[0]] + 9 - card2num[t[3]]
                else:
                    value += 13 - card2num[t[0]]
            elif p[1][2] >= 2:
                if '2' in t:
                    value -= 14
                for e in t:
                    value += 12 - card2num[e]
            elif p[1][1] >= 5:
                for e in t:
                    if 11 - card2num[e] > 0:
                        value += 11 - card2num[e]
            elif p[1][3] >= 2:
                if '2' in t:
                    value -= 21
                for e in list(set_help):
                    value += 12 - card2num[e]
            else:
                raise KeyError
            if not playable(t, card2):
                value += 10
            lose = lose_count(t, card1, card2)
            value += lose
    else:
        pass
    return value


def lose_count(t, card1, card2):  # 损失计算
    lose = 0
    after = copy.deepcopy(card1)
    be_broke = []
    for e in t:
        after.remove(e)
    p = pattern(t)
    if p[1][1] >= 5:
        for e in t:
            if after.count(e) >= 1:
                be_broke.append(e)
            if after.count(e) >= 2:
                lose -= 12
        if len(be_broke) > 2:
            lose -= 17
    if len(t) == 1:
        if after.count(t[0]) == 0:
            pass
        elif after.count(t[0]) == 1:
            if 12 - card2num[t[0]] > 0:
                lose -= 12.5 - card2num[t[0]]
        else:
            if card2num[t[0]] < 12:
                lose -= 12 - card2num[t[0]]
    if len(t) == 2:
        if after.count(t[0]) > 0:
            lose -= 20
    return lose


def is_end(op1, op2):  # 判断是否到达了双方都只有单双张的残局
    end = True
    for i in op1:
        if len(i) > 2:
            end = False
            return end
    for i in op2:
        if len(i) > 2:
            end = False
            return end
    return end


def is_sol_end(op):  # 判断一方是否只剩单双张
    for i in op:
        if len(i) > 2:
            return False
    else:
        return True
