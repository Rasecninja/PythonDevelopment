# Implementation of Complimentary Filter for MPU-6050 6-DOF IMU
# 
# Author: Philip Salmony [pms67@cam.ac.uk] http://philsal.co.uk/projects/imu-attitude-estimation
# Date: 4 August 2018
# Edited by Cesar Severo in 2021

from imu import *
from time import sleep, time
from math import sin, cos, tan, pi

#Simulation mode
imu = IMU(True)

phi_total=[]
theta_total=[]

# Iterations and sleep time
N = 1900
sleep_time = 0.01

# Filter coefficient
alpha = 0.1

print("Calculating average gyro bias...")
[bx, by, bz] = imu.get_gyro_bias(200)

# Complimentary filter estimates
phi_hat = 0.0
theta_hat = 0.0

print("Running...")

# Measured sampling time
dt = 0.0
start_time = time()

imu.sample_counter=0

for i in range(N):
    dt = time() - start_time
    start_time = time()
    
    # Get estimated angles from raw accelerometer data
    [phi_hat_acc, theta_hat_acc] = imu.get_acc_angles()
    
    # Get raw gyro data and subtract biases
    [p, q, r] = imu.get_gyro()
    p -= bx
    q -= by
    r -= bz
    
    # Calculate Euler angle derivatives 
    phi_dot = p + sin(phi_hat) * tan(theta_hat) * q + cos(phi_hat) * tan(theta_hat) * r
    theta_dot = cos(phi_hat) * q - sin(phi_hat) * r
    
    # Update complimentary filter
    phi_hat = (1 - alpha) * (phi_hat + dt * phi_dot) + alpha * phi_hat_acc
    theta_hat = (1 - alpha) * (theta_hat + dt * theta_dot) + alpha * theta_hat_acc   

    phi_total.append(phi_hat * 180.0 / pi)
    theta_total.append(theta_hat * 180.0 / pi)

import matplotlib.pyplot as plt

plt.plot(phi_total)
plt.show()
