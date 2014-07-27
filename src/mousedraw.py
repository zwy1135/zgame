# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 00:23:40 2014

@author: wy
"""

import pygame
from pygame.locals import *
from sys import exit
from random import randint

def main():
    screen = pygame.display.set_mode((640,480),0,32)
    pygame.display.set_caption("mouse draw")
    draw_flag = False    
    
    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            draw_flag = True
        elif event.type == MOUSEBUTTONUP:
            draw_flag = False
        elif draw_flag and event.type == MOUSEMOTION:
            rancol = (randint(0,255),randint(0,255),randint(0,255))
            screen.set_at(event.pos,rancol)
        
        pygame.display.update()
        
if __name__=="__main__":
    main()
        