import numpy as np

#神经网络
class Net():
	def __init__(self):
		D=np.load('student/张景淇/net.npz')
		k=0
		self.w1w=[0]*4
		self.w1b=[0]*4
		self.w2w=[0]*4
		self.w2b=[0]*4
		for i in range(4):
			self.w1w[i]=D['arr_'+str(k)]
			k+=1
			self.w1b[i]=D['arr_'+str(k)]
			k+=1
			self.w2w[i]=D['arr_'+str(k)]
			k+=1
			self.w2b[i]=D['arr_'+str(k)]
			k+=1
		self.head_w=D['arr_16']
		self.head_b=D['arr_17']
	def cal_point(self,x):
		t=np.array(x/4)
		for i in range(4):
			y=np.matmul(t,self.w1w[i])+self.w1b[i]
			y=np.maximum(0,y)
			y=np.matmul(y,self.w2w[i])+self.w2b[i]
			t=np.maximum(0,t+y)
		t=np.matmul(t,self.head_w)+self.head_b
		return t

#判断手牌是否连续
def check_continuity(hand,start,end,num):
	for i in range(start,end):
		if hand[i]<num:
			return -i
	return True

#排列组合生成器
def combinations(iterable, r):
	n=len(iterable)
	if r > n:
		return
	indices = list(range(r))
	yield [iterable[i] for i in indices]
	while True:
		for i in range(r-1,-1,-1):
			if indices[i] != i + n - r:
				break
		else:
			return
		indices[i] += 1
		for j in range(i+1, r):
			indices[j] = indices[j-1] + 1
		yield [iterable[i] for i in indices]

#获取所有排列组合
def get_all_comb(hand,new_result,num):
	result=[]
	tem_list=[]
	three_num=0
	for x in range(13):
		if new_result[x]==0 and hand[x]>=num:
			tem_list.append(x)
		elif new_result[x]==3:
			three_num+=1
	a=list(combinations(tem_list,three_num))
	for x in a:
		new_result2=new_result.copy()
		for y in x:
			new_result2[y]=num
		result.append(new_result2)
	return result

#获取所有顺子
def get_all_straight(hand,type_c):
	minlen=5 if type_c==1 else 2
	result=[]
	if hand[12]>=type_c and hand[0]>=type_c:
		add_A=(hand[11]>=type_c)
		if add_A and type_c==1:
			if hand[1] and hand[2]:
				new_result=np.zeros(13,dtype=int)
				new_result[12]=1
				new_result[11]=1
				for i in range(3):
					new_result[i]=1
				result.append(new_result)
		if check_continuity(hand,1,minlen-1,type_c)==True:
			point=3 if type_c==1 else 0
			while point<11:
				if hand[point]>=type_c:
					new_result=np.zeros(13,dtype=int)
					new_result[12]=type_c
					for j in range(point+1):
						new_result[j]=type_c
					result.append(new_result)
					if type_c==3:
						result+=get_all_comb(hand,new_result,1)
						result+=get_all_comb(hand,new_result,2)
					if add_A and point!=10:
						new_result2=new_result.copy()
						new_result2[11]=type_c
						result.append(new_result2)
						if type_c==3:
							result+=get_all_comb(hand,new_result2,1)
							result+=get_all_comb(hand,new_result2,2)
				else:
					break
				point+=1
	i=0
	while i<14-minlen:
		ex=check_continuity(hand,i,i+minlen,type_c)
		if ex==True:
			max_c=(not i==0)+12
			for k in range(i+minlen-1,max_c):
				if hand[k]>=type_c:
					new_result=np.zeros(13,dtype=int)
					for j in range(i,k+1):
						new_result[j]=type_c
					result.append(new_result)
					if type_c==3:
						result+=get_all_comb(hand,new_result,1)
						result+=get_all_comb(hand,new_result,2)
				else:
					for j in range(i+1,k-minlen+1):
						for x in range(j+minlen,k+1):
							new_result=np.zeros(13,dtype=int)
							for y in range(j,x):
								new_result[y]=type_c
							result.append(new_result)
							if type_c==3:
								result+=get_all_comb(hand,new_result,1)
								result+=get_all_comb(hand,new_result,2)
					i=k
					break
		else:
			i=-ex
		i+=1
	return result

#获取所有合适牌型
def get_feasible_cards(hand,rival):
	if len(hand)!=13 or len(rival)!=13:
		print("error argv")
		return
	result=[np.zeros(13,dtype=int)]
	if 4 in rival:
		for i in range(rival.index(4)+1,13):
			if hand[i]==4:
				new_result=np.zeros(13,dtype=int)
				new_result[i]=4
				result.append(new_result)
		return result
	else:
		for i in range(13):
			if hand[i]==4:
				new_result=np.zeros(13,dtype=int)
				new_result[i]=4
				result.append(new_result)
	sum_c=sum(rival)
	if sum(hand)<sum_c:
		return result
	if sum_c==0:
		del result[0]
		for i in range(13):
			for j in range(1,min(hand[i]+1,4)):
				new_result=np.zeros(13,dtype=int)
				new_result[i]=j
				result.append(new_result)
		for i in range(13):
			if hand[i]>=3:
				for j in range(13):
					if hand[j] and i!=j:
						new_result=np.zeros(13,dtype=int)
						new_result[i]=3
						new_result[j]=1
						result.append(new_result)
						if hand[j]>1:
							new_result=np.zeros(13,dtype=int)
							new_result[i]=3
							new_result[j]=2
							result.append(new_result)
		for i in range(1,4):
			result+=get_all_straight(hand,i)
	elif sum_c<4:
		for i in range(rival.index(sum_c)+1,13):
			if hand[i]>=sum_c:
				new_result=np.zeros(13,dtype=int)
				new_result[i]=sum_c
				result.append(new_result)
	else:
		one=rival.count(1)
		two=rival.count(2)
		three=rival.count(3)
		if three!=1:
			three_type=0
			if three>1:
				num=3
				main_num=three
				if one:
					three_type=1
				elif two:
					three_type=2
			elif one:
				num=1
				main_num=one
			else:
				num=2
				main_num=two
			tem=0
			if rival[12]==num:
				if rival[11]==num:
					if rival[0]==0:
						return result
					if hand[12]>=num:
						if check_continuity(hand,0,main_num-1,num)==True:
							new_result=np.zeros(13,dtype=int)
							new_result[12]=num
							for i in range(main_num-1):
								new_result[i]=num
							if three_type!=0:
								result+=get_all_comb(hand,new_result,three_type)
							else:
								result.append(new_result)
			else:
				tem=rival.index(num)+1
			while tem<(14-main_num) :
				if hand[tem]>=num:
					ex=check_continuity(hand,tem,tem+main_num,num)
					if ex==True:
						new_result=np.zeros(13,dtype=int)
						for i in range(tem,tem+main_num):
							new_result[i]=num
						if three_type!=0:
							result+=get_all_comb(hand,new_result,three_type)
						else:
							result.append(new_result)
					else:
						tem=-ex

				tem+=1
		else:
			for i in range(rival.index(3)+1,13):
				if hand[i]>=3:
					tem=(two==1)+1
					for j in range(13):
						if hand[j]>=tem and i!=j:
							new_result=np.zeros(13,dtype=int)
							new_result[i]=3
							new_result[j]=tem
							result.append(new_result)

	return result

#从所有合适牌型中提取最佳牌型
def get_best_cards(net,hand1,hand2,result):
	maxpoint=-10000
	maxi=0
	for i in range(len(result)):
		input_=np.concatenate((result[i],hand1,hand2),axis=0)
		a=net.cal_point(input_)[0]
		if maxpoint<a:
			maxi=i
			maxpoint=a
	return result[maxi],maxpoint


def choosePlayer(teamName):
	new_module = __import__(teamName) 
	return new_module.Player()


class Player:
	def __init__(self):
		self.name="张景淇and毛子宸队"
		self.card_dict={'3':0,'4':1,'5':2,'6':3,'7':4,'8':5,'9':6,'10':7,'J':8,'Q':9,'K':10,'A':11,'2':12}
		self.card_keys=list(self.card_dict.keys())
		self.net=Net()

	#将牌转换成一个记录每种牌有几张的数组，此数组长度固定为13
	def cards_to_list(self,cards):
		result=np.zeros(13,dtype=int)
		for i in cards:
			if i in self.card_keys:
				result[self.card_dict[i]]+=1
			else:
				return False
		return result
	def list_to_cards(self,lis):
		result=[]
		for i in range(13):
			for j in range(lis[i]):
				result.append(self.card_keys[i])
		return result

	def newGame(self, hand1, hand2, opponent):
		"""
		  hand1: 自己手里的牌，比如：['A', 'A', '2', '2']，字母大写
		  hand2: 对方手里的牌
		  opponent: 对手名称
		"""
		self.hand1=self.cards_to_list(hand1)
		self.hand2=self.cards_to_list(hand2)
		self.opponent=opponent

	def play(self, t):
		"""
		  t: 对手出的牌, []表示自己先手或者对方pass
		  return: 自己出的牌，需要能压住t
		"""
		rival=self.cards_to_list(t)
		self.hand2=self.hand2-rival
		result=get_feasible_cards(self.hand1,rival.tolist())
		rival_,unknow=get_best_cards(self.net,self.hand1,self.hand2,result)
		return self.list_to_cards(rival_)

	def ack(self, t):
		"""
		  t: 裁判确认的有效出牌
	
		"""
		self.hand1=self.hand1-self.cards_to_list(t)
	def teamName(self):
		return self.name
