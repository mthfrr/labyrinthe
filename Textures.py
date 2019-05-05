import pygame as pg

import sys
import os
os.chdir('D:\Projet_isn')
import labyrinthe4 as labyrinthe

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

laby.gen(150)

laby.printLaby()

print(laby.laby[0,0].doors)
screen.blit(background, (0,0))


### BOUSSOLE

compass = pg.image.load('compass.png')
def boussole(dir) :
    screen.blit(pg.transform.rotate(compass, 90*(-dir%4)), (0,0))
    return

boussole(0)

### TEXTURES

dir = 0
x=0
y=0
coor=[x,y]

class CImage():
    def __init__(self, type, skin, posx, posy, orientation):
        self.type = type
        self.skin = skin
        self.posx = posx
        self.posy = posy
        self.orientation = orientation
        self.dist = abs(posx*10)+abs(posy)+0.1
        if orientation == 0:
            self.dist += 0.1
        if orientation == 2:
            self.dist -= 0.1
        if type == "floor":
            self.dist += 0.2

    def render(self):
        drawImage(self.type, self.skin, self.posx, self.posy, self.orientation)
        #pg.display.flip()
        #pg.time.delay(500)

loaded = {}

def drawImage (type, skin, posx, posy, orientation):
    name = 'img/A/%s_%s%0+4d%+04d_%+04d.png'%(type, skin, posx, posy, orientation)
    if name in loaded:
        img=loaded[name]
    else:
        img = pg.image.load(name)
        print (name)
        loaded[name] = img
    screen.blit(img, (0,0))

images = set()

def construction (aRoom, direction, i, j, images):
    #print(isDoors)
    isDoors = aRoom.doors
    screen.blit(background, (0,0))
    im = CImage ("floor", "stones", i, j, (direction)%4)
    images.add(im)
    for d in range (4):
        if isDoors[d] == 0 :
            im = CImage ("wall", "stones", i, j, (d-direction)%4)
        else:
            im = CImage ("tunnel", "stones", i, j, (d-direction)%4)
        images.add(im)

construction(laby.laby[x,y], dir,0 ,0, images)

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
        construction (r, dir%4, i+1, j, images)
        voisins(r, userDir, i+1, j, images, disti+1, distj)
    r = aRoom.doors[(userDir+1)%4]
    if r != 0:
        construction (r, dir%4, i, j+1, images)
        voisins(r, userDir, i, j+1, images, disti, distj+1)
    r = aRoom.doors[(userDir+3)%4]
    if r != 0:
        construction (r, dir%4, i, j-1, images)
        voisins(r, userDir, i, j-1, images, disti, distj+1)




def affichage(userRoom, userDir) :
    images = set()
    construction (userRoom, userDir, 0, 0, images)
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
            elif event.key == 27:
                pg.quit()
            affichage(laby.laby[x,y], dir)

pg.quit()
