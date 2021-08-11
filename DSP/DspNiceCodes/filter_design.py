#################################################################################
#                                                                               #
#                     Filter Design Using Scipy Signal                          #
#     																			#
#################################################################################

""" 
	Creating a IIR Filter using Scipy and using the results to apply 
	in the real time process function

            jw                 -jw              -jwM
   jw    B(e  )    b[0] + b[1]e    + ... + b[M]e
H(e  ) = ------ = -----------------------------------
            jw                 -jw              -jwN
         A(e  )    a[0] + a[1]e    + ... + a[N]e
"""

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


########################### Variables ############################
order=4
fs=48000
fcut=10000
fc=fcut/(fs/2)
filter_type="butter"
output_type="ba"

###################### Getting coeficients ########################
b, a = signal.iirfilter(order, fc, btype='low',analog=False,ftype=filter_type,output=output_type)


################### Testing Custom coeficients ####################
# b=[-0.3496,-1.2962,-1]
# a=[1,1.2962,0.3496]

################## Ploting Poles and Zeros  #######################
#Checking filter performance and stability
zplane(b,a)
w, h = signal.freqz(b, a, worN=2048)
freq=w * fs * 1.0 / (2 * np.pi)
amp=20*np.log10(abs(h)) #Convert to dB
angle=180 * np.angle(h) / np.pi 	# Convert to degrees

################ Ploting Frequency/Phase Response  ################
plt.figure()
plt.subplot(211)
plt.title('Frequency Response',fontsize=14)
plt.semilogx(freq, amp)
plt.ylabel('Amplitude [dB]')
plt.xlabel('Frequency [Hz]')
plt.xlim(20,20000)
plt.ylim(-150,5)
plt.grid(which='both', linestyle='-', color='grey')
plt.xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000], ["20", "50", "100", "200", "500", "1K", "2K", "5K", "10K", "20K"])
plt.subplot(212)
plt.semilogx(freq, angle)
plt.ylabel('Phase [Deg]')
plt.xlabel('Frequency [Hz]')
plt.xlim(20,20000)
plt.grid(which='both', linestyle='-', color='grey')
plt.xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000], ["20", "50", "100", "200", "500", "1K", "2K", "5K", "10K", "20K"])
plt.show()

################ Printing filter coeficients  ################
print("\n-------------------------- Filter coeficients ----------------------\n")
alpha=[a[i] for i in range(len(a))]
beta=[b[i] for i in range(len(b))]
print("a =",alpha,"\n")
print("b =",beta,"\n")

