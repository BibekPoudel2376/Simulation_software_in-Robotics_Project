% Get the maximum time available in the timeseries
max_time = max(d_total.Time);

% Generate the desired time steps, but ensure they do not exceed the maximum time
desired_times = 0:0.2:max_time;

% Resample the timeseries at the desired time points
resampled_ts = resample(d_total, desired_times);

% Extract the resampled data and time
time_stamp = resampled_ts.Time;
data = resampled_ts.Data;

% Include the last time and data point, if not already included
if time_stamp(end) < max_time
    time_stamp(end+1) = d_total.Time(end); % Add the last time
    data(end+1) = d_total.Data(end);       % Add the last data value
end

% Find the index of data at 4 seconds
index = find(d_total.Time == 4, 1);
length_of_horizontal_track = d_total.Data(index); % Length of horizontal track

fprintf('The horizontal track is %.3f\n', length_of_horizontal_track);

% Parameters for ramp
angle = 0.8; % angle in radians (30 degrees)
ramp_length = 30;

% Horizontal Track
horizontal_track_x = [0, length_of_horizontal_track];
horizontal_track_y = [0, 0];

% Ramp Part
ramp_x = linspace(length_of_horizontal_track, length_of_horizontal_track + ramp_length * cos(angle), 100);
ramp_y = linspace(0, ramp_length * sin(angle), 100);

% Calculate x and y positions of the cart
x_positions = zeros(size(time_stamp));
y_positions = zeros(size(time_stamp));

for i = 1:length(time_stamp)
    if time_stamp(i) <= 4
        % Horizontal motion
        x_positions(i) = data(i);
        y_positions(i) = 0;
    else
        % Ramp motion
        x_positions(i) = length_of_horizontal_track + (data(i) - length_of_horizontal_track) * cos(angle);
        y_positions(i) = (data(i) - length_of_horizontal_track) * sin(angle);
    end
end

% Plot the track
figure;
plot(horizontal_track_x, horizontal_track_y, 'b-', 'LineWidth', 2);
hold on;
plot(ramp_x, ramp_y, 'g-', 'LineWidth', 2);

% Set up plot properties
xlabel('Horizontal Distance (m)');
ylabel('Vertical Distance (m)');
title('Cart Motion on Track and Ramp');
axis equal;
xlim([0, max(ramp_x)]);
ylim([0, max(ramp_y) + 1]);
grid on;

% Create a point object for the cart
cart = plot(x_positions(1), y_positions(1), 'ro', 'MarkerSize', 10, 'MarkerFaceColor', 'r');

% Animation loop
for i = 1:length(time_stamp)
    % Update cart position
    set(cart, 'XData', x_positions(i), 'YData', y_positions(i));
    
    % Update title with current time
    title(sprintf('Cart Motion on Track and Ramp (Time: %.2f s)', time_stamp(i)));
    
    % Force MATLAB to draw the updated plot
    drawnow;
    
    % Pause to control animation speed
    pause(0.9); % Adjust this value for faster or slower animation speed
end
