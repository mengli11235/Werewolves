#!/usr/bin/python
OriginList = ['t', 'd', 'w1', 'w2', 'w3', 'w4', 'v1', 'v2', 'v3', 'v4', 'se', 'wi', 'gr', 'ht']

def changeknowledge(oldk, newk):
     if checkconflict(oldk, newk):
         return None

def contradicts(oldk, newk):
    return -1

def checkconflict(kn, newk):
    falseorigin = [0] * len(OriginList)
    key, value = newk
    for k in kn[key]:
        belief, origin = k
        for v in value:
            contra = contradicts(belief, v[0])
            if contra == -1:
                kn[key].remove(k)
                kn[key].append(v)
                falseorigin[OriginList.index(origin)] += 1
            elif contra == 1:
                falseorigin[OriginList.index(v[1])] += 1
            elif contra == 0:
                kn[key].append(v)

    return kn, falseorigin
