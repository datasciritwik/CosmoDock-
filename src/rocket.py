import pygame
import math
from settings import (
    THRUST_POWER, ROTATION_SPEED, INITIAL_FUEL, 
    FUEL_CONSUMPTION_RATE, RCS_THRUST_POWER, RCS_FUEL_CONSUMPTION
)
from physics import apply_gravity, apply_thrust

class Rocket:
    def __init__(self, x, y):
        self.original_image = pygame.image.load("assets/images/rocket.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        # Position and movement
        self.x = x
        self.y = y
        self.angle = 90  # Starting angle (pointing up)
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Dimensions
        self.width = self.rect.width
        self.height = self.rect.height
        
        # Rocket status
        self.fuel = INITIAL_FUEL
        self.is_thrusting = False
        self.is_rotating_left = False
        self.is_rotating_right = False
        self.is_using_rcs = False
        
        # Thruster animation
        self.thruster_frames = []
        # In a real implementation, load thruster animation frames here
        
        # Collision properties
        self.collision_radius = min(self.width, self.height) // 2
        
    def update(self):
        # Apply gravity
        apply_gravity(self)
        
        # Handle rotation
        if self.is_rotating_left:
            self.angle += ROTATION_SPEED
        if self.is_rotating_right:
            self.angle -= ROTATION_SPEED
        
        # Keep angle in the range [0, 360)
        self.angle = self.angle % 360
        
        # Handle main thruster
        if self.is_thrusting and self.fuel > 0:
            apply_thrust(self, THRUST_POWER, self.angle)
            self.fuel -= FUEL_CONSUMPTION_RATE
        
        # Handle RCS thrusters for fine adjustments
        if self.is_using_rcs and self.fuel > 0:
            apply_thrust(self, RCS_THRUST_POWER, self.angle)
            self.fuel -= RCS_FUEL_CONSUMPTION
        
        # Update position based on velocity
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Apply drag (very slight in space)
        self.velocity_x *= 0.995
        self.velocity_y *= 0.995
        
        # Update the rocket image based on the current angle
        self.image = pygame.transform.rotate(self.original_image, -self.angle + 90)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def draw(self, screen):
        # Draw the rocket at its current position and rotation
        screen.blit(self.image, self.rect)
        
        # Draw thruster flames if thrusting
        if self.is_thrusting and self.fuel > 0:
            self.draw_thruster(screen)
    
    def draw_thruster(self, screen):
        # This is a simple thruster visualization
        # In a real implementation, you would use animated flame sprites
        
        # Calculate thruster position at the bottom of the rocket
        thruster_length = 20
        thruster_width = 10
        
        # Calculate the position at the bottom of the rocket
        angle_rad = math.radians(self.angle)
        flame_x = self.x - math.cos(angle_rad) * self.height/2
        flame_y = self.y + math.sin(angle_rad) * self.height/2
        
        # Draw a simple flame triangle
        points = [
            (flame_x, flame_y),
            (flame_x - thruster_width/2 * math.sin(angle_rad), 
             flame_y - thruster_width/2 * math.cos(angle_rad)),
            (flame_x - thruster_length * math.cos(angle_rad), 
             flame_y + thruster_length * math.sin(angle_rad)),
            (flame_x + thruster_width/2 * math.sin(angle_rad), 
             flame_y + thruster_width/2 * math.cos(angle_rad))
        ]
        
        pygame.draw.polygon(screen, (255, 165, 0), points)  # Orange flame
        
    def get_velocity_magnitude(self):
        """Get the total velocity magnitude."""
        return math.sqrt(self.velocity_x**2 + self.velocity_y**2)
    
    def is_fuel_empty(self):
        """Check if the rocket is out of fuel."""
        return self.fuel <= 0
    
    def reset(self, x, y):
        """Reset the rocket to initial state."""
        self.x = x
        self.y = y
        self.angle = 90
        self.velocity_x = 0
        self.velocity_y = 0
        self.fuel = INITIAL_FUEL
        self.is_thrusting = False
        self.is_rotating_left = False
        self.is_rotating_right = False
        self.is_using_rcs = False