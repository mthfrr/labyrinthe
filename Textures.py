import pygame as pg

import sys
import os
os.chdir('R:\Projet isn')
import numpy as np
import labyrinthe

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

laby.gen(30)

laby.printLaby()

print(laby.laby[0,0].doors)
screen.blit(background, (0,0))


### BOUSSOLE

compass = pg.image.load('compass.png')
def boussole(dir) :
    screen.blit(pg.transform.rotate(compass, 90*(dir%4)), (0,0))
    return

boussole(0)

### TEXTURES 

dir = 0
x=0
y=0
coor=[x,y] 

def render (type, skin, posx, posy, orientation) :
    screen.blit(pg.image.load('img/A/%s_%s%0+4d%+04d_%+04d.png'%(type, skin, posx, posy, orientation)), (0,0))
    
    
    return

def cardinaux (coord) :
    if laby.laby[coord[0],coord[1]].doors[0] == 0 :
        East = 0
    else :
        East = 1
    if laby.laby[coord[0],coord[1]].doors[1] == 0 :
        North = 0
    else :
        North = 1
    if laby.laby[coord[0],coord[1]].doors[2] == 0 :
        West = 0
    else :
        West = 1
    if laby.laby[coord[0],coord[1]].doors[3] == 0 :
        South = 0
    else :
        South = 1
    return [East, North, West, South]



def construction (East, North, West, South, direction) :
    screen.blit(background, (0,0))
    render ("floor", "stones", 0, 0, (dir)%4)
    if South == 1 :
        render ("Arch", "stones", 0, 0, (-dir+3)%4)
    else :
        render ("wall", "stones", 0, 0, (-dir+3)%4)
    if North == 1 :
        render ("Arch", "stones", 0, 0, (-dir+1)%4)
    else :
        render ("wall", "stones", 0, 0, (-dir+1)%4)
    if East == 1 :
        render ("Arch", "stones", 0, 0, (-dir)%4)
    else :
        render ("wall", "stones", 0, 0, (-dir)%4)
    if West == 1 :
        render ("Arch", "stones", 0, 0, (-dir+2)%4)
    else :
        render ("wall", "stones", 0, 0, (-dir+2)%4)
    boussole(dir)
    print(cardinaux(coor))
    print(dir%4)
    print(coor)
    return
    
construction(cardinaux(coor)[0], cardinaux(coor)[1], cardinaux(coor)[2], cardinaux(coor)[3], dir)




### BOUCLE INFINIE
while 1:
    for event in pg.event.get() :
        if event.type==pg.QUIT:
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == 273: #haut
                if dir%4 == 0 and cardinaux(coor)[1] == 1 :
                    coor[1]+=1
                    construction (cardinaux(coor)[0], cardinaux(coor)[1], cardinaux(coor)[2], cardinaux(coor)[3], dir)
                elif dir%4 == 1 and cardinaux(coor)[2] == 1 :
                    coor[0]-=1
                    construction (cardinaux(coor)[0], cardinaux(coor)[1], cardinaux(coor)[2], cardinaux(coor)[3], dir)
                elif dir%4 == 2 and cardinaux(coor)[3] == 1 :
                    coor[1]-=1
                    construction (cardinaux(coor)[0], cardinaux(coor)[1], cardinaux(coor)[2], cardinaux(coor)[3], dir)
                elif dir%4 == 3 and cardinaux(coor)[0] == 1 :
                    coor[0]+=1
                    construction (cardinaux(coor)[0], cardinaux(coor)[1], cardinaux(coor)[2], cardinaux(coor)[3], dir)
            elif event.key == 274: #bas
                pass
            elif event.key == 275: #droite
                dir-=1
                construction (cardinaux(coor)[0], cardinaux(coor)[1], cardinaux(coor)[2], cardinaux(coor)[3], dir)
            elif event.key == 276: #gauche
                dir+=1
                construction (cardinaux(coor)[0], cardinaux(coor)[1], cardinaux(coor)[2], cardinaux(coor)[3], dir)
        else :
            pass
                    
        pg.display.flip()    
pg.quit()



'''

### CLOCK
clock = pg.time.Clock()

crashed = False

while not crashed:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            crashed = True

        print(event)

    pg.display.update()
    clock.tick(60)
'''
