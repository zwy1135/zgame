# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 16:27:23 2014

@author: wy
"""

import pygame
from pygame.locals import *
from gameobjects.vector2 import Vector2
from sys import exit
from random import randint


SCREEN_SIZE = (800,600)
NEST_POSITION = (SCREEN_SIZE[0]/2,SCREEN_SIZE[1]/2)
NEST_SIZE = 200
ANT_COUNT_START = 10






class State():
    def __init__(self,name):
        self.name = name
        
    def do_action(self):
        pass
    
    def entry_action(self):
        pass
    
    def exit_action(self):
        pass
    
    def check_condition(self):
        pass

class StateMachine():
    def __init__(self):
        self.states = {}
        self.active_state = None
        
    def add_state(self,state):
        self.states[state.name] = state
        
    def set_state(self,state_name):
        if self.active_state != None:
            self.active_state.exit_action()
        self.active_state = self.states[state_name]
        self.active_state.entry_action()
        
    def process(self):
        if self.active_state == None:
            return None
        self.active_state.do_action()
        new_state_name = self.active_state.check_condition()
        if new_state_name != None:
            self.set_state(new_state_name)
            
            
class AntStateExploring(State):
    def __init__(self,ant):
        State.__init__(self,"exploring")
        self.ant = ant
        
    def random_destination(self):
        w,h = SCREEN_SIZE
        self.ant.destination = Vector2(randint(0,w),randint(0,h))
        print "setting %s des to %s"%(str(self.ant),str(self.ant.destination))
        
    def do_action(self):
        if self.ant.location.get_distance_to(self.ant.destination)<2:
            self.random_destination()
            
    def entry_action(self):
        self.ant.speed = 120
        self.random_destination()
        
    def check_condition(self):
        leaf = self.ant.world.get_close_entity("leaf",self.ant.location)
        if leaf != None:
            self.ant.leaf_id = leaf.id
            return "seeking"
            
        spider = self.ant.world.get_close_entity("spider",self.ant.location)
        if spider != None:
            self.ant.spider_id = spider.id
            return "hunting"
        
        return None
        
class AntStateSeeking(State):
    def __init__(self,ant):
        State.__init__(self,"seeking")
        self.ant = ant
        
    def entry_action(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        self.ant.destination = leaf.location
        self.ant.speed = 160 + randint(-20,20)
        
    def check_condition(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf == None:
            return "exploring"
        elif self.ant.location.get_distance_to(leaf.location)<1:
            return "delivering"
        return None
        
    def exit_action(self):
        leaf = self.ant.world.get(self.ant.leaf_id)
        if leaf != None:
            self.ant.carry(leaf.image)
            self.ant.world.remove_entity(leaf.id)
        
class AntStateDelivering(State):
    def __init__(self,ant):
        State.__init__(self,"delivering")
        self.ant = ant
        
    def entry_action(self):
        self.ant.destination = Vector2(*NEST_POSITION)
        self.ant.speed = 60
        
    def check_condition(self):
        distance = self.ant.location.get_distance_to(Vector2(*NEST_POSITION))
        if distance < NEST_SIZE:
            return "exploring"
            
            
    def exit_action(self):
        self.ant.drop()
        
class AntStateHunting(State):
    def __init__(self,ant):
        State.__init__(self,"hunting")
        self.ant = ant
        
    def entry_action(self):
        self.speed = 160
        
    def do_action(self):
        spider =self.ant.world.get(self.ant.spider_id)
        if spider == None:
            return
        self.ant.destination = spider.location
        distance = self.ant.location.get_distance_to(spider.location)        
        if distance < 10:
            spider.bitten()
            
    def check_condition(self):
        spider = self.ant.world.get(self.ant.spider_id)
        if spider == None:
            return "exploring"
        elif spider.health <= 0:
            self.ant.gotKill = True
            return "delivering"
            
    def exit_action(self):
        spider = self.ant.world.get(self.ant.spider_id)
        if spider != None:
            self.ant.carry(spider.image)
            self.ant.world.remove_entity(self.ant.spider_id)
            
class SpiderStateHunting(State):
    def __init__(self,spider):
        State.__init__(self,"hunting")
        self.spider = spider
        
    def do_action(self):
        ant = self.spider.world.get(self.spider.ant_id)
        if ant == None:
            ant = self.spider.world.get_close_entity("ant",self.spider.location)
            if ant != None:
                self.spider.ant_id = ant.id
        if ant == None:
            return None
        else:
            self.spider.destination = ant.location
            distance = self.spider.location.get_distance_to(ant.location)
            if distance < 10:
                ant.bitten()
        
        
            
            
            
            
            


class GameEntity(object):
    def __init__(self,world,name,image):
        self.world = world
        self.name = name
        self.image = image
        self.location = Vector2()
        self.destination = Vector2()
        self.speed = 0
        self.brain = StateMachine()
        self.id = 0
        
    def __repr__(self):
        return "%s:%s"%(str(self.name),str(self.id))
        
    def render(self,surface):
        location = self.location - Vector2(*self.image.get_size())/2
        surface.blit(self.image,location)
        
    def process(self,timepassed):
        self.brain.process()
        if self.speed > 0 and self.location != self.destination:
            vec_to_dest = self.destination - self.location
            distance = vec_to_dest.get_length()
            heading = vec_to_dest.get_normalized()
            movement = min(distance,timepassed * self.speed)
            self.location += movement * heading
            
class Leaf(GameEntity):
    def __init__(self,world,image):
        GameEntity.__init__(self,world,"leaf",image)
        
class Spider(GameEntity):
    def __init__(self,world,image):
        GameEntity.__init__(self,world,"spider",image)
        self.health = 25
        self.speed = 50 + randint(-20,20)
        self.ant_id = None
        self.brain.add_state(SpiderStateHunting(self))
        
    def bitten(self):
        self.health -= randint(0,10)
        if self.health <= 0:
            self.image = pygame.transform.flip(self.image,0,1)
            
    def render(self,surface):
        GameEntity.render(self,surface)
        w,h = self.image.get_size()
        x,y = self.location
        bar_x = x-12
        bar_y = y + h
        surface.fill((255,0,0),(bar_x,bar_y,25,4))
        surface.fill((0,255,0),(bar_x,bar_y,self.health,4))
        

class Ant(GameEntity):
    def __init__(self,world,image):
        GameEntity.__init__(self,world,"ant",image)
        self.leaf_id = None
        self.spider_id = None
        self.gotKill = False
        self.carry_image = None
        for state in [AntStateExploring(self),AntStateSeeking(self),AntStateDelivering(self),AntStateHunting(self)]:
            self.brain.add_state(state)
            
    def bitten(self):
        self.world.remove_entity(self.id)
        
    def render(self,surface):
        GameEntity.render(self,surface)
        #font = pygame.font.SysFont("arial.ttf",18)
        #id_img = font.render(str(self.id),True,(255,0,0))
        #surface.blit(id_img,self.location)
        if self.carry_image != None:
            x,y = self.location
            w,h = self.carry_image.get_size()
            surface.blit(self.carry_image,(x-w,y-h/2))
            
    def carry(self,image):
        self.carry_image = image
        
    def drop(self):
        self.carry_image = None
        count = 1
        if self.gotKill:
            count = 5
            self.gotKill = False
        for i in range(count):
            print "add",
            new_ant = Ant(self.world,self.image)
            new_ant.location = Vector2(self.location)
            new_ant.brain.set_state("exploring")
            self.world.add_entity(new_ant)
            print new_ant
        
            
        
           

            
class World(object):
    def __init__(self):
        self.entities = {}
        self.entity_id = 0
        
        self.background = pygame.Surface(SCREEN_SIZE)
        self.background.fill((255,255,255))
        pygame.draw.circle(self.background,(0,255,0),NEST_POSITION,NEST_SIZE)
        
    def add_entity(self,entity):
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1
        
    def remove_entity(self,entity_id):
        self.entities.pop(entity_id,None)
        
    def get(self,entity_id):
        return self.entities.get(entity_id)
        
    def render(self,surface):
        surface.blit(self.background,(0,0))
        for entity in self.entities.values():
            #print "rendering",entity,
            entity.render(surface)
            
        #print ""
            
    def get_close_entity(self,name,position,distance = 100):
        for entity in self.entities.values():
            if entity.name == name:
                if position.get_distance_to(entity.location) < distance:
                    return entity
        return None
        
    def process(self,timepassed):
        #print self.entities.values()
        for entity in self.entities.values():
            entity.process(timepassed)
            
def run():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE,0,32)
    world = World()
    clock = pygame.time.Clock()
    
    ant_image = pygame.image.load("../data/image/ant.png").convert_alpha()
    leaf_image = pygame.image.load("../data/image/leaf.png").convert_alpha()
    spider_image = pygame.image.load("../data/image/spider.png").convert_alpha()
    
    w,h = SCREEN_SIZE
    
    for i in range(ANT_COUNT_START):
        new_ant = Ant(world,ant_image)
        new_ant.location = Vector2(*NEST_POSITION)
        new_ant.brain.set_state("exploring")
        world.add_entity(new_ant)
        
    while True:
        event = pygame.event.poll()
        if event.type == QUIT:
            exit()
        
        timepassed = clock.tick(30)/1000.0
        
        if randint(0,20)==0:
            new_leaf = Leaf(world,leaf_image)
            new_leaf.location = Vector2(randint(0,w),randint(0,h))
            world.add_entity(new_leaf)
            
        if randint(0,50) == 0:
            new_spider = Spider(world,spider_image)
            new_spider.brain.set_state("hunting")
            new_spider.location = Vector2(randint(0,w),randint(0,h))
            world.add_entity(new_spider)
            
        world.process(timepassed)
        world.render(screen)
        
        pygame.display.update()
        
        
if __name__=="__main__":
    run()
    
    
    
    
        