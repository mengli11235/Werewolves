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

    def update(self, newset):
        self.kn = newset

    def changek(self, newk):
        # print(newk)
        self.kn = model.checkconflict(self.kn, newk)

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
        if self.rule == "naive":
            return self.getName()

        if self.rule == "first":
            if self.rule == "naive":
                if random.random() > 0.5:
                    return self.getName()
                else:
                    return 'not' + self.getName()

    def villagervote(self):
        if self.rule == "naive":
            card = 0
            while True:
                card = random.randrange(0, len(PlayerList))
                if PlayerList[card] not in DeadList and PlayerList[card] != self.getName() and IdentityList[card] != 'seer':
                    break
            return card

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
        if self.rule == "naive":
            return self.getName()

        if self.rule == "first":
            if self.rule == "naive":
                if random.random() > 0.5:
                    return self.getName()
                else:
                    return 'not' + self.getName()

    def chooseKill(self, night, killlist):
        if self.target == "simple":
            if night == 1:
                return random.randrange(0, len(killlist))
            else:
                return random.randrange(0, len(killlist))

    def wolfvote(self):
        if self.rule == "naive":
            card = 0
            while True:
                card = random.randrange(4, len(PlayerList))
                if PlayerList[card] not in DeadList and PlayerList[card] != self.getName():
                    break
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
                    return True
                elif random.random() > 0.5:
                    self.revived = 1
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
                        if PlayerList[card] not in DeadList and  PlayerList[card] != self.getName() and IdentityList[card] != "seer":
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
        self.guarded = guarded

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
            print(self.guarded)
            return PlayerList[card]

class Hunter(Villager):
    def __init__(self, kn, name, rule, target):
        Villager.__init__(self, kn, name, rule, target)

    def retaliate(self):
        if self.target == "simple":
            card = 0
            while True:
                card = random.randrange(0, len(PlayerList))
                if PlayerList[card] not in DeadList and IdentityList[card] != "seer":
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

    def discuss(self):
        for p in self.spelist:
            p.chooseSpeech()
        for p in self.villist:
            p.chooseSpeech()
        for p in self.wolflist:
            p.chooseSpeech()

    def vote(self):
        bins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for v in self.villist:
            bins[v.villagervote()] += 1
        for v in self.spelist:
            bins[v.villagervote()] += 1
        for w in self.wolflist:
            bins[w.wolfvote()] += 1
        vic = PlayerList[bins.index(max(bins))]
        return vic

    def wolfKill(self):
        bins = []
        if len(self.villist) < len(self.spelist):
            bins = [0] * len(self.villist)
            for w in self.wolflist:
                bins[w.chooseKill(self.night, self.villist)] += 1
        else:
            bins = [0] * len(self.spelist)
            for w in self.wolflist:
                bins[w.chooseKill(self.night, self.spelist)] += 1

        if len(self.villist) < len(self.spelist):
            vic = self.villist[bins.index(max(bins))].getName()
        else:
            vic = self.spelist[int(bins.index(max(bins)))].getName()
        return vic

    def overnight(self):
        self.night += 1
        # my_tuple = tuple(my_list)

        guarded = ""
        checked = ""
        if self.gr.getName() not in DeadList:
            guarded = self.gr.guard(self.night)
        if self.se.getName() not in DeadList:
            checked = self.se.seecard()
        vicList = []
        victim = self.wolfKill()

        if not self.wi.revive(victim) or self.wi.getName() in DeadList:
            if victim != guarded:
                DeadList.append(victim)
                vicList.append(victim)

        poisoned = ""
        if self.wi.getName() not in DeadList and len(DeadList) < len(PlayerList)-1:
            poisoned = self.wi.poison()
        if poisoned != "":
            DeadList.append(poisoned)
            vicList.append(poisoned)

        revenged = ""
        if "ht" in vicList and len(DeadList) < len(PlayerList):
            revenged = self.ht.retaliate()
        if revenged != "":
            DeadList.append(revenged)
            vicList.append(revenged)

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
        print(self.v1.kn)
        self.announce(vicList, 'd')
        if "se" not in vicList and checked != "" and checked not in vicList:
            self.announce([checked], 't')
        self.discuss()
        vicList = []
        executed = self.vote()
        DeadList.append(executed)
        vicList.append(executed)
        revenged = ""
        if "ht" in vicList and len(DeadList) < len(PlayerList):
            revenged = self.ht.retaliate()
        if revenged != "":
            DeadList.append(revenged)
            vicList.append(revenged)
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
        if not self.wolflist:
            return "The villagers win"
        if not self.spelist:
            return "The werewolves win"
        if not self.villist:
            return "The werewolves win"
        return ""

def main(argv):
    defaultSpeechRule = "naive"
    defaultTactics = "simple"
    if (len(sys.argv)) > 1:
        defaultSpeechRule = str(sys.argv[1])
    if (len(sys.argv)) == 3:
        defaultTactics = str(sys.argv[2])
    print(str(sys.argv))
    m1 = Model(defaultSpeechRule, defaultTactics)
    m1.initialSet()
    while True:
        vicList, checked = m1.overnight()
        tempword = m1.checkwin()
        if tempword != "":
            print(tempword + " after night "+str(m1.night) +". Game ends")
            break
        m1.overday(vicList, checked)
        tempword = m1.checkwin()
        if tempword != "":
            print(tempword + " after night "+str(m1.night) +". Game ends")
            break
    print(DeadList)
    # print(model.falseorigin)
    # for p in m1.spelist:
    #     print(p.kn)
    # for p in m1.villist:
    #     print(p.kn)
    # for p in m1.wolflist:
    #     print(p.kn)

if __name__ == "__main__":
    main(sys.argv[1:])


