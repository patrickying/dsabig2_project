本项目为北京大学2019-2020学年春季学期环境科学与工程学院《数据结构与算法（B）》课程大作业，主要功能为1v1两人明牌斗地主的智能出牌程序
程序名称（队名）为 DeltaGo，由叶刘杭、刘时健、王嘉露、田睿轩共同完成

本项目包括了3份文件（'DeltaGo.py','MCST.py','suijichupai.py'）,使用时务必将3份文件放在一个目录下。
其中 DeltaGo.py 是由原 team1 文件改动得到的，即运行的时候作为 attacker 或 defender 引用的文件。

本项目采用Python3编写，调用了包括 treelib，numpy 等后期下载的库和 itertools，re，copy，time，math，sym，random 等预装库，核心采用蒙特卡洛树搜索算法

程序运行方式：
big2.py -a \<attacker\> -d \<defender\> -g \<game\>
attacker是先手方的代码项目名，defender是后手方的代码项目名，game是裁判员的发牌序号
其中 attacker 和 defender 用 DeltaGo 代替即可运行智能出牌程序 DeltaGo