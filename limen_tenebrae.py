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
