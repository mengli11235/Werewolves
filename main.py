#!/usr/bin/python

import sys
import random

PlayerList = ['w1', 'w2', 'w3', 'w4', 'v1', 'v2', 'v3', 'v4', 'se', 'wi', 'gr', 'ht']
IdentityList = ['werewolf', 'werewolf', 'werewolf', 'werewolf', 'villager', 'villager', 'villager', 'villager', 'seer',
                'witch', 'guardian', 'hunter']
DeadList = []

class Player:

    def __init__(self, kn, name):
        self.kn = kn
        self.name = name

    def update(self, newk):
        self.kn = newk

    def changek(self, target, newk):
        self.kn[target] = newk

    def getName(self):
        return self.name()

class Villager(Player):

    def __init__(self, kn, name, rule):
        Player.__init__(self, kn, name)
        self.rule = rule

    def chooseSpeech(self):
        if random.random() > 0.5:
            return self.kn['self.name']
        else:
            return 'not'+self.kn['self.name']

class Werewolf(Player):

    def __init__(self, kn, name, rule, target):
        Player.__init__(self, kn, name)
        self.rule = rule
        self.target = target
    def chooseSpeech(self):
        if random.random() > 0.5:
            return self.kn['self.name']
        else:
            return 'not'+self.kn['self.name']
    def chooseKill(self, night, killlist):
        if night == 1:
            return random.randrange(0, len(killlist))
        else:
            return random.randrange(0, len(killlist))

class Seer(Villager):
    def __init__(self, kn, name, rule, seen):
        Villager.__init__(self, kn, name, rule)
        self.seen = seen

    def chooseSpeech(self):
        if random.random() > 0.5:
            return self.kn['self.name']
        else:
            return 'not' + self.kn['self.name']

    def seecard(self):
            card = 0
            while True:
                card = random.randrange(0, len(PlayerList))
                if PlayerList[card] not in self.seen and PlayerList[card] not in DeadList:
                    self.seen.append(PlayerList[card])
                    break
            self.changek(PlayerList[card], IdentityList[card])
            return PlayerList[card]


class Witch(Villager):
    def __init__(self, kn, name, rule, target):
        Villager.__init__(self, kn, name, rule)
        self.target = target

    def chooseSpeech(self):
        if random.random() > 0.5:
            return self.kn['self.name']
        else:
            return 'not'+self.kn['self.name']
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
            return self.kn['self.name']
        else:
            return 'not'+self.kn['self.name']

    def guard(self, night):
        if night == 1:
            return self.name
        card = 0
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
            return self.kn['self.name']
        else:
            return 'not'+self.kn['self.name']

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
        self.w1 = Werewolf([], 'w1', self.rule, target)
        self.w2 = Werewolf([], 'w2', self.rule, target)
        self.w3 = Werewolf([], 'w3', self.rule, target)
        self.w4 = Werewolf([], 'w4', self.rule, target)
        self.se = Seer([], 'se', self.rule, [])
        self.wi = Witch([], 'wi', self.rule, target)
        self.gr = Guardian([], 'gr', self.rule, "")
        self.ht = Hunter([], 'ht', self.rule, target)
        self.villist = [self.v1, self.v2, self.v3, self.v4]
        self.spelist = [self.se, self.wi, self.gr, self.ht]
        self.wolflist = [self.w1, self.w2, self.w3, self.w4]

    def initialSet(self):
        newk = {'v1': 'notwerewolf', 'v2': 'notwerewolf', 'v3': 'notwerewolf', 'v4': 'notwerewolf', 'w1': 'werewolf',
                'w2': 'werewolf', 'w3': 'werewolf', 'w4': 'werewolf', 'se': 'notwerewolf', 'wi': 'notwerewolf', 'gr': 'notwerewolf', 'ht': 'notwerewolf'}
        # print(newk['v2'])
        for v in self.villist:
            v.update({'v1': 'villager'})
        for w in self.wolflist:
            w.update(newk)
        self.se.update({'se': 'seer'})
        self.wi.update({'wi': 'witch'})
        self.gr.update({'gr': 'guardian'})
        self.se.update({'ht': 'hunter'})
        # print(self.w2.kn)

    def wolfKill(self):
        bins = [0, 0, 0, 0]
        if len(self.villist) < len(self.spelist):
            killlist = self.villist
        else:
            killlist = self.spelist
        for w in self.wolflist:
                bins[w.chooseKill(self.night, killlist)] += 1
        vic = killlist[bins.index(max(bins))].getName()
        return vic

    def overnight(self):
        self.night += 1
        guarded = self.gr.guard(self.night)
        checked = self.se.seecard()
        vicList = []
        victim = self.wolfKill()

        if not self.wi.revive(victim.getName()):
            if victim.getName() != guarded:
                DeadList.append(victim.getName())
                vicList.append(victim.getName())

        poisoned = self.wi.poison()
        if poisoned != "":
            DeadList.append(poisoned)
            vicList.append(poisoned)

        if "ht" in vicList:
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
        return vicList



def setup():
    pass

def main(argv):
    print(str(sys.argv))
    m1 = Model('naive', 'simple')
    m1.initialSet()
    setup()

if __name__ == "__main__":
   main(sys.argv[1:])


