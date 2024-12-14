import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from core.terrain import Terrain
from core.entities.avatar import Avatar
from PIL import Image

class Game:
    def __init__(self, width=1280, height=720):
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("3D World MVP - Debug Mode")
        
        # Initialize OpenGL
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Set up the perspective
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (width/height), 0.1, 150.0)
        glMatrixMode(GL_MODELVIEW)
        
        # Set clear color to dark blue for debugging
        glClearColor(0.0, 0.0, 0.2, 1.0)
        
        # Initialize game objects
        self.terrain = Terrain(size=50, scale=1)  # Reduced size for testing
        self.avatar = Avatar(position=(0, 5, 0))  # Raised position for better view
        self.textures = self._load_textures()
        self.running = True
        
        # Lock mouse for camera control
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        
        print("Game initialized successfully")
        
    def _load_textures(self):
        textures = {}
        texture_files = {
            'grass': 'game/assets/textures/grass.jpg',
        }
        
        for name, path in texture_files.items():
            try:
                image = Image.open(path)
                ix = image.size[0]
                iy = image.size[1]
                image = image.tobytes('raw', 'RGBX', 0, -1)
                
                texid = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, texid)
                glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
                
                textures[name] = texid
            except FileNotFoundError:
                print(f"Warning: Texture file not found: {path}")
                # Create a simple checkerboard texture
                textures[name] = self._create_default_texture()
                
        return textures
        
    def _create_default_texture(self):
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        
        # Create a simple checkerboard pattern
        size = 64
        pattern = []
        for i in range(size):
            for j in range(size):
                c = 255 if (i + j) % 2 == 0 else 0
                pattern.extend([c, c, c, 255])
                
        glTexImage2D(GL_TEXTURE_2D, 0, 3, size, size, 0, GL_RGBA, GL_UNSIGNED_BYTE, bytes(pattern))
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        
        return texid
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEMOTION:
                # Rotate avatar based on mouse movement
                self.avatar.rotate(event.rel[0] * 0.5)
                
        # Handle continuous keyboard input
        keys = pygame.key.get_pressed()
        forward = keys[pygame.K_w] - keys[pygame.K_s]
        right = keys[pygame.K_d] - keys[pygame.K_a]
        
        if forward or right:
            self.avatar.move(forward, right)
                    
    def update(self):
        self.avatar.update(self.terrain)
        
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Update camera to follow avatar
        camera_pos, look_at = self.avatar.get_camera_position()
        gluLookAt(*camera_pos, *look_at, 0, 1, 0)
        
        # Set up lighting
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1])
        
        # Draw debug grid
        self._draw_debug_grid()
        
        # Draw terrain with enhanced visibility
        glColor3f(0.5, 0.8, 0.5)  # Set color to light green
        self.terrain.draw(self.textures['grass'])
        
        # Draw avatar
        self.avatar.draw()
        
        pygame.display.flip()
        
    def _draw_debug_grid(self):
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        
        # Draw grid lines
        glColor3f(0.5, 0.5, 0.5)
        for i in range(-10, 11):
            glVertex3f(i, 0, -10)
            glVertex3f(i, 0, 10)
            glVertex3f(-10, 0, i)
            glVertex3f(10, 0, i)
            
        # Draw coordinate axes
        glColor3f(1, 0, 0)  # X axis (red)
        glVertex3f(0, 0, 0)
        glVertex3f(5, 0, 0)
        
        glColor3f(0, 1, 0)  # Y axis (green)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 5, 0)
        
        glColor3f(0, 0, 1)  # Z axis (blue)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 5)
        
        glEnd()
        glEnable(GL_LIGHTING)
        
    def run(self):
        print("Starting game loop")
        clock = pygame.time.Clock()
        frame_count = 0
        
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            
            frame_count += 1
            if frame_count % 60 == 0:  # Print debug info every 60 frames
                print(f"FPS: {clock.get_fps():.1f}")
                print(f"Avatar position: {self.avatar.position}")
            
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 