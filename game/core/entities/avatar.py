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
        
        # Draw body (simple cylinder for now)
        self._draw_cylinder(self.radius, self.height)
        
        # Draw head (sphere)
        glPushMatrix()
        glTranslatef(0, self.height * 0.8, 0)
        quad = gluNewQuadric()
        gluSphere(quad, self.radius * 0.7, 16, 16)
        glPopMatrix()
        
        glPopMatrix()
        
    def _draw_cylinder(self, radius, height):
        quad = gluNewQuadric()
        glColor3f(0.8, 0.8, 1.0)  # Light blue color
        gluCylinder(quad, radius, radius, height, 16, 1)
        
    def move(self, forward, right):
        # Calculate movement direction based on rotation
        angle = np.radians(self.rotation)
        dx = np.sin(angle) * forward + np.cos(angle) * right
        dz = np.cos(angle) * forward - np.sin(angle) * right
        
        speed = 0.1
        self.position[0] += dx * speed
        self.position[2] += dz * speed
        
        self.walking = forward != 0 or right != 0
        
    def rotate(self, angle):
        self.rotation = (self.rotation + angle) % 360
        
    def get_camera_position(self):
        # Position camera behind and slightly above avatar
        angle = np.radians(self.rotation)
        camera_distance = 5
        camera_height = 2
        
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