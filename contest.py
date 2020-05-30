import os
import multiprocessing

folder = ['王子豪.','刘成武.','吕韪帆.','张可尔.','张景淇.','杜鹏举.','林逸晴.','苑博.','曹义彬.','谭淞宸.','叶刘杭.']
file = ['王子豪_Team5','main','吕韪帆_TeamEnvironMen','张可尔_alphapoker','张景淇and毛子宸队','Du','myTeam','苑博_team-yuan-jiang',\
        '曹义彬_大作业','谭淞宸_awesome','DeltaGo']

def PK(command):
    os.system(command)

for att in range(len(folder)):
    for de in range(len(folder)):
        if att != de and de != 5 and att != 5:
            for gameing in range(11):
                command = "python big2.py -a %s -d %s -g %s" % ('student.'+ folder[att]+file[att],'student.'+ folder[de]+file[de],gameing)
                # pool = multiprocessing.Pool(processes=4)
                PK(command)
                # os.system("python big2.py -a %s -d %s -g %s" % ('student.'+ folder[att]+file[att],'student.'+ folder[de]+file[de],1))
# command = "python big2.py -a %s -d %s -g %s" % ('student.'+ folder[0]+file[0],'student.'+ folder[5]+file[5],1)
# PK(command)