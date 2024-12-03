clc;
clear;
close all;

% Define constants
g = 9.81; % Gravity (m/s^2)
mu = 0.1; % Coefficient of friction
mass = 1.0; % Mass of the ball (kg)
time_step = 0.01; % Time step for simulation (s)

% Define the curved path (e.g., sinusoidal curve)
curve = @(x) 0.5 * sin(2 * pi * x / 10); % Example: sinusoidal path
curve_slope = @(x) (pi / 10) * cos(2 * pi * x / 10); % Slope of the curve

% Simulation function
simulate_ball = @(external_force) simulate(curve, curve_slope, mass, g, mu, external_force, time_step);

% Main Execution
while true
    try
        % Get external force input
        external_force = input('Enter the external force to apply (N): ');
        
        % Simulate the ball's motion
        [positions, cleared] = simulate_ball(external_force);
        
        % Display result
        if cleared
            fprintf('The ball successfully cleared the path!\n');
        else
            fprintf('The ball did not clear the path.\n');
        end
        
        % Animate the motion
        animate_motion(curve, positions);
    catch ME
        if strcmp(ME.identifier, 'MATLAB:InputParser:ArgumentFailedValidation')
            disp('Invalid input. Please enter a numeric value for the force.');
        else
            fprintf('\nExiting simulation.\n');
            break;
        end
    end
end

%% Function to Simulate Ball's Motion
function [positions, cleared] = simulate(curve, curve_slope, mass, g, mu, external_force, time_step)
    x = 0; % Initial x-position
    v_x = 0; % Initial velocity
    positions = [x, curve(x)]; % Store (x, y) positions

    while x < 10
        % Calculate forces
        slope = curve_slope(x);
        theta = atan(slope); % Slope angle
        f_gravity = mass * g * sin(theta); % Gravity component along slope
        normal_force = mass * g * cos(theta); % Normal force
        friction_force = mu * normal_force; % Friction force

        % Net force along the path
        net_force = f_gravity + external_force - friction_force;
        acceleration = net_force / mass;

        % Update velocity and position
        v_x = v_x + acceleration * time_step;
        x = x + v_x * time_step;
        y = curve(x); % Update y based on curve

        positions = [positions; x, y]; % Append new position
        if v_x <= 0 % Ball stops
            cleared = false;
            return;
        end
    end
    cleared = true; % Ball cleared the path
end

%% Function to Animate the Motion
function animate_motion(curve, positions)
    x_vals = positions(:, 1);
    y_vals = positions(:, 2);

    % Generate path curve
    x_curve = linspace(0, 10, 500);
    y_curve = curve(x_curve);

    % Create figure
    figure;
    plot(x_curve, y_curve, 'b-', 'LineWidth', 2); % Plot the path
    hold on;
    ball = plot(x_vals(1), y_vals(1), 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r'); % Ball
    title('Ball Sliding Over a Curved Path');
    xlabel('x (m)');
    ylabel('y (m)');
    axis([0, 10, -1, 1]);
    grid on;

    % Animate ball motion
    for i = 1:length(x_vals)
        set(ball, 'XData', x_vals(i), 'YData', y_vals(i));
        pause(0.01);
    end
end
