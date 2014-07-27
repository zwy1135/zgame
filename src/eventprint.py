# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 17:58:51 2014

@author: wy
"""

SCREEN_SIZE = (640,480)

import pygame
from pygame.locals import *
from sys import exit

def main():
    pygame.init()
    
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
    pygame.display.set_caption("event print")
    font = pygame.font.SysFont("arial.ttf",18)
    font_height = font.get_height()
    font_width = font_height
    count = 0
    char = 'a'
    flag = False
    
    while True:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            char = event.unicode
            flag = True
        elif event.type == KEYUP:
            flag = False
        elif event.type == QUIT:
            exit()
        if flag:
            count += 1
            screen.blit(font.render(char,True,(0,233,233)),(count*font_width%SCREEN_SIZE[0],int(count*font_width/SCREEN_SIZE[0])*font_height))
        
        pygame.display.update()
        
        

if __name__ == "__main__":
    main()