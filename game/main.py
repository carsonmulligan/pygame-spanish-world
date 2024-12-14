import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from core.player import Player
from core.world import World

class Game:
    def __init__(self, width=1280, height=720):
        pygame.init()
        pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Language Border Crossing - 3D World")
        
        # Initialize OpenGL
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Set up the perspective
        gluPerspective(45, (width/height), 0.1, 50.0)
        
        # Initialize game objects
        self.player = Player()
        self.world = World()
        self.running = True
        
        # Lock and hide mouse cursor for camera control
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEMOTION:
                # Rotate camera based on mouse movement
                self.player.rotate(event.rel[0])
                
        # Handle continuous keyboard input
        keys = pygame.key.get_pressed()
        forward = keys[pygame.K_w] - keys[pygame.K_s]
        right = keys[pygame.K_d] - keys[pygame.K_a]
        
        # Calculate new position
        new_position = self.player.position.copy()
        if forward or right:
            self.player.move(forward, right)
            
            # Check for collisions and revert if necessary
            if self.world.check_collision(self.player.position):
                self.player.position = new_position
                    
    def update(self):
        pass
        
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Update camera position based on player
        self.player.update_camera()
        
        # Set up lighting
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
        
        # Draw the world
        self.world.draw()
        
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            pygame.time.wait(10)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 