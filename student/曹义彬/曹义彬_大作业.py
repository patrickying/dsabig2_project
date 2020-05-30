# -*- coding: utf-8 -*-
"""
Created on Tue May 12 10:16:00 2020

@author: 刘潞
"""

Card_dict = dict(zip([x for x in '3456789'] + ['10'] + [x for x in 'JQKA2'] + [x for x in range(3, 16)], \
                     [x for x in range(3, 16)] + [x for x in '3456789'] + ['10'] + [x for x in
                                                                                    'JQKA2']))  # 牌的字符对应的data中的位置，位置对应的字符也要加进去，例：A:14,14:A都要在字典中


class HandCardData:
    def __init__(self):
        self.data = [0 for _ in range(16)]  # 记录现有的牌的数据

        self.size = 0  # 记录当前手牌数目

    def addCard(self, CardList):
        self.size += len(CardList)
        for card in CardList:
            self.data[Card_dict[card]] += 1

    def remove(self, CardList):
        self.size -= len(CardList)
        for card in CardList:
            self.data[Card_dict[card]] -= 1

    def ListType(self):  # 列表形式表示手牌
        return [Card_dict[i] for i in range(3, 16) for _ in range(self.data[i])]

    def outRange(self, opp):
        tmp_list = []
        if if_ahandCard(opp) == 'SINGLE':
            opp_start = Card_dict[opp[0]]
            while opp_start <= 14:
                opp_start += 1
                if self.data[opp_start] >= 1 and self.data[opp_start] != 4:
                    tmp_list.append([Card_dict[opp_start]])
            for i in range(3, 16):
                if self.data[i] == 4:
                    tmp_list.append([Card_dict[i]] * 4)
        if if_ahandCard(opp) == 'THREE':
            opp_start = Card_dict[opp[0]]
            while opp_start <= 14:
                opp_start += 1
                if self.data[opp_start] == 3:
                    tmp_list.append([Card_dict[opp_start]] * 3)
            for i in range(3, 16):
                if self.data[i] == 4:
                    tmp_list.append([Card_dict[i]] * 4)
        if if_ahandCard(opp) == 'DOUBLE':
            opp_start = Card_dict[opp[0]]
            while opp_start <= 14:
                opp_start += 1
                if self.data[opp_start] >= 2 and self.data[opp_start] != 4:
                    tmp_list.append([Card_dict[opp_start]] * 2)
            for i in range(3, 16):
                if self.data[i] == 4:
                    tmp_list.append([Card_dict[i]] * 4)
        if if_ahandCard(opp) == 'THREE_TAKE_ONE':
            tmp_data = [0 for _ in range(16)]
            for card in opp:
                tmp_data[Card_dict[card]] += 1
            opp_start = tmp_data.index(3)
            while opp_start <= 14:
                opp_start += 1
                if self.data[opp_start] == 3:
                    tmp_Value = 0
                    tmp_Round = float('inf')
                    tmp_taken = 0
                    for i in range(3, 16):
                        if i != opp_start and self.data[i] != 0 and self.data[i] != 4:
                            tmp_HandCard = HandCardData()
                            tmp_HandCard.addCard(self.ListType())
                            tmp_HandCard.remove([Card_dict[i]] + [Card_dict[opp_start]] * 3)
                            num = NeedRound_and_TotalValue(tmp_HandCard)
                            if num[0] < tmp_Round:
                                tmp_Round = num[0]
                                tmp_taken = i
                                tmp_Value = num[1]
                            elif NeedRound_and_TotalValue(tmp_HandCard)[1] > tmp_Value:
                                tmp_Round = num[0]
                                tmp_taken = i
                                tmp_Value = num[1]
                            else:
                                pass
                    if tmp_taken != 0:
                        tmp_list.append([Card_dict[opp_start]] * 3 + [Card_dict[tmp_taken]])
            for i in range(3, 16):
                if self.data[i] == 4:
                    tmp_list.append([Card_dict[i]] * 4)
        if if_ahandCard(opp) == 'THREE_TAKE_DOUBLE':
            tmp_data = [0 for _ in range(16)]
            for card in opp:
                tmp_data[Card_dict[card]] += 1
            opp_start = tmp_data.index(3)
            while opp_start <= 14:
                opp_start += 1
                if self.data[opp_start] == 3:
                    tmp_Value = 0
                    tmp_Round = float('inf')
                    tmp_taken = 0
                    for i in range(3, 16):
                        if i != opp_start and self.data[i] >= 2 and self.data[i] != 4:
                            tmp_HandCard = HandCardData()
                            tmp_HandCard.addCard(self.ListType())
                            tmp_HandCard.remove([Card_dict[i]] * 2 + [Card_dict[opp_start]] * 3)
                            num = NeedRound_and_TotalValue(tmp_HandCard)
                            if num[0] < tmp_Round:
                                tmp_Round = num[0]
                                tmp_taken = i
                                tmp_Value = num[1]
                            elif NeedRound_and_TotalValue(tmp_HandCard)[1] > tmp_Value:
                                tmp_Round = num[0]
                                tmp_taken = i
                                tmp_Value = num[1]
                            else:
                                pass
                    if tmp_taken != 0:
                        tmp_list.append([Card_dict[opp_start]] * 3 + [Card_dict[tmp_taken]] * 2)
            for i in range(3, 16):
                if self.data[i] == 4:
                    tmp_list.append([Card_dict[i]] * 4)
        if if_ahandCard(opp) == 'BOMB':
            opp_start = Card_dict[opp[0]]
            while opp_start <= 14:
                opp_start += 1
                if self.data[opp_start] >= 4:
                    tmp_list.append([Card_dict[opp_start]] * 4)

        if if_ahandCard(opp) == 'DOUBLE_LINE':
            tmp_data = [0 for _ in range(16)]
            for card in opp:
                tmp_data[Card_dict[card]] += 1
            if tmp_data[3] == 2:
                for card in opp:
                    if card == 'A':
                        tmp_data[1] += 1
                        tmp_data[14] -= 1
                    if card == '2':
                        tmp_data[2] += 1
                        tmp_data[15] -= 1
            opp_len = len(set(opp))
            opp_start = tmp_data.index(2)
            while opp_start <= 15 - opp_len:
                opp_start += 1
                symbol = 1
                for i in range(opp_len):
                    if self.data[opp_start + i] < 2:
                        symbol = 0
                if symbol == 1:
                    tmp_list.append([Card_dict[opp_start + i] for i in range(opp_len)] * 2)
            for i in range(3, 16):
                if self.data[i] == 4:
                    tmp_list.append([Card_dict[i]] * 4)
        if if_ahandCard(opp) == 'LINE':
            tmp_data = [0 for _ in range(16)]
            for card in opp:
                tmp_data[Card_dict[card]] += 1
            if tmp_data[3] == 1:
                for card in opp:
                    if card == 'A':
                        tmp_data[1] += 1
                        tmp_data[14] -= 1
                    if card == '2':
                        tmp_data[2] += 1
                        tmp_data[15] -= 1
            opp_len = len(set(opp))
            opp_start = tmp_data.index(1)
            while opp_start <= 15 - opp_len:
                opp_start += 1
                symbol = 1
                for i in range(opp_len):
                    if self.data[opp_start + i] < 1:
                        symbol = 0
                if symbol == 1:
                    tmp_list.append([Card_dict[opp_start + i] for i in range(opp_len)])
            for i in range(3, 16):
                if self.data[i] == 4:
                    tmp_list.append([Card_dict[i]] * 4)
        if if_ahandCard(opp) == 'THREE_LINE':
            tmp_data = [0 for _ in range(16)]
            TakeChance = 0
            S_or_D = 0  # 记录带的是单还是双，1是双，0是单
            for card in opp:
                tmp_data[Card_dict[card]] += 1

            if tmp_data[3] == 3:
                for card in opp:
                    if card == 'A':
                        tmp_data[1] += 1
                        tmp_data[14] -= 1
                    if card == '2':
                        tmp_data[2] += 1
                        tmp_data[15] -= 1
            if 2 in tmp_data:
                S_or_D = 2
                TakeChance = tmp_data.count(2)
            elif 1 in tmp_data:
                S_or_D = 1
                TakeChance = tmp_data.count(1)
            else:
                pass
            tmp_data = [3 if i == 3 else 0 for i in tmp_data]
            opp_len = tmp_data.count(3)
            opp_start = tmp_data.index(3)
            while opp_start <= 15 - opp_len:
                opp_start += 1
                symbol = 1
                for i in range(opp_len):
                    if self.data[opp_start + i] < 3:
                        symbol = 0
                if symbol == 1:
                    if S_or_D == 0:
                        tmp_list.append([Card_dict[opp_start + i] for i in range(opp_len)] * 3)
                    else:
                        self.remove([Card_dict[opp_start + i] for i in range(opp_len)] * 3)
                        tmp_record = []
                        if _count(self.data, S_or_D) >= TakeChance:
                            while TakeChance >= 1:
                                tmp_Value = 0
                                tmp_Round = float('inf')
                                tmp_taken = 0
                                for i in range(3, 16):
                                    if i != opp_start and self.data[i] >= S_or_D and self.data[i] != 4:
                                        tmp_HandCard = HandCardData()
                                        tmp_HandCard.addCard(self.ListType())
                                        tmp_HandCard.remove([Card_dict[i]] * S_or_D)
                                        num = NeedRound_and_TotalValue(tmp_HandCard)
                                        if num[0] < tmp_Round:
                                            tmp_Round = num[0]
                                            tmp_taken = i
                                            tmp_Value = num[1]
                                        elif NeedRound_and_TotalValue(tmp_HandCard)[1] > tmp_Value:
                                            tmp_Round = num[0]
                                            tmp_taken = i
                                            tmp_Value = num[1]
                                        else:
                                            pass
                                if tmp_taken != 0:
                                    tmp_record += [Card_dict[tmp_taken]] * S_or_D
                                    self.remove([Card_dict[tmp_taken] for _ in range(S_or_D)])
                                TakeChance -= 1
                            tmp_list.append([Card_dict[opp_start + i] for i in range(opp_len)] * 3 + tmp_record)
                        self.addCard([Card_dict[opp_start + i] for i in range(opp_len)] * 3 + tmp_record)

            for i in range(3, 16):
                if self.data[i] == 4:
                    tmp_list.append([Card_dict[i]] * 4)
        return tmp_list


def if_ahandCard(CardList):  # 判断当前牌能否一手打出，如果可以打出就返回这种牌的类型，不能打出就返回False
    if len(CardList) == 1:  # 判断单牌
        return 'SINGLE'
    if len(CardList) == 2:
        if CardList[0] == CardList[1]:  # 判断对子
            return 'DOUBLE'
    if len(CardList) == 3:  # 判断三同
        if CardList[0] == CardList[1] and CardList[1] == CardList[2]:
            return 'THREE'
    if len(CardList) == 4:  # 判断三带一
        tmp_data = [0 for _ in range(16)]
        for card in CardList:
            tmp_data[Card_dict[card]] += 1
        for i in tmp_data:
            if i == 3:
                return 'THREE_TAKE_ONE'
    if len(CardList) == 4:
        tmp_data = [0 for _ in range(16)]
        for card in CardList:
            tmp_data[Card_dict[card]] += 1
        for i in tmp_data:
            if i == 4:
                return 'BOMB'
    if len(CardList) == 5:  # 判断三带二
        tmp_data = [0 for _ in range(16)]
        for card in CardList:
            tmp_data[Card_dict[card]] += 1
        if 3 in tmp_data and 2 in tmp_data:
            return 'THREE_TAKE_DOUBLE'
    if len(CardList) >= 4:  # 判断双连
        tmp_data = [0 for _ in range(16)]
        for card in CardList:
            tmp_data[Card_dict[card]] += 1
        if tmp_data[3] == 2:
            for card in CardList:
                if card == 'A':
                    tmp_data[1] += 1
                    tmp_data[14] -= 1
                if card == '2':
                    tmp_data[2] += 1
                    tmp_data[15] -= 1
        if wh_continous(tmp_data, 2):
            return 'DOUBLE_LINE'
    if len(CardList) >= 5:  # 判断顺子
        tmp_data = [0 for _ in range(16)]
        for card in CardList:
            tmp_data[Card_dict[card]] += 1
        if tmp_data[3] == 1:
            for card in CardList:
                if card == 'A':
                    tmp_data[1] += 1
                    tmp_data[14] -= 1
                if card == '2':
                    tmp_data[2] += 1
                    tmp_data[15] -= 1
        if wh_continous(tmp_data, 1):
            return 'LINE'
    if len(CardList) >= 6:  # 判断三连
        tmp_data = [0 for _ in range(16)]
        for card in CardList:
            tmp_data[Card_dict[card]] += 1
        if tmp_data[3] == 3:
            for card in CardList:
                if card == 'A':
                    tmp_data[1] += 1
                    tmp_data[14] -= 1
                if card == '2':
                    tmp_data[2] += 1
                    tmp_data[15] -= 1

        if wh_continous(tmp_data, 3):
            return 'THREE_LINE'
    if len(CardList) >= 8:  # 判断三连
        tmp_data = [0 for _ in range(16)]
        for card in CardList:
            tmp_data[Card_dict[card]] += 1
        if tmp_data[3] == 3:
            for card in CardList:
                if card == 'A':
                    tmp_data[1] += 1
                    tmp_data[14] -= 1
                if card == '2':
                    tmp_data[2] += 1
                    tmp_data[15] -= 1
        if 2 in tmp_data and 1 not in tmp_data and 4 not in tmp_data:
            Maybe_round = tmp_data.count(2)
            tmp_data = [3 if i == 3 else 0 for i in tmp_data]
            if wh_continous(tmp_data, 3) and wh_continous(tmp_data, 3) == Maybe_round:
                return 'THREE_LINE'
        if 1 in tmp_data and 2 not in tmp_data and 4 not in tmp_data:
            Maybe_round = tmp_data.count(1)
            tmp_data = [3 if i == 3 else 0 for i in tmp_data]
            if wh_continous(tmp_data, 3) and wh_continous(tmp_data, 3) == Maybe_round:
                return 'THREE_LINE'

    return False


def wh_continous(tmp_data, i):  # 判断是否从某一位置开始都是i张的连续牌,且返回总共有多少连牌
    index = 0
    for j in range(len(tmp_data)):
        if tmp_data[j] != 0:
            index = j
            break
    Totalround = 0
    symbol = 1
    for j in range(index, len(tmp_data)):
        if symbol == 0 and tmp_data[j] != 0:
            return False
        if symbol == 1 and tmp_data[j] == 0:
            symbol = 0
        if symbol == 1 and tmp_data[j] != i:
            return False
        if symbol == 1 and tmp_data[j] == i:
            Totalround += 1
            continue
        if symbol == 1 and tmp_data[j] == 0:
            symbol = 0
    return Totalround


def define_Value(CardList):  # 判断价值，连牌只能比较牌数一样的，炸弹大于其他所有类型
    if if_ahandCard(CardList):
        tmp_data = [0 for _ in range(16)]
        for card in CardList:
            tmp_data[Card_dict[card]] += 1
        if if_ahandCard(CardList) != 'BOMB':
            if if_ahandCard(CardList) in ['LINE', 'DOUBLE_LINE']:
                if '3' in CardList:
                    for card in CardList:
                        if card == 'A':
                            tmp_data[1] += 1
                            tmp_data[14] -= 1
                        if card == '2':
                            tmp_data[2] += 1
                            tmp_data[15] -= 1
            if if_ahandCard(CardList) == 'THREE_LINE':
                if tmp_data[3] == 3:
                    for card in CardList:
                        if card == 'A':
                            tmp_data[1] += 1
                            tmp_data[14] -= 1
                        if card == '2':
                            tmp_data[2] += 1
                            tmp_data[15] -= 1
            if if_ahandCard(CardList) == 'THREE_LINE' or if_ahandCard(CardList) == 'THREE_TAKE_ONE' or \
                    if_ahandCard(CardList) == 'THREE_TAKE_DOUBLE':
                tmp_data = [3 if i == 3 else 0 for i in tmp_data]
            for j in range(len(tmp_data) - 1, 0, -1):
                if tmp_data[j] == 1:
                    return j
                elif tmp_data[j] == 2:
                    return j + 15
                elif tmp_data[j] == 3:
                    return j + 30
        else:
            for i in range(3, 16):
                if tmp_data[i] == 4:
                    return i + 45


def NeedRound_and_TotalValue(HandCardType):
    if len(HandCardType.ListType()) == 0:
        return (0, 0)
    else:
        Now_card = _TotalHand(HandCardType)[0]
        tmp_card = HandCardData()
        tmp_card.addCard(HandCardType.ListType())
        tmp_card.remove(Now_card)
        return [NeedRound_and_TotalValue(tmp_card)[0] + 1,
                NeedRound_and_TotalValue(tmp_card)[1] + define_Value(Now_card)]


def _count(tmp_data, chance):  # 计算列表中大于chance的个数，必要的话可以选择不计算炸弹进去
    count = 0
    for i in range(len(tmp_data)):
        if tmp_data[i] >= chance and tmp_data[i] != 4:
            count += 1
    return count


def count_(tmp_data, chance):
    count = 0
    for i in range(len(tmp_data)):
        if tmp_data[i] == chance and tmp_data[i] != 4:
            count += 1
    return count


# 这个牌对面出了会不会变成一手
def getBestHand(our_Card, opp_Card, opp):
    # 记得把对手的手牌减掉他出的牌，我们的手牌也要减掉我们的牌
    # return 出牌的列表
    # （1）先手出牌：出数量最大的，价值最小的，三带的情况，优先带对子，在不破坏顺子和三连的情况下，出尽量小的单张 ；（1人做1、2部分） （2）对面有出牌的时候，我们做出的回应：利用outrange选一个价值最小的（三连的情况你们要自己判断，三连我只能给三连的牌，不能给单张的）
    # （3）特殊情况：（ 2人做）
    ourcard, oppcard, oppcard_, count, value, card_ = HandCardData(), HandCardData(), HandCardData(), 0, 100, []
    ourcard.addCard(our_Card)
    oppcard.addCard(opp_Card)
    oppcard_.addCard(opp_Card)
    if opp == []:
        legalcard = TotalHand(ourcard)
        for card in legalcard:
            count = 0
            if oppcard.outRange(card) == [] and if_ahandCard(card) != 'BOMB' and define_Value([card[0]]) <= 10:
                return card
            elif if_ahandCard(card) == 'BOMB':
                if if_ahandCard(opp_Card) != False or if_ahandCard(our_Card) != False:
                    return card
            else:
                for CD in oppcard.outRange(card):
                    oppcard_.remove(CD)
                    if if_ahandCard(oppcard_.ListType()) == False and oppcard_.ListType() != []:
                        oppcard_.addCard(CD)
                        continue
                    else:
                        oppcard_.addCard(CD)
                        count += 1
                if count != 0:
                    pass
                else:
                    ourcard.remove(card)
                    if define_Value([card[0]]) <= 11 or if_ahandCard(ourcard.ListType()) != False:
                        ourcard.addCard(card)
                        return card
                    else:
                        ourcard.addCard(card)
        for card_ in legalcard:
            if oppcard.outRange(card_) == [] and if_ahandCard(card_) != 'BOMB':
                return card_
        return legalcard[0]
    elif opp != []:
        if ourcard.outRange(opp) == []:
            return []
        elif if_ahandCard(opp_Card) == False:
            tmp_Round = float('inf')
            tmp_taken = 0
            for card in ourcard.outRange(opp):
                tmp_HandCard = HandCardData()
                tmp_HandCard.addCard(ourcard.ListType())
                tmp_HandCard.remove(card)
                num = NeedRound_and_TotalValue(tmp_HandCard)
                if num[0] < tmp_Round:
                    tmp_Round = num[0]
                    tmp_taken = card
                else:
                    pass
            return tmp_taken
        else:
            return ourcard.outRange(opp)[-1]


def TotalHand_(our_Card):
    result, card = [], []
    for i in range(3, len(our_Card.data)):
        if i != len(our_Card.data) - 1 and our_Card.data[i] == 3 and our_Card.data[
            i + 1] == 3:  # 如果有连续两个三个的就能构成三顺 尚未考虑夹带的牌
            count = 0
            for j in range(i + 1, len(our_Card.data)):  # 计算有几个三个的相连
                if our_Card.data[j] == 3:
                    count += 1
                else:
                    break
            for k in range(i, i + count + 1):  # 把所有三个相连的都写进去
                card = card + [Card_dict[k]] * 3
            result.append(card)  # 将这个三顺加入
            card = []
            # 三顺带东西
        if i <= len(our_Card.data) - 5 and our_Card.data[i] >= 1 and our_Card.data[
            i + 1] >= 1:  # 如果有连续两个的就去检测能否构成顺子，而且目前采取的是都拆开的方法
            count = 1
            for j in range(i + 1, len(our_Card.data)):  # 检测一下连续的有几个
                if our_Card.data[j] >= 1:
                    count += 1
                else:
                    break
            if count >= 5:  # 如果大于五个的话就可以构成顺子了
                for k in range(i, i + count):
                    card = card + [Card_dict[k]]
                result.append(card)
                card = []
            else:
                pass
        if i != len(our_Card.data) - 1 and our_Card.data[i] == 2 and our_Card.data[i + 1] == 2:  # 如果有连续两个的就可以构成双顺
            count = 1
            for j in range(i + 1, len(our_Card.data)):  # 测试一下一共有几个连续的对子
                if our_Card.data[j] == 2:
                    count += 1
                else:
                    break
            for k in range(i, i + count):  # 组成出牌
                card = card + [Card_dict[k]] * 2
            result.append(card)
            card = []
        if our_Card.data[i] == 3:  # 如果是三个的
            count = 0
            for j in range(0, len(our_Card.data)):  # 三代二的情况
                if our_Card.data[j] == 2:
                    card = [Card_dict[i]] * 3 + [Card_dict[j]] * 2
                    count += 1
                    break
            if count == 0:
                for k in range(0, len(our_Card.data)):  # 三代一的情况
                    if our_Card.data[k] == 1:
                        card = [Card_dict[i]] * 3 + [Card_dict[k]]
                        count += 1
                        break
            if count == 1:
                result.append(card)  # 把对方出的那张牌出出去
                card = []
            else:
                card = [Card_dict[i]] * 3
                result.append(card)  # 把对方出的那张牌出出去
                card = []
        if our_Card.data[i] == 2:  # 出对子
            card = [Card_dict[i]] * 2
            result.append(card)
            card = []
        if our_Card.data[i] == 1:  # 出单牌
            card = [Card_dict[i]]
            result.append(card)
            card = []
        if our_Card.data[i] == 0:
            pass
        if our_Card.data[i] == 4:
            card = [Card_dict[i]] * 4
            result.append(card)
            card = []
    exchanges = True
    passnum = len(result) - 1
    while passnum > 0 and exchanges:
        exchanges = False
        for i in range(passnum):
            if len(result[i]) < len(result[i + 1]):
                exchanges = True
                result[i], result[i + 1] = result[i + 1], result[i]
        passnum -= 1
    return result


def _TotalHand(our_Card):
    result, card = [], []
    for i in range(3, len(our_Card.data)):
        if i != len(our_Card.data) - 1 and our_Card.data[i] == 3 and our_Card.data[
            i + 1] == 3:  # 如果有连续两个三个的就能构成三顺 尚未考虑夹带的牌
            count = 0
            for j in range(i + 1, len(our_Card.data)):  # 计算有几个三个的相连
                if our_Card.data[j] == 3:
                    count += 1
                else:
                    break
            for k in range(i, i + count + 1):  # 把所有三个相连的都写进去
                card = card + [Card_dict[k]] * 3
            result.append(card)  # 将这个三顺加入
            card = []
            # 三顺带东西
        if i <= len(our_Card.data) - 5 and our_Card.data[i] >= 1 and our_Card.data[
            i + 1] >= 1:  # 如果有连续两个的就去检测能否构成顺子，而且目前采取的是都拆开的方法
            count = 1
            for j in range(i + 1, len(our_Card.data)):  # 检测一下连续的有几个
                if our_Card.data[j] >= 1:
                    count += 1
                else:
                    break
            if count >= 5:  # 如果大于五个的话就可以构成顺子了
                for k in range(i, i + count):
                    card = card + [Card_dict[k]]
                result.append(card)
                card = []
            else:
                pass
        if i != len(our_Card.data) - 1 and our_Card.data[i] == 2 and our_Card.data[i + 1] == 2:  # 如果有连续两个的就可以构成双顺
            count = 1
            for j in range(i + 1, len(our_Card.data)):  # 测试一下一共有几个连续的对子
                if our_Card.data[j] == 2:
                    count += 1
                else:
                    break
            for k in range(i, i + count):  # 组成出牌
                card = card + [Card_dict[k]] * 2
            result.append(card)
            card = []
        if our_Card.data[i] == 3:  # 如果是三个的
            card = [Card_dict[i]] * 3
            result.append(card)  # 把对方出的那张牌出出去
            card = []
        if our_Card.data[i] == 2:  # 出对子
            card = [Card_dict[i]] * 2
            result.append(card)
            card = []
        if our_Card.data[i] == 1:  # 出单牌
            card = [Card_dict[i]]
            result.append(card)
            card = []
        if our_Card.data[i] == 0:
            pass
        if our_Card.data[i] == 4:
            card = [Card_dict[i]] * 4
            result.append(card)
            card = []
    exchanges = True
    passnum = len(result) - 1
    while passnum > 0 and exchanges:
        exchanges = False
        for i in range(passnum):
            if len(result[i]) < len(result[i + 1]):
                exchanges = True
                result[i], result[i + 1] = result[i + 1], result[i]
        passnum -= 1
    return result


def TotalHand(our_Card):
    result, card, right, temp = [], [], 0, []
    for i in range(3, len(our_Card.data)):
        if i != len(our_Card.data) - 1 and our_Card.data[i] == 3 and our_Card.data[
            i + 1] == 3:  # 如果有连续两个三个的就能构成三顺 尚未考虑夹带的牌
            count = 0
            for j in range(i + 1, len(our_Card.data)):  # 计算有几个三个的相连
                if our_Card.data[j] == 3:
                    count += 1
                else:
                    break
            for k in range(i, i + count + 1):  # 把所有三个相连的都写进去
                card = card + [Card_dict[k]] * 3
            if count_(our_Card.data, 2) >= count + 1:
                for m in range(3, len(our_Card.data)):
                    if our_Card.data[m] == 2:
                        right += 1
                        card = card + [Card_dict[k]] * 2
                    if right == 2:
                        break
            if count_(our_Card.data, 1) >= count + 1 and right == 0:
                temp, lenth1 = card, 0
                for n in range(3, len(our_Card.data)):
                    if our_Card.data[n] == 1:
                        right += 1
                        temp = temp + [Card_dict[n]]
                    if right == 2:
                        lenth1 = len(TotalHand_(our_Card)[0])
                        our_Card.remove(temp)
                        if len(TotalHand_(our_Card)[0]) >= lenth1 - 2:
                            our_Card.addCard(temp)
                            card = temp
                            break
                        else:
                            our_Card.addCard(temp)
                            break
            result.append(card)  # 将这个三顺加入
            card = []
            # 三顺带东西
        if i <= len(our_Card.data) - 5 and our_Card.data[i] >= 1 and our_Card.data[
            i + 1] >= 1:  # 如果有连续两个的就去检测能否构成顺子，而且目前采取的是都拆开的方法
            count = 1
            for j in range(i + 1, len(our_Card.data)):  # 检测一下连续的有几个
                if our_Card.data[j] >= 1:
                    count += 1
                else:
                    break
            if count >= 5:  # 如果大于五个的话就可以构成顺子了
                for k in range(i, i + count):
                    card = card + [Card_dict[k]]
                result.append(card)
                card = []
            else:
                pass
        if i != len(our_Card.data) - 1 and our_Card.data[i] >= 2 and our_Card.data[i + 1] >= 2:  # 如果有连续两个的就可以构成双顺
            count = 1
            for j in range(i + 1, len(our_Card.data)):  # 测试一下一共有几个连续的对子
                if our_Card.data[j] >= 2:
                    count += 1
                else:
                    break
            for k in range(i, i + count):  # 组成出牌
                card = card + [Card_dict[k]] * 2
            result.append(card)
            card = []
        if our_Card.data[i] == 3:  # 如果是三个的
            tmp_list = []
            for j in range(3, 16):
                if j != i and our_Card.data[j] >= 2 and our_Card.data[j] != 4:
                    tmp_list.append([Card_dict[j]] * 2)
            for j in range(3, 16):
                if j != i and our_Card.data[j] >= 1 and our_Card.data[j] != 4:
                    tmp_list.append([Card_dict[j]])
                tmp_Value = 0
                tmp_Round = float('inf')
                tmp_taken = []
            for card in tmp_list:
                tmp_HandCard = HandCardData()
                tmp_HandCard.addCard(our_Card.ListType())
                tmp_HandCard.remove([Card_dict[i]] * 3 + card)
                num = NeedRound_and_TotalValue(tmp_HandCard)
                if num[0] < tmp_Round:
                    tmp_Round = num[0]
                    tmp_taken = card
                    tmp_Value = num[1]
                elif NeedRound_and_TotalValue(tmp_HandCard)[1] > tmp_Value:
                    tmp_Round = num[0]
                    tmp_taken = card
                    tmp_Value = num[1]
                else:
                    pass
            if tmp_taken == []:
                card = [Card_dict[i]] * 3
                result.append(card)  # 把对方出的那张牌出出去
                card = []
            else:
                card = [Card_dict[i]] * 3 + tmp_taken
                result.append(card)  # 把对方出的那张牌出出去
                card = []
        if our_Card.data[i] == 2:  # 出对子
            card = [Card_dict[i]] * 2
            result.append(card)
            card = []
        if our_Card.data[i] == 1:  # 出单牌
            card = [Card_dict[i]]
            result.append(card)
            card = []
        if our_Card.data[i] == 0:
            pass
        if our_Card.data[i] == 4:
            card = [Card_dict[i]] * 4
            result.append(card)
            card = []
    exchanges = True
    passnum = len(result) - 1
    while passnum > 0 and exchanges:
        exchanges = False
        for i in range(passnum):
            if len(result[i]) < len(result[i + 1]):
                exchanges = True
                result[i], result[i + 1] = result[i + 1], result[i]
        passnum -= 1
    return result


class Player:
    def __init__(self):
        self.name = "lbw"

    def newGame(self, hand1, hand2, opponent):
        self.myhand = hand1
        self.yourhand = hand2
        self.opponent = opponent
        pass

    def play(self, t):
        if t != []:
            for c in t:
                self.yourhand.remove(c)
        return getBestHand(self.myhand, self.yourhand, t)

    def ack(self, t):
        # print("ack: {}".format(self.myHand))
        for c in t:
            self.myhand.remove(c)
        pass

    def teamName(self):
        return self.name

