from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time
import numpy as np

# ============================================================================
# INTERACTIVE BLACK HOLE & SUPERNOVA VISUALIZER
# CSE423 Final Project - Team Implementation
# 
# SOLAR SYSTEM & BLACK HOLE SIMULATION - COMPREHENSIVE FEATURE SET
# ============================================================================
#
# CORE SIMULATION FEATURES:
# • Solar System Simulation: Sun at center with 8 planets in stable orbits
# • Controllable Spaceship: Spawn with G, control with W/S/A/D/E/Q/Z/C, despawn with L
# • Advanced Camera Movement: Zoom with 5/6, cycle views with V (orbital/third-person/first-person)
# • Black Hole Implementation: Triggered by B key (Sun -> Supernova -> Black Hole sequence)
# • Gravitational Force Simulation: Realistic physics with Sun/black hole gravity
# • Event Horizon and Destruction: Planets destroyed at event horizon, become particle clouds
# • Free-Floating Physics (Collision Preset): P key removes Sun, planets set on collision course
# • Collision Detection and Rebound: Realistic planet-to-planet interactions based on mass/velocity
# • Interactive Supernova: X key triggers red giant expansion -> engulfs planets -> supernova explosion
# • Reset Functionality: R key resets entire simulation to initial state
#
# FEATURE ATTRIBUTION BY DEVELOPER:
# ============================================================================
# 
# SHAHID GALIB - FEATURES 1-3: VISUAL FOUNDATION & SOLAR SYSTEM
# • Feature 1: Window Setup & Starfield Background (2000 stars)
# • Feature 2: Complete Solar System (Sun + 8 Planets with realistic orbits)
# • Feature 3: Orbital Camera System with Mouse Controls
#
# FARHAN ZARIF - FEATURES 4-6: BLACK HOLE PHYSICS & EFFECTS  
# • Feature 4: Black Hole Visual Effects (Photon Ring, Accretion Disk, Lensing)
# • Feature 5: Gravitational Physics Engine (Newton's Law, Velocity Verlet)
# • Feature 6: Black Hole Capture Mechanics (Tidal Forces, Event Horizon)
#
# EVAN YUVRAJ MUNSHI - FEATURES 7-9: INTERACTIVE SYSTEMS & SEQUENCES
# • Feature 7: Interactive Supernova (X key: Red giant expansion -> supernova explosion)
# • Feature 8: Free-Floating Physics (P key: Collision preset with Sun removal)
# • Feature 9: Collision Detection & Rebound (Realistic planet-to-planet interactions)
# ============================================================================
# ============================================================================
# TUNABLE CONSTANTS
# ============================================================================

# SHAHID GALIB - VISUAL FOUNDATION & SOLAR SYSTEM CONSTANTS
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
STARFIELD_COUNT = 2000
SUN_INITIAL_RADIUS = 20.0
SUN_MASS = 1000.0
GAME_STATE_MENU = 0
GAME_STATE_SIMULATION = 1
game_state = GAME_STATE_MENU
mouse_x = 0
mouse_y = 0
start_button_hover = False
MENU_MAIN = 0
MENU_ABOUT = 1

# Planet configuration data: [name, mass, radius, orbit_distance, color, initial_angle]
PLANET_DATA = [
    ["Mercury", 10.0, 3.0, 80.0, (0.7, 0.7, 0.7), 0.0],
    ["Venus", 15.0, 4.0, 110.0, (1.0, 0.8, 0.0), 45.0],
    ["Earth", 20.0, 5.0, 150.0, (0.0, 0.5, 1.0), 90.0],
    ["Mars", 12.0, 4.0, 200.0, (1.0, 0.3, 0.0), 135.0],
    ["Jupiter", 100.0, 15.0, 300.0, (1.0, 0.6, 0.2), 180.0],
    ["Saturn", 80.0, 12.0, 400.0, (1.0, 1.0, 0.6), 225.0],
    ["Uranus", 40.0, 8.0, 500.0, (0.0, 1.0, 1.0), 27]
]

# ============================================================================
# GLOBAL VARIABLES
# ============================================================================

# SHAHID GALIB - VISUAL FOUNDATION & SOLAR SYSTEM VARIABLES
last_time = 0.0
current_time = 0.0
is_solar_system_active = True
sun_exists = True
sun_position = np.array([0.0, 0.0, 0.0])
planets = []
selected_planet_index = 0
starfield = []
camera_state = {
    'target': np.array([0.0, 0.0, 0.0]),
    'distance': 200.0,
    'azimuth': 0.0,
    'elevation': 30.0,
    'is_following_planet': False
}
spaceship_exists = False
spaceship_position = np.array([0.0, 0.0, 200.0])
spaceship_velocity = np.array([0.0, 0.0, 0.0])
spaceship_rotation = np.array([0.0, 0.0, 0.0])
spaceship_scale = 4.0
spaceship_physics_mode = True
camera_mode = 0
spaceship_thrust = 200.0
spaceship_max_speed = 100.0
spaceship_collision_radius = 8.0
camera_transition_active = False
camera_transition_start = 0.0
camera_transition_duration = 0.6
camera_start_pos = np.array([0.0, 0.0, 0.0])
camera_start_target = np.array([0.0, 0.0, 0.0])

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

# SHAHID GALIB - VISUAL FOUNDATION & SOLAR SYSTEM UTILITIES
def normalize_vector(v):
    """Normalize a numpy vector"""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def lerp(a, b, t):
    """Linear interpolation between a and b by factor t"""
    return a + t * (b - a)

def lerp_color(color1, color2, t):
    """Linear interpolation between two RGB colors"""
    return tuple(lerp(color1[i], color2[i], t) for i in range(3))

def show_screen():
  pass
def keyboard_listener():
  pass
def special_key_listener():
  pass
def mouse_listener():
  pass
def idle():
  pass


def main():
    """Main function to initialize and run the simulation"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Limen Tenebrae: An Interactive Black Hole Physics Simulator")
    
    glEnable(GL_DEPTH_TEST)
    
    glClearColor(0.0, 0.0, 0.1, 1.0)
    
    glutDisplayFunc(show_screen)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    glutIdleFunc(idle)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
