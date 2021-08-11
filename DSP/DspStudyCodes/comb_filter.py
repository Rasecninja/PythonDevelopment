#### Comb Filter ####

'''
        Transfer function

        H(z)= b0 +bd*z^-d

'''

import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
import os
from scipy import signal

###################### Imput variables ###################

fs=10000 #Sampling frequency

seeds=[65321,12043,2769] #Seeds (1,2 and 3)

size=1000 #Output samples for the random code 

d=5 #Delay samples

a=1 #Alpha value

####################### Functions ############################
# Making 16bit random numbers
#Main Loop for each sample
def get_random(seeds,size):
    if len(seeds)>3:
        return 0
    array=[]
    seed_count=0
    gama=0
    for i in range(size):
        val=bin(seeds[seed_count]**2)
        val=val[2:]
        if len(val)>32:
            val=val[(len(val)-32):]
        val=val.zfill(32)
        val=val[0+gama:16+gama]
        val=int(val,2)
        if gama==15:
            gama=0
        else:
            gama+=1
        if seed_count==2:
            seeds[seed_count]=val+seeds[0]
            seed_count=0
        else:
            seeds[seed_count]=val+seeds[seed_count+1]
            seed_count+=1
        #array.append(val)   #Non normalized
        array.append((val/(2**15-1))-1)   #Normalized
    return array

# Output the frequency array
def get_fft(array,fs):
    ts=1/(int(fs))
    t=np.arange(0,(len(array)*ts),ts)
    n=np.size(t)
    fr=(int(fs)/2)*np.linspace(0,1,int(n/2))
    resp=np.fft.fft(array)
    freq=(2/n)*abs(resp[0:np.size(fr)])
    return freq,fr,t #Array, frequency in hz, time in sec

def comb_filter(array,d,a):
    output=[]
    for i in range(len(array)):
            if i>(d-1):
                output.append(array[i]+a*array[i-d])
            else:
                output.append(array[i])
    return output                

########################## Ploting ##################################
Original_array=get_random(seeds,size)
Original_array_fft,O_fr,O_t=get_fft(Original_array,fs)

Comb_array=comb_filter(Original_array,d,a)
Comb_array_fft,Comb_fr,Comb_t=get_fft(Comb_array,fs)

### Frequency response of the filter ###
b=[]
for i in range(d+1):
    if i==0:
        b.append(1)
    elif i==(d):
        b.append(a)
    else:
        b.append(0)
w, h = signal.freqz(b)

plt.figure()
plt.subplot(121)
plt.plot(w/math.pi, 20 * np.log10(abs(h)), 'b'); plt.title('Comb Filter Frequency Response')
plt.ylabel('Amplitude [dB]'); plt.xlabel('Frequency [pi*rad/sample]')
plt.subplot(122)
plt.plot(Comb_fr[1:],Comb_array_fft[1:],'r'); plt.title('Comb Filter Result on White Noise')
plt.xlabel('Frequency(Hz)');plt.ylabel('Amplitude')
plt.show()
