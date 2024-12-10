import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import CubicSpline

# Parameters
mass = 500  # kg
u = 0.1  # coefficient of friction
g = 9.81  # m/s^2
thrust_provided_by_launcher = 32000 # N
distance_thrust_is_applied = 3  # m

# Cubic spline nodes for the track
x_points = [0, 10, 20, 30]
y_points = [0, 0, 5, 5]
cs = CubicSpline(x_points, y_points)

# Function to get a position on the spline track
def get_position_cubic(distance):
    x = min(max(0, distance), x_points[-1])  # Clamp position
    y = cs(x)
    return x, y

# Runge-Kutta integration method
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

# Update acceleration to account for slope
def acceleration(t, v):
    x = v * t if t > 0 else 0
    thrust = thrust_provided_by_launcher if x <= distance_thrust_is_applied else 0

    slope = cs.derivative()(x)
    angle = np.arctan(slope) if t > 0 else 0  
    drag = u * mass * g * np.cos(angle)
    gravity = mass * g * np.sin(angle)
    net_force = thrust - drag - gravity
    return net_force / mass

# Run simulation using the Runge-Kutta method
result = runge_kutta(acceleration, 0, 0, 5, 0.01)
t, v = zip(*result)

# Calculate distances
distances = [0]
for i in range(1, len(v)):
    distances.append(distances[-1] + v[i] * (t[i] - t[i - 1]))

# Identify when and where the roller coaster stops
stop_time, stop_x, stop_y = None, None, None
for i in range(len(t)):
    if v[i] <= 1e-3:
        stop_time = t[i]
        stop_x, stop_y = get_position_cubic(distances[i])
        print(f"Roller coaster stops at t={stop_time:.2f}s at position (x,y)=({stop_x:.2f},{stop_y:.2f})m")
        break

if stop_time is None:
    stop_time = t[-1]
    stop_x, stop_y = get_position_cubic(distances[-1])
    print(f"Roller coaster stops at t={stop_time:.2f}s at position (x,y)=({stop_x:.2f},{stop_y:.2f})m")

# Plot Velocity over Time
plt.figure()
plt.plot(t, v, label='Velocity (m/s)')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.title('Velocity vs Time with Inclined Spline Track')
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

# Animation of the roller coaster on spline track
fig, ax = plt.subplots()
ax.set_xlim(0, x_points[-1])
ax.set_ylim(0, max(y_points) + 1)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Height (m)')
ax.set_title('Roller Coaster Simulation with Inclined Spline Track')

# Plot Track
track_x = np.linspace(0, x_points[-1], num=500)
track_y = cs(track_x)
ax.plot(track_x, track_y, 'k-', label='Track')

cart, = ax.plot([], [], 'ro', markersize=8)

def update(frame):
    if frame < len(t):
        x_pos, y_pos = get_position_cubic(distances[frame])
        cart.set_data([x_pos], [y_pos])
    else:
        cart.set_data([stop_x], [stop_y])
    return cart,

anim = FuncAnimation(fig, update, frames=len(t) + 1, interval=10, blit=True)
plt.legend()
plt.show() 0x0d