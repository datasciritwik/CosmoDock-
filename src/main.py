import pygame
import sys
import os
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS, BLACK, WHITE,
    STATE_MENU, STATE_PLAYING, STATE_SUCCESS, STATE_FAILURE, STATE_PAUSED,
    THRUST_SOUND, WARNING_SOUND, DOCK_SUCCESS_SOUND, CRASH_SOUND, SPACE_AMBIENCE_SOUND,
    EARTH_POSITION, EARTH_RADIUS
)
from game_state import GameState
from physics import calculate_distance
from utils import (
    load_image, load_sound, create_stars_background, 
    create_missing_directories, create_placeholder_assets
)

class Game:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Create screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        
        # Set up clock
        self.clock = pygame.time.Clock()
        
        # Create necessary directories and placeholder assets
        create_missing_directories()
        create_placeholder_assets()
        
        # Load background images
        self.stars_bg = create_stars_background(SCREEN_WIDTH, SCREEN_HEIGHT, 150)
        try:
            self.earth_image = load_image("assets/images/earth.png")
        except:
            # Create a simple earth circle if image loading fails
            self.earth_image = pygame.Surface((EARTH_RADIUS*2, EARTH_RADIUS*2), pygame.SRCALPHA)
            pygame.draw.circle(self.earth_image, (0, 100, 200), (EARTH_RADIUS, EARTH_RADIUS), EARTH_RADIUS)
        
        # Initialize game state
        self.game_state = GameState()
        
        # Load sounds
        self.load_game_sounds()
        
        # Start background ambience
        if 'ambience' in self.game_state.sounds:
            self.game_state.sounds['ambience'].play(-1)  # Loop indefinitely
    
    def load_game_sounds(self):
        # Load and store sounds in the game state
        self.game_state.sounds = {
            'thrust': load_sound(THRUST_SOUND),
            'warning': load_sound(WARNING_SOUND),
            'dock_success': load_sound(DOCK_SUCCESS_SOUND),
            'crash': load_sound(CRASH_SOUND),
            'ambience': load_sound(SPACE_AMBIENCE_SOUND)
        }
    
    def handle_events(self):
        for event in pygame.event.get():
            # Quit events
            if event.type == pygame.QUIT:
                return False
            
            # Key press events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                # State-specific key handling
                if self.game_state.current_state == STATE_MENU:
                    if event.key == pygame.K_SPACE:
                        self.game_state.current_state = STATE_PLAYING
                
                elif self.game_state.current_state in [STATE_SUCCESS, STATE_FAILURE]:
                    if event.key == pygame.K_SPACE:
                        self.game_state.reset_game()
                
                elif self.game_state.current_state == STATE_PLAYING:
                    # Thruster controls
                    if event.key == pygame.K_UP:
                        self.game_state.rocket.is_thrusting = True
                        if 'thrust' in self.game_state.sounds:
                            self.game_state.sounds['thrust'].play()
                    
                    # Rotation controls
                    if event.key == pygame.K_LEFT:
                        self.game_state.rocket.is_rotating_left = True
                    if event.key == pygame.K_RIGHT:
                        self.game_state.rocket.is_rotating_right = True
                    
                    # RCS thrusters
                    if event.key == pygame.K_SPACE:
                        self.game_state.rocket.is_using_rcs = True
            
            # Key release events
            if event.type == pygame.KEYUP:
                if self.game_state.current_state == STATE_PLAYING:
                    if event.key == pygame.K_UP:
                        self.game_state.rocket.is_thrusting = False
                        if 'thrust' in self.game_state.sounds:
                            self.game_state.sounds['thrust'].stop()
                    
                    if event.key == pygame.K_LEFT:
                        self.game_state.rocket.is_rotating_left = False
                    if event.key == pygame.K_RIGHT:
                        self.game_state.rocket.is_rotating_right = False
                    
                    if event.key == pygame.K_SPACE:
                        self.game_state.rocket.is_using_rcs = False
        
        return True
    
    def update(self):
        # Update game state
        self.game_state.update()
        
        # Play warnings if needed
        if self.game_state.ui.speed_warning or self.game_state.ui.fuel_warning:
            if 'warning' in self.game_state.sounds and not pygame.mixer.find_channel().get_busy():
                self.game_state.sounds['warning'].play()
    
    def draw(self):
        # Clear the screen
        self.screen.fill(BLACK)
        
        # Draw stars background
        self.screen.blit(self.stars_bg, (0, 0))
        
        # Draw Earth
        earth_pos = (
            EARTH_POSITION[0] - EARTH_RADIUS,
            EARTH_POSITION[1] - EARTH_RADIUS
        )
        self.screen.blit(self.earth_image, earth_pos)
        
        # Draw game objects
        if self.game_state.current_state != STATE_MENU:
            self.game_state.rocket.draw(self.screen)
            self.game_state.iss.draw(self.screen)
        
        # Draw UI elements based on current state
        if self.game_state.current_state == STATE_MENU:
            self.game_state.ui.draw_menu(self.screen)
        
        elif self.game_state.current_state == STATE_PLAYING:
            # Calculate distance for UI
            distance = calculate_distance(self.game_state.rocket, self.game_state.iss)
            self.game_state.ui.draw_hud(self.screen, self.game_state.rocket, self.game_state.iss, distance)
        
        elif self.game_state.current_state == STATE_SUCCESS:
            distance = calculate_distance(self.game_state.rocket, self.game_state.iss)
            self.game_state.ui.draw_hud(self.screen, self.game_state.rocket, self.game_state.iss, distance)
            self.game_state.ui.draw_game_over(self.screen, True)
        
        elif self.game_state.current_state == STATE_FAILURE:
            distance = calculate_distance(self.game_state.rocket, self.game_state.iss)
            self.game_state.ui.draw_hud(self.screen, self.game_state.rocket, self.game_state.iss, distance)
            self.game_state.ui.draw_game_over(self.screen, False)
            # Draw specific failure message
            failure_message = self.game_state.get_failure_message()
            self.game_state.ui.draw_warning(self.screen, failure_message)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Maintain frame rate
            self.clock.tick(FPS)
        
        # Clean up and quit
        pygame.quit()
        sys.exit()

# Entry point
if __name__ == "__main__":
    game = Game()
    game.run()