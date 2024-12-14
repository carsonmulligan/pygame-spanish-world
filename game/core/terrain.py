import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from noise import snoise2  # For better terrain generation

class Terrain:
    def __init__(self, size=100, scale=1):
        self.size = size
        self.scale = scale
        self.height_map = None
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.generate_terrain()
        
    def generate_terrain(self):
        # Generate height map using Perlin noise
        self.height_map = np.zeros((self.size, self.size))
        scale = 50.0
        octaves = 6
        persistence = 0.5
        lacunarity = 2.0
        
        for i in range(self.size):
            for j in range(self.size):
                x = i/scale
                y = j/scale
                elevation = snoise2(x, y, octaves, persistence, lacunarity)
                self.height_map[i][j] = elevation
        
        # Normalize height map
        self.height_map = (self.height_map - self.height_map.min()) / (self.height_map.max() - self.height_map.min())
        self.height_map *= 5  # Maximum height
        
        # Generate vertices, normals, and texture coordinates
        for z in range(self.size - 1):
            for x in range(self.size - 1):
                # Vertices for current quad
                v1 = self._get_vertex(x, z)
                v2 = self._get_vertex(x + 1, z)
                v3 = self._get_vertex(x + 1, z + 1)
                v4 = self._get_vertex(x, z + 1)
                
                # Calculate normal for lighting
                normal = self._calculate_normal(v1, v2, v3)
                
                self.vertices.extend([v1, v2, v3, v4])
                self.normals.extend([normal] * 4)
                
                # Texture coordinates
                self.texcoords.extend([
                    (x/10, z/10),
                    ((x+1)/10, z/10),
                    ((x+1)/10, (z+1)/10),
                    (x/10, (z+1)/10)
                ])
    
    def _get_vertex(self, x, z):
        return (
            (x - self.size/2) * self.scale,
            self.height_map[x][z],
            (z - self.size/2) * self.scale
        )
    
    def _calculate_normal(self, v1, v2, v3):
        # Calculate surface normal for lighting
        u = np.subtract(v2, v1)
        v = np.subtract(v3, v1)
        normal = np.cross(u, v)
        return normal / np.linalg.norm(normal)
    
    def draw(self, grass_texture):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, grass_texture)
        
        glBegin(GL_QUADS)
        for i in range(0, len(self.vertices), 4):
            for j in range(4):
                glNormal3fv(self.normals[i + j])
                glTexCoord2fv(self.texcoords[i + j])
                glVertex3fv(self.vertices[i + j])
        glEnd()
        
    def get_height(self, x, z):
        # Get interpolated height at any point
        terrain_x = int((x + self.size/2) / self.scale)
        terrain_z = int((z + self.size/2) / self.scale)
        
        if 0 <= terrain_x < self.size-1 and 0 <= terrain_z < self.size-1:
            return self.height_map[terrain_x][terrain_z]
        return 0 