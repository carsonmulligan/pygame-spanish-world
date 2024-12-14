import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

class NPC:
    def __init__(self, position, name, hut_position):
        self.position = list(position)
        self.name = name
        self.rotation = 0
        self.height = 1.7
        self.radius = 0.3
        self.walking = False
        self.hut_position = hut_position
        self.walk_radius = 3.0
        self.walk_speed = 0.02
        self.time = 0
        
        # Default colors
        self.outfit_color = (1.0, 0.8, 0.4)  # Light yellow shirt
        self.pants_color = (0.4, 0.7, 1.0)   # Light blue shorts
        self.skin_color = (0.8, 0.6, 0.4)    # Tanned skin
        self.hat_color = (0.9, 0.8, 0.6)     # Straw hat
        
    def update(self, terrain):
        # Update NPC height based on terrain
        ground_height = terrain.get_height(self.position[0], self.position[2])
        self.position[1] = ground_height + self.height/2
        
        # Make NPC walk in a pattern around the hut
        self.time += self.walk_speed
        self.position[0] = self.hut_position[0] + math.cos(self.time) * self.walk_radius
        self.position[2] = self.hut_position[2] + math.sin(self.time) * self.walk_radius
        
        # Update rotation to face walking direction
        self.rotation = math.degrees(math.atan2(
            math.cos(self.time + 0.1) - math.cos(self.time),
            math.sin(self.time + 0.1) - math.sin(self.time)
        ))
            
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 1, 0)
        
        # Enable better lighting for the character
        glEnable(GL_LIGHTING)
        glEnable(GL_NORMALIZE)
        
        # Draw body (cylinder with custom outfit)
        glColor3f(*self.outfit_color)
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        glRotatef(90, 1, 0, 0)
        
        # Draw torso
        gluCylinder(quad, self.radius, self.radius, self.height * 0.6, 16, 1)
        
        # Draw pants/shorts
        glColor3f(*self.pants_color)
        gluCylinder(quad, self.radius, self.radius * 0.8, self.height * 0.3, 16, 1)
        
        # Draw head
        glRotatef(-90, 1, 0, 0)
        glTranslatef(0, self.height * 0.8, 0)
        glColor3f(*self.skin_color)
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, self.radius * 0.7, 16, 16)
        
        # Draw hat
        glColor3f(*self.hat_color)
        glTranslatef(0, self.radius * 0.3, 0)
        gluDisk(quad, 0, self.radius * 1.2, 16, 1)  # Hat brim
        glTranslatef(0, 0.1, 0)
        gluCylinder(quad, self.radius * 0.8, 0, self.radius * 0.5, 16, 1)  # Hat top
        
        glPopMatrix()
        
        # Draw name tag
        self._draw_name_tag()
        
    def _draw_name_tag(self):
        glDisable(GL_LIGHTING)
        glColor3f(1, 1, 1)  # White text
        glRasterPos3f(self.position[0], self.position[1] + self.height + 0.3, self.position[2])
        
        # Draw a small marker above the NPC
        glPointSize(5.0)
        glBegin(GL_POINTS)
        glVertex3f(self.position[0], self.position[1] + self.height + 0.4, self.position[2])
        glEnd()
        
        glEnable(GL_LIGHTING)