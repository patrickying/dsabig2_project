'''
使用方法
如下import main.py程序
将玩家新建为main.py中定义的PlayerInterface类型的对象
使用PlayerInterface类的方法newGame、play即可运行
play与newGame的定义与ppt所示相同
默认输入时'A'、'10'、'J'、'Q'、'K'代表卡牌A、10、J、Q、K
'''
import main
import time
fi = main.PlayerInterface()
fi.newGame(['Q', 'J', '8', '8', '7', '7', '6', '6' ,'3'],['2' ,'A' ,'A' ,'10' ,'10' ,'9' ,'6' ,'5'],'enemy')
staT = time.time()
print(fi.play([]))
fi.ack(['6', '6', '7', '7', '8', '8'])
print('First Time Use {}ms'.format((time.time()-staT)*1000))
print(fi.play([]))
fi.ack(['3'])
print(fi.play(['5']))
fi.ack(['Q'])
print(fi.play(['2']))
fi.ack([])
print(fi.play(['10','10']))
fi.ack([])
print(fi.play(['A','A']))
fi.ack([])
print(fi.play(['6']))
fi.ack(['J'])