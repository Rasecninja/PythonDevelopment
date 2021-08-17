#################################################################################
#                                                                               #
#                      Directionality coeficients                               #
#     																			#
#################################################################################

'''
	Fractional delay filter is used for directionality applications


	Delay = Phase Front Mic(Deg) - Phase Rear Mic(Deg)
		    -------------------------------------------
					     360 * f

	The delay calculated will be for one frequency just since the phase changes
	for every frequency.

	The idea is to keep on filter fixed and only change the coeficients in the
	rear mic filter

'''

################# Imports #########################
import math
import numpy as np
import scipy.io.wavfile as wav
from scipy import signal
import sys
import matplotlib.pyplot as plt


#Importing files from different directory
sys.path.append('../Libraries')

from real_time_dsp import *
from zplane import zplane 

print("\n---------------- Directionality Fractional Delay Coeficients ---------------------")

################### Variables ####################
fs=48000
reference_freq=1000
beta=1 #Cardioid
mic_distance=0.00877
speed_sound=343
delay=(beta*mic_distance)/speed_sound
#Calculating phase difference in degrees
phase_difference=delay*reference_freq*360
print("\nDESIRED")
print("Phase delay: ",phase_difference)
print("Time delay: ",delay*1e+6,"us")


################### Rear Mic Filter #################### Original Coeficients
b=[-0.1012,-0.8770,-1]
a=[1,0.8770,0.1012]

w, h = signal.freqz(b, a, worN=2048)
freq=w * fs * 1.0 / (2 * np.pi)
amp=20*np.log10(abs(h)) #Convert to dB
angle=180 * np.angle(h) / np.pi 	# Convert to degrees
mag=abs(h)

x=[freq[i] for i in range(len(freq))]	#Finding which channel is 1kHz
channel=x.index(996.0937499999999)

print("\nCURRENT")
print("Rear Mic Angle (1kHz):",angle[channel])

rear_angle=angle[channel]

################### Front Mic Filter #################### Original Coeficients
b=[-0.3496,-1.2962,-1]
a=[1,1.2962,0.3496]

w, h = signal.freqz(b, a, worN=2048)
freq=w * fs * 1.0 / (2 * np.pi)
amp=20*np.log10(abs(h)) #Convert to dB
angle=180 * np.angle(h) / np.pi 	# Convert to degrees
mag=abs(h)

print("Front Mic Angle (1kHz):",angle[channel])

front_angle=angle[channel]

################ Calculating delay between 2 filters  ################
phase_delay=front_angle-rear_angle
print("Phase delay: ",phase_delay)
time_delay=phase_delay/(360*996.0937499999999)
print("Time delay : ",time_delay*1e+6,"us")


#################### Adjusting the rear filter  ####################
adjust_angle=front_angle-phase_difference
angle=angle/angle[channel]
angle=angle*adjust_angle
#transforming back to retangular format
h=mag*np.exp(1j*(angle*np.pi/180))

#From Matlab function invfreqz get b and a (using calculated h and w)
b=np.asarray([-0.196274721749747,-1.090317590724696,-1])
a=np.asarray([1.000000000000000, 1.090317590724696, 0.196274721749747])

w, h = signal.freqz(b, a, worN=2048)
freq=w * fs * 1.0 / (2 * np.pi)
amp=20*np.log10(abs(h)) #Convert to dB
angle=180 * np.angle(h) / np.pi 	# Convert to degrees
mag=abs(h)

rear_angle=angle[channel]

print("\nADJUSTED")
print("Front Mic Angle (1kHz):",front_angle)
print("Rear Mic Angle (1kHz):",angle[channel])
phase_delay=front_angle-rear_angle
print("Phase delay: ",phase_delay)
time_delay=phase_delay/(360*996.0937499999999)
print("Time delay : ",time_delay*1e+6,"us")

print("\n-----------------------------------------------------------------------------------")

# h1=[h[i] for i in range(len(h))]
# print(h1)

