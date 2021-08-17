#################################################################################
#                                                                               #
#                Frame energy in frequency and time domain                      #
#                                                                               #
#################################################################################

from math import sin
from pylab import *
from math import pi

# Input Signal
x=[sin(2*pi*(440/44100)*i) for i in range(256)]
y=fft(x)

#Time domain energy
x_energy=[x[i]**2 for i in range(len(y))]
summ2=0
for i in range(256):
	summ2=summ2+x_energy[i]
summ2=summ2
print("Time domain energy: ",summ2)

#Full spectrum energy
y_energy=[abs(y[i])**2 for i in range(len(y))]
summ1=0
for i in range(256):
	summ1=summ1+y_energy[i]
summ1=summ1/256
print("Full spectrum energy: ",summ1)

#Half spectrum energy
y_half=y.copy()[:129]
y_energy_half=[abs(y_half[i])**2 for i in range(129)]
summ3=0
for i in range(129):
	summ3=summ3+y_energy_half[i]
for i in range(127):
	summ3=summ3+y_energy_half[i+1]
summ3=summ3/(256)
print("Half spectrum energy: ",summ3)
