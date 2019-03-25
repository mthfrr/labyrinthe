import random


class CRoom():
    def __init__(self, pos):
        self.pos = pos
        self.doors = [0, 0, 0, 0] # East, North, West, South (odre trigo)
        self.texture = "A"
        self.distCentre = 0
        return

    def __str__(self):
        t = []
        for e in self.doors:
            if e == 0:
                t.append(0)
            else:
                t.append(1)
        return 'ROOM %s - %s'%(str(self.pos), str(t))
        return str(t)

    def setDist(self, dist):
        self.distCentre = dist
        return

    def link(self, target, room):
        if  target[0]-self.pos[0] == 1:
            self.doors[0] = room
        elif target[1]-self.pos[1] == 1:
            self.doors[1] = room
        elif target[0]-self.pos[0] == -1:
            self.doors[2] = room
        elif target[1]-self.pos[1] == -1:
            self.doors[3] = room
        else:
            print("room.openDoor : target - pos != 1 or -1")

    def outDoors(self):
        return self.doors

    def outTexture(self):
        return self.texture

class CLaby():
    def __init__(self):
        return

    def initRandom(self, n=None):
        if n:
            random.seed(n)
        else:
            random.seed()

    def gen(self, n=9):
        for rooms, (i,j) in self.stepGen(n):
            pass

    def stepGen(self, n=9):
        room = CRoom((0,0)) # pos = (x, y)
        self.laby = {(0,0) : room}
        a, b = 0, 0
        for _ in range(n):
            A, B = a, b
            if random.randint(0, 1):
                a += random.choice((-1, 1))
            else:
                b += random.choice((-1, 1))
            if (a, b) not in self.laby.keys():
                self.laby[a, b] = CRoom((a, b))
            self.laby[a, b].link((A, B), self.laby[A, B])
            self.laby[A, B].link((a, b), self.laby[a, b])

            yield self.laby, (a,b)

    def addDistance(self, room):
        print(room.outDoors())
        for nroom in room.outDoors():
            if nroom != 0 and room.distCentre == 0:
                print(nroom)
                nroom.setDist(room.distCentre+1)
                return self.addDistance(nroom)

        return

    def out(self):
        return self.laby

    def printLaby(self):
        keylist = list(self.laby.keys())
        x, y = [], []
        for i in range(len(keylist)):
            x.append(keylist[i][0])
            y.append(keylist[i][1])
        x = [min(x), max(x)]
        y = [min(y), max(y)]
        #print(x, y)

        for j in range(y[0], y[1]):
            for i in range(x[0], x[1]):
                if (i,j) in keylist:
                    if (i,j) == (0,0):
                        print("O", end='')
                    else:
                        print("+", end='')
                else:
                    print(" ", end='')
            print("")
        return


if __name__ == '__main__':
    laby = CLaby()
    laby.gen(30)
    laby.printLaby()
