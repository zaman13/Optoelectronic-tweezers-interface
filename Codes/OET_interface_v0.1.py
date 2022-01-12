

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:34:23 2021

@author: Asif
"""

import pygame
import sys
import numpy as np



pygame.init()
fps=60
fpsclock=pygame.time.Clock()
sur_obj=pygame.display.set_mode((1600,900),pygame.FULLSCREEN)
pygame.display.set_caption("Keyboard_Input")
White=(255,255,255)
background_color=(0,0,0)


p1=[120]  # center of the circles/rings
p2=[120]  # center of the circles/rings

step=5
step_s=1

s1 = [70]     
# s2 = [65,45]
s2 = [6]      # widht of the circles/rings

s3 = [7]

lp = True
border_width = 5


# This function takes the previous coordinates and keyboard input to find the new coordinates of the object position
def move_object(active_ind,p1,p2,key_input):
    if key_input[pygame.K_LEFT]:
        p1[active_ind] -= step
    if key_input[pygame.K_UP]:
        p2[active_ind] -= step
    if key_input[pygame.K_RIGHT]:
        p1[active_ind] += step
    if key_input[pygame.K_DOWN]:
        p2[active_ind] += step

    return p1, p2


# Object scaling function. Changes the size of the object
def scale_object(active_ind,s1,s2,key_input):
    if key_input[pygame.K_a]:
        s1[active_ind] -= step_s
    if key_input[pygame.K_q]:
        s1[active_ind] += step_s
    if key_input[pygame.K_s]:
        s2[active_ind] -= step_s
    if key_input[pygame.K_w]:
        s2[active_ind] += step_s
    if key_input[pygame.K_d]:
        s3[active_ind] -= step_s
    if key_input[pygame.K_e]:
        s3[active_ind] += step_s
    
    
    
    
    if key_input[pygame.K_a]:
        mods = pygame.key.get_mods()
        
        if mods & pygame.KMOD_CTRL:
            s2[active_ind] = 10 + s2[active_ind]
            
      
     # add new object       
    if key_input[pygame.K_n]:
        mods = pygame.key.get_mods()
        
        if mods & pygame.KMOD_CTRL:
            p1.append(30)
            p2.append(30)
            s1.append(70)
            s2.append(6)
            s3.append(7)
            
            
            
            

    return p1, p2, s1, s2, s3



def draw_object(obj_type):
    return 0
    

def open_circle(active_ind):
    pygame.draw.circle(sur_obj, (5,0,0), (p1[active_ind]+s1[active_ind]-0.5*s2[active_ind], p2[active_ind]),s3[active_ind],0)

def draw_window():
    
    for m in range(len(p1)):
        # pygame.draw.rect(sur_obj, (255,0,0), (p1[m], p2[m], s1[m], s2[m]))
        pygame.draw.circle(sur_obj, (255,0,0), (p1[m], p2[m]),s1[m],s2[m])
        # pygame.draw.arc(sur_obj, (255,0,0), (p1[m], p2[m],s1[m],s1[m]),-3, 3, s2[m])
        # pygame.draw.arc(sur_obj, (255,0,0), (p1[m]+0.4, p2[m]-0.4,s1[m],s1[m]-1),-3, 3, s2[m])
        


active_ind = 0

while lp:
    fpsclock.tick(fps)
    sur_obj.fill(background_color)
    
    key_input = pygame.key.get_pressed()   
    
    
    if key_input[pygame.K_1]:
        mods = pygame.key.get_mods()
        
        if mods & pygame.KMOD_CTRL:
            active_ind = 0
 
    if key_input[pygame.K_2]:
        mods = pygame.key.get_mods()
        
        if mods & pygame.KMOD_CTRL:
            active_ind = 1

 
    # if pygame.event.type == pygame.KEYUP & key_input[pygame.K_p]:
    #     mods = pygame.key.get_mods()
        
    #     if  mods & pygame.KMOD_CTRL & len(p1) < active_ind + 1:
    #         active_ind += 1
          
     

    
    draw_window()


    if key_input[pygame.K_o]:
        open_circle(active_ind)
        
    # if key_input[pygame.K_5]:
        # pygame.draw.circle(sur_obj, (255,0,0), (p1, p2),s1)
    
    
    for eve in pygame.event.get():
        if eve.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    p1, p2 = move_object(active_ind,p1,p2,key_input)
    p1,p2, s1, s2, s3 = scale_object(active_ind,s1,s2,key_input)
    

         
        
    if key_input[pygame.K_x]:
        pygame.quit()
 
        
        
    pygame.display.update()
    fpsclock.tick(fps)
    
    

