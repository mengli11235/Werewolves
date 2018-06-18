#!/usr/bin/python
OriginList = ['t', 'd', 'w1', 'w2', 'w3', 'w4', 'v1', 'v2', 'v3', 'v4', 'se', 'wi', 'gr', 'ht']
Cardlist = ['werewolf', 'villager', 'seer', 'witch', 'guardian', 'hunter']

def contrarule(oldb, newb):
    if 'not'+oldb == newb or 'not'+newb == oldb:
        return True
    elif oldb in Cardlist and newb in Cardlist and newb != oldb:
        return True
    else:
        return False


def contradicts(oldk, newk, falseorigin):
    # if both the same
    if oldk[0] == newk[0]:
        return 2
    # if contradicts
    if contrarule(oldk[0], newk[0]):
        if oldk[1] == 't' or oldk[1] == 'd':
            return 1
        # new knowledge prevails old belief
        elif newk[1] == 't':
            return -1
        # if someone's death announced
        elif newk[1] == 'd':
            return -2
        # otherwise check their credibility
        if falseorigin[OriginList.index(newk[1])] < falseorigin[OriginList.index(oldk[1])]:
            # print(falseorigin)
            return -1
        else:
            return 1
    return 0

def checkconflict(kn, newk, falseorigin):
    key, value = newk
    # print(key)
    for k in kn[key]:
        belief, origin = k
        for v in value:
            contra = contradicts(k, v, falseorigin)
            # if mere duplicates
            if v in kn[key]:
                value.remove(v)
                continue
            # if new knowledge prevails old belief
            if contra == -1:
                kn[key].remove(k)
                kn[key].append(v)
                falseorigin[OriginList.index(origin)] += 1
            # if someone's death announced
            elif contra == -2:
                kn[key].remove(k)
                kn[key].append(v)
            # if new belief is wrong
            elif contra == 1:
                falseorigin[OriginList.index(v[1])] += 1
            # if both belief confirm each other, then increase the speecher's credits
            elif contra == 2:
                falseorigin[OriginList.index(v[1])] += -1
                falseorigin[OriginList.index(origin)] += -1
            # if no contradiction
            elif contra == 0:
                kn[key].append(v)

    # if there is no previous belief about that player
    if not kn[key]:
        for v in value:
            kn[key].append(v)
    # print(falseorigin)
    return kn, falseorigin
