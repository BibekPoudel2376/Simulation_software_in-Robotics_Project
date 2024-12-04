% Parameters
mass = 500;  % kg
u = 0.1;  % coefficient of friction
g = 9.81;  % m/s^2
thrust_provided_by_launcher = 8000;  % N
distance_thrust_is_applied = 3;  % m

% Track Dimensions
x1 = 10;  % flat
x2 = 10;  % incline
x3 = 10;  % flat after incline
theta = 30;  % incline angle (degrees)

% Function to get angle based on position
function angle = get_angle_from_x_position(x, x1, x2, theta)
    if x <= x1
        angle = 0;
    elseif x <= x1 + x2
        angle = theta;
    else
        angle = 0;
    end
end

% Runge-Kutta Method
function result = runge_kutta(f, y0, t0, t1, h)
    n = ceil((t1 - t0) / h);
    t = t0;
    y = y0;
    result = [t, y];
    for i = 1:n
        k1 = h * f(t, y);
        k2 = h * f(t + h / 2, y + k1 / 2);
        k3 = h * f(t + h / 2, y + k2 / 2);
        k4 = h * f(t + h, y + k3);
        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6;
        t = t + h;
        result = [result; t, y];
    end
end

% Acceleration function
function a = acceleration(t, v, x1, x2, theta, u, mass, g, thrust_provided_by_launcher, distance_thrust_is_applied)
    persistent distance;
    if isempty(distance)
        distance = 0;
    end
    x = distance + v * t;
    angle = get_angle_from_x_position(x, x1, x2, theta);
    thrust = (x <= distance_thrust_is_applied) * thrust_provided_by_launcher;
    drag = u * mass * g * cosd(angle);
    gravity = mass * g * sind(angle);
    net_force = thrust - drag - gravity;
    a = net_force / mass;
    distance = x;
end

% Solve velocity using Runge-Kutta
result = runge_kutta(@(t, v) acceleration(t, v, x1, x2, theta, u, mass, g, thrust_provided_by_launcher, distance_thrust_is_applied), 0, 0, 5, 0.01);
t = result(:, 1);
v = result(:, 2);

% Calculate Cumulative Distance
distances = cumtrapz(t, v);

% Get position from distance
function [x, y] = get_position(distance, x1, x2, theta)
    if distance <= x1
        x = distance;
        y = 0;
    elseif distance <= x1 + x2
        x = x1 + (distance - x1) * cosd(theta);
        y = (distance - x1) * sind(theta);
    else
        x = x1 + x2 * cosd(theta) + (distance - x1 - x2);
        y = x2 * sind(theta);
    end
end

% Stopping condition
stop_time = NaN;
stop_x = NaN;
stop_y = NaN;
for i = 1:length(t)
    if abs(v(i)) < 1e-3
        stop_time = t(i);
        [stop_x, stop_y] = get_position(distances(i), x1, x2, theta);
        fprintf('Roller coaster stops at t=%.2fs at position (x,y)=(%.2f,%.2f)m\n', stop_time, stop_x, stop_y);
        break;
    end
end

if isnan(stop_time) && distances(end) >= x1 + x2 + x3
    stop_time = t(end);
    [stop_x, stop_y] = get_position(x1 + x2 + x3, x1, x2, theta);
    fprintf('Roller coaster completes the track at t=%.2fs at position (x,y)=(%.2f,%.2f)m\n', stop_time, stop_x, stop_y);
elseif isnan(stop_time)
    stop_time = t(end);
    [stop_x, stop_y] = get_position(distances(end), x1, x2, theta);
    fprintf('Roller coaster stops at t=%.2fs at position (x,y)=(%.2f,%.2f)m\n', stop_time, stop_x, stop_y);
end

% Animation
figure;
hold on;
track_x = [0, x1, x1 + x2 * cosd(theta), x1 + x2 * cosd(theta) + x3];
track_y = [0, 0, x2 * sind(theta), x2 * sind(theta)];
plot(track_x, track_y, 'k-', 'LineWidth', 2);
xlim([0, max(track_x)]);
ylim([0, max(track_y) + 1]);
xlabel('Distance (m)');
ylabel('Height (m)');
title('Roller Coaster Simulation');
cart = plot(0, 0, 'ro', 'MarkerSize', 8, 'MarkerFaceColor', 'r');

for frame = 1:length(t)
    if frame <= length(distances)
        [x_pos, y_pos] = get_position(distances(frame), x1, x2, theta);
    else
        x_pos = stop_x;
        y_pos = stop_y;
    end
    set(cart, 'XData', x_pos, 'YData', y_pos);
    pause(0.01);
end
