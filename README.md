# Limen Tenebrae: An Interactive Black Hole Simulator

**Limen Tenebrae** is a real-time, interactive 3D simulation of a solar system, its destruction, and the birth of a black hole. Built with Python and OpenGL, this project visualizes complex astrophysical concepts, including gravitational physics, stellar evolution, and the dramatic effects of a singularity. Users can explore a dynamic solar system, trigger cataclysmic events like supernovae, and pilot a spaceship through the cosmos to witness the spectacle from any angle.



![Artist's conception of a black hole](https://www.nasa.gov/wp-content/uploads/2023/05/cygx1-blackhole.jpg)


---

## ✨ Key Features

This simulation is packed with features designed to create an engaging and educational experience:

* **Complete Solar System:** A fully rendered solar system with the Sun and all eight planets, each with accurate orbital mechanics based on Newton's Law of Universal Gravitation.
* **Stunning Black Hole Visuals:** Witness a visually captivating black hole, complete with a rotating accretion disk featuring Doppler beaming, a bright photon ring, and gravitational lensing effects.
* **Dynamic Event Sequences:**
    * **Red Giant Phase:** Trigger the Sun's expansion into a red giant, engulfing the inner planets.
    * **Supernova Explosion:** Watch the Sun collapse and explode in a brilliant supernova, scattering particles across space.
    * **Planetary Capture & Debris:** Planets caught in the black hole's gravity are "spaghettified," torn apart, and absorbed, creating a persistent debris cloud that inherits the planet's color.
* **Interactive Spaceship Piloting:** Spawn and fly a Star Destroyer-class spaceship in first-person or third-person view. Navigate the solar system, dodge celestial bodies, and get a front-row seat to the cosmic action.
* **Advanced Physics Engine:** Utilizes a Velocity Verlet integration method for stable and accurate physics. The simulation also features an elastic collision model for planet-to-planet interactions.
* **Interactive UI & Controls:** An in-simulation Heads-Up Display (HUD) provides real-time data on celestial bodies, while a full suite of keyboard controls allows for camera manipulation, event triggers, and spaceship movement.

---

## 🚀 Technologies Used

* **Language:** Python 3
* **Graphics:** PyOpenGL (The Python binding for OpenGL)
* **Physics & Numerics:** NumPy
* **Windowing & Callbacks:** PyGLUT

---

## 🎮 Controls

| Key          | Action                                                                   |
| :----------- | :----------------------------------------------------------------------- |
| **B** | Trigger the Sun -> Supernova -> Black Hole sequence.                     |
| **X** | Trigger the Red Giant expansion sequence.                                |
| **P** | Activate a preset to demonstrate planet-planet collision physics.        |
| **R** | Reset the entire simulation to its initial state.                        |
| **Arrow Keys** | **Up/Down:** Increase/Decrease black hole mass. <br> **Left/Right:** Cycle through planet selection. |
| **F / H** | **F:** Focus camera on the selected planet. <br> **H:** Reset camera to the origin. |
| **G / L** | **G:** Spawn the spaceship near the selected planet. <br> **L:** Despawn the spaceship. |
| **V** | Toggle camera mode (Orbital -> Third-Person -> First-Person).            |
| **W/S/A/D** | Control spaceship thrust and yaw (turn).                                 |
| **E/Q** | Control spaceship pitch (up/down).                                       |
| **Z/C** | Control spaceship roll.                                                  |
| **5 / 6** | Zoom camera in and out.                                                  |
| **ESC** | Return to the main menu.                                                 |

---

## 👥 Team & Contributions

This project was a collaborative effort by three developers, with features implemented as follows:

### **Part 1: Visual Foundation - Shahid Galib**

* **Feature 1: Starfield & Window Setup:** Established the dynamic 2000-star background and initial OpenGL window.
* **Feature 2: Complete Solar System:** Implemented the Sun and all 8 planets with their unique properties and orbital data.
* **Feature 3: Orbital Camera System:** Created the orbital camera with mouse controls for 3D navigation.

### **Part 2: Physics & Core Mechanics - Farhan Zarif**

* **Feature 4: Black Hole Visual Effects:** Designed the accretion disk, photon ring, and lensing effects.
* **Feature 5: Gravitational Physics Engine:** Built the core simulation engine using Newton's Law and Velocity Verlet integration.
* **Feature 6: Black Hole Capture Mechanics:** Implemented the logic for tidal forces, spaghettification, and the event horizon.

### **Part 3: Interactivity & State Management - Evan Yuvraj Munshi**

* **Feature 7: Supernova & Debris System:** Created the supernova explosion and the persistent debris particle systems.
* **Feature 8: User Controls & HUD:** Developed the interactive menu, Heads-Up Display, and all keyboard/mouse inputs.
* **Feature 9: State Management & Sequences:** Managed the complex event chains (e.g., Red Giant phase) and the collision detection system.
