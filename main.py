#!/usr/bin/python

import sys
import random
import model

PlayerList = ['w1', 'w2', 'w3', 'w4', 'v1', 'v2', 'v3', 'v4', 'se', 'wi', 'gr', 'ht']
IdentityList = ['werewolf', 'werewolf', 'werewolf', 'werewolf', 'villager', 'villager', 'villager', 'villager', 'seer',
                'witch', 'guardian', 'hunter']
DeadList = []

class Player:

    def __init__(self, kn, name):
        self.kn = kn
        self.name = name
        self.falseorigin = [0] * 14

    def update(self, newset):
        self.kn = newset

    def changek(self, newk):
        # print(newk)
        self.kn, self.falseorigin = model.checkconflict(self.kn, newk, self.falseorigin)
        # print(self.falseorigin)

    def getName(self):
        return self.name

    def getTarget(self):
        return self.getName()

    def checkValidity(self, tocheck, checktype):
        for k in self.kn[tocheck]:
            belief, origin = k
            if belief == checktype and origin == 't':
                # print("if go")
                return True
        return False

class Villager(Player):

    def __init__(self, kn, name, rule, target):
        Player.__init__(self, kn, name)
        self.rule = rule
        self.target = target

    def chooseSpeech(self):
        playerAlive = PlayerList[:]
        for x in DeadList:
            # print(x)
            if x in playerAlive:
                playerAlive.remove(x)

        if 'se' in playerAlive:
            playerAlive.remove('se')
        if self.getName() in playerAlive:
            playerAlive.remove(self.getName())

        if self.rule == "naive":
            return IdentityList[PlayerList.index(self.getName())]

        if self.rule == "first":
            if random.random() > 0.5:
                return IdentityList[PlayerList.index(self.getName())]
            else:
                return 'not' + IdentityList[PlayerList.index(self.getName())]

        if self.rule == "second":
            if random.random() > 0.5:
                return 'knowing' + playerAlive[random.randrange(0, len(playerAlive))]
            else:
                return 'not knowing' + playerAlive[random.randrange(0, len(playerAlive))]

        if self.rule == "third":
            if random.random() > 0.5:
                return 'knowing' + playerAlive[random.randrange(0, len(playerAlive))] + 'knows' + IdentityList[PlayerList.index(self.getName())]
            else:
                return 'not knowing' + playerAlive[random.randrange(0, len(playerAlive))] + 'knows' + IdentityList[PlayerList.index(self.getName())]

    def villagervote(self):
        if self.rule == "naive":
            card = 0
            while True:
                card = random.randrange(0, len(PlayerList))
                if PlayerList[card] not in DeadList and PlayerList[card] != self.getName() and IdentityList[card] != 'seer':
                    break
            return card

        else:
            falseO = self.falseorigin[2:]
            playerAlive = PlayerList[:]
            for x in DeadList:
                # print(x)
                if x in playerAlive:
                    i = playerAlive.index(x)
                    del falseO[i]
                    del playerAlive[i]
            # print(playerAlive)

            return PlayerList.index(playerAlive[falseO.index(max(falseO))])

    # function unused in final version 
    def checkVillager(self, tocheck):
        for k in self.kn[tocheck]:
            belief, origin = k
            if (belief == "villager" or belief == "witch" or belief == "seer" or belief == "guardian" or belief == "hunter" ) and origin == 't':
                # print("if go")
                return True
        return False

class Werewolf(Player):

    def __init__(self, kn, name, rule, target):
        Player.__init__(self, kn, name)
        self.rule = rule
        self.target = target

    def chooseSpeech(self):
        playerAlive = PlayerList[:]
        for x in DeadList:
            # print(x)
            if x in playerAlive:
                playerAlive.remove(x)

        if 'se' in playerAlive:
            playerAlive.remove('se')
        if self.getName() in playerAlive:
            playerAlive.remove(self.getName())

        if self.rule == "naive":
            return IdentityList[PlayerList.index(self.getName())]

        if self.rule == "first":
            if random.random() > 0.5:
                return IdentityList[PlayerList.index(self.getName())]
            else:
                return 'not' + IdentityList[PlayerList.index(self.getName())]

        if self.rule == "second":
            if random.random() > 0.5:
                return 'knowing' + playerAlive[random.randrange(0, len(playerAlive))]
            else:
                return 'not knowing' + playerAlive[random.randrange(0, len(playerAlive))]

        if self.rule == "third":
            if random.random() > 0.5:
                return 'knowing' + playerAlive[random.randrange(0, len(playerAlive))] + 'knows' + IdentityList[PlayerList.index(self.getName())]
            else:
                return 'not knowing' + playerAlive[random.randrange(0, len(playerAlive))] + 'knows' + IdentityList[PlayerList.index(self.getName())]

    def chooseKill(self, night):
        if self.target == "simple":
            if night == 1:
                return random.randrange(4, len(PlayerList))
            else:
                while True:
                    card = random.randrange(4, len(PlayerList))
                    if PlayerList[card] not in DeadList:
                        return card

    def wolfvote(self):
        if self.rule == "naive":
            card = 0
            while True:
                card = random.randrange(4, len(PlayerList))
                if PlayerList[card] not in DeadList:
                    break
            return card

        else:
            while True:
                # print("woo")
                card = random.randrange(4, len(PlayerList))
                if PlayerList[card] not in DeadList:
                    return card


class Seer(Villager):
    def __init__(self, kn, name, rule, seen, target):
        Villager.__init__(self, kn, name, rule, target)
        self.seen = seen

    def seecard(self):
        if self.target == "simple":
            card = 0
            tempbin = 0
            for i in DeadList:
                if i in self.seen:
                    tempbin += 1
            if len(self.seen) + len(DeadList) - tempbin == len(PlayerList):
                return ""

            while True:
                card = random.randrange(0, len(PlayerList))
                if PlayerList[card] not in self.seen and PlayerList[card] not in DeadList:
                    self.seen.append(PlayerList[card])
                    break

            self.changek((PlayerList[card], [(IdentityList[card], 't')]))
            return PlayerList[card]


class Witch(Villager):
    def __init__(self, kn, name, rule, target):
        Villager.__init__(self, kn, name, rule, target)
        self.poisoned = 0
        self.revived = 0

    def revive(self, victim):
        if self.target == "simple":
            if self.revived == 0:
                if victim == self.getName():
                    self.revived = 1
                    print("The witch chose to revive " + victim)
                    return True
                elif random.random() > 0.5:
                    self.revived = 1
                    print("The witch chose to revive " + victim)
                    return True
                else:
                    return False

    def poison(self):
        if self.target == "simple":
            if self.poisoned == 0:
                if random.random() > 0.5:
                    card = 0
                    while True:
                        card = random.randrange(0, len(PlayerList))
                        if PlayerList[card] not in DeadList and PlayerList[card] != self.getName():
                            break
                    self.poisoned = 1
                    return PlayerList[card]
                else:
                    return ""
            else:
                return ""


class Guardian(Villager):
    def __init__(self, kn, name, rule, guarded, target):
        Villager.__init__(self, kn, name, rule, target)
        self.guarded = self.getName()

    def guard(self, night):
        if self.target == "simple":
            if night == 1:
                return self.getName()
            card = 0
            if len(DeadList) == len(PlayerList)-1 and self.guarded == self.getName():
                return ""
            while True:
                card = random.randrange(0, len(PlayerList))
                if PlayerList[card] not in DeadList and PlayerList[card] != self.guarded:
                    break
            self.guarded = PlayerList[card]
            return PlayerList[card]

class Hunter(Villager):
    def __init__(self, kn, name, rule, target):
        Villager.__init__(self, kn, name, rule, target)

    def retaliate(self):
        if self.target == "simple":
            card = 0
            while True:
                card = random.randrange(0, len(PlayerList))
                if PlayerList[card] not in DeadList:
                    break
            return PlayerList[card]

class Model:
    def __init__(self, rule, target):
        self.rule = rule
        self.night = 0
        self.v1 = Villager([], 'v1', self.rule, target)
        self.v2 = Villager([], 'v2', self.rule, target)
        self.v3 = Villager([], 'v3', self.rule, target)
        self.v4 = Villager([], 'v4', self.rule, target)
        self.villist = [self.v1, self.v2, self.v3, self.v4]
        self.w1 = Werewolf([], 'w1', self.rule, target)
        self.w2 = Werewolf([], 'w2', self.rule, target)
        self.w3 = Werewolf([], 'w3', self.rule, target)
        self.w4 = Werewolf([], 'w4', self.rule, target)
        self.wolflist = [self.w1, self.w2, self.w3, self.w4]
        self.se = Seer([], 'se', self.rule, ['se'], target)
        self.wi = Witch([], 'wi', self.rule, target)
        self.gr = Guardian([], 'gr', self.rule, [], target)
        self.ht = Hunter([], 'ht', self.rule, target)
        self.spelist = [self.se, self.wi, self.gr, self.ht]
    def initialSet(self):
        kwolf = {'v1': [('notwerewolf', 't')], 'v2': [('notwerewolf', 't')], 'v3': [('notwerewolf', 't')], 'v4': [('notwerewolf', 't')], 'w1': [('werewolf', 't')],
                'w2': [('werewolf', 't')], 'w3': [('werewolf', 't')], 'w4': [('werewolf', 't')], 'se': [('notwerewolf', 't')], 'wi': [('notwerewolf', 't')], 'gr': [('notwerewolf', 't')], 'ht': [('notwerewolf', 't')]}
        # print(kwolf['v2'])
        for i, v in enumerate(self.villist):
            inik = {'v1': [], 'v2': [], 'v3': [], 'v4': [], 'w1': [], 'w2': [], 'w3': [], 'w4': [], 'se': [], 'wi': [],
                    'gr': [], 'ht': []}
            v.update(inik)
            v.kn[v.getName()] = [('villager', 't')]
        for w in self.wolflist:
            w.update(kwolf)
        for v in self.spelist:
            inik = {'v1': [], 'v2': [], 'v3': [], 'v4': [], 'w1': [], 'w2': [], 'w3': [], 'w4': [], 'se': [], 'wi': [],
                    'gr': [], 'ht': []}
            v.update(inik)
            v.kn[v.getName()] = [(IdentityList[PlayerList.index(v.getName())], 't')]

    def announce(self, toannounce, announcetype):
        for p in self.spelist:
            for i in toannounce:
                p.changek((i, [(IdentityList[PlayerList.index(i)], announcetype)]))
        for p in self.villist:
            for i in toannounce:
                p.changek((i, [(IdentityList[PlayerList.index(i)], announcetype)]))
        for p in self.wolflist:
            for i in toannounce:
                p.changek((i, [(IdentityList[PlayerList.index(i)], announcetype)]))

    def speechannounce(self, toannounce, announcetype):
        for p in self.spelist:
            for i in toannounce:
                p.changek((announcetype, [(i, announcetype)]))
        for p in self.villist:
            for i in toannounce:
                p.changek((announcetype, [(i, announcetype)]))
        for p in self.wolflist:
            for i in toannounce:
                p.changek((announcetype, [(i, announcetype)]))

    def discuss(self):
        for p in self.spelist:
            toannounce = p.chooseSpeech()
            # print(toannounce)
            self.speechannounce([toannounce], p.getName())
        for p in self.villist:
            toannounce = p.chooseSpeech()
            self.speechannounce([toannounce], p.getName())
        for p in self.wolflist:
            toannounce = p.chooseSpeech()
            self.speechannounce([toannounce], p.getName())

    def vote(self):
        bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for v in self.villist:
            bins[v.villagervote()] += 1
        for v in self.spelist:
            bins[v.villagervote()] += 1
        for w in self.wolflist:
            bins[w.wolfvote()] += 1
        vic = PlayerList[bins.index(max(bins))]

        # There is a tie in voting
        max1 = max(bins)
        bins.remove(max1)
        if max(bins) == max1:
            return ""
        return vic

    def wolfKill(self):
        bins = [0] * len(PlayerList)
        for w in self.wolflist:
            bins[w.chooseKill(self.night)] += 1
        vic = PlayerList[bins.index(max(bins))]
        return vic

    def overnight(self):
        self.night += 1
        print("The night " + str(self.night) + " begins:")
        # my_tuple = tuple(my_list)

        guarded = ""
        checked = ""
        if self.gr.getName() not in DeadList:
            guarded = self.gr.guard(self.night)
        if self.se.getName() not in DeadList:
            checked = self.se.seecard()
        vicList = []
        victim = self.wolfKill()

        if self.wi.getName() in DeadList or not self.wi.revive(victim):
            if self.gr.getName() in DeadList or victim != guarded:
                DeadList.append(victim)
                vicList.append(victim)
                print("Player " + victim + " has been killed by wolves;")
            else:
                print("The guardian guards " + self.gr.guarded + " this night.")

        poisoned = ""
        if self.wi.getName() not in DeadList and len(DeadList) < len(PlayerList)-2:
            poisoned = self.wi.poison()
        if poisoned != "":
            DeadList.append(poisoned)
            vicList.append(poisoned)
            print("Player " + poisoned + " has been poisoned by the witch;")

        revenged = ""
        if "ht" in vicList and len(DeadList) < len(PlayerList):
            revenged = self.ht.retaliate()
        if revenged != "":
            DeadList.append(revenged)
            vicList.append(revenged)
            print("Player " + revenged + " has been killed by angry hunter;")

        for any in self.villist:
            if any.getName() in vicList:
                self.villist.remove(any)
        for any in self.spelist:
            if any.getName() in vicList:
                self.spelist.remove(any)
        if "se" not in vicList:
            self.announce(["se"], 't')
        return vicList, checked

    def overday(self, vicList, checked):
        # print(self.v1.kn)
        print("Next day:")
        self.announce(vicList, 'd')
        if "se" not in vicList and "se" not in DeadList and checked != "" and checked not in vicList:
            self.announce([checked], 't')
        self.discuss()
        vicList = []
        executed = self.vote()
        if executed != "":
            DeadList.append(executed)
            vicList.append(executed)
            print("Player " + executed + " has been executed by the majority vote;")
        else:
            print("There is a tie in voting, no one is executed")
        revenged = ""
        if "ht" in vicList and len(DeadList) < len(PlayerList):
            revenged = self.ht.retaliate()
        if revenged != "":
            DeadList.append(revenged)
            vicList.append(revenged)
            print("Player " + revenged + " has been killed by angry hunter;")
        for any in self.villist:
            if any.getName() in vicList:
                self.villist.remove(any)
        for any in self.spelist:
            if any.getName() in vicList:
                self.spelist.remove(any)
        for any in self.wolflist:
            if any.getName() in vicList:
                self.wolflist.remove(any)
        self.announce(vicList, 'd')


    def checkwin(self):
        if 'w1' in DeadList and 'w2' in DeadList and 'w3' in DeadList and 'w4' in DeadList:
            return "The villagers win", 0
        if 'se' in DeadList and 'wi' in DeadList and 'gr' in DeadList and 'ht' in DeadList:
            return "The werewolves win", 1
        if 'v1' in DeadList and 'v2' in DeadList and 'v3' in DeadList and 'v4' in DeadList:
            return "The werewolves win", 1
        return "", 0

def main(argv):
    defaultSpeechRule = "first"
    defaultTactics = "simple"
    if (len(sys.argv)) > 1:
        defaultSpeechRule = str(sys.argv[1])
    if (len(sys.argv)) == 3:
        defaultTactics = str(sys.argv[2])
    print(str(sys.argv))
    epochindex = 0
    scoreboard = [0, 0]
    while epochindex < 100:
        m1 = Model(defaultSpeechRule, defaultTactics)
        m1.initialSet()
        epochindex += 1
        print("Game Iteration " + str(epochindex))
        global DeadList
        DeadList = []
        while True:
            vicList, checked = m1.overnight()
            tempword, score = m1.checkwin()
            if tempword != "":
                print(tempword + " after night "+str(m1.night) +". Game ends")
                scoreboard[score] += 1
                break
            m1.overday(vicList, checked)
            tempword, score = m1.checkwin()
            if tempword != "":
                print(tempword + " after night "+str(m1.night) +". Game ends")
                scoreboard[score] += 1
                break
        print(DeadList)
    print("Final score[villagers, werewolves]: " +str(scoreboard))
    # print(model.falseorigin)
    # for p in m1.spelist:
    #     print(p.kn)
    # for p in m1.villist:
    #     print(p.kn)
    # for p in m1.wolflist:
    #     print(p.kn)

if __name__ == "__main__":
    main(sys.argv[1:])


