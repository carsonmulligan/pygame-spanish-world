import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class BeachHut:
    def __init__(self, position, name="Barraca 87"):
        self.position = list(position)
        self.name = name
        self.width = 4.0
        self.depth = 3.0
        self.height = 3.0
        self.roof_height = 1.5
        
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        
        # Draw main structure
        glColor3f(0.8, 0.7, 0.5)  # Light wood color
        self._draw_walls()
        
        # Draw thatched roof
        glColor3f(0.7, 0.6, 0.4)  # Darker thatch color
        self._draw_roof()
        
        # Draw counter/bar
        glColor3f(0.6, 0.5, 0.3)  # Dark wood color
        self._draw_counter()
        
        # Draw sign
        self._draw_sign()
        
        glPopMatrix()
        
    def _draw_walls(self):
        # Front wall with opening
        glBegin(GL_QUADS)
        # Left side of opening
        glVertex3f(-self.width/2, 0, -self.depth/2)
        glVertex3f(-self.width/4, 0, -self.depth/2)
        glVertex3f(-self.width/4, self.height, -self.depth/2)
        glVertex3f(-self.width/2, self.height, -self.depth/2)
        
        # Right side of opening
        glVertex3f(self.width/4, 0, -self.depth/2)
        glVertex3f(self.width/2, 0, -self.depth/2)
        glVertex3f(self.width/2, self.height, -self.depth/2)
        glVertex3f(self.width/4, self.height, -self.depth/2)
        
        # Top of opening
        glVertex3f(-self.width/4, self.height*0.7, -self.depth/2)
        glVertex3f(self.width/4, self.height*0.7, -self.depth/2)
        glVertex3f(self.width/4, self.height, -self.depth/2)
        glVertex3f(-self.width/4, self.height, -self.depth/2)
        
        # Back wall
        glVertex3f(-self.width/2, 0, self.depth/2)
        glVertex3f(self.width/2, 0, self.depth/2)
        glVertex3f(self.width/2, self.height, self.depth/2)
        glVertex3f(-self.width/2, self.height, self.depth/2)
        
        # Side walls
        glVertex3f(-self.width/2, 0, -self.depth/2)
        glVertex3f(-self.width/2, 0, self.depth/2)
        glVertex3f(-self.width/2, self.height, self.depth/2)
        glVertex3f(-self.width/2, self.height, -self.depth/2)
        
        glVertex3f(self.width/2, 0, -self.depth/2)
        glVertex3f(self.width/2, 0, self.depth/2)
        glVertex3f(self.width/2, self.height, self.depth/2)
        glVertex3f(self.width/2, self.height, -self.depth/2)
        glEnd()
        
    def _draw_roof(self):
        glBegin(GL_TRIANGLES)
        # Front gable
        glVertex3f(-self.width/2, self.height, -self.depth/2)
        glVertex3f(self.width/2, self.height, -self.depth/2)
        glVertex3f(0, self.height + self.roof_height, -self.depth/2)
        
        # Back gable
        glVertex3f(-self.width/2, self.height, self.depth/2)
        glVertex3f(self.width/2, self.height, self.depth/2)
        glVertex3f(0, self.height + self.roof_height, self.depth/2)
        glEnd()
        
        # Roof slopes
        glBegin(GL_QUADS)
        glVertex3f(-self.width/2, self.height, -self.depth/2)
        glVertex3f(-self.width/2, self.height, self.depth/2)
        glVertex3f(0, self.height + self.roof_height, self.depth/2)
        glVertex3f(0, self.height + self.roof_height, -self.depth/2)
        
        glVertex3f(self.width/2, self.height, -self.depth/2)
        glVertex3f(self.width/2, self.height, self.depth/2)
        glVertex3f(0, self.height + self.roof_height, self.depth/2)
        glVertex3f(0, self.height + self.roof_height, -self.depth/2)
        glEnd()
        
    def _draw_counter(self):
        counter_height = self.height * 0.4
        counter_depth = self.depth * 0.3
        
        glBegin(GL_QUADS)
        # Counter top
        glVertex3f(-self.width/3, counter_height, -self.depth/2)
        glVertex3f(self.width/3, counter_height, -self.depth/2)
        glVertex3f(self.width/3, counter_height, -self.depth/2 + counter_depth)
        glVertex3f(-self.width/3, counter_height, -self.depth/2 + counter_depth)
        
        # Counter front
        glVertex3f(-self.width/3, 0, -self.depth/2)
        glVertex3f(self.width/3, 0, -self.depth/2)
        glVertex3f(self.width/3, counter_height, -self.depth/2)
        glVertex3f(-self.width/3, counter_height, -self.depth/2)
        glEnd()
        
    def _draw_sign(self):
        glPushMatrix()
        glTranslatef(0, self.height + self.roof_height/2, -self.depth/2 - 0.1)
        
        # Sign board
        glColor3f(0.9, 0.9, 0.8)  # Light colored sign
        glBegin(GL_QUADS)
        glVertex3f(-self.width/3, -0.3, 0)
        glVertex3f(self.width/3, -0.3, 0)
        glVertex3f(self.width/3, 0.3, 0)
        glVertex3f(-self.width/3, 0.3, 0)
        glEnd()
        
        # Sign text would go here (needs proper text rendering)
        glColor3f(0.2, 0.2, 0.2)  # Dark text color
        glRasterPos3f(-self.width/4, 0, 0.1)
        
        glPopMatrix() 