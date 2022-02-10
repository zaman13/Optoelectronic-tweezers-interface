

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
LCTRL + n : Create new circle object (left ctrl key only)
RCTRL + n : Create new gear sprite object (right ctrl key only)
SHIFT + n : Create new rectangle object 
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
PAGEUP    : Save data file


Version updates:
    0.6.1: Feb 4, 2022: Changed the default position of new objects 
    0.7.1: Feb 5, 2022: Added sprites. Changed active object marker to #. Also added some limits to max/min values of s1,s2,s3 etc.
    0.9.1: Feb 7, 2022: Sprtie rotation around its center added (no drift). Delete object bug fix.
    0.9.3: Feb 9, 2022: Save and load data files containing position of shapes.
"""



import pygame
import sys
import numpy as np
import csv







#==============================================================================
# File I/O control variables
read_data_from_file = 'y'               # read data from file? y/n
data_file_name = 'gears1.csv'           # data file name
#==============================================================================


pygame.init()
fps=60   # frames per second, refresh rate of the video screen 
fpsclock=pygame.time.Clock()
sur_obj=pygame.display.set_mode((1600,900),pygame.FULLSCREEN)
font = pygame.font.SysFont('Arial', 12, bold=True)    

White=(255,255,255)
background_color=(0,0,0)
foreground_color_default = (0,255,0)

label_color = (55,55,55)

px_default = 120
py_default = 120
rot_default = 0

radius_default = 70
width_default = 6
opening_radius_default = 10
label_radius_factor = 0.25 # label_raidus = label_radius_factor * circle radius
label_width = 2
#==============================================================================



#==============================================================================
# Load sprites
#==============================================================================

gear_sprite = pygame.image.load('sprite3.svg').convert_alpha()        
line_sprite = pygame.image.load('sprite1.svg').convert_alpha()        

sprites = [gear_sprite, line_sprite]      # load all the sprites in an array
#==============================================================================




#==============================================================================
# The parameters associated with each object
#==============================================================================
px=[px_default]  # x center of the circles/rings
py=[py_default]  # y center of the circles/rings
rot = [0]        # rotation of the opening. Zero radians refer to the 3 O'clock position
p_type = [0]     # Type of the object. 0 = circle, 1 = rectangle


s1 = [radius_default]           # circle/ring radius
s2 = [width_default]            # widht of the circles/rings
s3 = [opening_radius_default]   # radius of the opening
# a circle of radius s3 and color = background_color is drawn to create the opening

FR = [foreground_color_default[0]]
FG = [foreground_color_default[1]]
FB = [foreground_color_default[2]]
#==============================================================================




#==============================================================================
# Motion control parameter
#==============================================================================

step=5
step_s=1
step_c = 5
step_rot = np.pi/100
#==============================================================================


lp = True





# render a given font into an image
txt_label = font.render('Text to write', True,
                  pygame.Color(White),
                  pygame.Color(background_color))



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

    # Vestion 0.7 update: added some limits
    if key_input[pygame.K_a]:
        s1[active_ind] = s1[active_ind] - step_s if s1[active_ind] > 0 else 0
        
    if key_input[pygame.K_q]:
        s1[active_ind] += step_s
        
        
        
        
        
        
    if key_input[pygame.K_s]:
        s2[active_ind] = s2[active_ind] - step_s if s2[active_ind] > 0 else 0
        
    if key_input[pygame.K_w]:
        if p_type[active_ind] == 0:
            s2[active_ind] = s2[active_ind] + step_s if s2[active_ind] < s1[active_ind] else s2[active_ind]
        if p_type[active_ind] == 1:
            s2[active_ind] = s2[active_ind] + step_s    
        
            
            
        
    if key_input[pygame.K_d]:
        s3[active_ind] = s3[active_ind] - step_s 
        
    if key_input[pygame.K_e]:
        s3[active_ind] += step_s
    
    
    #rotate + change red color
    if key_input[pygame.K_r]:
        rot[active_ind] = rot[active_ind]-step_rot if rot[active_ind] >=0 else 2*np.pi-step_rot
         
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_CTRL:
            FR[active_ind] = FR[active_ind] + step_c if FR[active_ind] < 255 else FR[active_ind]
        if mods & pygame.KMOD_ALT:
            FR[active_ind] = FR[active_ind] - step_c if FR[active_ind] > step_c else FR[active_ind]


    # rotate     
    if key_input[pygame.K_f]:
        rot[active_ind] = rot[active_ind]+step_rot if rot[active_ind] <=2*np.pi else 0+step_rot
        
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
 
#==============================================================================    



#==============================================================================
# funciton to append default parameters of new object. Object type is appended 
# in the new_object function
#==============================================================================

def append_default(active_ind):
      px.append(px[active_ind] + 2.2*s1[active_ind])
      py.append(py[active_ind] + 0*s1[active_ind])
      rot.append(0)
      # FR.append(foreground_color_default[0])
      # FG.append(foreground_color_default[1])
      # FB.append(foreground_color_default[2])
      FR.append(FR[active_ind])
      FG.append(FG[active_ind])
      FB.append(FB[active_ind])
            
      s1.append(s1[active_ind])
      s2.append(s2[active_ind])
      s3.append(opening_radius_default)
      
      return 0
#==============================================================================   




#==============================================================================
def new_object(event,active_ind):
   if event.key ==  pygame.K_n:
       mods = pygame.key.get_mods()
       
       if mods:
           append_default(active_ind)
           active_ind = len(px) - 1
       
       if mods & pygame.KMOD_LCTRL:
           p_type.append(0)
           
       if mods & pygame.KMOD_SHIFT:
           p_type.append(1)
           
       if mods & pygame.KMOD_RCTRL:
           p_type.append(2)
           
       if mods & pygame.KMOD_RALT:
           p_type.append(3)
                
    
  
   return active_ind


#==============================================================================

# change active object selection or delete selected object
def change_active_object(event,active_ind):
    # select next active object. If at the end of list, then go back to zero.
    if event.key ==  pygame.K_EQUALS:
        active_ind = active_ind + 1 if len(px)> active_ind + 1 else 0
                
    
    # select previous active object. If zero, then circle back to the end of the list..            
    if event.key ==  pygame.K_MINUS:
        active_ind = active_ind - 1 if active_ind > 0 else len(px)-1
    
    
    # delete active object
    if event.key ==  pygame.K_DELETE:
        
        if len(px) > 1:
            del px[active_ind]
            del py[active_ind]
            del s1[active_ind]
            del s2[active_ind]
            del s3[active_ind]
            del rot[active_ind]
            del FR[active_ind]
            del FG[active_ind]
            del FB[active_ind]
            del p_type[active_ind]
            active_ind = active_ind -1 if active_ind-1 >= 0 else 0
        
      
    
    
    return active_ind
            
            
            

    
# Create opening in the circle

def open_circle(active_ind):
    # Draws a circle in black color to create opening in the object
    tx = px[active_ind]+s1[active_ind]-0.5*s2[active_ind]  # x coordinate of the opening is set at the middle of the right rim along x axis
    ty = py[active_ind]                                    # y coordinate of the opening is the same as the y coordinate of the object
    
    [tx,ty] = rotate(tx,ty,px[active_ind],py[active_ind],rot[active_ind])
   
    
    pygame.draw.circle(sur_obj, background_color, (tx, ty),s3[active_ind],0)
    return 0



def draw_window(active_ind):
    
    for m in range(len(px)):
        
        
        label_str = str(m) + '#' if active_ind == m else str(m)
        
        txt_label = font.render(label_str, True,
                  pygame.Color(label_color),
                  pygame.Color(background_color))
        txt_label.set_alpha(100)
        # pygame.draw.rect(sur_obj, (255,0,0), (px[m], py[m], s1[m], s2[m]))
        if p_type[m] == 0:
            pygame.draw.circle(sur_obj, (FR[m],FG[m],FB[m]), (int(px[m]), int(py[m])),int(s1[m]),int(s2[m]))
            sur_obj.blit(txt_label, (px[m]+0.9*s1[m], py[m]-0.9*s1[m]))
           
            
            
            
        if p_type[m] == 1:
            pygame.draw.rect(sur_obj, (FR[m],FG[m],FB[m]), (px[m], py[m], s1[m], s2[m]))
            sur_obj.blit(txt_label, (px[m]+0.9*s1[m], py[m]-16))
            
                    
        if p_type[m] >= 2:
            sprite_original = pygame.transform.scale(sprites[p_type[m]-2], (s1[m], s1[m]))
            sprite = sprite_original.copy()
            sprite_rect = sprite_original.get_rect(center = (px[m],py[m]))
            
            sur_obj.blit(txt_label, sprite_rect)

            rot[m] = rot[m] + (s3[m]-opening_radius_default)*step_rot*2


            sprite = pygame.transform.rotate(sprite, rot[m])
            sprite_rect = sprite.get_rect(center = sprite_rect.center)
            
            # https://www.reddit.com/r/pygame/comments/2p1pi4/how_to_spin_an_image_on_its_center/
           

            sur_obj.blit(sprite, sprite_rect)
        



def data_write():
    with open('save.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(px)
        spamwriter.writerow(py)
        spamwriter.writerow(rot)
        spamwriter.writerow(p_type)
        spamwriter.writerow(s1)
        spamwriter.writerow(s2)
        spamwriter.writerow(s3)
        spamwriter.writerow(FR)
        spamwriter.writerow(FG)
        spamwriter.writerow(FB)
        
    return 0 



# def data_read(fname):
#     with open(fname, newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
#         for row in spamreader:
#             ux = row
            
#     return ux 

def data_read(fname):
    with open(fname, 'r') as read_obj:
        data_reader = csv.reader(read_obj, delimiter=' ', quotechar='|')
        ux = list(data_reader)
    
    px.clear()
    py.clear()
    rot.clear()
    p_type.clear()
    s1.clear()
    s2.clear()
    s3.clear()
    FR.clear()
    FG.clear()
    FB.clear()
    
    for m in range(len(ux[0])):
        
        px.append(int(float(ux[0][m])))
        py.append(int(float(ux[1][m])))
        rot.append(float(ux[2][m]))
        p_type.append(int(float(ux[3][m])))
        s1.append(float(ux[4][m]))
        s2.append(float(ux[5][m]))
        s3.append(float(ux[6][m]))
        FR.append(int(ux[7][m]))
        FG.append(int(ux[8][m]))
        FB.append(int(ux[9][m]))
        
        
    return 0  
    



#==============================================================================
# Main loop
#==============================================================================


#==============================================================================
# Read data from a file
#==============================================================================
if read_data_from_file == 'y':
    data_read(data_file_name)

#==============================================================================





active_ind = 0

while lp:
    
    fpsclock.tick(fps)
    sur_obj.fill(background_color)
    
    key_input = pygame.key.get_pressed()   
    
    
    
    move_object(active_ind, key_input)
    modify_object(active_ind, key_input)
    
    draw_window(active_ind)
    
    


    if key_input[pygame.K_o]:
        open_circle(active_ind)
        
    
    # The following events are addressed specifically so that multiple events aren't registered from a single click
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
                active_ind = new_object(event, active_ind)
                active_ind = change_active_object(event, active_ind)


    if key_input[pygame.K_PAGEUP]:
        data_write()
    
       
    if key_input[pygame.K_x]:
        pygame.quit()
        
        
        
    pygame.display.update()
    fpsclock.tick(fps)
    
    
#==============================================================================
# End main loop
#==============================================================================
