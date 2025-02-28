import math
from src.settings import GRAVITY, EARTH_POSITION, EARTH_RADIUS

def apply_gravity(obj, distance_factor=1.0):
    """
    Apply gravity to an object based on its distance from Earth.
    The gravity effect decreases with distance.
    
    Args:
        obj: Object with position, velocity attributes
        distance_factor: Factor to adjust gravity (1.0 is full Earth gravity)
    """
    # Calculate distance from Earth center
    distance_to_earth = math.sqrt((obj.x - EARTH_POSITION[0])**2 + (obj.y - EARTH_POSITION[1])**2)
    
    # Normalize distance (1.0 at Earth's surface, decreasing as we get farther)
    normalized_distance = EARTH_RADIUS / max(distance_to_earth, EARTH_RADIUS)
    
    # Calculate gravity effect - decreases with square of distance
    gravity_effect = GRAVITY * normalized_distance**2 * distance_factor
    
    # Apply gravity to velocity
    obj.velocity_y += gravity_effect

def apply_thrust(obj, thrust_power, angle=90):
    """
    Apply thrust to an object in the direction of its angle.
    
    Args:
        obj: Object with velocity attributes
        thrust_power: Amount of thrust to apply
        angle: Angle in degrees (default 90 = upward)
    """
    # Convert angle to radians
    angle_rad = math.radians(angle)
    
    # Calculate thrust components
    thrust_x = thrust_power * math.cos(angle_rad)
    thrust_y = -thrust_power * math.sin(angle_rad)  # Negative because y increases downward
    
    # Apply thrust to velocity
    obj.velocity_x += thrust_x
    obj.velocity_y += thrust_y

def calculate_distance(obj1, obj2):
    """Calculate distance between two objects with x, y attributes."""
    return math.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)

def check_collision(obj1, obj2, collision_threshold):
    """Check if two objects are colliding based on a distance threshold."""
    distance = calculate_distance(obj1, obj2)
    return distance < collision_threshold

def calculate_approach_speed(obj1, obj2):
    """Calculate the approach speed between two objects."""
    # Calculate relative velocity
    rel_vx = obj1.velocity_x - obj2.velocity_x
    rel_vy = obj1.velocity_y - obj2.velocity_y
    
    # Get unit vector in the direction from obj1 to obj2
    dx = obj2.x - obj1.x
    dy = obj2.y - obj1.y
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance == 0:
        return 0
    
    dx /= distance
    dy /= distance
    
    # Project the relative velocity onto the direction vector
    approach_speed = rel_vx * dx + rel_vy * dy
    
    return approach_speed

def check_docking_alignment(rocket, iss, threshold):
    """Check if the rocket is aligned with the ISS docking port."""
    # This is a simplified alignment check
    # In a more advanced version, you would check the rocket's angle as well
    horizontal_alignment = abs(rocket.x - iss.docking_port_x) < threshold
    return horizontal_alignment