# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 22:35:42 2014

@author: wy
"""

import pygame as pg
from pygame.locals import *
from sys import exit
from math import *
from gameobjects.vector2 import Vector2

background_img = "../data/image/sushiplate.jpg"
sprite_img = "../data/image/fugu.png"

def main():
    
    screen = pg.display.set_mode((640,480),0,32)
    pg.display.set_caption("follow mouse")
    
    background = pg.image.load(background_img).convert()
    sprite = pg.image.load(sprite_img).convert_alpha()
    
    clock = pg.time.Clock()
    
    sprite_position = Vector2()
    mouse_position = Vector2()
    heading = Vector2()
    I = Vector2()
    
    while True:
        event = pg.event.poll()
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEMOTION:
            mouse_position = Vector2.from_iter(event.pos)
            
        time_passed = clock.tick(30)/1000.0
        
        vector_to_mouse = Vector2.from_points(sprite_position,mouse_position) - Vector2(*sprite.get_size())/2
        I += vector_to_mouse      
        
        heading = vector_to_mouse * 10 + I * 0.3
        sprite_position += heading * time_passed
        
        screen.blit(background,(0,0))
        screen.blit(sprite,sprite_position)
        
        pg.display.update()
        
if __name__=="__main__":
    main()
        
    
    
