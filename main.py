#!/usr/bin/python

import sys
import random
import model

# predefined player name and identity lists
PlayerList = ['w1', 'w2', 'w3', 'w4', 'v1', 'v2', 'v3', 'v4', 'se', 'wi', 'gr', 'ht']
IdentityList = ['werewolf', 'werewolf', 'werewolf', 'werewolf', 'villager', 'villager', 'villager', 'villager', 'seer',
                'witch', 'guardian', 'hunter']
DeadList = []

# all players inherit this class
class Player:

    def __init__(self, kn, name):
        self.kn = kn  # knowledge model
        self.name = name  # player name
        self.falseorigin = [0] * 14  # credits on each player

    # initialize knowledge model
    def update(self, newset):
        self.kn = newset

    # change knowledge model
    def changek(self, newk):
        self.kn, self.falseorigin = model.checkconflict(self.kn, newk, self.falseorigin)

    def getName(self):
        return self.name

    # unused in final
    def checkValidity(self, tocheck, checktype):
        for k in self.kn[tocheck]:
            belief, origin = k
            if belief == checktype and origin == 't':
                # print("if go")
                return True
        return False

# special villagers also inherit from this class
class Villager(Player):

    def __init__(self, kn, name, rule, target):
        Player.__init__(self, kn, name)
        # order of knowledge
        self.rule = rule
        # more tactics, not implemented
        self.target = target

    # choose speech during discuss in day session
    def chooseSpeech(self):
        # limit possible referees, no dead, seer, or itself
        playerAlive = PlayerList[:]
        for x in DeadList:
            # print(x)
            if x in playerAlive:
                playerAlive.remove(x)

        if 'se' in playerAlive:
            playerAlive.remove('se')
        if self.getName() in playerAlive:
            playerAlive.remove(self.getName())

        # speak true identity
        if self.rule == "naive":
            return IdentityList[PlayerList.index(self.getName())]

        # speak randomly about self's identity
        if self.rule == "first":
            if random.random() > 0.5:
                return IdentityList[PlayerList.index(self.getName())]
            else:
                return 'not' + IdentityList[PlayerList.index(self.getName())]

        # speak about other's identity
        if self.rule == "second":
            if random.random() > 0.5:
                return 'knowing' + playerAlive[random.randrange(0, len(playerAlive))]
            else:
                return 'notknowing' + playerAlive[random.randrange(0, len(playerAlive))]

        # speak about other's knowledge about other's identity
        if self.rule == "third":
            if random.random() > 0.5:
                return 'knowing' + playerAlive[random.randrange(0, len(playerAlive))] + 'knows' + IdentityList[PlayerList.index(self.getName())]
            else:
                return 'notknowing' + playerAlive[random.randrange(0, len(playerAlive))] + 'knows' + IdentityList[PlayerList.index(self.getName())]

    # vote function of villagers
    def villagervote(self):
        if self.rule == "naive":
            card = 0
            # vote randomly
            while True:
                card = random.randrange(0, len(PlayerList))
                if PlayerList[card] not in DeadList and PlayerList[card] != self.getName() and IdentityList[card] != 'seer':
                    break
            return card

        else:
            # vote based on model and fuzzy logic
            falseO = self.falseorigin[2:]
            playerAlive = PlayerList[:]
            for x in DeadList:
                if x in playerAlive:
                    i = playerAlive.index(x)
                    del falseO[i]
                    del playerAlive[i]

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

    # wereeolf speech, not different from villagers in final
    def chooseSpeech(self):
        playerAlive = PlayerList[:]
        for x in DeadList:
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
                return 'notknowing' + playerAlive[random.randrange(0, len(playerAlive))]

        if self.rule == "third":
            if random.random() > 0.5:
                return 'knowing' + playerAlive[random.randrange(0, len(playerAlive))] + 'knows' + IdentityList[PlayerList.index(self.getName())]
            else:
                return 'notknowing' + playerAlive[random.randrange(0, len(playerAlive))] + 'knows' + IdentityList[PlayerList.index(self.getName())]

    # kill anyone but not werewolf
    def chooseKill(self, night):
        if self.target == "simple":
            if night == 1:
                return random.randrange(4, len(PlayerList))
            else:
                while True:
                    card = random.randrange(4, len(PlayerList))
                    if PlayerList[card] not in DeadList:
                        return card

    # vote anyone but not werewolf
    def wolfvote(self):
        if self.rule == "naive":
            card = 0
            while True:
                card = random.randrange(4, len(PlayerList))
                if PlayerList[card] not in DeadList:
                    break
            return card

        else:
            # can be different
            while True:
                card = random.randrange(4, len(PlayerList))
                if PlayerList[card] not in DeadList:
                    return card

# Seer inherits from Villager
class Seer(Villager):
    def __init__(self, kn, name, rule, seen, target):
        Villager.__init__(self, kn, name, rule, target)
        self.seen = seen

    # See a players card
    def seecard(self):
        if self.target == "simple":
            card = 0
            # to make sure no overlap of seen playeres but then dead
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

# Witch inherits from Villager
class Witch(Villager):
    def __init__(self, kn, name, rule, target):
        Villager.__init__(self, kn, name, rule, target)
        self.poisoned = 0
        self.revived = 0

    # revive one player during night
    def revive(self, victim):
        if self.target == "simple":
            if self.revived == 0:
                if victim == self.getName():
                    # always save herself
                    self.revived = 1
                    print("The witch chose to revive " + victim)
                    return True
                elif random.random() > 0.5:
                    # otherwise randomly
                    self.revived = 1
                    print("The witch chose to revive " + victim)
                    return True
                else:
                    return False

    # poison a player
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

# Guardian inherits from Villager
class Guardian(Villager):
    def __init__(self, kn, name, rule, guarded, target):
        Villager.__init__(self, kn, name, rule, target)
        self.guarded = self.getName()

    # guard a player
    def guard(self, night):
        if self.target == "simple":
            if night == 1:
                return self.getName()
            card = 0
            if len(DeadList) == len(PlayerList)-1 and self.guarded == self.getName():
                return ""
            # more randomly
            while True:
                card = random.randrange(0, len(PlayerList))
                if PlayerList[card] not in DeadList and PlayerList[card] != self.guarded:
                    break
            self.guarded = PlayerList[card]
            return PlayerList[card]

# Hunter inherits from Villager
class Hunter(Villager):
    def __init__(self, kn, name, rule, target):
        Villager.__init__(self, kn, name, rule, target)

    # retaliate upon death
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
        # players initialization
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
        # knowledge set initialization
        kwolf = {'v1': [('notwerewolf', 't')], 'v2': [('notwerewolf', 't')], 'v3': [('notwerewolf', 't')], 'v4': [('notwerewolf', 't')], 'w1': [('werewolf', 't')],
                'w2': [('werewolf', 't')], 'w3': [('werewolf', 't')], 'w4': [('werewolf', 't')], 'se': [('notwerewolf', 't')], 'wi': [('notwerewolf', 't')], 'gr': [('notwerewolf', 't')], 'ht': [('notwerewolf', 't')]}

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
        # announce to every survivers
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
        # announce the speech during discuss session
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
        # each survivers can speak
        for p in self.spelist:
            toannounce = p.chooseSpeech()
            self.speechannounce([toannounce], p.getName())
        for p in self.villist:
            toannounce = p.chooseSpeech()
            self.speechannounce([toannounce], p.getName())
        for p in self.wolflist:
            toannounce = p.chooseSpeech()
            self.speechannounce([toannounce], p.getName())

    def vote(self):
        # main vote funtion
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
        # main wolves' choice of killing
        # based on vote as well
        bins = [0] * len(PlayerList)
        for w in self.wolflist:
            bins[w.chooseKill(self.night)] += 1
        vic = PlayerList[bins.index(max(bins))]
        return vic

    # each night
    def overnight(self):
        self.night += 1
        print("The night " + str(self.night) + " begins:")

        guarded = ""
        checked = ""
        # guardian and seer alive
        if self.gr.getName() not in DeadList:
            guarded = self.gr.guard(self.night)
        if self.se.getName() not in DeadList:
            checked = self.se.seecard()
        vicList = []
        victim = self.wolfKill()

        # if not guarded or revived, then killed by wolf
        if self.wi.getName() in DeadList or not self.wi.revive(victim):
            if self.gr.getName() in DeadList or victim != guarded:
                DeadList.append(victim)
                vicList.append(victim)
                print("Player " + victim + " has been killed by wolves;")
            else:
                print("The guardian guards " + self.gr.guarded + " this night.")

        poisoned = ""
        # death by poison
        if self.wi.getName() not in DeadList and len(DeadList) < len(PlayerList)-2:
            poisoned = self.wi.poison()
        if poisoned != "":
            DeadList.append(poisoned)
            vicList.append(poisoned)
            print("Player " + poisoned + " has been poisoned by the witch;")

        revenged = ""
        # death by hunter
        if "ht" in vicList and len(DeadList) < len(PlayerList):
            revenged = self.ht.retaliate()
        if revenged != "":
            DeadList.append(revenged)
            vicList.append(revenged)
            print("Player " + revenged + " has been killed by angry hunter;")

        # update survivors
        for any in self.villist:
            if any.getName() in vicList:
                self.villist.remove(any)
        for any in self.spelist:
            if any.getName() in vicList:
                self.spelist.remove(any)
        if "se" not in vicList:
            self.announce(["se"], 't')
        return vicList, checked

    # each day
    def overday(self, vicList, checked):
        print("Next day:")
        # announce victims
        self.announce(vicList, 'd')

        # update seek's check as truth
        if "se" not in vicList and "se" not in DeadList and checked != "" and checked not in vicList:
            self.announce([checked], 't')

        # discuss, important
        self.discuss()

        # victim executed by majority vote
        vicList = []
        executed = self.vote()
        if executed != "":
            DeadList.append(executed)
            vicList.append(executed)
            print("Player " + executed + " has been executed by the majority vote;")
        else:
            print("There is a tie in voting, no one is executed")

        # hunter also can revenge here
        revenged = ""
        if "ht" in vicList and len(DeadList) < len(PlayerList):
            revenged = self.ht.retaliate()
        if revenged != "":
            DeadList.append(revenged)
            vicList.append(revenged)
            print("Player " + revenged + " has been killed by angry hunter;")
        # update survivors
        for any in self.villist:
            if any.getName() in vicList:
                self.villist.remove(any)
        for any in self.spelist:
            if any.getName() in vicList:
                self.spelist.remove(any)
        for any in self.wolflist:
            if any.getName() in vicList:
                self.wolflist.remove(any)
        # announce death
        self.announce(vicList, 'd')

    # check which side has won
    def checkwin(self):
        if 'w1' in DeadList and 'w2' in DeadList and 'w3' in DeadList and 'w4' in DeadList:
            return "The villagers win", 0
        if 'se' in DeadList and 'wi' in DeadList and 'gr' in DeadList and 'ht' in DeadList:
            return "The werewolves win", 1
        if 'v1' in DeadList and 'v2' in DeadList and 'v3' in DeadList and 'v4' in DeadList:
            return "The werewolves win", 1
        return "", 0

def main(argv):
    # commandline input
    defaultSpeechRule = "first"
    defaultTactics = "simple"
    if (len(sys.argv)) > 1:
        defaultSpeechRule = str(sys.argv[1])
    if (len(sys.argv)) == 3:
        defaultTactics = str(sys.argv[2])
    # print(str(sys.argv))
    # index and scores of epoches
    epochindex = 0
    scoreboard = [0, 0]
    while epochindex < 100:
        m1 = Model(defaultSpeechRule, defaultTactics)
        m1.initialSet()
        epochindex += 1
        print("Game Iteration " + str(epochindex))
        global DeadList
        DeadList = []

        # each epoch
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
    # Final results
    print("Final score[villagers, werewolves]: " +str(scoreboard))
if __name__ == "__main__":
    main(sys.argv[1:])


