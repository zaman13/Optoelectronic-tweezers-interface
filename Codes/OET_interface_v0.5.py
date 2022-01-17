

# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 20:34:23 2021

@author: Mohammad Asif Zaman


Keyboard commands:
    
x         : Quit/exit program    
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
r         : Rotate opening counter-clockwise
f         : Rotate opening clockwise
e         : Increase radius of the opening
f         : Decrease radius of the opening
CTRL + r  : Increase red color of the active object
CTRL + g  : Increase green color of the active object
CTRL + b  : Increase blue color of the active object
ALT + r   : Decrease red color of the active object
ALT + g   : Decrease green color of the active object
ALT + b   : Decrease blue color of the active object 

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
default_foreground_color = (0,255,0)

px_default = 120
py_default = 120
rot_default = 0

radius_default = 70
width_default = 6
opening_radius_default = 10

FR = [default_foreground_color[0]]
FG = [default_foreground_color[1]]
FB = [default_foreground_color[2]]


px=[px_default]  # center of the circles/rings
py=[py_default]  # center of the circles/rings
rot = [0]

step=5
step_s=1
step_c = 5
step_rot = np.pi/100



s1 = [radius_default]     # circle/ring radius
# s2 = [65,45]
s2 = [width_default]      # widht of the circles/rings

s3 = [opening_radius_default]   # radius of the opening
# a circle of radius s3 and color = background_color is drawn to create the opening


lp = True
#border_width = 5


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


# Object scaling, rotation, color change function. 
def modify_object(active_ind, key_input):
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
    
    
    #rotate + change red color
    if key_input[pygame.K_r]:
        rot[active_ind] -= step_rot
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_CTRL:
            FR[active_ind] = FR[active_ind] + step_c if FR[active_ind] < 255 else FR[active_ind]
        if mods & pygame.KMOD_ALT:
            FR[active_ind] = FR[active_ind] - step_c if FR[active_ind] > step_c else FR[active_ind]

    # rotate     
    if key_input[pygame.K_f]:
        rot[active_ind] += step_rot
        
#   change green color
    if key_input[pygame.K_g]:
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_CTRL:
            FG[active_ind] = FG[active_ind] + step_c if FG[active_ind] < 255 else FG[active_ind]
        if mods & pygame.KMOD_ALT:
            FG[active_ind] = FG[active_ind] - step_c if FG[active_ind] > step_c else FG[active_ind]

#   change blue color
    if key_input[pygame.K_b]:
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_CTRL:
            FB[active_ind] = FB[active_ind] + step_c if FB[active_ind] < 255 else FB[active_ind]
        if mods & pygame.KMOD_ALT:
            FB[active_ind] = FB[active_ind] - step_c if FB[active_ind] > step_c else FB[active_ind]
  
        
    
    
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
           FR.append(default_foreground_color[0])
           FG.append(default_foreground_color[1])
           FB.append(default_foreground_color[2])
           s1.append(radius_default)
           s2.append(width_default)
           s3.append(opening_radius_default) 
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
   
    
    pygame.draw.circle(sur_obj, background_color, (tx, ty),s3[active_ind],0)
    return 0



def draw_window():
    
    for m in range(len(px)):
        # pygame.draw.rect(sur_obj, (255,0,0), (px[m], py[m], s1[m], s2[m]))
        pygame.draw.circle(sur_obj, (FR[m],FG[m],FB[m]), (px[m], py[m]),s1[m],s2[m])
        # pygame.draw.arc(sur_obj, (255,0,0), (px[m], py[m],s1[m],s1[m]),-3, 3, s2[m])
        # pygame.draw.arc(sur_obj, (255,0,0), (px[m]+0.4, py[m]-0.4,s1[m],s1[m]-1),-3, 3, s2[m])
        


active_ind = 0

while lp:
    
    fpsclock.tick(fps)
    sur_obj.fill(background_color)
    
    key_input = pygame.key.get_pressed()   
    
    
    
    move_object(active_ind, key_input)
    modify_object(active_ind, key_input)
    
    draw_window()
       


    if key_input[pygame.K_o]:
        open_circle(active_ind)
        
    if key_input[pygame.K_1]:
        mods = pygame.key.get_mods()
        
        if mods & pygame.KMOD_CTRL:
            active_ind = 0
 
    if key_input[pygame.K_2]:
        mods = pygame.key.get_mods()
        
        if mods & pygame.KMOD_CTRL:
            active_ind = 1   
    
    # The following events are addressed specifically so that multiple events aren't registered from a single click
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
                active_ind = new_object(event, active_ind)
                active_ind = change_active_object(event, active_ind)


            



          
     

    
 
    # if key_input[pygame.K_5]:
        # pygame.draw.circle(sur_obj, (255,0,0), (px, py),s1)
    
    
  
    
    
    
    


         
        
    if key_input[pygame.K_x]:
        pygame.quit()
 
        
        
    pygame.display.update()
    fpsclock.tick(fps)
    
    

