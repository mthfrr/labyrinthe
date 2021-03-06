# vim:set encoding=utf-8

import os

from PIL import Image, ImageDraw, ImageFont


import labyrinthe
import random


class CMapper():
    def __init__(self):
        self.loadTiles()

    def loadTiles(self, path='./img_map/'):
        self.tiles = {}
        for i in range(2**4):
            s = '{0:04b}'.format(i)
            s = s.replace('0','o')
            s = s.replace('1','x')
            try:
                img = Image.open(path+'%s.png'%(s))
                self.tiles[s] = img
                img = Image.open(path+'%s_d.png'%(s))
                self.tiles[s+'_d'] = img
            except FileNotFoundError:
                img = None
        self.arrow = Image.open(path+'arrow.png')

    def drawMap(self, roomDict, mapName = 'the_map.png', withCoord=False):
        keylist = list(roomDict.keys())
        xMin = min([i for i,j in keylist])
        xMax = max([i for i,j in keylist])+1
        yMin = min([j for i,j in keylist])
        yMax = max([j for i,j in keylist])+1
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax


        dx, dy = self.tiles['oooo'].size # tile png size

        self.fnt = ImageFont.truetype('font/Arial.ttf', 10)
        self.fnt2 = ImageFont.truetype('font/arialbd.ttf', 12)

        image = Image.new('RGB', (dx*(xMax-xMin), dy*(yMax-yMin)))
        drawObj = ImageDraw.Draw(image)

        for j in range(yMax-1, yMin-1,-1):
            for i in range(xMin, xMax):
                try:
                    r = roomDict[(i,j)]
                    s = ''
                    for d in r.doors:
                        if d == 0:
                            s += 'x'  # wall
                        else:
                            s += 'o'  # door
                    if not r.BigRoomId:
                        s += '_d'
                    im = self.tiles[s]
                except KeyError:
                    im = self.tiles['xxxx']
                    r = None

                x,y = dx*(i-xMin), dy*(yMax-j-1)
                image.paste(im, (x, y))
                if withCoord:
                    if (i,j) == (0,0):
                        drawObj.text((x+dx/2-10,y+dy/2-10), "%d %d"%(i,j), font=self.fnt2, fill=(255, 0, 0))
                    else:
                        drawObj.text((x+dx/2-10,y+dy/2-10), "%d %d"%(i,j), font=self.fnt, fill=(0, 0, 0))

        i,j = 0,0
        msg = 'GO'
        x,y = dx*(i-xMin), dy*(yMax-j-1)
        w, h = drawObj.textsize(msg, font=self.fnt2)
        drawObj.text((x+dx/2-w/2,y+dy/2-h/2), msg, font=self.fnt2, fill=(255, 0, 0))

        self.image = image
        self.drawObj = drawObj

    def writeInRoom(self, msg, coord, fill=(0, 255, 0)):
        i,j = coord
        dx, dy = self.tiles['oooo'].size
        x,y = dx*(i-self.xMin), dy*(self.yMax-j-1)

        w, h = self.drawObj.textsize(msg, font=self.fnt2)
        self.drawObj.text((x+dx/2-w/2,y+dy/2-h/2), msg, font=self.fnt2, fill=fill)

    def drawInRoom(self, direction, coord):
        i,j = coord
        dx, dy = self.tiles['oooo'].size
        x,y = dx*(i-self.xMin), dy*(self.yMax-j-1)

        im = self.arrow.rotate( 90*direction, expand=1 )
        self.image.paste(im, (x, y), im)


    def saveMap(self, mapName = 'the_map.png'):
        self.image.save(mapName)


if __name__ == '__main__':
    N = 50
    seed = 8
    seed = random.randint(1,256)

    laby = labyrinthe.CLaby()
    mapper = CMapper()

    filelist = [ f for f in os.listdir("mapsOut") if f.endswith(".png") ]
    for f in filelist:
        os.remove(os.path.join("mapsOut", f))

    filelist = [ f for f in os.listdir("mapsSpread") if f.endswith(".png") ]
    for f in filelist:
        os.remove(os.path.join("mapsSpread", f))

    laby.initRandom(seed)
    for no, (rooms, (i,j)) in enumerate(laby.stepGen(N)):
        mapper.drawMap(rooms)
        mapper.saveMap('mapsOut/the_map_%03d.png'%(no))

    laby.initRandom(seed)
    laby.gen(N)

    mapper.drawMap(laby.laby)
    mapper.writeInRoom( 'START', (0,0) )
    mapper.writeInRoom( 'END', laby.end )
    mapper.saveMap('the_map.png')

    aMap = laby.spread(laby.end)
    for k,v in aMap.items():
        mapper.writeInRoom( '%d'%(v), k )
    mapper.saveMap('the_map_with_distance.png')


    no = 0
    for frontiere, aMap in laby.spreadGen(laby.end):
        mapper.drawMap(laby.laby)
        for k,v in aMap.items():
            if k in frontiere:
                mapper.writeInRoom( '%d'%(v), k, (255, 0, 0))
            else:
                mapper.writeInRoom( '%d'%(v), k )
        mapper.saveMap('mapsSpread/the_map_%03d.png'%(no))
        no += 1


    mapper.drawMap(laby.laby)
    for aRoom in laby.laby.values():
        mapper.drawInRoom(laby.dirToEnd(aRoom.pos), aRoom.pos)
        mapper.writeInRoom( '%d'%(laby.dirToEnd(aRoom.pos)), aRoom.pos )
    mapper.writeInRoom( 'START', (0,0) )
    mapper.writeInRoom( 'END', laby.end )

    mapper.saveMap('the_map_with_hint.png')

