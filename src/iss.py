import pygame
from settings import ISS_X, ISS_Y, DOCKING_PORT_OFFSET_X, DOCKING_PORT_OFFSET_Y

class ISS:
    def __init__(self):
        self.original_image = pygame.image.load("assets/images/iss.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        # Position
        self.x = ISS_X
        self.y = ISS_Y
        self.rect.center = (self.x, self.y)
        
        # Docking port position (relative to ISS center)
        self.docking_port_x = self.x + DOCKING_PORT_OFFSET_X
        self.docking_port_y = self.y + DOCKING_PORT_OFFSET_Y
        
        # For collision detection
        self.width = self.rect.width
        self.height = self.rect.height
        self.collision_radius = max(self.width, self.height) / 2
        
        # ISS has zero velocity (stationary in this game)
        self.velocity_x = 0
        self.velocity_y = 0
    
    def update(self):
        # ISS is stationary in this version of the game
        pass
    
    def draw(self, screen):
        # Draw the ISS
        screen.blit(self.image, self.rect)
        
        # Optional: Draw the docking port visually
        pygame.draw.circle(
            screen, 
            (255, 255, 0),  # Yellow
            (int(self.docking_port_x), int(self.docking_port_y)), 
            5,  # Radius
            2   # Line thickness
        )