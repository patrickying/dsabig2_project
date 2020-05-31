import os
import multiprocessing

folder = ['王子豪.','刘成武.','吕韪帆.','张可尔.','张景淇.','杜鹏举.','林逸晴.','苑博.','曹义彬.','谭淞宸.','叶刘杭.']
file = ['王子豪_Team5','main','吕韪帆_TeamEnvironMen','张可尔_alphapoker','张景淇and毛子宸队','Du','myTeam','苑博_team-yuan-jiang',\
        '曹义彬_大作业','谭淞宸_awesome','DeltaGo']

def PK(command):
    os.system(command)

if __name__ == "__main__":
    for att in range(2,len(folder)):
        for de in range(len(folder)):
            if att != de and  (att == 6 or de == 6):
                for gameing in range(6,11,5):
                    # command = "python big2.py -a %s -d %s -g %s" % ('student.'+ folder[att]+file[att],'student.'+ folder[de]+file[de],gameing)
                    command_list = []
                    for game in range(gameing,gameing+5):
                        command = "python big2.py -a %s -d %s -g %s" % (
                        'student.' + folder[att] + file[att], 'student.' + folder[de] + file[de], game)
                        command_list.append(command)
                    pool = multiprocessing.Pool(processes=5)
                    pool.map(PK, command_list)
