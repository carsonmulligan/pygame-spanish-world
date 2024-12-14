import pygame
from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class Player:
    def __init__(self, position=(0, 1, 0)):
        self.position = list(position)
        self.rotation = 0  # Rotation around Y axis (in degrees)
        self.speed = 0.1
        self.turn_speed = 2.0
        self.camera_height = 1.7  # Height of camera from ground
        
    def move(self, forward=0, right=0):
        # Calculate movement direction based on rotation
        angle = np.radians(self.rotation)
        dx = np.sin(angle) * forward + np.cos(angle) * right
        dz = np.cos(angle) * forward - np.sin(angle) * right
        
        # Update position
        self.position[0] += dx * self.speed
        self.position[2] += dz * self.speed
        
    def rotate(self, angle):
        self.rotation = (self.rotation + angle * self.turn_speed) % 360
        
    def update_camera(self):
        # Position camera at player's eye level
        camera_pos = [self.position[0], self.position[1] + self.camera_height, self.position[2]]
        
        # Calculate look-at point based on rotation
        angle = np.radians(self.rotation)
        look_at = [
            camera_pos[0] + np.sin(angle),
            camera_pos[1],
            camera_pos[2] + np.cos(angle)
        ]
        
        # Update OpenGL camera
        glLoadIdentity()
        gluLookAt(
            *camera_pos,    # Camera position
            *look_at,       # Look-at point
            0, 1, 0         # Up vector
        ) 