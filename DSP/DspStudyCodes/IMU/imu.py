# Helper class for the Complimentary and Kalman filters
# 
# Author: Philip Salmony [pms67@cam.ac.uk] http://philsal.co.uk/projects/imu-attitude-estimation
# Date: 4 August 2018
# Edited by Cesar Severo in 2021

import math
from time import sleep
import csv
import numpy as np

class IMU:
        
    def __init__(self, simulation=False):
        self.simulation=simulation
        if(type(self.simulation)!=bool): self.simulation=False
        if(self.simulation): self.init_simulation()
        else: self.init_driver()
        
    def init_driver(self):
        import smbus
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.addr = 0x68
        
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(self.addr, self.power_mgmt_1, 0)
        
        print("[IMU] Initialised.")

    def init_simulation(self):
        self.total_samples=0
        with open('imu_data.csv') as f:
            self.total_samples=sum(1 for line in f)
        self.total_samples-=1 #Removing the first row

        self.total_ax=np.zeros(self.total_samples)
        self.total_ay=np.zeros(self.total_samples)
        self.total_az=np.zeros(self.total_samples)

        self.total_gx=np.zeros(self.total_samples)
        self.total_gy=np.zeros(self.total_samples)
        self.total_gz=np.zeros(self.total_samples)

        self.sample_counter=0

        with open('imu_data.csv') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for line in csv_data:
                if line_count == 0:
                    line_count += 1
                else:
                    self.total_ax[line_count-1]=float(line[1])
                    self.total_ay[line_count-1]=float(line[2])
                    self.total_az[line_count-1]=float(line[3])
                    self.total_gx[line_count-1]=float(line[4])
                    self.total_gy[line_count-1]=float(line[5])
                    self.total_gz[line_count-1]=float(line[6])
                    line_count += 1
    
    # rad/s
    def get_gyro_bias(self, N=100):
        bx = 0.0
        by = 0.0
        bz = 0.0
        
        for i in range(N):
            [gx, gy, gz] = self.get_gyro()
            bx += gx
            by += gy
            bz += gz
            self.sample_counter+=1
            sleep(0.01)
            
        return [bx / float(N), by / float(N), bz / float(N)]            
        
    # rad/s
    def get_gyro(self):
        gx,gy,gz=0,0,0
        if(self.simulation):
            gx=self.total_gx[self.sample_counter]
            gy=self.total_gy[self.sample_counter]
            gz=self.total_gz[self.sample_counter]
            # Don't update sample counter in gyro
        else:    
            gx = self.read_word_2c(0x43) * math.pi / (180.0 * 131.0)
            gy = self.read_word_2c(0x45) * math.pi / (180.0 * 131.0)
            gz = self.read_word_2c(0x47) * math.pi / (180.0 * 131.0)
        return [gx, gy, gz]        
        
    # m/s^2
    def get_acc(self):
        ax,ay,az=0,0,0
        if(self.simulation):
            ax=self.total_ax[self.sample_counter]
            ay=self.total_ay[self.sample_counter]
            az=self.total_az[self.sample_counter]
            self.sample_counter+=1
        else:
            ax = self.read_word_2c(0x3b) / 16384.0
            ay = self.read_word_2c(0x3d) / 16384.0
            az = self.read_word_2c(0x3f) / 16384.0
        return [ax, ay, az]
    
    # rad
    def get_acc_angles(self):
        [ax, ay, az] = self.get_acc()
        phi = math.atan2(ay, math.sqrt(ax ** 2.0 + az ** 2.0))
        theta = math.atan2(-ax, math.sqrt(ay ** 2.0 + az ** 2.0))
        return [phi, theta]
      
    def read_byte(self, reg_adr):
        return self.bus.read_byte_data(self.addr, reg_adr)
    
    def read_word(self, reg_adr):
        high = self.bus.read_byte_data(self.addr, reg_adr)
        low = self.bus.read_byte_data(self.addr, reg_adr + 1)
        val = (high << 8) + low
        return val
    
    def read_word_2c(self, reg_adr):
        val = self.read_word(reg_adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
            