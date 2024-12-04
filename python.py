import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Runge-Kutta Method
def runge_kutta(f, y0, t0, t1, h):
    n = int((t1 - t0) / h)
    t = t0
    y = y0
    result = [(t, y)]
    
    for i in range(n):
        k1 = h * f(t, y)
        k2 = h * f(t + h / 2, y + k1 / 2)
        k3 = h * f(t + h / 2, y + k2 / 2)
        k4 = h * f(t + h, y + k3)
        
        y += (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += h
        result.append((t, y))
    
    return result

# Parameters
mass = 500  # kg
u = 0.1  # coefficient of friction
g = 9.81  # m/s^2
thrust_provided_by_launcher = 8000  # N
distance_thrust_is_applied = 3  # m

# Track Dimensions
x1 = 10  # flat
x2 = 10  # incline
x3 = 10  # flat after incline
theta = 30  # incline angle (degrees)

def get_angle_from_x_position(x):
    if x <= x1:
        return 0
    elif x <= x1 + x2:
        return theta
    else:
        return 0

def acceleration(t, v):
    x = v * t if t > 0 else 0  # Calculate position from velocity
    angle = get_angle_from_x_position(x)
    thrust = thrust_provided_by_launcher if x <= distance_thrust_is_applied else 0
    drag = u * mass * g * np.cos(np.radians(angle))
    gravity = mass * g * np.sin(np.radians(angle))
    net_force = thrust - drag - gravity
    return net_force / mass

# Solve Velocity with Runge-Kutta
result = runge_kutta(acceleration, 0, 0, 5, 0.01)
t, v = zip(*result)

# Calculate Cumulative Distance
distances = [0]
for i in range(1, len(v)):
    distances.append(distances[-1] + v[i] * (t[i] - t[i - 1]))

def get_position(distance):
    if distance <= x1:
        return distance, 0
    elif distance <= x1 + x2:
        x = x1 + (distance - x1) * np.cos(np.radians(theta))
        y = (distance - x1) * np.sin(np.radians(theta))
        return x, y
    else:
        x = x1 + x2 * np.cos(np.radians(theta)) + (distance - x1 - x2)
        y = x2 * np.sin(np.radians(theta))
        return x, y

# Stopping Condition
stop_time, stop_x, stop_y = None, None, None
for i in range(len(t)):
    if v[i] <= 1e-3:  # Near-zero velocity threshold
        stop_time = t[i]
        stop_x, stop_y = get_position(distances[i])
        print(f"Roller coaster stops at t={stop_time:.2f}s at position (x,y)=({stop_x:.2f},{stop_y:.2f})m")
        break

# Check if the cart completes the track
if stop_time is None and distances[-1] >= x1 + x2 + x3:
    stop_time = t[-1]
    stop_x, stop_y = get_position(x1 + x2 + x3)
    print(f"Roller coaster completes the track at t={stop_time:.2f}s at position (x,y)=({stop_x:.2f},{stop_y:.2f})m")
elif stop_time is None:
    stop_time = t[-1]
    stop_x, stop_y = get_position(distances[-1])
    print(f"Roller coaster stops at t={stop_time:.2f}s at position (x,y)=({stop_x:.2f},{stop_y:.2f})m")

# Plot Velocity over Time
plt.figure()
plt.plot(t, v, label='Velocity (m/s)')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity vs Time')
plt.legend()
plt.grid(True)
plt.show()

# Plot Distance over Time
plt.figure()
plt.plot(t, distances, label='Distance (m)')
plt.xlabel('Time (s)')
plt.ylabel('Distance (m)')
plt.title('Distance vs Time')
plt.legend()
plt.grid(True)
plt.show()

# Animation
fig, ax = plt.subplots()
ax.set_xlim(0, x1 + x2 * np.cos(np.radians(theta)) + x3)
ax.set_ylim(0, x2 * np.sin(np.radians(theta)) + 1)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Height (m)')
ax.set_title('Roller Coaster Simulation')

# Plot Track
track_x = [0, x1, x1 + x2 * np.cos(np.radians(theta)), x1 + x2 * np.cos(np.radians(theta)) + x3]
track_y = [0, 0, x2 * np.sin(np.radians(theta)), x2 * np.sin(np.radians(theta))]
ax.plot(track_x, track_y, 'k-')

cart, = ax.plot([], [], 'ro', markersize=8)

def update(frame):
    if frame < len(t):
        x_pos, y_pos = get_position(distances[frame])
        cart.set_data([x_pos], [y_pos])
    else:
        cart.set_data([stop_x], [stop_y])  # Final position if animation ends
    return cart,

anim = FuncAnimation(fig, update, frames=len(t) + 1, interval=10, blit=True)

plt.show()
