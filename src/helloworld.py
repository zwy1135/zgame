# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 16:50:51 2014

@author: wy
"""

background_img = "../data/image/sushiplate.jpg"
mouse_img = "../data/image/fugu.png"

import pygame
from pygame.locals import *
from sys import exit

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((640,480),0,32)
    
    pygame.display.set_caption("hello world!")
    
    background = pygame.image.load(background_img).convert()
    mouse = pygame.image.load(mouse_img).convert_alpha()
    
    while True:
        event = pygame.event.poll()
        if event.type == QUIT:
            exit()
        
        screen.blit(background,(0,0))
        
        x,y = pygame.mouse.get_pos()
        
        x -= mouse.get_width()/2
        y -= mouse.get_height()/2
        
        screen.blit(mouse,(x,y))
        
        pygame.display.update()
        
if __name__ == "__main__":
    main()