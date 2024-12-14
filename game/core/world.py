import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

class World:
    def __init__(self):
        self.terrain_size = 100
        self.terrain_scale = 1
        self.buildings = []
        self.textures = {}
        self._init_textures()
        self._generate_terrain()
        self._init_buildings()
        
    def _init_textures(self):
        # Load textures for terrain and buildings
        texture_files = {
            'grass': 'game/assets/textures/grass.jpg',
            'building': 'game/assets/textures/building.jpg'
        }
        
        for name, path in texture_files.items():
            texture = self._load_texture(path)
            self.textures[name] = texture
            
    def _load_texture(self, path):
        image = Image.open(path)
        ix = image.size[0]
        iy = image.size[1]
        image = image.tobytes('raw', 'RGBX', 0, -1)
        
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        return texture_id
        
    def _generate_terrain(self):
        # Create a simple flat terrain with slight elevation variations
        vertices = []
        texcoords = []
        for z in range(self.terrain_size):
            for x in range(self.terrain_size):
                # Add slight random elevation
                y = np.sin(x * 0.1) * 0.2 + np.cos(z * 0.1) * 0.2
                vertices.append((x - self.terrain_size/2, y, z - self.terrain_size/2))
                texcoords.append((x/10, z/10))
                
        self.terrain_vertices = vertices
        self.terrain_texcoords = texcoords
        
    def _init_buildings(self):
        # Add some sample buildings
        building_positions = [
            (-10, 0, -10),  # Mexico area
            (10, 0, 10),    # Spain area
            (-5, 0, 15)     # Argentina area
        ]
        
        for pos in building_positions:
            self.buildings.append({
                'position': pos,
                'size': (3, 5, 3)  # width, height, depth
            })
            
    def draw(self):
        self._draw_terrain()
        self._draw_buildings()
        
    def _draw_terrain(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures['grass'])
        
        glBegin(GL_QUADS)
        for z in range(self.terrain_size - 1):
            for x in range(self.terrain_size - 1):
                # Get vertices for current quad
                v1 = self.terrain_vertices[z * self.terrain_size + x]
                v2 = self.terrain_vertices[z * self.terrain_size + (x + 1)]
                v3 = self.terrain_vertices[(z + 1) * self.terrain_size + (x + 1)]
                v4 = self.terrain_vertices[(z + 1) * self.terrain_size + x]
                
                # Get texture coordinates
                t1 = self.terrain_texcoords[z * self.terrain_size + x]
                t2 = self.terrain_texcoords[z * self.terrain_size + (x + 1)]
                t3 = self.terrain_texcoords[(z + 1) * self.terrain_size + (x + 1)]
                t4 = self.terrain_texcoords[(z + 1) * self.terrain_size + x]
                
                # Draw quad
                glTexCoord2f(*t1); glVertex3f(*v1)
                glTexCoord2f(*t2); glVertex3f(*v2)
                glTexCoord2f(*t3); glVertex3f(*v3)
                glTexCoord2f(*t4); glVertex3f(*v4)
        glEnd()
        
    def _draw_buildings(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures['building'])
        
        for building in self.buildings:
            pos = building['position']
            size = building['size']
            
            glPushMatrix()
            glTranslatef(*pos)
            
            # Draw a simple textured cube
            glBegin(GL_QUADS)
            # Front face
            glTexCoord2f(0, 0); glVertex3f(-size[0]/2, 0, -size[2]/2)
            glTexCoord2f(1, 0); glVertex3f(size[0]/2, 0, -size[2]/2)
            glTexCoord2f(1, 1); glVertex3f(size[0]/2, size[1], -size[2]/2)
            glTexCoord2f(0, 1); glVertex3f(-size[0]/2, size[1], -size[2]/2)
            # Back face
            glTexCoord2f(0, 0); glVertex3f(-size[0]/2, 0, size[2]/2)
            glTexCoord2f(1, 0); glVertex3f(size[0]/2, 0, size[2]/2)
            glTexCoord2f(1, 1); glVertex3f(size[0]/2, size[1], size[2]/2)
            glTexCoord2f(0, 1); glVertex3f(-size[0]/2, size[1], size[2]/2)
            # Other faces...
            glEnd()
            
            glPopMatrix()
            
    def check_collision(self, position):
        # Simple collision detection with buildings
        for building in self.buildings:
            bpos = building['position']
            bsize = building['size']
            
            # Check if position is inside building bounds
            if (abs(position[0] - bpos[0]) < bsize[0]/2 and
                abs(position[2] - bpos[2]) < bsize[2]/2):
                return True
        return False 