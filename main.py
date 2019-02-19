#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import os
import pygame as pg
import numpy as np   

class Display:
	def __init__(self):
		return
	
	
## colors
BLACK = [0,0,0]
WHITE = [255,255,255]
RED = [150,0,0]
GRAY = [20,20,20]

SCREENWIDTH=800
SCREENHEIGHT=800

pg.init()


## screen
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pg.display.set_mode(size)
pg.display.set_caption('Window1')
screen.fill(GRAY)


pg.display.flip()
clock = pg.time.Clock()

## prog


## loop
pg.display.flip()

while  1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
        #print(event)
    
    pg.display.flip()
    clock.tick(60)

pg.quit()