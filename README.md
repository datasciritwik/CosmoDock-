# CosmoDock

# Rocket to ISS - Docking Game

A 2D space simulation game where players control a rocket and attempt to dock with the International Space Station.

## Features

- Realistic physics with gravity, momentum, and inertia
- Fuel management system
- Precise docking mechanics
- Visual and audio feedback

## Installation

1. Clone this repository:
```
git clone https://github.com/datasciritwik/CosmoDock-.git
cd CosmoDock-
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## How to Play

Run the game using:
```
python src/main.py
```

### Controls

- **UP Arrow**: Apply thrust
- **LEFT/RIGHT Arrow**: Rotate the rocket
- **SPACE**: Activate fine-tuned RCS thrusters
- **ESC**: Quit game

### Objective

Successfully dock with the International Space Station by:
1. Achieving a stable approach
2. Keeping your speed below the maximum docking speed
3. Aligning properly with the docking port
4. Conserving enough fuel to complete the mission

## Game Mechanics

- **Gravity**: Stronger near Earth, weaker in space
- **Thrust**: Consumes fuel and propels the rocket
- **Momentum**: The rocket will continue moving without thrust
- **Docking**: Requires precise alignment and approach speed

## Requirements

- Python 3.7+
- Pygame 2.0+

## Credits

This game was created using Python and Pygame.

## License

MIT