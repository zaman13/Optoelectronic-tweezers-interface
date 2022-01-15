

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:34:23 2021

@author: Mohammad Asif Zaman


Keyboard commands:
    
Arrow keys: Movement
q         : Increase object size
a         : Decrease object size
w         : Increase width of the object
d         : Decrease width of the object
CTRL + n  : Create new object
CTRL + 1  : Select object 1
CTRL + 2  : Select object 2
Delete    : Delete selected object
=         : Select next object
-         : Select previous object
o         : Create opening
r         : Rotate opening clockwise
f         : Rotate opening counter-clockwise

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

px_default = 120
py_default = 120
rot_default = 0

px=[px_default]  # center of the circles/rings
py=[py_default]  # center of the circles/rings
rot = [0]

step=5
step_s=1
step_rot = np.pi/100

s1 = [70]     
# s2 = [65,45]
s2 = [6]      # widht of the circles/rings

s3 = [7]

lp = True
border_width = 5


# This function takes the previous coordinates and keyboard input to find the new coordinates of the object position
def move_object(active_ind, key_input):
    if key_input[pygame.K_LEFT]:
        px[active_ind] -= step
    if key_input[pygame.K_UP]:
        py[active_ind] -= step
    if key_input[pygame.K_RIGHT]:
        px[active_ind] += step
    if key_input[pygame.K_DOWN]:
        py[active_ind] += step

    return 0


# Object scaling function. Changes the size of the object
def scale_object(active_ind, key_input):
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
    if key_input[pygame.K_r]:
        rot[active_ind] += step_rot
    if key_input[pygame.K_f]:
        rot[active_ind] -= step_rot
       
    
    
    
    if key_input[pygame.K_a]:
        mods = pygame.key.get_mods()
        
        if mods & pygame.KMOD_CTRL:
            s2[active_ind] = 10 + s2[active_ind]
            

    return 0



def rotate(x,y,xo,yo,theta): #rotate x,y around xo,yo by theta (rad)
    xr=np.cos(theta)*(x-xo)-np.sin(theta)*(y-yo)  + xo
    yr=np.sin(theta)*(x-xo)+np.cos(theta)*(y-yo)  + yo
    return [xr,yr]
    


def new_object(event,active_ind):
   if event.key ==  pygame.K_n:
       mods = pygame.key.get_mods()
        
       if mods & pygame.KMOD_CTRL:
           px.append(px_default)
           py.append(py_default)
           s1.append(70)
           s2.append(6)
           s3.append(7) 
           rot.append(0)
           active_ind += 1
  
   return active_ind




# change active object selection or delete selected object
def change_active_object(event,active_ind):
    # select next active object
    if event.key ==  pygame.K_EQUALS:
        if len(px) > active_ind + 1: 
            active_ind += 1
    

    # select previous active object            
    if event.key ==  pygame.K_MINUS:
        if  active_ind  > 0: 
            active_ind -= 1           
    
    
    # delete active object
    if event.key ==  pygame.K_DELETE:
        del px[active_ind]
        del py[active_ind]
        del s1[active_ind]
        del s2[active_ind]
        del s3[active_ind]
        active_ind = 0
    
    
    return active_ind
            
            
            

    
# Create opening in the circle

def open_circle(active_ind):
    # Draws a circle in black color to create opening in the object
    tx = px[active_ind]+s1[active_ind]-0.5*s2[active_ind]  # x coordinate of the opening is set at the middle of the right rim along x axis
    ty = py[active_ind]                                    # y coordinate of the opening is the same as the y coordinate of the object
    
    [tx,ty] = rotate(tx,ty,px[active_ind],py[active_ind],rot[active_ind])
   
    
    pygame.draw.circle(sur_obj, (5,0,0), (tx, ty),s3[active_ind],0)
    return 0



def draw_window():
    
    for m in range(len(px)):
        # pygame.draw.rect(sur_obj, (255,0,0), (px[m], py[m], s1[m], s2[m]))
        pygame.draw.circle(sur_obj, (255,0,0), (px[m], py[m]),s1[m],s2[m])
        # pygame.draw.arc(sur_obj, (255,0,0), (px[m], py[m],s1[m],s1[m]),-3, 3, s2[m])
        # pygame.draw.arc(sur_obj, (255,0,0), (px[m]+0.4, py[m]-0.4,s1[m],s1[m]-1),-3, 3, s2[m])
        


active_ind = 0

while lp:
    fpsclock.tick(fps)
    sur_obj.fill(background_color)
    
    key_input = pygame.key.get_pressed()   
    
    
    move_object(active_ind, key_input)
    scale_object(active_ind, key_input)
    
    
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
                active_ind = new_object(event, active_ind)
                active_ind = change_active_object(event, active_ind)


            
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
        
    #     if  mods & pygame.KMOD_CTRL & len(px) < active_ind + 1:
    #         active_ind += 1
          
     

    
    draw_window()


    if key_input[pygame.K_o]:
        open_circle(active_ind)
        
    # if key_input[pygame.K_5]:
        # pygame.draw.circle(sur_obj, (255,0,0), (px, py),s1)
    
    
  
    
    
    
    


         
        
    if key_input[pygame.K_x]:
        pygame.quit()
 
        
        
    pygame.display.update()
    fpsclock.tick(fps)
    
    

