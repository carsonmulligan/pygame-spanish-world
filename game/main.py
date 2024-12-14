import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from core.terrain import Terrain
from core.entities.avatar import Avatar
from core.entities.beach_hut import BeachHut
from core.entities.npc import NPC
from PIL import Image

class Game:
    def __init__(self, width=1280, height=720):
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Beach Scene - Barraca 87")
        
        # Initialize OpenGL with better lighting
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)  # Add second light for better illumination
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Enable blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Set up the perspective
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (width/height), 0.1, 150.0)
        glMatrixMode(GL_MODELVIEW)
        
        # Set clear color to sky blue
        glClearColor(0.529, 0.808, 0.922, 1.0)  # Sky blue
        
        # Initialize game objects
        self.terrain = Terrain(size=50, scale=1)
        self.avatar = Avatar(position=(0, 1, 0))
        
        # Initialize beach hut and NPCs
        hut_position = [5, 0, -5]  # Position the hut on the beach
        self.beach_hut = BeachHut(hut_position)
        
        # Create Artur (beach vendor) and Cowboy
        self.artur = NPC(position=[5, 0, -3], name="Artur", hut_position=hut_position)
        self.artur.outfit_color = (1.0, 0.8, 0.4)  # Yellow shirt
        self.artur.pants_color = (0.4, 0.7, 1.0)   # Light blue shorts
        
        self.cowboy = NPC(position=[3, 0, -3], name="Cowboy", hut_position=hut_position)
        self.cowboy.outfit_color = (0.6, 0.3, 0.1)  # Brown shirt
        self.cowboy.pants_color = (0.2, 0.2, 0.7)   # Dark blue jeans
        self.cowboy.walk_radius = 2.0  # Smaller walking radius
        self.cowboy.walk_speed = 0.015  # Slower walking speed
        
        self.textures = self._load_textures()
        self.running = True
        
        # Lock mouse for camera control
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        
        print("Beach scene initialized successfully")
        
    def _load_textures(self):
        textures = {}
        texture_files = {
            'beachscape': 'game/assets/textures/beachscape.png',
            'sand': 'game/assets/textures/beachscape.png',  # Use same texture for sand
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
                self.avatar.rotate(event.rel[0] * 0.5)
                
        # Handle continuous keyboard input
        keys = pygame.key.get_pressed()
        forward = keys[pygame.K_w] - keys[pygame.K_s]
        right = keys[pygame.K_d] - keys[pygame.K_a]
        
        if forward or right:
            self.avatar.move(forward, right)
                    
    def update(self):
        self.avatar.update(self.terrain)
        self.artur.update(self.terrain)
        self.cowboy.update(self.terrain)
        
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Update camera to follow avatar
        camera_pos, look_at = self.avatar.get_camera_position()
        gluLookAt(*camera_pos, *look_at, 0, 1, 0)
        
        # Set up main sunlight
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 0.8, 0.6, 0])  # Angled sunlight
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.5, 0.5, 0.5, 1])  # Brighter ambient
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.95, 0.8, 1])  # Warm sunlight
        
        # Add fill light for shadows
        glLightfv(GL_LIGHT1, GL_POSITION, [-0.5, 0.5, -0.2, 0])  # Fill light
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.2, 0.2, 0.25, 1])  # Slight blue tint
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.3, 0.3, 0.35, 1])  # Soft fill
        
        # Draw terrain with beach texture
        self.terrain.draw(self.textures['beachscape'])
        
        # Draw beach hut
        self.beach_hut.draw()
        
        # Draw NPCs
        self.artur.draw()
        self.cowboy.draw()
        
        # Draw avatar
        self.avatar.draw()
        
        pygame.display.flip()
        
    def run(self):
        print("Starting beach scene")
        clock = pygame.time.Clock()
        frame_count = 0
        
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            
            frame_count += 1
            if frame_count % 60 == 0:
                print(f"FPS: {clock.get_fps():.1f}")
                print(f"Avatar position: {self.avatar.position}")
            
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 