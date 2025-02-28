from settings import (
    STATE_MENU, STATE_PLAYING, STATE_SUCCESS, STATE_FAILURE, STATE_PAUSED,
    SCREEN_WIDTH, SCREEN_HEIGHT
)
from rocket import Rocket
from iss import ISS
from ui import UI
from physics import (
    calculate_distance, check_collision, calculate_approach_speed,
    check_docking_alignment
)
from settings import (
    MAX_DOCKING_SPEED, DOCKING_ALIGNMENT_THRESHOLD, DOCKING_DISTANCE_THRESHOLD
)

class GameState:
    def __init__(self):
        self.current_state = STATE_MENU
        self.rocket = Rocket(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.iss = ISS()
        self.ui = UI()
        
        # Game status flags
        self.docking_successful = False
        self.out_of_fuel = False
        self.crashed = False
        self.drifted_away = False
        
        # Sound effects will be loaded in main.py
        self.sounds = {}
        
    def update(self):
        if self.current_state == STATE_PLAYING:
            # Update game objects
            self.rocket.update()
            self.iss.update()
            
            # Check win/lose conditions
            self.check_docking()
            self.check_failure_conditions()
    
    def check_docking(self):
        # Calculate distance between rocket and ISS docking port
        distance = calculate_distance(
            self.rocket, 
            type('obj', (), {'x': self.iss.docking_port_x, 'y': self.iss.docking_port_y})
        )
        
        # Check if close enough to dock
        if distance < DOCKING_DISTANCE_THRESHOLD:
            # Check approach speed
            approach_speed = calculate_approach_speed(self.rocket, self.iss)
            
            # Check alignment
            aligned = check_docking_alignment(
                self.rocket, self.iss, DOCKING_ALIGNMENT_THRESHOLD
            )
            
            # Successful docking conditions
            if abs(approach_speed) < MAX_DOCKING_SPEED and aligned:
                self.docking_successful = True
                self.current_state = STATE_SUCCESS
                if 'dock_success' in self.sounds:
                    self.sounds['dock_success'].play()
            # Crash condition - too fast
            elif abs(approach_speed) >= MAX_DOCKING_SPEED:
                self.crashed = True
                self.current_state = STATE_FAILURE
                if 'crash' in self.sounds:
                    self.sounds['crash'].play()
    
    def check_failure_conditions(self):
        # Check if out of fuel
        if self.rocket.is_fuel_empty():
            self.out_of_fuel = True
            self.current_state = STATE_FAILURE
        
        # Check if rocket has drifted too far away
        if (self.rocket.x < -200 or self.rocket.x > SCREEN_WIDTH + 200 or 
            self.rocket.y < -200 or self.rocket.y > SCREEN_HEIGHT + 200):
            self.drifted_away = True
            self.current_state = STATE_FAILURE
        
        # Check for collision with ISS (outside of docking port)
        if check_collision(self.rocket, self.iss, self.rocket.collision_radius + self.iss.collision_radius):
            # If we're not near the docking port, it's a crash
            if not check_docking_alignment(self.rocket, self.iss, DOCKING_ALIGNMENT_THRESHOLD * 2):
                self.crashed = True
                self.current_state = STATE_FAILURE
                if 'crash' in self.sounds:
                    self.sounds['crash'].play()
    
    def reset_game(self):
        # Reset the rocket
        self.rocket.reset(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        # Reset game status
        self.current_state = STATE_PLAYING
        self.docking_successful = False
        self.out_of_fuel = False
        self.crashed = False
        self.drifted_away = False
    
    def get_failure_message(self):
        if self.out_of_fuel:
            return "OUT OF FUEL"
        elif self.crashed:
            return "CRASHED INTO ISS"
        elif self.drifted_away:
            return "DRIFTED OUT OF RANGE"
        else:
            return "MISSION FAILED"