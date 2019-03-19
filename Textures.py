import pygame as pg

import sys
import os
os.chdir('R:\Projet isn')
import numpy as np

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





### TEXTURES 

k_ini = 0       #coordonnée en k initiale
i_ini = 0       #coordonnée en i initiale
j_ini=0         #coordonnée en j initiale
skin = "A"



def keypressed(x, y, z) :
    print ("a")
    background = pg.image.load('back.png').convert()
    screen.blit(background, (0, 0))
    i=x
    for j in range((y+3)%4, y-1, -1):
        k = 1
        name = "tunnel"
        screen.blit(pg.image.load('img/%s_%s%0+4d%+04d_%+04d.png'%(name, skin, i, j, k)), (0,0))
        name = "dalle"
        screen.blit(pg.image.load('img/%s_%s%0+4d%+04d_%+04d.png'%(name, skin, i, j, k)), (0,0))
        name = "mur"
        k = 0
        screen.blit(pg.image.load('img/%s_%s%0+4d%+04d_%+04d.png'%(name, skin, i, j, k)), (0,0))
        k = 2
        screen.blit(pg.image.load('img/%s_%s%0+4d%+04d_%+04d.png'%(name, skin, i, j, k)), (0,0))
    return


keypressed(i_ini, j_ini, k_ini)

### BOUCLE INFINIE
while 1:
    for event in pg.event.get() :
        if event.type==pg.QUIT:
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == 273:
                print(event.key)
                j_ini=j_ini-1
                print (j_ini)
                keypressed(i_ini, j_ini, k_ini) 
            elif event.key == 274:
                print(event.key)
            elif event.key == 275:
                print(event.key)
            elif event.key == 276:
                print(event.key)
            else:
                print(event.key) 
                    
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