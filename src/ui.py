import pygame
from src.settings import (
    WHITE, BLACK, RED, GREEN, YELLOW, SCREEN_WIDTH, SCREEN_HEIGHT,
    MAX_DOCKING_SPEED, INITIAL_FUEL
)

class UI:
    def __init__(self):
        # Initialize fonts
        pygame.font.init()
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_large = pygame.font.Font(None, 72)
        
        # Warning indicator states
        self.speed_warning = False
        self.fuel_warning = False
        
    def draw_hud(self, screen, rocket, iss, distance):
        # Draw velocity info
        velocity_text = f"Velocity: {rocket.get_velocity_magnitude():.1f} m/s"
        vel_surface = self.font_small.render(velocity_text, True, WHITE)
        screen.blit(vel_surface, (10, 10))
        
        # Draw fuel gauge
        self.draw_fuel_bar(screen, rocket.fuel)
        
        # Draw distance to ISS
        distance_text = f"Distance to ISS: {distance:.1f} m"
        dist_surface = self.font_small.render(distance_text, True, WHITE)
        screen.blit(dist_surface, (10, 40))
        
        # Draw approach speed indicator
        self.draw_approach_speed(screen, rocket, iss)
        
        # Draw alignment indicator
        self.draw_alignment_indicator(screen, rocket, iss)
        
    def draw_fuel_bar(self, screen, fuel):
        # Draw fuel bar background
        bar_width = 150
        bar_height = 20
        bar_x = SCREEN_WIDTH - bar_width - 10
        bar_y = 10
        
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Draw fuel level
        fuel_percentage = max(0, min(1, fuel / INITIAL_FUEL))
        filled_width = int(bar_width * fuel_percentage)
        
        # Choose color based on fuel level
        color = GREEN
        if fuel_percentage < 0.5:
            color = YELLOW
        if fuel_percentage < 0.25:
            color = RED
            self.fuel_warning = True
        else:
            self.fuel_warning = False
            
        pygame.draw.rect(screen, color, (bar_x, bar_y, filled_width, bar_height))
        
        # Draw fuel text
        fuel_text = f"Fuel: {int(fuel)}"
        fuel_surface = self.font_small.render(fuel_text, True, WHITE)
        screen.blit(fuel_surface, (bar_x, bar_y + bar_height + 5))
    
    def draw_approach_speed(self, screen, rocket, iss):
        # Calculate the vertical component of velocity (for approach)
        approach_speed = abs(rocket.velocity_y)
        
        # Position for the indicator
        indicator_x = SCREEN_WIDTH - 170
        indicator_y = 70
        
        # Draw the label
        speed_text = f"Approach Speed: {approach_speed:.1f} m/s"
        
        # Set color based on speed
        color = GREEN
        if approach_speed > MAX_DOCKING_SPEED * 0.7:
            color = YELLOW
        if approach_speed > MAX_DOCKING_SPEED:
            color = RED
            self.speed_warning = True
        else:
            self.speed_warning = False
            
        speed_surface = self.font_small.render(speed_text, True, color)
        screen.blit(speed_surface, (indicator_x, indicator_y))
    
    def draw_alignment_indicator(self, screen, rocket, iss):
        # Calculate horizontal alignment
        x_diff = rocket.x - iss.docking_port_x
        
        # Position for the indicator
        indicator_x = SCREEN_WIDTH // 2 - 100
        indicator_y = SCREEN_HEIGHT - 50
        indicator_width = 200
        indicator_height = 20
        
        # Draw alignment bar background
        pygame.draw.rect(screen, WHITE, (indicator_x, indicator_y, indicator_width, indicator_height), 1)
        
        # Draw center marker
        center_x = indicator_x + indicator_width // 2
        pygame.draw.line(screen, WHITE, (center_x, indicator_y - 5), (center_x, indicator_y + indicator_height + 5), 2)
        
        # Calculate position of alignment indicator
        # Map x_diff from [-100, 100] to [0, indicator_width]
        normalized_diff = max(-100, min(100, x_diff))
        indicator_pos = center_x + normalized_diff
        
        # Draw indicator
        pygame.draw.circle(screen, YELLOW, (int(indicator_pos), indicator_y + indicator_height // 2), 10)
        
        # Draw alignment text
        alignment_text = "Alignment"
        alignment_surface = self.font_small.render(alignment_text, True, WHITE)
        screen.blit(alignment_surface, (indicator_x, indicator_y - 25))
    
    def draw_game_over(self, screen, success):
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with alpha
        screen.blit(overlay, (0, 0))
        
        # Draw game over message
        if success:
            message = "DOCKING SUCCESSFUL!"
            color = GREEN
        else:
            message = "MISSION FAILED"
            color = RED
            
        text_surface = self.font_large.render(message, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(text_surface, text_rect)
        
        # Draw restart instructions
        restart_text = "Press SPACE to Restart or ESC to Quit"
        restart_surface = self.font_medium.render(restart_text, True, WHITE)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        screen.blit(restart_surface, restart_rect)
        
    def draw_menu(self, screen):
        # Draw title
        title_text = "ROCKET TO ISS"
        title_surface = self.font_large.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        screen.blit(title_surface, title_rect)
        
        # Draw instructions
        instructions = [
            "Mission: Dock with the International Space Station",
            "",
            "Controls:",
            "UP Arrow: Apply Thrust",
            "LEFT/RIGHT Arrow: Rotate Rocket",
            "SPACE: Fine-tuned RCS Thrusters",
            "ESC: Quit Game",
            "",
            "Press SPACE to Begin Mission"
        ]
        
        y_pos = SCREEN_HEIGHT // 2 - 50
        for line in instructions:
            text_surface = self.font_medium.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, y_pos))
            screen.blit(text_surface, text_rect)
            y_pos += 30
    
    def draw_warning(self, screen, message):
        # Draw warning message at the center of the screen
        text_surface = self.font_medium.render(message, True, RED)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text_surface, text_rect)