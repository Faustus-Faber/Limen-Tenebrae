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

# FARHAN ZARIF - BLACK HOLE PHYSICS & EFFECTS CONSTANTS
BLACK_HOLE_MASS = 1000.0
BLACK_HOLE_SCALE_FACTOR = 0.1
BLACK_HOLE_VISUAL_RADIUS = 20.0
BLACK_HOLE_FADE_IN_DURATION = 0.5
ACCRETION_DISK_ROTATION_SPEED = 0.5
TIDAL_RADIUS_MULTIPLIER = 3.0
LOGICAL_CAPTURE_RADIUS_MULTIPLIER = 5.0
SPIRAL_DECAY_RATE = 0.02
G = 10000.0
DT = 0.016

# EVAN YUVRAJ MUNSHI - INTERACTIVE SYSTEMS & SEQUENCES CONSTANTS
SUPERNOVA_DURATION = 3.0
RED_GIANT_DURATION = 5.0
RED_GIANT_MAX_RADIUS = 120.0
RED_GIANT_EXPANSION_RATE = (RED_GIANT_MAX_RADIUS - SUN_INITIAL_RADIUS) / RED_GIANT_DURATION
DEBRIS_LIFETIME = 1000.0
DEBRIS_EXPLOSION_SPEED = 50.0
COLLISION_THRESHOLD_MULTIPLIER = 1.2
RESTITUTION_COEFFICIENT = 0.8
MIN_COLLISION_VELOCITY = 0.1

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

# FARHAN ZARIF - BLACK HOLE PHYSICS & EFFECTS VARIABLES
is_black_hole_active = False
black_hole_position = np.array([0.0, 0.0, 0.0])
black_hole_mass = BLACK_HOLE_MASS
black_hole_alpha = 0.0
accretion_disk_rotation = 0.0

# EVAN YUVRAJ MUNSHI - INTERACTIVE SYSTEMS & SEQUENCES VARIABLES
is_supernova_active = False
keys_locked = False
is_red_giant_active = False
red_giant_start_time = 0.0
current_sun_radius = SUN_INITIAL_RADIUS
engulfed_planets = []
supernova_particles = []
supernova_start_time = 0.0
debris_particles = []
debris_generation_cooldown = 0.0
sequence_start_time = 0.0
sequence_stage = 0

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

def calculate_schwarzschild_radius(mass):
    """Calculate Schwarzschild radius for given mass"""
    return BLACK_HOLE_SCALE_FACTOR * mass

def calculate_tidal_radius(mass):
    """Calculate tidal radius for spaghettification"""
    return calculate_schwarzschild_radius(mass) * TIDAL_RADIUS_MULTIPLIER

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Draw text at screen coordinates"""
    glColor3f(1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

#Munshi
def reset_simulation():
    """Reset the simulation to initial state"""
    global is_solar_system_active, is_black_hole_active, is_supernova_active
    global sun_exists, black_hole_mass, black_hole_alpha, selected_planet_index
    global supernova_particles, debris_particles, sequence_start_time, sequence_stage
    global accretion_disk_rotation, camera_state
    
    is_solar_system_active = True
    is_black_hole_active = False
    is_supernova_active = False
    
    sun_exists = True
    
    black_hole_mass = BLACK_HOLE_MASS
    black_hole_alpha = 0.0
    accretion_disk_rotation = 0.0
    
    sequence_start_time = 0.0
    sequence_stage = 0
    
    selected_planet_index = 0
    
    supernova_particles.clear()
    debris_particles.clear()
    
    init_planets()
    
    camera_state['target'] = np.array([0.0, 0.0, 0.0])
    camera_state['distance'] = 200.0
    camera_state['azimuth'] = 0.0
    camera_state['elevation'] = 30.0
    
    print("Simulation reset to initial state")
# ============================================================================
# SHAHID GALIB - FEATURE 1: WINDOW SETUP & STARFIELD BACKGROUND
# ============================================================================

def init_starfield():
    """Initialize background starfield with 2000 random stars"""
    global starfield
    starfield = []
    for _ in range(STARFIELD_COUNT):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        r = random.uniform(1000, 2000)
        
        x = r * math.sin(phi) * math.cos(theta)
        y = r * math.sin(phi) * math.sin(theta)
        z = r * math.cos(phi)
        
        brightness = random.uniform(0.3, 1.0)
        starfield.append([x, y, z, brightness])

# ============================================================================
# SHAHID GALIB - FEATURE 2: COMPLETE SOLAR SYSTEM (SUN + 8 PLANETS)
# ============================================================================

def init_planets():
    """Initialize all planets with their orbital positions"""
    global planets
    planets = []
    
    for i, (name, mass, radius, orbital_radius, color, initial_angle) in enumerate(PLANET_DATA):
        angle_rad = math.radians(initial_angle)
        position = np.array([
            orbital_radius * math.cos(angle_rad),
            orbital_radius * math.sin(angle_rad),
            0.0
        ])
        
        if is_solar_system_active:
            orbital_speed = math.sqrt(G * SUN_MASS / orbital_radius)
            velocity = np.array([
                -orbital_speed * math.sin(angle_rad),
                orbital_speed * math.cos(angle_rad),
                0.0
            ])
        else:
            velocity = np.array([0.0, 0.0, 0.0])
        
        planet = {
            'name': name,
            'mass': mass,
            'radius': radius,
            'position': position,
            'velocity': velocity,
            'acceleration': np.array([0.0, 0.0, 0.0]),
            'color': color,
            'orbital_trail': [position.copy()],
            'captured': False,
            'spaghettified': False,
            'spaghetti_factor': 1.0
        }
        planets.append(planet)

def init_simulation():
    """Initialize the entire simulation"""
    global last_time
    init_starfield()
    init_planets()
    last_time = time.time()


# ============================================================================
# DRAWING FUNCTIONS
# ============================================================================

# SHAHID GALIB - FEATURE 1: STARFIELD BACKGROUND
def draw_starfield():
    """Draw background starfield (2000 stars)"""
    glPointSize(1.0)
    glBegin(GL_POINTS)
    
    for star in starfield:
        x, y, z, brightness = star
        glColor3f(brightness, brightness, brightness)
        glVertex3f(x, y, z)
    
    glEnd()

# ============================================================================
# SHAHID GALIB - FEATURE 3: ORBITAL CAMERA SYSTEM & SPACESHIP MECHANICS
# (Spherical Coordinates, Camera Transitions, Spaceship Controls, Interactive Navigation)
# ============================================================================

def setup_camera():
    """Setup camera using spherical coordinates or spaceship perspectives with smooth transitions"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, 1.25, 0.1, 5000.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    def spherical_to_cartesian(state):
        azimuth_rad = math.radians(state['azimuth'])
        elevation_rad = math.radians(state['elevation'])
        distance = state['distance']
        cam_x = distance * math.cos(elevation_rad) * math.cos(azimuth_rad)
        cam_y = distance * math.cos(elevation_rad) * math.sin(azimuth_rad)
        cam_z = distance * math.sin(elevation_rad)
        target = state['target']
        return np.array([cam_x + target[0], cam_y + target[1], cam_z + target[2]]), target.copy()

    if camera_mode == 0 or not spaceship_exists:
        desired_pos, desired_target = spherical_to_cartesian(camera_state)
    else:
        yaw = math.radians(spaceship_rotation[1])
        pitch = math.radians(spaceship_rotation[0])
        forward = np.array([math.cos(yaw) * math.cos(pitch), math.sin(yaw) * math.cos(pitch), math.sin(pitch)])
        up = np.array([0.0, 0.0, 1.0])
        if camera_mode == 1:
            desired_pos = spaceship_position - forward * (spaceship_scale * 8.0) + up * (spaceship_scale * 3.0)
            desired_target = spaceship_position + forward * (spaceship_scale * 6.0)
        else:
            desired_pos = spaceship_position + forward * (spaceship_scale * 1.2) + up * (spaceship_scale * 0.4)
            desired_target = desired_pos + forward * (spaceship_scale * 20.0)

    global camera_transition_active, camera_transition_start, camera_start_pos, camera_start_target, camera_transition_duration
    if camera_transition_active:
        t = (time.time() - camera_transition_start) / max(0.001, camera_transition_duration)
        if t >= 1.0:
            camera_transition_active = False
            curr_pos = desired_pos
            curr_target = desired_target
        else:
            curr_pos = lerp(camera_start_pos, desired_pos, t)
            curr_target = lerp(camera_start_target, desired_target, t)
    else:
        curr_pos = desired_pos
        curr_target = desired_target

    gluLookAt(curr_pos[0], curr_pos[1], curr_pos[2],
              curr_target[0], curr_target[1], curr_target[2],
              0.0, 0.0, 1.0)

# SHAHID GALIB - FEATURE 2: SOLAR SYSTEM (SUN + 8 PLANETS)
def draw_sun():
    """Draw the Sun as a glowing yellow sphere or red giant"""
    glPushMatrix()
    
    glTranslatef(sun_position[0], sun_position[1], sun_position[2])
    
    if is_red_giant_active:
        glColor3f(1.0, 0.3, 0.1)
        radius = current_sun_radius
    else:
        glColor3f(1.0, 1.0, 0.0)
        radius = 30.0
    
    quadric = gluNewQuadric()
    gluSphere(quadric, radius, 20, 20)
    
    glPopMatrix()

def draw_planets():
    """Draw all planets with trails and Saturn's rings"""
    for i, planet in enumerate(planets):
        if planet['captured'] or is_planet_engulfed(planet):
            continue
            
        glColor3f(0.3, 0.3, 0.3)
        glPointSize(1.0)
        glBegin(GL_POINTS)
        for trail_pos in planet['orbital_trail'][-100:]:  # Last 100 positions
            glVertex3f(trail_pos[0], trail_pos[1], trail_pos[2])
        glEnd()

        # FARHAN ZARIF'S PART - Spaghettification effect
        if planet['spaghettified']:
            direction_to_bh = normalize_vector(black_hole_position - planet['position'])
            glTranslatef(planet['position'][0], planet['position'][1], planet['position'][2])
            angle = math.degrees(math.atan2(direction_to_bh[1], direction_to_bh[0]))
            glRotatef(angle, 0, 0, 1)
            
            stretch_factor = planet['spaghetti_factor']
            glScalef(1.0 / stretch_factor, stretch_factor, 1.0)
        else:
            glTranslatef(planet['position'][0], planet['position'][1], planet['position'][2])
        
        color = planet['color']
        glColor3f(color[0], color[1], color[2])
        
        quadric = gluNewQuadric()
        gluSphere(quadric, planet['radius'], 10, 10)
        
        if i == 5 and not planet['spaghettified']:  
            draw_saturn_rings(planet['radius'])
        
        glPopMatrix()

def draw_saturn_rings(planet_radius):
    """Draw Saturn's rings using GL_QUADS"""
    glColor3f(0.8, 0.8, 0.6) 
    
    inner_radius = planet_radius * 1.5
    outer_radius = planet_radius * 2.5
    segments = 32
    
    glBegin(GL_QUADS)
    for i in range(segments):
        angle1 = 2.0 * math.pi * i / segments
        angle2 = 2.0 * math.pi * (i + 1) / segments
        cos_a1 = math.cos(angle1)
        sin_a1 = math.sin(angle1)
        cos_a2 = math.cos(angle2)
        sin_a2 = math.sin(angle2)
        
        glVertex3f(inner_radius * cos_a1, inner_radius * sin_a1, 0.0)
        glVertex3f(outer_radius * cos_a1, outer_radius * sin_a1, 0.0)
        glVertex3f(outer_radius * cos_a2, outer_radius * sin_a2, 0.0)
        glVertex3f(inner_radius * cos_a2, inner_radius * sin_a2, 0.0)
    
    glEnd()

def request_camera_transition(new_mode):
    global camera_mode, camera_transition_active, camera_transition_start, camera_start_pos, camera_start_target
    camera_mode = new_mode
    az = math.radians(camera_state['azimuth'])
    el = math.radians(camera_state['elevation'])
    dist = camera_state['distance']
    cx = dist * math.cos(el) * math.cos(az) + camera_state['target'][0]
    cy = dist * math.cos(el) * math.sin(az) + camera_state['target'][1]
    cz = dist * math.sin(el) + camera_state['target'][2]
    camera_start_pos = np.array([cx, cy, cz])
    camera_start_target = camera_state['target'].copy()
    camera_transition_active = True
    camera_transition_start = time.time()


def spawn_spaceship_near_selected_planet():
    global spaceship_exists, spaceship_position, spaceship_velocity, spaceship_rotation, G
    if not planets:
        return
    idx = max(0, min(len(planets) - 1, selected_planet_index))
    planet = planets[idx]
    dir_vec = planet['position'] - sun_position
    dir_norm = normalize_vector(dir_vec) if np.linalg.norm(dir_vec) > 0 else np.array([1.0, 0.0, 0.0])
    offset = dir_norm * (planet['radius'] * 3.0 + 20.0)
    spaceship_position = planet['position'] + offset + np.array([0.0, 0.0, planet['radius'] * 0.5 + 5.0])
    tangent = np.array([-dir_norm[1], dir_norm[0], 0.0])
    yaw = math.degrees(math.atan2(tangent[1], tangent[0]))
    spaceship_rotation = np.array([0.0, yaw, 0.0])
    spaceship_velocity = np.array([0.0, 0.0, 0.0])
    spaceship_exists = True
    request_camera_transition(1)
    print(f"Star Destroyer spawned near {planet['name']}")


def update_spaceship(dt):
    global spaceship_position, spaceship_velocity
    if not spaceship_exists:
        return

    damping = 0.98
    spaceship_velocity *= damping
    
    speed = np.linalg.norm(spaceship_velocity)
    if speed > spaceship_max_speed:
        spaceship_velocity = (spaceship_velocity / speed) * spaceship_max_speed

    proposed = spaceship_position + spaceship_velocity * dt

    for p in planets:
        if p.get('captured', False) or is_planet_engulfed(p):
            continue
        to_ship = proposed - p['position']
        dist = np.linalg.norm(to_ship)
        min_dist = p['radius'] + spaceship_collision_radius
        if dist < max(0.1, min_dist):
            n = normalize_vector(to_ship if dist > 0 else np.array([1.0, 0.0, 0.0]))
            proposed = p['position'] + n * min_dist
            radial_v = np.dot(spaceship_velocity, n)
            spaceship_velocity -= radial_v * n

    if sun_exists:
        to_ship = proposed - sun_position
        dist = np.linalg.norm(to_ship)
        min_dist = current_sun_radius + spaceship_collision_radius
        if dist < max(0.1, min_dist):
            n = normalize_vector(to_ship if dist > 0 else np.array([1.0, 0.0, 0.0]))
            proposed = sun_position + n * min_dist
            radial_v = np.dot(spaceship_velocity, n)
            spaceship_velocity -= radial_v * n

    if is_black_hole_active:
        to_ship = proposed - black_hole_position
        dist = np.linalg.norm(to_ship)
        min_dist = BLACK_HOLE_VISUAL_RADIUS + spaceship_collision_radius
        if dist < max(0.1, min_dist):
            n = normalize_vector(to_ship if dist > 0 else np.array([1.0, 0.0, 0.0]))
            proposed = black_hole_position + n * min_dist
            radial_v = np.dot(spaceship_velocity, n)
            spaceship_velocity -= radial_v * n

    spaceship_position = proposed


def draw_star_destroyer():
    if not spaceship_exists:
        return

    glPushMatrix()
    glTranslatef(spaceship_position[0], spaceship_position[1], spaceship_position[2])
    glRotatef(spaceship_rotation[1], 0, 0, 1)
    glRotatef(spaceship_rotation[0], 0, 1, 0)
    glRotatef(spaceship_rotation[2], 1, 0, 0)
    glScalef(spaceship_scale, spaceship_scale, spaceship_scale)

    glColor3f(0.85, 0.85, 0.9)

    hull_len = 1.2
    hull_wid = 0.6
    hull_hei = 0.12
    segs = 10
    z_top = hull_hei * 0.5
    z_bot = -hull_hei * 0.5

    for s in range(segs):
        t1 = s / float(segs)
        t2 = (s + 1) / float(segs)
        x1 = -hull_len * (0.5 - t1)
        x2 = -hull_len * (0.5 - t2)
        w1 = hull_wid * (1.0 - 0.85 * t1)
        w2 = hull_wid * (1.0 - 0.85 * t2)
        glBegin(GL_QUADS)
        glColor3f(0.82 - 0.02 * s, 0.82 - 0.02 * s, 0.86 - 0.02 * s)
        glVertex3f(x1, -w1, z_top)
        glVertex3f(x1,  w1, z_top)
        glVertex3f(x2,  w2, z_top)
        glVertex3f(x2, -w2, z_top)
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(0.75 - 0.02 * s, 0.75 - 0.02 * s, 0.8 - 0.02 * s)
        glVertex3f(x1, -w1, z_bot)
        glVertex3f(x2, -w2, z_bot)
        glVertex3f(x2,  w2, z_bot)
        glVertex3f(x1,  w1, z_bot)
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(0.7, 0.7, 0.75)
        glVertex3f(x1, -w1, z_bot)
        glVertex3f(x1, -w1, z_top)
        glVertex3f(x2, -w2, z_top)
        glVertex3f(x2, -w2, z_bot)
        glEnd()
        glBegin(GL_QUADS)
        glColor3f(0.7, 0.7, 0.75)
        glVertex3f(x1,  w1, z_bot)
        glVertex3f(x2,  w2, z_bot)
        glVertex3f(x2,  w2, z_top)
        glVertex3f(x1,  w1, z_top)
        glEnd()

    glPushMatrix()
    glTranslatef(hull_len * 0.15, 0.0, z_top + 0.03)
    for i in range(4):
        scale = 1.0 - i * 0.15
        glColor3f(0.85, 0.85, 0.9)
        glPushMatrix()
        glScalef(hull_len * 0.5 * scale, hull_wid * 0.5 * scale, 0.06)
        glutSolidCube(1.0)
        glPopMatrix()
        glTranslatef(hull_len * 0.03, 0.0, 0.025)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(hull_len * 0.25, 0.0, z_top + 0.12)
    glScalef(0.3, 0.2, 0.15)
    glutSolidCube(1.0)
    glPopMatrix()

    quad = gluNewQuadric()
    glPushMatrix()
    glTranslatef(hull_len * 0.3, 0.1, z_top + 0.21)
    gluSphere(quad, 0.05, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(hull_len * 0.3, -0.1, z_top + 0.21)
    gluSphere(quad, 0.05, 10, 10)
    glPopMatrix()

    glColor3f(0.6, 0.65, 0.75)
    for yoff in [-0.2, 0.0, 0.2]:
        glPushMatrix()
        glTranslatef(-hull_len * 0.5 - 0.06, yoff, 0.0)
        glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 0.06, 0.06, 0.15, 10, 10)
        glPopMatrix()

    glPopMatrix()

# ============================================================================
# FARHAN ZARIF - FEATURE 4: BLACK HOLE VISUAL EFFECTS
# (Photon Ring, Accretion Disk, Gravitational Lensing)
# ============================================================================

def draw_simulation_black_hole():
    """Draw black hole with event horizon and accretion disk using allowed OpenGL functions"""
    if black_hole_alpha <= 0.0:
        return
        
    glPushMatrix()
    glTranslatef(black_hole_position[0], black_hole_position[1], black_hole_position[2])
    
    draw_accretion_disk()
    draw_photon_ring()
    
    glColor3f(0.0, 0.0, 0.0)
    quadric = gluNewQuadric()
    gluSphere(quadric, BLACK_HOLE_VISUAL_RADIUS, 32, 32)
    draw_black_hole_glow()
    
    glPopMatrix()

def draw_accretion_disk():
    """Draw rotating accretion disk with Interstellar-style appearance"""
    global accretion_disk_rotation
    
    accretion_disk_rotation += ACCRETION_DISK_ROTATION_SPEED
    
    inner_radius = BLACK_HOLE_VISUAL_RADIUS * 2.5  
    outer_radius = BLACK_HOLE_VISUAL_RADIUS * 6.0  
    segments = 128  
    rings = 24
    
    cam_dir = normalize_vector(np.array([
        camera_state['distance'] * math.cos(math.radians(camera_state['elevation'])) * math.cos(math.radians(camera_state['azimuth'])),
        camera_state['distance'] * math.cos(math.radians(camera_state['elevation'])) * math.sin(math.radians(camera_state['azimuth'])),
        camera_state['distance'] * math.sin(math.radians(camera_state['elevation']))
    ]))
    
    for ring in range(rings):
        radius1 = inner_radius + (outer_radius - inner_radius) * ring / rings
        radius2 = inner_radius + (outer_radius - inner_radius) * (ring + 1) / rings
        
        glBegin(GL_QUADS)
        for i in range(segments):
            angle1 = 2.0 * math.pi * i / segments + math.radians(accretion_disk_rotation)
            angle2 = 2.0 * math.pi * (i + 1) / segments + math.radians(accretion_disk_rotation)
            cos_a1 = math.cos(angle1)
            sin_a1 = math.sin(angle1)
            cos_a2 = math.cos(angle2)
            sin_a2 = math.sin(angle2)
            
            orbital_speed = 0.3 
            velocity = np.array([-orbital_speed * sin_a1, orbital_speed * cos_a1, 0.0])
            
            doppler_factor = max(0.2, 1.0 + np.dot(velocity, cam_dir) * 0.8)
            
            t = ring / rings
            if t < 0.3:
                base_color = lerp_color((1.0, 1.0, 0.9), (1.0, 0.9, 0.3), t / 0.3)
            elif t < 0.7:
                base_color = lerp_color((1.0, 0.9, 0.3), (1.0, 0.5, 0.1), (t - 0.3) / 0.4)
            else:
                base_color = lerp_color((1.0, 0.5, 0.1), (0.6, 0.1, 0.0), (t - 0.7) / 0.3)
            
            distance_factor = 1.2 - (t * 0.8) 
            color = tuple(min(1.0, c * doppler_factor * distance_factor) for c in base_color)
            
            turbulence = 0.7 + 0.3 * math.sin(angle1 * 4.0 + accretion_disk_rotation * 0.15)
            flicker = 0.9 + 0.1 * math.sin(angle1 * 8.0 + accretion_disk_rotation * 0.3)
            final_color = tuple(min(1.0, c * turbulence * flicker) for c in color)
            
            glColor3f(final_color[0], final_color[1], final_color[2])
            glVertex3f(radius1 * cos_a1, radius1 * sin_a1, 0.0)
            glVertex3f(radius2 * cos_a1, radius2 * sin_a1, 0.0)
            glVertex3f(radius2 * cos_a2, radius2 * sin_a2, 0.0)
            glVertex3f(radius1 * cos_a2, radius1 * sin_a2, 0.0)
        
        glEnd()
    
def draw_photon_ring():
    """Draw bright photon ring using allowed OpenGL functions"""
    photon_radius = BLACK_HOLE_VISUAL_RADIUS * 1.5
    segments = 128
    
    for ring_layer in range(3):
        inner_radius = photon_radius + ring_layer * 1.0
        outer_radius = inner_radius + 0.5
        
        intensity = 1.0 - ring_layer * 0.3
        glColor3f(intensity, intensity * 0.9, intensity * 0.6)
        
        glBegin(GL_QUADS)
        for i in range(segments):
            angle1 = 2.0 * math.pi * i / segments
            angle2 = 2.0 * math.pi * (i + 1) / segments
            
            cos_a1 = math.cos(angle1)
            sin_a1 = math.sin(angle1)
            cos_a2 = math.cos(angle2)
            sin_a2 = math.sin(angle2)
            
            glVertex3f(inner_radius * cos_a1, inner_radius * sin_a1, 0.0)
            glVertex3f(outer_radius * cos_a1, outer_radius * sin_a1, 0.0)
            glVertex3f(outer_radius * cos_a2, outer_radius * sin_a2, 0.0)
            glVertex3f(inner_radius * cos_a2, inner_radius * sin_a2, 0.0)
        glEnd()

def draw_black_hole_glow():
    """Draw black hole glow using allowed OpenGL functions"""
    if black_hole_alpha <= 0.0:
        return
    
    for glow_layer in range(6):
        inner_radius = BLACK_HOLE_VISUAL_RADIUS * (1.1 + glow_layer * 0.15)
        outer_radius = BLACK_HOLE_VISUAL_RADIUS * (1.3 + glow_layer * 0.2)
        
        intensity = 0.8 - (glow_layer * 0.12)
        
        if glow_layer < 2:
            glColor3f(intensity, intensity * 0.6, intensity * 0.2)
        elif glow_layer < 4:
            glColor3f(intensity * 0.9, intensity * 0.5, intensity * 0.15)
        else:
            glColor3f(intensity * 0.7, intensity * 0.3, intensity * 0.1)
        
        segments = 64
        
        glBegin(GL_QUADS)
        for i in range(segments):
            angle1 = 2.0 * math.pi * i / segments
            angle2 = 2.0 * math.pi * (i + 1) / segments
            
            cos_a1 = math.cos(angle1)
            sin_a1 = math.sin(angle1)
            cos_a2 = math.cos(angle2)
            sin_a2 = math.sin(angle2)
            
            glVertex3f(inner_radius * cos_a1, inner_radius * sin_a1, 0.0)
            glVertex3f(outer_radius * cos_a1, outer_radius * sin_a1, 0.0)
            glVertex3f(outer_radius * cos_a2, outer_radius * sin_a2, 0.0)
            glVertex3f(inner_radius * cos_a2, inner_radius * sin_a2, 0.0)
        glEnd()

# ============================================================================
# EVAN YUVRAJ MUNSHI - FEATURE 7: SUPERNOVA EXPLOSION & DEBRIS SYSTEM
# (Visual Effects, Particle Systems, Stellar Death Simulation)
# ============================================================================

def draw_supernova_explosion():
    """Draw supernova explosion effect"""
    if not supernova_particles:
        return
        
    glPointSize(5.0)
    glBegin(GL_POINTS)
    
    for particle in supernova_particles:
        pos = particle['position']
        age = particle['age']
        lifetime = particle['lifetime']
        
        t = age / lifetime
        if t < 0.3:
            color = lerp_color((1.0, 1.0, 1.0), (1.0, 1.0, 0.0), t / 0.3)
        elif t < 0.7:
            color = lerp_color((1.0, 1.0, 0.0), (1.0, 0.5, 0.0), (t - 0.3) / 0.4)
        else:
            color = lerp_color((1.0, 0.5, 0.0), (0.5, 0.0, 0.0), (t - 0.7) / 0.3)
        glColor3f(color[0], color[1], color[2])
        glVertex3f(pos[0], pos[1], pos[2])
    
    glEnd()

def draw_debris():
    """Draw debris particles with optimized performance"""
    if not debris_particles:
        return
    
    camera_pos = np.array([0.0, 0.0, camera_state['distance']])
    
    near_particles = []
    far_particles = []
    
    for particle in debris_particles:
        distance_to_camera = np.linalg.norm(particle['position'] - camera_pos)
        
        if distance_to_camera > BLACK_HOLE_VISUAL_RADIUS * 15.0:
            continue
            
        if distance_to_camera < BLACK_HOLE_VISUAL_RADIUS * 5.0:
            near_particles.append(particle)
        else:
            far_particles.append(particle)
    
    if near_particles:
        glPointSize(3.0)
        glBegin(GL_POINTS)
        for particle in near_particles:
            pos = particle['position']
            age = particle['age']
            lifetime = particle['lifetime']
            
            t = age / lifetime
            if 'color' in particle:
                planet_color = particle['color']
                dark_color = (planet_color[0] * 0.3, planet_color[1] * 0.3, planet_color[2] * 0.3)
                color = lerp_color(planet_color, dark_color, t * 0.7)
            else:
                color = lerp_color((1.0, 1.0, 0.0), (0.3, 0.0, 0.0), t)
            

            glColor3f(color[0], color[1], color[2])
            glVertex3f(pos[0], pos[1], pos[2])
        glEnd()
    
    if far_particles:
        glPointSize(1.5)
        glBegin(GL_POINTS)
        for particle in far_particles:
            pos = particle['position']
            age = particle['age']
            lifetime = particle['lifetime']
            
            t = age / lifetime
            if 'color' in particle:
                color = particle['color']
            else:
                color = (1.0, 0.8, 0.0)
            
            glColor3f(color[0], color[1], color[2])
            glVertex3f(pos[0], pos[1], pos[2])
        glEnd()

# ============================================================================
# UTLITY FUNCTIONS (HUD)
# ============================================================================

def draw_hud():
    """Draw heads-up display"""
    if planets and selected_planet_index < len(planets):
        planet = planets[selected_planet_index]
        
        draw_text(10, 750, f"Selected Planet: {planet['name']}", GLUT_BITMAP_HELVETICA_18)
        
        velocity_mag = np.linalg.norm(planet['velocity'])
        acceleration_mag = np.linalg.norm(planet['acceleration'])
        
        kinetic_energy = 0.5 * planet['mass'] * velocity_mag * velocity_mag
        potential_energy = 0.0
        
        if is_solar_system_active and sun_exists:
            r_sun = np.linalg.norm(planet['position'] - sun_position)
            if r_sun > 0:
                potential_energy += -G * SUN_MASS * planet['mass'] / r_sun
        
        if is_black_hole_active:
            r_bh = np.linalg.norm(planet['position'] - black_hole_position)
            if r_bh > 0:
                potential_energy += -G * black_hole_mass * planet['mass'] / r_bh
        
        total_energy = kinetic_energy + potential_energy
        
        status = "Normal"
        if planet['captured']:
            status = "Captured"
        elif planet['spaghettified']:
            status = "Spaghettified"
        
        draw_text(10, 720, f"Velocity: {velocity_mag:.2f}", GLUT_BITMAP_HELVETICA_18)
        draw_text(10, 700, f"Acceleration: {acceleration_mag:.2f}", GLUT_BITMAP_HELVETICA_18)
        draw_text(10, 680, f"Total Energy: {total_energy:.2f}", GLUT_BITMAP_HELVETICA_18)
        draw_text(10, 660, f"Status: {status}", GLUT_BITMAP_HELVETICA_18)
    
    draw_text(700, 750, "System Statistics", GLUT_BITMAP_HELVETICA_18)
    draw_text(700, 720, f"Black Hole Mass: {black_hole_mass:.0f}", GLUT_BITMAP_HELVETICA_18)
    
    captured_count = sum(1 for p in planets if p.get('captured', False))
    active_planets = len([p for p in planets if not p.get('captured', False)])
    
    draw_text(700, 700, f"Active Planets: {active_planets}", GLUT_BITMAP_HELVETICA_18)
    draw_text(700, 680, f"Planets Captured: {captured_count}", GLUT_BITMAP_HELVETICA_18)
    draw_text(700, 660, f"Debris Particles: {len(debris_particles)}", GLUT_BITMAP_HELVETICA_18)
    
    state_text = "Solar System"
    if is_black_hole_active:
        state_text = "Black Hole Active"
    elif is_supernova_active:
        state_text = "Supernova"
    
    draw_text(700, 640, f"State: {state_text}", GLUT_BITMAP_HELVETICA_18)

def draw_instructions():
    """Draw on-screen instructions"""
    instructions = [
        "Controls:",
        "B - Black Hole spawn",
        "X - Delete Sun",
        "P - Collision Rebound Preset",
        "R - Reset simulation to initial state",
        "Up/Down Arrow - Adjust black hole mass",
        "Left/Right Arrow - Select planet",
        "F - Focus camera on selected planet",
        "H - Reset camera to center",
        "G - Spawn Star Destroyer near selected planet",
        "L - Despawn Star Destroyer",
        "V - Toggle camera mode (Normal/Third/First)",
        "W/S - Thrust Forward/Backward (2x power)",
        "A/D - Yaw Left/Right (enhanced)",
        "E/Q - Pitch Up/Down",
        "Z/C - Roll Left/Right",
        "5/6 - Zoom In/Out"
    ]
    
    start_y = 340
    for i, instruction in enumerate(instructions):
        font = GLUT_BITMAP_HELVETICA_18 if i == 0 else GLUT_BITMAP_HELVETICA_18
        draw_text(10, start_y - i * 20, instruction, font)

# ============================================================================
# FARHAN ZARIF - FEATURE 5: GRAVITATIONAL PHYSICS ENGINE
# (Newton's Law of Universal Gravitation, Velocity Verlet Integration)
# ============================================================================

def update_physics(dt):
    """Update physics simulation"""
    global accretion_disk_rotation, camera_state
    
    if camera_state['is_following_planet'] and planets and selected_planet_index < len(planets):
        camera_state['target'] = planets[selected_planet_index]['position'].copy()
    
    update_red_giant_expansion(dt)
    update_supernova_particles(dt)
    update_debris_particles(dt)
    
    for planet in planets[:]:
        if planet['captured']:
            continue
            
        acceleration = calculate_gravitational_acceleration(planet['position'])
        
        dt2 = dt * dt
        planet['position'] += planet['velocity'] * dt + 0.5 * planet['acceleration'] * dt2
        
        new_acceleration = calculate_gravitational_acceleration(planet['position'])
        planet['velocity'] += 0.5 * (planet['acceleration'] + new_acceleration) * dt
        planet['acceleration'] = new_acceleration
        
        planet['orbital_trail'].append(planet['position'].copy())
        if len(planet['orbital_trail']) > 200:
            planet['orbital_trail'].pop(0)
        
        if is_black_hole_active:
            check_black_hole_interactions(planet)
    
    update_collision_physics()
    update_spaceship(dt)

def calculate_gravitational_acceleration(position):
    """Calculate gravitational acceleration at given position"""
    acceleration = np.array([0.0, 0.0, 0.0])
    
    if sequence_stage >= 1:
        r_vec = sun_position - position 
        r_mag = np.linalg.norm(r_vec)
        if r_mag > 0:
            acc_magnitude = G * black_hole_mass / (r_mag * r_mag)
            acceleration += acc_magnitude * normalize_vector(r_vec)
    else:
        if is_solar_system_active and sun_exists:
            r_vec = sun_position - position
            r_mag = np.linalg.norm(r_vec)
            if r_mag > 0:
                acc_magnitude = G * SUN_MASS / (r_mag * r_mag)
                acceleration += acc_magnitude * normalize_vector(r_vec)
        
        if is_black_hole_active:
            r_vec = black_hole_position - position
            r_mag = np.linalg.norm(r_vec)
            if r_mag > 0:
                acc_magnitude = G * black_hole_mass / (r_mag * r_mag)
                acceleration += acc_magnitude * normalize_vector(r_vec)
    
    return acceleration
#Evan
def update_supernova_particles(dt):
    """Update supernova particle positions and ages"""
    global supernova_particles
    
    for i in range(len(supernova_particles) - 1, -1, -1):
        particle = supernova_particles[i]
        particle['position'] += particle['velocity'] * dt
        particle['age'] += dt
        
        if particle['age'] >= particle['lifetime']:
            supernova_particles.pop(i)
            
def update_debris_particles(dt):
    """Update debris particle positions and ages with optimized performance"""
    global debris_particles, debris_generation_cooldown
    
    if debris_generation_cooldown > 0:
        debris_generation_cooldown -= dt
    
    if len(debris_particles) == 0:
        return

    for i in range(len(debris_particles) - 1, -1, -1):
        particle = debris_particles[i]
        
        current_distance = np.linalg.norm(particle['position'] - black_hole_position)
        
        if current_distance > BLACK_HOLE_VISUAL_RADIUS * 8.0:
            particle['position'] += particle['velocity'] * dt * 0.5  
            particle['age'] += dt
            
            if particle['age'] >= particle['lifetime'] or current_distance > BLACK_HOLE_VISUAL_RADIUS * 12.0:
                debris_particles.pop(i)
            continue
        
        if is_black_hole_active and particle['age'] > particle.get('absorption_delay', 0.0):
            if current_distance > BLACK_HOLE_VISUAL_RADIUS:
                distance_factor = max(0.5, BLACK_HOLE_VISUAL_RADIUS * 5.0 / current_distance)  
                gravity_strength = (G * black_hole_mass * 2.0) / (current_distance * current_distance + 10.0)
                to_black_hole = (black_hole_position - particle['position']) / current_distance
                acceleration = to_black_hole * gravity_strength * 0.2 * distance_factor  
                particle['velocity'] += acceleration * dt
                
                effective_age = particle['age'] - particle.get('absorption_delay', 0.0)
                age_factor = min(1.0, effective_age / (particle['lifetime'] * 0.3))  
                
                if age_factor > 0.05:  
                    proximity_factor = max(2.0, (BLACK_HOLE_VISUAL_RADIUS * 6.0) / current_distance)
                    spiral_strength = SPIRAL_DECAY_RATE * 2.0 * age_factor * proximity_factor 
                    spiral_velocity = to_black_hole * spiral_strength * current_distance * 0.3  
                    particle['velocity'] += spiral_velocity * dt
                    decay_rate = 0.02 * proximity_factor * age_factor  
                    particle['velocity'] *= (1.0 - decay_rate)  
        
        particle['position'] += particle['velocity'] * dt
        particle['age'] += dt
        
        if is_black_hole_active:
            distance_to_bh = np.linalg.norm(particle['position'] - black_hole_position)
            
            absorption_radius = BLACK_HOLE_VISUAL_RADIUS * 1.2  
            inner_radius = BLACK_HOLE_VISUAL_RADIUS * 2.5
            outer_radius = BLACK_HOLE_VISUAL_RADIUS * 6.0
            
            if distance_to_bh < absorption_radius:
                if 'absorption_effect' not in particle:
                    particle['absorption_effect'] = True
                    particle['color'] = (min(1.0, particle['color'][0] * 2.0), 
                                       particle['color'][1] * 0.3, 
                                       particle['color'][2] * 0.3)

                debris_particles.pop(i)
                continue
            
            if distance_to_bh > outer_radius:
                direction_to_bh = (black_hole_position - particle['position']) / distance_to_bh
                particle['position'] = black_hole_position + direction_to_bh * (outer_radius - 5.0)
                orbital_speed = math.sqrt(G * black_hole_mass / outer_radius) * 0.6
                tangent = np.array([-direction_to_bh[1], direction_to_bh[0], 0])
                if np.linalg.norm(tangent) > 0:
                    tangent = tangent / np.linalg.norm(tangent)
                    particle['velocity'] = tangent * orbital_speed + direction_to_bh * random.uniform(-2.0, 0.5)
                else:
                    particle['velocity'] = np.array([orbital_speed, 0, 0])
            
            if distance_to_bh <= BLACK_HOLE_VISUAL_RADIUS * 1.2: 
                debris_particles.pop(i)
                continue
        
        if particle['age'] >= particle['lifetime']:
            debris_particles.pop(i)

def handle_sequences(dt):
    """Handle timed sequences (supernova to black hole)"""
    global sequence_stage, is_supernova_active, is_black_hole_active, black_hole_alpha
    global sun_exists, supernova_particles, sequence_start_time, is_solar_system_active
    
    if sequence_stage == 0:
        return  
    
    elapsed_time = current_time - sequence_start_time
    
    if sequence_stage == 1:  
        if not supernova_particles:  
            create_supernova_explosion()
            sun_exists = False
        
        if elapsed_time >= SUPERNOVA_DURATION:
            sequence_stage = 2
            is_supernova_active = False
    
    elif sequence_stage == 2:  
        fade_progress = (elapsed_time - SUPERNOVA_DURATION) / BLACK_HOLE_FADE_IN_DURATION
        black_hole_alpha = min(1.0, fade_progress)
        
        if fade_progress >= 1.0:
            sequence_stage = 3
            black_hole_alpha = 1.0
    
    elif sequence_stage == 3:  
        pass
#Evan
def update_red_giant_expansion(dt):
    """Update red giant expansion phase"""
    global current_sun_radius, is_red_giant_active, is_supernova_active, sun_exists
    global is_solar_system_active
    
    if not is_red_giant_active:
        return
    
    elapsed_time = current_time - red_giant_start_time
    
    if elapsed_time < RED_GIANT_DURATION:
        progress = elapsed_time / RED_GIANT_DURATION
        current_sun_radius = SUN_INITIAL_RADIUS + (RED_GIANT_MAX_RADIUS - SUN_INITIAL_RADIUS) * progress
        check_planet_engulfing()
        
        print(f"Red giant expansion: {progress*100:.1f}% complete, radius: {current_sun_radius:.1f}")
    else:
        print("Red giant phase complete - transitioning to supernova!")
        is_red_giant_active = False
        is_solar_system_active = False
        sun_exists = False
        is_supernova_active = True
        create_supernova_explosion()

def check_planet_engulfing():
    """Check if any planets should be engulfed by the red giant"""
    global engulfed_planets
    
    for planet in planets:
        if planet['name'] not in engulfed_planets:
            distance = np.linalg.norm(planet['position'] - sun_position)
            if distance <= current_sun_radius:
                engulfed_planets.append(planet['name'])
                print(f"{planet['name']} has been engulfed by the red giant!")

def is_planet_engulfed(planet):
    """Check if a planet has been engulfed"""
    return planet['name'] in engulfed_planets

def create_supernova_explosion():
    """Create supernova explosion particles"""
    global supernova_particles
    
    supernova_particles = []
    num_particles = 500
    
    for _ in range(num_particles):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        speed = random.uniform(50.0, 200.0)
        velocity = np.array([
            speed * math.sin(phi) * math.cos(theta),
            speed * math.sin(phi) * math.sin(theta),
            speed * math.cos(phi)
        ])
        
        particle = {
            'position': sun_position.copy(),
            'velocity': velocity,
            'age': 0.0,
            'lifetime': random.uniform(2.0, 4.0)
        }
        supernova_particles.append(particle)
# ============================================================================
# FARHAN ZARIF - FEATURE 6: BLACK HOLE CAPTURE MECHANICS
# (Tidal Forces, Event Horizon, Schwarzschild Radius Physics)
# ============================================================================

def check_black_hole_interactions(planet):
    """Check planet interactions with black hole"""
    distance_to_bh = np.linalg.norm(planet['position'] - black_hole_position)
    rs = calculate_schwarzschild_radius(black_hole_mass)
    tidal_radius = calculate_tidal_radius(black_hole_mass)
    logical_capture_radius = rs * LOGICAL_CAPTURE_RADIUS_MULTIPLIER
    
    if distance_to_bh <= BLACK_HOLE_VISUAL_RADIUS:
        capture_planet(planet)
        return
    
    if 'logically_captured' not in planet:
        planet['logically_captured'] = False
    
    if not planet['logically_captured'] and distance_to_bh <= logical_capture_radius:
        planet['logically_captured'] = True
    
    accretion_disk_outer_radius = BLACK_HOLE_VISUAL_RADIUS * 6.0
    if distance_to_bh <= accretion_disk_outer_radius or planet['logically_captured']:
        to_bh = black_hole_position - planet['position']
        distance = np.linalg.norm(to_bh)
        
        if distance > 0:
            orbital_speed = np.sqrt(G * black_hole_mass / distance) * 0.8  
            to_bh_normalized = to_bh / distance
            current_vel = planet['velocity']
            current_speed = np.linalg.norm(current_vel)
            if current_speed > 0.1:
                current_vel_normalized = current_vel / current_speed
                radial_component = np.dot(current_vel_normalized, to_bh_normalized)
                tangential_component = current_vel_normalized - radial_component * to_bh_normalized
                tangential_mag = np.linalg.norm(tangential_component)
                
                if tangential_mag > 0.01:
                    tangential_dir = tangential_component / tangential_mag
                else:
                    if abs(to_bh_normalized[2]) < 0.9:
                        tangential_dir = np.cross(to_bh_normalized, np.array([0.0, 0.0, 1.0]))
                    else:
                        tangential_dir = np.cross(to_bh_normalized, np.array([1.0, 0.0, 0.0]))
                    tangential_dir = tangential_dir / np.linalg.norm(tangential_dir)
            else:
                if abs(to_bh_normalized[2]) < 0.9:
                    tangential_dir = np.cross(to_bh_normalized, np.array([0.0, 0.0, 1.0]))
                else:
                    tangential_dir = np.cross(to_bh_normalized, np.array([1.0, 0.0, 0.0]))
                tangential_dir = tangential_dir / np.linalg.norm(tangential_dir)
            
            if distance <= accretion_disk_outer_radius:
                orbital_speed *= 0.6  
                orbital_decay = 0.95   
                inward_factor = 0.25   
                
                spiral_tightness = (accretion_disk_outer_radius - distance) / accretion_disk_outer_radius
                inward_factor += spiral_tightness * 0.15  
                
                if distance <= BLACK_HOLE_VISUAL_RADIUS * 3.0:
                    proximity_factor = (BLACK_HOLE_VISUAL_RADIUS * 3.0 - distance) / (BLACK_HOLE_VISUAL_RADIUS * 3.0)
                    inward_factor += proximity_factor * 0.5  
            else:
                orbital_decay = 0.99  
                inward_factor = 0.05   
            
            orbital_velocity = tangential_dir * orbital_speed * orbital_decay
            inward_velocity = to_bh_normalized * (orbital_speed * inward_factor)
            planet['velocity'] = orbital_velocity + inward_velocity
    
    if distance_to_bh <= accretion_disk_outer_radius and not planet['spaghettified']:
        planet['spaghettified'] = True
        planet['spaghetti_factor'] = 1.0
    
    if planet['spaghettified']:
        stretch_factor = max(1.0, accretion_disk_outer_radius / distance_to_bh)
        planet['spaghetti_factor'] = min(5.0, stretch_factor)

def capture_planet(planet):
    """Capture a planet by the black hole - creates supernova-like explosion"""
    global debris_particles, debris_generation_cooldown, current_time
    
    if current_time < debris_generation_cooldown:
        planet['captured'] = True
        return
    
    if len(debris_particles) > 800: 
        debris_particles = debris_particles[-600:] 
    
    debris_generation_cooldown = current_time + 0.5
    planet['captured'] = True
    planet_to_bh = black_hole_position - planet['position']
    distance_to_bh = np.linalg.norm(planet_to_bh)

    if distance_to_bh > 0:
        direction_to_bh = planet_to_bh / distance_to_bh
    else:
        direction_to_bh = np.array([1.0, 0.0, 0.0])
    
    planet_velocity_normalized = np.array([0.0, 0.0, 0.0])
    planet_speed = np.linalg.norm(planet['velocity'])
    avoid_direction = planet_speed > 1.0 
    if avoid_direction:
        planet_velocity_normalized = planet['velocity'] / planet_speed
    
    planet_color = planet['color']
    planet_mass = planet['mass']
    planet_radius = planet['radius']
    planet_name = planet.get('name', 'Unknown')
    
    volume_factor = (planet_radius ** 3) / 125.0  
    mass_factor = planet_mass / 20.0  
    base_debris_count = int(50 + (mass_factor * 80) + (volume_factor * 60))
    
    composition_multiplier = 1.0
    if 'Mercury' in planet_name:
        composition_multiplier = 0.8  
    elif 'Venus' in planet_name:
        composition_multiplier = 1.1  
    elif 'Earth' in planet_name:
        composition_multiplier = 1.2  
    elif 'Mars' in planet_name:
        composition_multiplier = 0.9 
    elif 'Jupiter' in planet_name:
        composition_multiplier = 2.5  
    elif 'Saturn' in planet_name:
        composition_multiplier = 2.2  
    elif 'Uranus' in planet_name:
        composition_multiplier = 1.8  
    elif 'Neptune' in planet_name:
        composition_multiplier = 1.9  
    
    num_debris = int(base_debris_count * composition_multiplier)
    num_debris = max(30, min(150, num_debris))  
    
    if num_debris < 120:
        num_layers = 3
    elif num_debris < 200:
        num_layers = 4
    elif num_debris < 300:
        num_layers = 5
    else:
        num_layers = 6
    
    particles_per_layer = num_debris // num_layers
    
    for layer in range(num_layers):
        layer_speed_multiplier = 1.0 + (layer * 0.3)
        
        for _ in range(particles_per_layer):
            theta = random.uniform(0, 2 * math.pi)
            phi = random.uniform(0, math.pi)
            
            direction = np.array([
                math.sin(phi) * math.cos(theta),
                math.sin(phi) * math.sin(theta),
                math.cos(phi)
            ])
            
            if avoid_direction:
                dot_product = np.dot(direction, planet_velocity_normalized)
                if dot_product > 0.5:
                    perpendicular = np.array([-planet_velocity_normalized[1], planet_velocity_normalized[0], 0])
                    if np.linalg.norm(perpendicular) < 0.1:
                        perpendicular = np.array([0, -planet_velocity_normalized[2], planet_velocity_normalized[1]])
                    perpendicular = perpendicular / np.linalg.norm(perpendicular)
                    
                    direction = 0.7 * perpendicular + 0.3 * direction
                    direction = direction / np.linalg.norm(direction)
            
            inner_radius = BLACK_HOLE_VISUAL_RADIUS * 2.5
            outer_radius = BLACK_HOLE_VISUAL_RADIUS * 6.0
            
            if random.random() < 0.90:
                distance_from_bh = random.uniform(inner_radius, outer_radius)
                theta = random.uniform(0, 2 * math.pi)
                
                z_variation = (outer_radius - distance_from_bh) / outer_radius * 8.0
                z = random.uniform(-z_variation, z_variation)
                
                x = distance_from_bh * math.cos(theta) + random.uniform(-15.0, 15.0)
                y = distance_from_bh * math.sin(theta) + random.uniform(-15.0, 15.0)
                
                position = black_hole_position + np.array([x, y, z])
                
                orbital_speed = math.sqrt(G * black_hole_mass / distance_from_bh) * 0.5
                velocity = np.array([-y, x, 0]) * (orbital_speed / distance_from_bh)
                
                velocity += np.random.normal(0, 3.0, 3)
                
            else:
                distance_from_bh = random.uniform(outer_radius * 0.9, outer_radius * 1.1)
                theta = random.uniform(0, 2 * math.pi)
                phi = random.uniform(0.3, 0.8) * math.pi
                
                x = distance_from_bh * math.sin(phi) * math.cos(theta)
                y = distance_from_bh * math.sin(phi) * math.sin(theta)
                z = distance_from_bh * math.cos(phi)
                if random.random() < 0.5:
                    z = -z
                
                position = black_hole_position + np.array([x, y, z])
                
                orbital_speed = math.sqrt(G * black_hole_mass / distance_from_bh) * 0.4
                radial_dir = np.array([x, y, z]) / distance_from_bh
                tangent = np.array([-y, x, 0])
                if np.linalg.norm(tangent) > 0:
                    tangent = tangent / np.linalg.norm(tangent)
                    velocity = tangent * orbital_speed + radial_dir * random.uniform(-2.0, 0.5)
                else:
                    velocity = np.array([orbital_speed, 0, 0])
            
            velocity_multiplier = 1.0
            if 'Mercury' in planet_name:
                velocity_multiplier = 0.7
            elif 'Venus' in planet_name:
                velocity_multiplier = 1.3
            elif 'Earth' in planet_name:
                velocity_multiplier = 1.0
            elif 'Mars' in planet_name:
                velocity_multiplier = 0.8
            elif 'Jupiter' in planet_name:
                velocity_multiplier = 1.8
            elif 'Saturn' in planet_name:
                velocity_multiplier = 1.6
            elif 'Uranus' in planet_name:
                velocity_multiplier = 1.2
            elif 'Neptune' in planet_name:
                velocity_multiplier = 1.4
            
            velocity *= velocity_multiplier
            velocity += np.random.normal(0, 2.0 * velocity_multiplier, 3)
            
            base_lifetime = 10.0
            lifetime_modifier = 1.0
            if 'Mercury' in planet_name:
                lifetime_modifier = 0.8
            elif 'Venus' in planet_name:
                lifetime_modifier = 1.2
            elif 'Earth' in planet_name:
                lifetime_modifier = 1.1
            elif 'Mars' in planet_name:
                lifetime_modifier = 0.9
            elif 'Jupiter' in planet_name:
                lifetime_modifier = 1.8
            elif 'Saturn' in planet_name:
                lifetime_modifier = 1.6
            elif 'Uranus' in planet_name:
                lifetime_modifier = 1.3
            elif 'Neptune' in planet_name:
                lifetime_modifier = 1.4
            
            particle_lifetime = random.uniform(base_lifetime * 0.7, base_lifetime * 1.3) * lifetime_modifier
            
            mass_delay_factor = min(2.0, planet_mass / 50.0)
            base_delay = 1.5 * mass_delay_factor
            absorption_delay = random.uniform(0.0, base_delay)
            
            debris = {
                'position': position,
                'velocity': velocity,
                'color': planet_color,
                'age': 0.0,
                'lifetime': particle_lifetime,
                'initial_distance': np.linalg.norm(position - black_hole_position),
                'absorption_delay': absorption_delay,
                'planet_type': planet_name,
                'mass_factor': mass_factor
            }
            debris_particles.append(debris)
    
    for i in range(len(planets) - 1, -1, -1):
        if planets[i] is planet:
            planets.pop(i)
            break
            
# ============================================================================
# KEYBOARD & MOUSE FUNCTIONS
# ============================================================================

# SHAHID GALIB - VISUAL FOUNDATION & SOLAR SYSTEM CONTROLS
def keyboard_listener(key, x, y):
    """Handle keyboard input for all simulation controls"""
    global is_solar_system_active, is_black_hole_active, is_supernova_active
    global sequence_start_time, sequence_stage, black_hole_mass, selected_planet_index, keys_locked
    global spaceship_velocity, spaceship_rotation, spaceship_position, spaceship_scale, spaceship_exists
    global camera_mode, camera_transition_active, camera_transition_start, camera_start_pos, camera_start_target
    global G
    global game_state
    if key == b'\x1b':
        game_state = GAME_STATE_MENU
        print("Returning to main menu...")
        return
    if game_state != GAME_STATE_SIMULATION:
        return

    event_trigger_keys = [b'b', b'B', b'x', b'X', b'p', b'P']
    if keys_locked and key in event_trigger_keys:
        print("Event keys are locked! Press R to reset and unlock. Another event cannot be triggered.")
        return

    #Feature 4 - Farhan Zarif
    if key == b'b' or key == b'B':
        sequence_start_time = current_time
        sequence_stage = 1
        is_supernova_active = True
        is_black_hole_active = True
        sun_exists = False
        keys_locked = True
        print("Black hole sequence started! Keys locked until reset (R).")
    
    #Galib
    elif key == b'f' or key == b'F':
        if planets and selected_planet_index < len(planets):
            camera_state['target'] = planets[selected_planet_index]['position'].copy()
            camera_state['is_following_planet'] = True
            print(f"Camera now following {planets[selected_planet_index]['name']}")
            
    elif key == b'h' or key == b'H':
        camera_state['target'] = np.array([0.0, 0.0, 0.0])
        camera_state['is_following_planet'] = False
        print("Camera centered on origin, following disabled")
        
    elif key == b'r' or key == b'R':
        reset_simulation()
        keys_locked = False
        print("Simulation reset! Keys unlocked.")
        
    elif key == b'v' or key == b'V':
        if spaceship_exists:
            new_mode = 1 if camera_mode == 0 else (2 if camera_mode == 1 else 0)
            if new_mode == 0:
                yaw = math.radians(spaceship_rotation[1])
                pitch = math.radians(spaceship_rotation[0])
                forward = np.array([math.cos(yaw) * math.cos(pitch), math.sin(yaw) * math.cos(pitch), math.sin(pitch)])
                start_pos = spaceship_position - forward * (spaceship_scale * 8.0) + np.array([0.0, 0.0, spaceship_scale * 3.0])
                camera_start_pos = start_pos
                camera_start_target = spaceship_position + forward * (spaceship_scale * 6.0)
                camera_transition_active = True
                camera_transition_start = time.time()
                camera_mode = 0
            else:
                request_camera_transition(new_mode)
    
    elif key == b'w' or key == b'W':
        if spaceship_exists:
            yaw = math.radians(spaceship_rotation[1])
            pitch = math.radians(spaceship_rotation[0])
            forward = np.array([math.cos(yaw) * math.cos(pitch), math.sin(yaw) * math.cos(pitch), math.sin(pitch)])
            spaceship_velocity += forward * (spaceship_thrust * 0.025)
    elif key == b's' or key == b'S':
        if spaceship_exists:
            yaw = math.radians(spaceship_rotation[1])
            pitch = math.radians(spaceship_rotation[0])
            back = -np.array([math.cos(yaw) * math.cos(pitch), math.sin(yaw) * math.cos(pitch), math.sin(pitch)])
            spaceship_velocity += back * (spaceship_thrust * 0.025)
    elif key == b'a' or key == b'A':
        if spaceship_exists:
            spaceship_rotation[1] -= 8.0
    elif key == b'd' or key == b'D':
        if spaceship_exists:
            spaceship_rotation[1] += 8.0
    elif key == b'e' or key == b'E':
        # Pitch up
        if spaceship_exists:
            spaceship_rotation[0] += 6.0
            spaceship_rotation[0] = min(spaceship_rotation[0], 85.0)  
    elif key == b'q' or key == b'Q':
        if spaceship_exists:
            spaceship_rotation[0] -= 6.0
            spaceship_rotation[0] = max(spaceship_rotation[0], -85.0)  
    elif key == b'z' or key == b'Z':
        if spaceship_exists:
            spaceship_rotation[2] -= 10.0
    elif key == b'c' or key == b'C':
   
        if spaceship_exists:
            spaceship_rotation[2] += 10.0
    elif key == b'x' or key == b'X':
        if spaceship_exists:
            spaceship_velocity *= 0.3 
    elif key == b'g' or key == b'G':
        spawn_spaceship_near_selected_planet()
    elif key == b'l' or key == b'L':
        if spaceship_exists:
            spaceship_exists = False
            print("Star Destroyer despawned")
        else:
            print("No spaceship to despawn")
    elif key == b'h' or key == b'H':
        camera_state['target'] = np.array([0.0, 0.0, 0.0])
        camera_state['is_following_planet'] = False
        print("Camera centered on origin, following disabled")

    
    #Shahid Galib
    elif key == b'5':
        camera_state['distance'] = max(50.0, camera_state['distance'] - 50.0)
        print(f"Camera zoom in - Distance: {camera_state['distance']:.1f}")
    elif key == b'6':
        camera_state['distance'] = min(2000.0, camera_state['distance'] + 50.0)
        print(f"Camera zoom out - Distance: {camera_state['distance']:.1f}")

_index]['position'].copy()
                print(f"Camera now following {planets[selected_planet_index]['name']}")

def special_key_listener(key, x, y):
    """Handle special key input (arrow keys)"""
    global black_hole_mass, keys_locked

    #Zarif
    if key == GLUT_KEY_UP:
        black_hole_mass += 100.0
        
    elif key == GLUT_KEY_DOWN:
        black_hole_mass = max(100.0, black_hole_mass - 100.0)
    
    #Galib
    elif key == GLUT_KEY_LEFT:
        global selected_planet_index, camera_state
        if planets:
            selected_planet_index = (selected_planet_index - 1) % len(planets)
            if camera_state['is_following_planet']:
                camera_state['target'] = planets[selected_planet_index]['position'].copy()
                print(f"Camera now following {planets[selected_planet_index]['name']}")
            
    elif key == GLUT_KEY_RIGHT:
        if planets:
            selected_planet_index = (selected_planet_index + 1) % len(planets)
            if camera_state['is_following_planet']:
                camera_state['target'] = planets[selected_planet_index]['position'].copy()
                print(f"Camera now following {planets[selected_planet_index]['name']}")
                
# ============================================================================
# MAIN DISPLAY AND LOOP FUNCTIONS
# ============================================================================

def idle():
    """Idle function for continuous updates"""
    global current_time, last_time
    
    if game_state == GAME_STATE_SIMULATION:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        max_dt = DT * 3.0
        dt = min(dt, max_dt)
        
        accumulated_time = dt
        while accumulated_time >= DT:
            update_physics(DT)
            handle_sequences(DT)
            accumulated_time -= DT
        
        if accumulated_time > 0.001:
            update_physics(accumulated_time)
            handle_sequences(accumulated_time)
    
    glutPostRedisplay()

def show_screen():
    """Main display function"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    if game_state == GAME_STATE_SIMULATION:
        setup_camera()
        
        draw_starfield()
        
        if sun_exists and is_solar_system_active:
            draw_sun()
        
        if planets:
            draw_planets()

        draw_star_destroyer()
        
        if is_black_hole_active:
            draw_simulation_black_hole()
            
        if debris_particles:
            draw_debris()
    glutSwapBuffers()

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
    
    init_simulation()
    
    glutMainLoop()

if __name__ == "__main__":
    main()
