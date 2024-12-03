import numpy as np
import matplotlib.pyplot as plt

def simulate_coaster_with_initial_thrust(mass, angle_deg, initial_force, thrust_distance, friction_coefficient, horizontal_length, ramp_length):
    """
    Simulates motion of a rollercoaster with an initial thrust over a horizontal track and a ramp.
    
    Parameters:
    - mass: Mass of the rollercoaster in kg
    - angle_deg: Ramp angle in degrees
    - initial_force: Force provided by the actuator in Newtons
    - thrust_distance: Distance over which the actuator provides thrust in meters
    - friction_coefficient: Coefficient of friction
    - horizontal_length: Length of the horizontal track in meters
    - ramp_length: Length of the ramp in meters
    
    Returns:
    - success: True if the rollercoaster reaches the top of the ramp, False otherwise
    - positions: List of positions over time
    - times: List of time steps
    """
    # Constants
    g = 9.8  # Acceleration due to gravity in m/s^2
    angle_rad = np.radians(angle_deg)
    
    # Friction force
    friction_force_horizontal = friction_coefficient * mass * g
    friction_force_ramp = friction_coefficient * mass * g * np.cos(angle_rad)
    
    # Calculate velocity from initial thrust
    net_force_horizontal = initial_force - friction_force_horizontal
    if net_force_horizontal > 0:
        acceleration = net_force_horizontal / mass
        velocity = np.sqrt(2 * acceleration * thrust_distance)  # v^2 = 2 * a * d
    else:
        velocity = 0  # No movement if force is insufficient
    
    # Check if the rollercoaster can climb the ramp
    potential_energy_ramp = mass * g * (ramp_length * np.sin(angle_rad))  # m * g * h
    work_against_friction = friction_force_ramp * ramp_length  # F * d
    kinetic_energy = 0.5 * mass * velocity**2  # KE = 1/2 m v^2
    
    can_climb = kinetic_energy >= (potential_energy_ramp + work_against_friction)
    
    # Simulate positions for visualization
    positions = []
    times = []
    time_step = 0.1  # Iterate every 1 second
    position = 0
    time = 0
    
    # Plot setup
    plt.figure(figsize=(10, 6))
    plt.plot([0, horizontal_length], [0, 0], 'k-', label="Horizontal Track")  # Horizontal track
    plt.plot([horizontal_length, horizontal_length + ramp_length * np.cos(angle_rad)], 
             [0, ramp_length * np.sin(angle_rad)], 'k-', label="Ramp")  # Ramp
    plt.xlabel("Horizontal Distance (m)")
    plt.ylabel("Vertical Distance (m)")
    plt.title("Rollercoaster Motion with Initial Thrust")
    plt.legend()
    plt.grid()
    
    # Horizontal motion
    while position < horizontal_length and velocity > 0:
        positions.append(position)
        times.append(time)
        plt.plot(position, 0, 'ro')  # Rollercoaster as red circle
        plt.pause(1)  # Pause to simulate motion
        plt.draw()  # Update the plot
        position += velocity * time_step
        time += time_step
    
    # Ramp motion
    while position < (horizontal_length + ramp_length * np.cos(angle_rad)) and velocity > 0:
        positions.append(position)
        times.append(time)
        height = (position - horizontal_length) * np.tan(angle_rad)
        plt.plot(position, height, 'ro')  # Rollercoaster as red circle
        plt.pause(0.5)  # Pause to simulate motion
        plt.draw()  # Update the plot
        position += velocity * time_step  # Assume constant velocity for simplicity
        time += time_step
        # Update velocity due to gravity and friction
        velocity -= (g * np.sin(angle_rad) + friction_force_ramp / mass) * time_step
    
    success = position >= (horizontal_length + ramp_length * np.cos(angle_rad))
    
    plt.show()
    return success, positions, times

# Inputs
mass = 500  # Mass in kg
angle_deg = 30  # Ramp angle in degrees
initial_force = 4500  # Force from the actuator in Newtons
thrust_distance = 10  # Distance over which the actuator provides thrust in meters
friction_coefficient = 0.1  # Coefficient of friction
horizontal_length = 50  # Horizontal track length in meters
ramp_length = 20  # Ramp length in meters

# Simulation
success, positions, times = simulate_coaster_with_initial_thrust(
    mass, angle_deg, initial_force, thrust_distance, friction_coefficient, horizontal_length, ramp_length
)

# Output results
if success:
    print("The rollercoaster successfully climbs the ramp!")
else:
    print("The rollercoaster fails to climb the ramp.")
