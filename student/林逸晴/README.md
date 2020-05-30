# dsabig2
课程大作业框架代码

实现了主程序big2.py、裁判员dealer.py、只知道出单张牌的Team1.py、人工出牌Team2.py
裁判员现在只存了两幅牌。

程序运行方式：
big2.py -a \<attacker\> -d \<defender\> -g \<game\>
attacker是先手方的代码，defender是后手方的代码，game是裁判员的发牌序号

比如：
python3 big2.py -a Team1 -d Team2 -g 1
就是用第1副牌（前面还有第0副牌），让Team1和Team2打比赛。
