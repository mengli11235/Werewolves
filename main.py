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

class Villager(Player):

    def __init__(self, kn, name, rule):
        Player.__init__(self, kn, name)
        self.rule = rule

    def villagervote(self):
        if random.random() > 0.5:
            return PlayerList.index(self.getTarget())
        else:
            return PlayerList.index(self.getTarget())

class Werewolf(Player):

    def __init__(self, kn, name, rule, target):
        Player.__init__(self, kn, name)
        self.rule = rule
        self.target = target
    def chooseSpeech(self):
        if random.random() > 0.5:
            return self.kn[self.getName()]
        else:
            return 'not'+self.kn[self.getName()]
    def chooseKill(self, night, killlist):
        if night == 1:
            return random.randrange(0, len(killlist))
        else:
            return random.randrange(0, len(killlist))

    def wolfvote(self):
        if random.random() > 0.5:
            return PlayerList.index(self.getTarget())
        else:
            return PlayerList.index(self.getTarget())


class Seer(Villager):
    def __init__(self, kn, name, rule, seen):
        Villager.__init__(self, kn, name, rule)
        self.seen = seen

    def chooseSpeech(self):
        if random.random() > 0.5:
            return self.kn[self.getName()]
        else:
            return 'not' + self.kn[self.getName()]

    def seecard(self):
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
        Villager.__init__(self, kn, name, rule)
        self.target = target

    def chooseSpeech(self):
        if random.random() > 0.5:
            return self.kn[self.getName()]
        else:
            return 'not'+self.kn[self.getName()]
    def revive(self, victim):
        if random.random() > 0.5:
            return True
        else:
            return False

    def poison(self):
        if random.random() > 0.5:
            card = 0
            while True:
                card = random.randrange(0, len(PlayerList))
                if PlayerList[card] not in DeadList:
                    break
            return PlayerList[card]
        else:
            return ""


class Guardian(Villager):
    def __init__(self, kn, name, rule, guarded):
        Villager.__init__(self, kn, name, rule)
        self.guarded = guarded

    def chooseSpeech(self):
        if random.random() > 0.5:
            return self.kn[self.getName()]
        else:
            return 'not'+self.kn[self.getName()]

    def guard(self, night):
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
        Villager.__init__(self, kn, name, rule)
        self.target = target

    def chooseSpeech(self):
        if random.random() > 0.5:
            return self.kn[self.getName()]
        else:
            return 'not'+self.kn[self.getName()]

    def retaliate(self):
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
        self.v1 = Villager([], 'v1', self.rule)
        self.v2 = Villager([], 'v2', self.rule)
        self.v3 = Villager([], 'v3', self.rule)
        self.v4 = Villager([], 'v4', self.rule)
        self.villist = [self.v1, self.v2, self.v3, self.v4]
        self.w1 = Werewolf([], 'w1', self.rule, target)
        self.w2 = Werewolf([], 'w2', self.rule, target)
        self.w3 = Werewolf([], 'w3', self.rule, target)
        self.w4 = Werewolf([], 'w4', self.rule, target)
        self.wolflist = [self.w1, self.w2, self.w3, self.w4]
        self.se = Seer([], 'se', self.rule, ['se'])
        self.wi = Witch([], 'wi', self.rule, target)
        self.gr = Guardian([], 'gr', self.rule, [])
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
        pass

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
        return vicList, checked

    def overday(self, vicList, checked):
        print(self.se.kn)
        self.announce(vicList, 'd')
        if checked != "" and checked not in vicList:
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
    print(str(sys.argv))
    m1 = Model('naive', 'simple')
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

if __name__ == "__main__":
    main(sys.argv[1:])


