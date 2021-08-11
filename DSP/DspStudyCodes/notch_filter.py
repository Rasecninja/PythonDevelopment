######## NOTCH FILTER ###########

import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
import os

###################### Imput variables ###################

fs=16000 #Sampling frequency

fc=6000 #Cut off frequency

seeds=[65321,12043,2769] #Seeds (1,2 and 3)

size=16000 #Output samples for the random code 

a=0.9 #Alpha value

wn=2*math.pi*fc/fs #Cut off freq in rad/sample

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

# The notch filter
def notch_filter(array,a,wn):
    output=[]
    for i in range(len(array)):
        if i>1:
            output.append((2*a*math.cos(wn)*output[i-1]-(a**2)*output[i-2])+(((1+a)/2)*(array[i]-2*math.cos(wn)*array[i-1]+array[i-2])))
        else:
            output.append(array[i])
    return output


########################## Ploting ##################################

Original_array=get_random(seeds,size)
Original_array_fft,O_fr,O_t=get_fft(Original_array,fs)

Notch_array=notch_filter(Original_array,a,wn)
Notch_array_fft,Notch_fr,Notch_t=get_fft(Notch_array,fs)

# Saving a wav file with Scypi
#rate=16000
#data=np.asarray(Notch_array, dtype=np.int16)
#wav.write('comb_filter.wav',rate,data)

# Plotting with Matplotlib
plt.figure()
plt.subplot(211)
plt.plot(O_fr,[20*math.log10(i) for i in Original_array_fft]); plt.title('Notch Filter')
plt.xlabel('Frequency(Hz)');plt.ylabel('dB'); plt.ylim(-60,-30)
plt.subplot(212)
plt.plot(Notch_fr,[20*math.log10(i) for i in Notch_array_fft],'r')
plt.xlabel('Frequency(Hz)');plt.ylabel('dB'); plt.ylim(-60,-30)
plt.show()
