import os


folder = ['王子豪.','叶刘杭.','刘成武/','吕韪帆/']
file = ['王子豪_Team5','DeltaGo','main','吕韪帆_TeamEnvironMen']

for att in range(len(folder[:2])):
    for de in range(len(folder[:2])):
        if att != de:
            os.system("python big2.py -a %s -d %s -g %s" % ('student.'+ folder[att]+file[att],'student.'+ folder[de]+file[de],1))