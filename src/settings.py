# Game settings and constants

# Window settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "CosmoDock"
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)

# Physics settings
GRAVITY = 0.1  # Gravity force pulling downwards
THRUST_POWER = 0.2  # Rocket thrust power
ROTATION_SPEED = 3  # Rotation speed in degrees
INITIAL_FUEL = 1000  # Initial fuel amount
FUEL_CONSUMPTION_RATE = 1  # Fuel consumption per thrust
RCS_THRUST_POWER = 0.05  # Fine-tuned RCS thrust power
RCS_FUEL_CONSUMPTION = 0.5  # RCS fuel consumption rate

# Earth settings
EARTH_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT + 300)
EARTH_RADIUS = 400

# ISS settings
ISS_X = SCREEN_WIDTH // 2
ISS_Y = 100
DOCKING_PORT_OFFSET_X = 0  # Offset from ISS center
DOCKING_PORT_OFFSET_Y = 20  # Offset from ISS center

# Docking parameters
MAX_DOCKING_SPEED = 2.0  # Maximum speed allowed for successful docking
DOCKING_ALIGNMENT_THRESHOLD = 10  # Pixels of alignment tolerance
DOCKING_DISTANCE_THRESHOLD = 20  # Distance at which docking is possible

# Game states
STATE_MENU = 0
STATE_PLAYING = 1
STATE_SUCCESS = 2
STATE_FAILURE = 3
STATE_PAUSED = 4

# Asset paths
ROCKET_IMAGE = "assets/images/rocket.png"
ISS_IMAGE = "assets/images/iss.png"
EARTH_IMAGE = "assets/images/earth.png"
STARS_IMAGE = "assets/images/stars.png"
THRUST_SOUND = "assets/sounds/thrust.wav"
WARNING_SOUND = "assets/sounds/warning.wav"
DOCK_SUCCESS_SOUND = "assets/sounds/dock_success.wav"
CRASH_SOUND = "assets/sounds/crash.wav"
SPACE_AMBIENCE_SOUND = "assets/sounds/space_ambience.wav"