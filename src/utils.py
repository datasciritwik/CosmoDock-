import pygame
import os
import random

def load_image(filename, use_alpha=True):
    """Load an image from the assets folder with transparency."""
    try:
        if use_alpha:
            return pygame.image.load(filename).convert_alpha()
        else:
            return pygame.image.load(filename).convert()
    except pygame.error as e:
        print(f"Unable to load image: {filename}")
        print(e)
        return pygame.Surface((100, 100))

def load_sound(filename):
    """Load a sound file from the assets folder."""
    try:
        return pygame.mixer.Sound(filename)
    except pygame.error as e:
        print(f"Unable to load sound: {filename}")
        print(e)
        return None

def create_stars_background(width, height, num_stars=100):
    """Create a starry background surface."""
    bg = pygame.Surface((width, height))
    bg.fill((0, 0, 20))  # Dark blue background
    
    # Add random stars
    for _ in range(num_stars):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        brightness = random.randint(128, 255)
        size = random.randint(1, 3)
        pygame.draw.circle(bg, (brightness, brightness, brightness), (x, y), size)
    
    return bg

def create_missing_directories():
    """Create necessary directories if they don't exist."""
    directories = [
        "assets",
        "assets/images",
        "assets/sounds"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def create_placeholder_assets():
    """Create simple placeholder assets if the real ones don't exist."""
    # Placeholder for rocket
    if not os.path.exists("assets/images/rocket.png"):
        surface = pygame.Surface((20, 40), pygame.SRCALPHA)
        pygame.draw.polygon(surface, (200, 200, 200), [(10, 0), (0, 40), (20, 40)])
        pygame.image.save(surface, "assets/images/rocket.png")
        print("Created placeholder rocket image")
    
    # Placeholder for ISS
    if not os.path.exists("assets/images/iss.png"):
        surface = pygame.Surface((100, 50), pygame.SRCALPHA)
        pygame.draw.rect(surface, (180, 180, 180), (0, 20, 100, 30))
        pygame.draw.rect(surface, (120, 120, 120), (40, 0, 20, 20))
        pygame.draw.rect(surface, (100, 100, 100), (20, 30, 60, 10))
        pygame.image.save(surface, "assets/images/iss.png")
        print("Created placeholder ISS image")
    
    # Placeholder for Earth
    if not os.path.exists("assets/images/earth.png"):
        surface = pygame.Surface((800, 400), pygame.SRCALPHA)
        pygame.draw.circle(surface, (0, 100, 200), (400, 400), 400)
        pygame.image.save(surface, "assets/images/earth.png")
        print("Created placeholder Earth image")