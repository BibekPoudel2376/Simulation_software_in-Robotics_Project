%% Parameters for Three-Phase PMLSM Drive Example

% This example shows how to control the position in a three-phase 
% permanent magnet linear synchronous machine (PMLSM) drive. The Control 
% subsystem uses a PI-based cascade control structure with three control 
% loops, an outer position control loop, a speed control loop and two 
% inner current control loops. A controlled three-phase converter feeds 
% the PMLSM. The simulation uses step references. The Scopes subsystem 
% contains scopes that allow you to see the simulation results.

% Copyright 2019-2023 The MathWorks, Inc.

%% Machine Parameters
% PMSM parameters 
Fmax  = 2000;   % Max thrust [N]
PM    = 0.65;  % Permanent magnet flux linkage [Wb]
Ld    = 0.01;  % d-axis inductance [H]
Lq    = 0.01;  % q-axis inductance [H]
L0    = 2e-4;  % 0-axis inductance [H]
Rs    = 0.6;   % Stator resistance [Ohm]
mass  = 1000;    % Mass [Kg]
pitch = 0.1;  % Polar pitch [m]
Np = pi/pitch;

%% Control Parameters
Ts   = 5e-5;       % Fundamental sample time            [s]
fsw  = 2e3;        % PMSM drive switching frequency     [Hz]
Tsc  = 1e-3;       % Sample time for inner control loop [s]

Kp_id = 10;     % Proportional gain id controller
Ki_id = 1250;   % Integrator gain id controller
Kp_iq = Kp_id;     % Proportional gain iq controller
Ki_iq = Ki_id; % Integrator gain iq controller

Kp_v = 250;     % Proportional gain velocity controllera
Ki_v = 250;     % Integrator gain velocity controller

Kp_p = 200;     % Proportional gain velocity controller
Ki_p = 100;     % Integrator gain velocity controller
