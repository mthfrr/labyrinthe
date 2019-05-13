import pygame as pg

import sys
import os
path = os.path.dirname(os.path.abspath(__file__))
os.chdir(path)

import labyrinthe5 as labyrinthe

### COLOR
BLACK=[0,0,0]
WHITE=[255,255,255]
RED=[255,0,0]
GREEN=[0,255,0]
slate_gray=[112,138,144]
dark_slate_blue=[72,61,139]

pg.init()

### SCREEN
Largeur=800
Hauteur=600
SIZE=[Largeur, Hauteur]

screen=pg.display.set_mode(SIZE)

pg.display.set_caption("Lab")

background = pg.image.load('back.png').convert()


### LABYRINTHE
laby = labyrinthe.CLaby()

laby.initRandom(8)

laby.gen(30)

laby.printLaby()

print(laby.laby[0,0].doors)
screen.blit(background, (0,0))


### BOUSSOLE

compass = pg.image.load('img/compass.png')
def boussole(dir) :
    screen.blit(pg.transform.rotate(compass, 90*(-dir%4)), (0,0))
    return

boussole(0)

### TEXTURES

dir = 0
x=0
y=0
coor=[x,y]

welcome1 = pg.image.load('img\welcomeScreen_1.png')
welcome2 = pg.image.load('img\welcomeScreen_2.png')
welcome3 = pg.image.load('img\welcomeScreen_3.png')
screen.blit(welcome1, (0,0))
pg.display.flip()

class ImageNotFoundError(Exception): pass

class CImage():
    def __init__(self, type, posx, posy, orientation):
        self.type = type
        self.posx = posx
        self.posy = posy
        self.orientation = orientation
        self.dist = abs(posx*10)+abs(posy)+0.1
        if orientation == 0:
            self.dist += 0.1
        if orientation == 2:
            self.dist -= 0.1
        if type in ("floor","pavement"):
            self.dist += 1000


        try:
            self.image = pg.image.load('img/tiles/%s%0+2d%+02d_%d.png'%(self.type, self.posx, self.posy, self.orientation))
        except pg.error:
            if os.path.isfile('img/tiles/%s%0+2d%+02d_%d.empty'%(self.type, self.posx, self.posy, self.orientation)):
                self.image = None
            else:
                raise ImageNotFoundError

    def render(self):
        if self.image:
            screen.blit(self.image, (0,0))
        #pg.display.flip()
        #pg.time.delay(500)


images = set()



def load():
    loaded = {}
    for step, obj in enumerate(['floor', 'pavement', 'wall', 'tunnel']):
        for i in range (4):
            for j in range (-10, 10):
                for k in range (4):
                    try:
                        loaded[obj, i, j, k] = CImage(obj, i, j, k%4)
                    except ImageNotFoundError:
                        #print ('skipping %s %d %d %d'%(obj, i,j,k))
                        pass

        screen.blit(pg.image.load('img\welcomeScreen_%d.png'%(step+1)), (0,0))
        pg.display.flip()
    return loaded


loaded = load()
#print(loaded)





def construction (aRoom, direction, i, j, images, loaded):
    #print(isDoors)
    isDoors = aRoom.doors
    screen.blit(background, (0,0))
    if aRoom.BigRoomId == 0:
        im = loaded["floor", i, j, (direction)%4]
    else:
        im = loaded["pavement", i, j, (direction)%4]
    images.add(im)
    for d in range (4):
        if isDoors[d] == 0 :
            im = loaded["wall", i, j, (d-direction)%4]
        else:
            im = loaded["tunnel", i, j, (d-direction)%4]
        images.add(im)

construction(laby.laby[x,y], dir,0 ,0, images, loaded)

images = sorted(images, key=lambda x: x.dist, reverse=True)
for im in  images:
    im.render()

boussole(dir)


def voisins(aRoom, userDir, i, j, images, disti, distj):
    if disti >= 3:
        return
    if distj > disti+1:
        return
    r = aRoom.doors[userDir%4]
    if r != 0:
        construction (r, dir%4, i+1, j, images, loaded)
        voisins(r, userDir, i+1, j, images, disti+1, distj)
    r = aRoom.doors[(userDir+1)%4]
    if r != 0:
        construction (r, dir%4, i, j+1, images, loaded)
        voisins(r, userDir, i, j+1, images, disti, distj+1)
    r = aRoom.doors[(userDir+3)%4]
    if r != 0:
        construction (r, dir%4, i, j-1, images, loaded)
        voisins(r, userDir, i, j-1, images, disti, distj+1)




def affichage(userRoom, userDir) :
    images = set()
    construction (userRoom, userDir, 0, 0, images, loaded)
    voisins(userRoom, userDir, 0, 0, images, 0, 0)
    images = sorted(images, key=lambda x: x.dist, reverse=True)
    for im in images :
        im.render()
    boussole(dir)
    pg.display.flip()


VECT = [(1,0),(0,1),(-1,0),(0,-1)]

affichage(laby.laby[x,y], dir)


pg.display.flip()
#exit()

### BOUCLE INFINIE
while 1:
    for event in pg.event.get() :
        if event.type==pg.QUIT:
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == 273: #haut
                if laby.laby[x,y].doors[dir%4] != 0:
                    dx, dy = VECT[dir%4]
                    x += dx
                    y += dy
            elif event.key == 274: #bas
                if laby.laby[x,y].doors[(dir+2)%4] != 0:
                    dx, dy = VECT[dir%4]
                    x -= dx
                    y -= dy
            elif event.key == 275: #droite
                dir-=1
            elif event.key == 276: #gauche
                dir+=1
            elif event.key == 27: #échap
                pg.quit()
            print(x,y)
            affichage(laby.laby[x,y], dir)
            if laby.laby[x,y].isEnd:
                pg.time.delay(500)
                screen.blit(background, (0,0))
                pg.display.flip()
                pg.time.delay(2000)
                pg.quit()


pg.quit()
