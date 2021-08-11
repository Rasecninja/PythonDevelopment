######### DC FILTER ###########

import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
import os

#Fix Matplotlib issue
# os.environ['TCL_LIBRARY'] = r'C:\Users\OliveUnion\AppData\Local\Programs\Python\Python38-32\tcl\tcl8.6'
# os.environ['TK_LIBRARY'] = r'C:\Users\OliveUnion\AppData\Local\Programs\Python\Python38-32\tcl\tk8.6'

###################### Imput variables ###################

fs=48000 #Sampling frequency

seeds=[65321,12043,2769] #Seeds (1,2 and 3)

size=48000 #Output samples for the random code 

a=0.99 #Alpha value used in the type 0 filter

d=31 #The d (amount of delayed samples) value used in the type 1 filter 

filter_type=0 #Chooses between filters implementation

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

# The DC filter
def dc_filter(filter_type,array,a,d):
    output=[]
    if filter_type==0:
        for i in range(len(array)):
            if i>0:
                output.append((a*output[i-1])+(((1+a)/2)*(array[i]-array[i-1])))
            else:
                output.append(array[i])
    else:
        for i in range(len(array)):
            if i>=d:
                output.append(-output[i-1]-((1/d)*(array[i]-array[i-d]))+array[i-int(((d-1)/2))])
            else:
                output.append(array[i])
    return output


########################## Ploting ##################################

Original_array=get_random(seeds,size)
Original_array_fft,O_fr,O_t=get_fft(Original_array,fs)

DC_array=dc_filter(filter_type,Original_array,a,d)
DC_array_fft,DC_fr,DC_t=get_fft(DC_array,fs)

# Plotting with Matplotlib
plt.figure()
plt.subplot(211)
plt.plot(O_fr,Original_array_fft); plt.title('DC Filter')
plt.xlabel('Frequency(Hz)');plt.ylabel('Amplitude')
plt.subplot(212)
plt.plot(DC_fr,DC_array_fft,'r')
plt.xlabel('Frequency(Hz)');plt.ylabel('Magnitude')
plt.show()
