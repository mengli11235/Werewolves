#!/usr/bin/python

import sys

class Player:

    def __init__(self, kn, name):
        self.kn = kn
        self.name = name

    def update(self, newk):
        return self.kn.append(newk)

    def GetName(self):
        return self.name()

class Villager(Player):

    def __init__(self, kn, name, rule):
        Player.__init__(self, kn, name)
        self.rule = rule

class Werewolf(Player):

    def __init__(self, kn, name, rule, target):
        Player.__init__(self, kn, name)
        self.rule = rule
        self.target = target

class Seer(Villager):
    def __init__(self, kn, name, rule, target):
        Villager.__init__(self, kn, name, rule)
        self.target = target

class Witch(Villager):
    def __init__(self, kn, name, rule, target):
        Villager.__init__(self, kn, name, rule)
        self.target = target

class Guardian(Villager):
    def __init__(self, kn, name, rule, target):
        Villager.__init__(self, kn, name, rule)
        self.target = target

class Hunter(Villager):
    def __init__(self, kn, name, rule, target):
        Villager.__init__(self, kn, name, rule)
        self.target = target

class Model:
    def __init__(self, rule, target):
        self.rule = rule
        self.v1 = Villager([], 'Villager 1', self.rule)
        self.v2 = Villager([], 'Villager 2', self.rule)
        self.v3 = Villager([], 'Villager 3', self.rule)
        self.v4 = Villager([], 'Villager 4', self.rule)
        self.w1 = Werewolf([], 'Werewolf 1', self.rule, target)
        self.w2 = Werewolf([], 'Werewolf 1', self.rule, target)
        self.w3 = Werewolf([], 'Werewolf 1', self.rule, target)
        self.w4 = Werewolf([], 'Werewolf 1', self.rule, target)
        self.se = Seer([], 'Seer', self.rule, target)
        self.wi = Witch([], 'Witch', self.rule, target)
        self.gr = Guardian([], 'Guardian', self.rule, target)
        self.s1 = Hunter([], 'Hunter', self.rule, target)

def setup():
    pass

def main(argv):
    print(str(sys.argv))
    m1 = Model('naive', 'simple')
    setup()

if __name__ == "__main__":
   main(sys.argv[1:])


