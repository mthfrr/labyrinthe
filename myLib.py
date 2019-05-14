def dirToXY(direction):
    return [(1,0),(0,1),(-1,0),(0,-1)][direction]

def XYToDir(a, b):
    return [(1,0),(0,1),(-1,0),(0,-1)].index((a, b))

def getKey(val, dict):
    out = []
    for key, value in dict.items():
        if val == value:
            out.append(key)
    return out

def absDirToRel(actDir, absDir):
    while actDir%4 != 1:
        actDir = (actDir-1)%4
        absDir = (absDir-1)%4
    return absDir

if __name__ == '__main__':
    print(absDirToRel(0, 3))