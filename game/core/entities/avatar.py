import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Avatar:
    def __init__(self, position=(0, 0, 0)):
        self.position = list(position)
        self.rotation = 0
        self.height = 1.8
        self.radius = 0.3
        self.animation_state = 'idle'
        self.animation_frame = 0
        self.walking = False
        print(f"Avatar initialized at position {position}")
        
    def update(self, terrain):
        # Update avatar height based on terrain
        ground_height = terrain.get_height(self.position[0], self.position[2])
        self.position[1] = ground_height + self.height/2
        
        # Update animation
        if self.walking:
            self.animation_frame = (self.animation_frame + 1) % 60
            self.animation_state = 'walk'
        else:
            self.animation_state = 'idle'
            
    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(self.rotation, 0, 1, 0)
        
        # Draw direction indicator (arrow)
        glDisable(GL_LIGHTING)
        glColor3f(1, 1, 0)  # Yellow
        glBegin(GL_LINES)
        glVertex3f(0, self.height/2, 0)
        glVertex3f(0, self.height/2, self.radius * 2)
        glVertex3f(0, self.height/2, self.radius * 2)
        glVertex3f(0.2, self.height/2, self.radius * 1.5)
        glVertex3f(0, self.height/2, self.radius * 2)
        glVertex3f(-0.2, self.height/2, self.radius * 1.5)
        glEnd()
        glEnable(GL_LIGHTING)
        
        # Draw body (cylinder)
        glColor3f(0.3, 0.3, 1.0)  # Blue color
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        glRotatef(90, 1, 0, 0)  # Rotate to stand upright
        gluCylinder(quad, self.radius, self.radius, self.height, 16, 1)
        
        # Draw head (sphere)
        glRotatef(-90, 1, 0, 0)  # Rotate back
        glTranslatef(0, self.height * 0.8, 0)
        glColor3f(1.0, 0.8, 0.6)  # Skin color
        quad = gluNewQuadric()
        gluQuadricNormals(quad, GLU_SMOOTH)
        gluSphere(quad, self.radius * 0.7, 16, 16)
        
        glPopMatrix()
        
        # Draw debug info
        self._draw_debug_info()
        
    def _draw_debug_info(self):
        # Draw position marker
        glDisable(GL_LIGHTING)
        glColor3f(1, 0, 0)  # Red
        glPointSize(5.0)
        glBegin(GL_POINTS)
        glVertex3f(*self.position)
        glEnd()
        
        # Draw view direction
        glColor3f(1, 1, 0)  # Yellow
        glBegin(GL_LINES)
        start = self.position
        angle = np.radians(self.rotation)
        end = [
            start[0] + np.sin(angle) * 2,
            start[1],
            start[2] + np.cos(angle) * 2
        ]
        glVertex3f(*start)
        glVertex3f(*end)
        glEnd()
        glEnable(GL_LIGHTING)
        
    def move(self, forward, right):
        # Calculate movement direction based on rotation
        angle = np.radians(self.rotation)
        dx = np.sin(angle) * forward + np.cos(angle) * right
        dz = np.cos(angle) * forward - np.sin(angle) * right
        
        speed = 0.1
        self.position[0] += dx * speed
        self.position[2] += dz * speed
        
        self.walking = forward != 0 or right != 0
        if self.walking:
            print(f"Moving to position: {self.position}")
        
    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360
        
    def get_camera_position(self):
        # Position camera behind and slightly above avatar
        angle = np.radians(self.rotation)
        camera_distance = 5
        camera_height = 3  # Increased height for better view
        
        camera_pos = [
            self.position[0] - np.sin(angle) * camera_distance,
            self.position[1] + camera_height,
            self.position[2] - np.cos(angle) * camera_distance
        ]
        
        look_at = [
            self.position[0],
            self.position[1] + 1,
            self.position[2]
        ]
        
        return camera_pos, look_at