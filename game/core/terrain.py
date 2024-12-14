import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from noise import snoise2

class Terrain:
    def __init__(self, size=50, scale=1):
        self.size = size
        self.scale = scale
        self.height_map = None
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.water_level = -0.2  # Water level for ocean
        self.beach_start = 0.0   # Where beach starts
        self.generate_terrain()
        print(f"Beach terrain generated with size {size}x{size}")
        
    def generate_terrain(self):
        # Generate height map using Perlin noise
        self.height_map = np.zeros((self.size, self.size))
        scale = 25.0
        octaves = 4
        persistence = 0.5
        lacunarity = 2.0
        
        print("Generating beach height map...")
        for i in range(self.size):
            for j in range(self.size):
                x = i/scale
                y = j/scale
                # Create gradual slope for beach
                beach_gradient = (j / self.size) * 0.5
                elevation = snoise2(x, y, octaves, persistence, lacunarity) * 0.3
                self.height_map[i][j] = elevation - beach_gradient
        
        # Normalize height map
        self.height_map = (self.height_map - self.height_map.min()) / (self.height_map.max() - self.height_map.min())
        self.height_map *= 1.0  # Reduced maximum height for flatter beach
        
        print("Generating beach vertices and normals...")
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
                    (x/3, z/3),          # Increased tiling for better visibility
                    ((x+1)/3, z/3),
                    ((x+1)/3, (z+1)/3),
                    (x/3, (z+1)/3)
                ])
        
        print(f"Generated {len(self.vertices)} vertices")
    
    def _get_vertex(self, x, z):
        return (
            (x - self.size/2) * self.scale,
            self.height_map[x][z],
            (z - self.size/2) * self.scale
        )
    
    def _calculate_normal(self, v1, v2, v3):
        u = np.subtract(v2, v1)
        v = np.subtract(v3, v1)
        normal = np.cross(u, v)
        length = np.linalg.norm(normal)
        if length == 0:
            return (0, 1, 0)
        return normal / length
    
    def draw(self, grass_texture):
        # Draw terrain
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, grass_texture)
        
        glBegin(GL_QUADS)
        for i in range(0, len(self.vertices), 4):
            for j in range(4):
                vertex = self.vertices[i + j]
                # Color based on height (water, sand, vegetation)
                if vertex[1] < self.water_level:
                    glColor3f(0.0, 0.4, 0.8)  # Blue for water
                elif vertex[1] < self.beach_start:
                    glColor3f(0.9, 0.8, 0.6)  # Light yellow for sand
                else:
                    glColor3f(0.3, 0.6, 0.3)  # Green for vegetation
                    
                glNormal3fv(self.normals[i + j])
                glTexCoord2fv(self.texcoords[i + j])
                glVertex3fv(vertex)
        glEnd()
        
        # Draw water surface
        self._draw_water()
        
    def _draw_water(self):
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glColor4f(0.0, 0.4, 0.8, 0.5)  # Semi-transparent blue
        
        glBegin(GL_QUADS)
        # Draw water surface as a large quad
        size = self.size * self.scale
        glVertex3f(-size/2, self.water_level, -size/2)
        glVertex3f(size/2, self.water_level, -size/2)
        glVertex3f(size/2, self.water_level, size/2)
        glVertex3f(-size/2, self.water_level, size/2)
        glEnd()
        
        glDisable(GL_BLEND)
        glEnable(GL_TEXTURE_2D)
        
    def get_height(self, x, z):
        terrain_x = int((x + self.size/2) / self.scale)
        terrain_z = int((z + self.size/2) / self.scale)
        
        if 0 <= terrain_x < self.size-1 and 0 <= terrain_z < self.size-1:
            return max(self.height_map[terrain_x][terrain_z], self.water_level)
        return self.water_level