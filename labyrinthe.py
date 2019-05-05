# vim:set encoding=utf-8

import random
import math
from myLib import *

class CRoom():
    def __init__(self, pos):
        self.pos = pos # room coordinates
        self.doors = [0, 0, 0, 0] # East, North, West, South (odre trigo)
        self.texture = [0, 0, 0, 0] # 0 : couloir-couloir, 1 : salle-salle, 2 : couloir-salle, 3 : salle-couloir
        self.isEnd = 0 # is this room the end of the level
        self.BigRoomId = 0 # default is 0 means corridor
        self.possibleEnd = 0 # TEMP FOR DEBUG ONLY
        #self.object = 0 # 0 is no object, else is the object
        return

    def __str__(self): # nice display in case of a print(object)
        t = []
        for e in self.doors:
            if e == 0:
                t.append(0)
            else:
                t.append(1)
        return 'ROOM %s - %s'%(str(self.pos), str(t))
        return str(t)

    def link(self, target, room, texture): # create a one way-link with another room
        if  target[0]-self.pos[0] == 1:
            self.doors[0] = room
            self.texture[0] = texture
        elif target[1]-self.pos[1] == 1:
            self.doors[1] = room
            self.texture[1] = texture
        elif target[0]-self.pos[0] == -1:
            self.doors[2] = room
            self.texture[2] = texture
        elif target[1]-self.pos[1] == -1:
            self.doors[3] = room
            self.texture[3] = texture
        else:
            print("room.openDoor : target - pos != 1 or -1")

    def nbDoors(self):
        out = 0
        for door in self.doors:
            if door != 0:
                out += 1
        return out

    def outTexture(self): # not used
        return self.texture

class CLaby():
    def __init__(self):
        self.laby = {}
        self.end = 0 # pos of end
        return

    def initRandom(self, n=None):
        if n:
            random.seed(n)
        else:
            random.seed()

    def listNextRooms(self, pos):
        out = []
        for room in self.laby[pos].doors:
            if room != 0:
                out.append(room.pos)
        return out

    def connectedAndNot(self): 
        frontiere = [(0,0)]
        if self.listNextRooms((0,0)) != []:
            connected = {(0,0) : self.laby[(0,0)]}
        else:
            startRoom = self.laby[(0,0)]
            notConnected = {}
            for room in self.laby:
                if room != (0,0):
                    notConnected[room] = self.laby[room]
            return {(0,0) : startRoom}, notConnected 
        notConnected = {}
        while frontiere != []:
            pos = frontiere[0]
            for posNextRoom in self.listNextRooms(pos):
                if posNextRoom not in list(connected.keys()):
                    connected[posNextRoom] = self.laby[posNextRoom]
                    frontiere.append(posNextRoom)
            frontiere.pop(0)
        for room in self.laby:
            if room not in connected:
                notConnected[room] = self.laby[room]
        if len(notConnected)+len(connected) != len(self.laby):
            print("error connectedAndNot")
            exit()
        return connected, notConnected

    def spread(self, curr_pos):
        depth = 0
        frontiere = [curr_pos]
        aMap = {curr_pos : depth}
        while frontiere != []:
            pos = frontiere[0]
            for posNextRoom in self.listNextRooms(pos):
                if posNextRoom not in list(aMap.keys()):
                    aMap[posNextRoom] = aMap[pos]+1
                    frontiere.append(posNextRoom)
            frontiere.pop(0)
        if aMap.keys() == self.laby.keys():
            return aMap
        else:
            return aMap

    def dirToEnd(self, pos):
        endPos = self.end
        aMap = self.spread(endPos)
        direction = [] # distance to end for each direction (E, N, W, S)
        for i in range(4):
            da, db = dirToXY(i)
            print("")
            a, b = int(pos[0])+int(da), int(pos[1])+int(db)
            if (a, b) in aMap:
                direction.append(aMap[a,b])
        return direction.index(min(direction))

    def gen(self, n=9): # generating the labyrinth
        for rooms, (i,j) in self.stepGen(n): # calling stepGen as many times as necessary
            pass
        ## setting the end of the labyrinth
        self.aMap = self.spread((0,0)) # get the distance between any tile and the starting position
        possiblePos = []
        maxDist = max(self.aMap.values())
        for dist in self.aMap.values():
            key = getKey(dist, self.aMap)[0]
            if dist >= 0.6*maxDist and self.laby[key].nbDoors() == 1:
                possiblePos.append(self.laby[key])
                self.laby[key].possibleEnd = 1
        room = random.choice(possiblePos)
        room.isEnd = 1
        self.end = room.pos
        return self.laby

    def twoWaysLink(self, a, b, A, B):
        abId = self.laby[a, b].BigRoomId
        ABId = self.laby[A, B].BigRoomId
        if not(abId-ABId):
            texture1 = 1
            texture2 = 1
        elif abId == ABId == 0:
            texture1 = 0
            texture2 = 0
        elif abId !=  ABId != 0:
            texture1 = 0
            texture2 = 0
        elif abId == 0 and ABId !=0:
            texture1 = 2
            texture2 = 3
        elif ABId == 0 and abId !=0:
            texture1 = 3
            texture2 = 2
        else:
            print("twoWaysLink : ERROR", abId, ABId)
            exit()

        self.laby[a, b].link((A, B), self.laby[A, B], texture1) # creating a 2 ways link
        self.laby[A, B].link((a, b), self.laby[a, b], texture2)
        return

    def createRoom(self, sizeX, sizeY, posX, posY, roomId):
        for i in range(posX-1, posX+sizeX+1, 1):
            for j in range(posY-1, posY+sizeY+1, 1):
                if (i, j) in self.laby.keys():
                    return 0

        for i in range(posX, posX+sizeX, 1):
            for j in range(posY, posY+sizeY, 1):
                self.laby[i, j] = CRoom((i, j))
                self.laby[i, j].BigRoomId = roomId

        for i in range(posX, posX+sizeX, 1):
            for j in range(posY, posY+sizeY, 1):
                neighborsList = [(1, 0), (0, 1), (-1,0), (0,-1)]
                for k in neighborsList:
                    if (i+k[0], j+k[1]) in self.laby.keys() and (self.laby[i+k[0], j+k[1]].BigRoomId == self.laby[i, j].BigRoomId):
                        self.twoWaysLink(i, j, i+k[0], j+k[1])
        return 1

    def addPath(self):
        connected, notConnected = self.connectedAndNot()
        startRoom = random.choice(list(notConnected.values()))
        endRoom = random.choice(list(connected.values()))
        sPos = startRoom.pos
        ePos = endRoom.pos
        distance = (ePos[0]-sPos[0], ePos[1]-sPos[1])
        a, b = sPos[0], sPos[1]
        step = 1 if distance[0] > 0 else -1
        for i in range(step, distance[0]+step, step):
            a, b = i+sPos[0], sPos[1]
            if (a, b) not in self.laby:
                self.laby[a, b] = CRoom((a, b))
            self.twoWaysLink(a, b, a-step, b)

        sPos = (a,b)
        step = 1 if distance[1] > 0 else -1
        for j in range(step, distance[1]+step, step):
            a, b = sPos[0], j+sPos[1]
            if (a, b) not in self.laby:
                self.laby[a, b] = CRoom((a, b))
            self.twoWaysLink(a, b, a, b-step)
        return

    def addPLC(self):
        nbDoors = 4
        while nbDoors > 2: # less than 2 doors already exist
            startRoom = random.choice(list(self.laby.values()))
            nbDoors = startRoom.nbDoors()
        A, B = startRoom.pos[0], startRoom.pos[1]
        count = 0
        count2 = 0
        while count <=2 and count2 < 10:
            direction = random.randint(0,3)
            da, db = dirToXY(direction)
            a , b = A+da, B+db
            if (a, b) not in self.laby:
                self.laby[a, b] = CRoom((a, b))
                self.twoWaysLink(a, b, A, B)
                count += 1
                A, B = a, b
            count2 += 1

    def stepGen(self, n=9):
        room = CRoom((0,0)) # pos = (x, y)
        self.laby = {(0,0) : room} #init starting room
        a, b = 0, 0
        A, B = 0, 0
        roomNumber = 1
        areaTooSmall = 0
        x, y = int(n/12), int(n/12)
        while len(self.laby) <= n: # while there is less than n rooms or that 100 iteration wasn't enough
            if self.createRoom(random.choice([2,2,3,3,3,4,5]), random.choice([2,2,3,3,3,4,5]), random.randint(-x,x), random.randint(-y,y), roomNumber):
                roomNumber += 1
                yield self.laby, (a,b) # yield a intermediary position to enable the following the generation process
            else:
                areaTooSmall += 1
            if areaTooSmall > 2*n:
                areaTooSmall = 0
                x, y = x+2, y+2

        print(roomNumber-1, "rooms created")
        connected, notConnected = self.connectedAndNot()
        nbPath = 0
        while len(list(notConnected.keys())) != 0:
            self.addPath()
            connected, notConnected = self.connectedAndNot()
            nbPath += 1
            yield self.laby, (a,b)
        print(nbPath, "paths created")
        #print(len(list(self.laby.keys())), 2*x*2*y*0.9)
        nbPLC = 0
        while len(list(self.laby.keys())) <  2*x*2*y*0.9:
            #print("adding pointless corridors")
            self.addPLC() #pointless corridor
            nbPLC += 1
            yield self.laby, (a,b)
        print(nbPLC, "PLCs created")

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

        for j in range(y[1], y[0]-1, -1):
            for i in range(x[0], x[1]+1):
                if (i,j) in keylist:
                    if self.laby[(i,j)].isEnd:
                        print("\xb7XX\xb7", end='')
                    elif (i,j) == (0,0):
                        print("\xb7OO\xb7", end='')
                    else:
                        #print("\xb7[]\xb7", end='')
                        print("\xb7{0:2d}\xb7".format(self.aMap[i,j]), end='')
                else:
                    print("\xb7\xb7\xb7\xb7", end='')
            print("")
            if j != y[0]:
                for i in range(x[0], x[1]+1):
                    print("\xb7\xb7\xb7\xb7", end='')
                print("")
        print("\n")
        return


if __name__ == '__main__':

    laby = CLaby()
    laby.initRandom()
    laby.gen(150)
    laby.printLaby()

    # print(laby.laby)
    # for room in laby.laby.values():
    #     if room.isEnd == 1:
    #         endFound = 1
    # if endFound != 1:
    #     print("error multiple/no end(s)")