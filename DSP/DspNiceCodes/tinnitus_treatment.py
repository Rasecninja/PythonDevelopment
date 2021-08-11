##########################################################################
#                                                                        #
#                        Tinnitus Treatment                              #
#                                                                        #
##########################################################################

'''
    Tinnitus treatment using white noise with 
    notch filter in the costumer's frequency

Usage of the following techniques:
- Random number generation
- Notch filter 
- DC filter
'''
import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
import os

###################### Imput variables ###################

fs=44100 #Sampling frequency

fc=11000 #Cut off frequency

wn=2*math.pi*fc/fs #Cut off freq in rad/sample

seeds=[65321,12043,2769] #Seeds (1,2 and 3)

size=441000 #Output samples for the random code 

a_dc=0.9 #Alpha value used in the dc filter

a_t=0.9 #Alpha value used in the notch filter

gain=-12 #Gain factor to be applied in the output file (in dB)

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

# The DC filter
def dc_filter(array,a):
    output=[]
    for i in range(len(array)):
        if i>0:
            output.append((a*output[i-1])+(((1+a)/2)*(array[i]-array[i-1])))
        else:
            output.append(array[i])
    return output

# The notch filter
def notch_filter(array,a,wn):
    output=[]
    for i in range(len(array)):
        if i>1:
            output.append((2*a*math.cos(wn)*output[i-1]-(a**2)*output[i-2])+(((1+a)/2)*(array[i]-2*math.cos(wn)*array[i-1]+array[i-2])))
        else:
            output.append(array[i])
    return output

# Output the frequency array
def get_fft(array,fs):
    ts=1/(int(fs))
    t=np.arange(0,(len(array)*ts),ts)
    n=np.size(t)
    fr=(int(fs)/2)*np.linspace(0,1,int(n/2))
    resp=np.fft.fft(array)
    freq=(2/n)*abs(resp[0:np.size(fr)]) 
    #(2/n) is for normalizing since the FFT size is set as the size of the input array 
    # FFT amplitude is always half of the FFT points
    # In this case N-FFT ( np.fft.fft(array,len(array)) ) is the same as the lenght of the input array ( len(array) )
    return freq,fr,t #Array, frequency in hz, time in sec


########################## Ploting ##################################

Original_array=get_random(seeds,size)
Original_array_fft,Original_fr,Original_t=get_fft(Original_array,fs)

Notch_array=notch_filter(Original_array,a_t,wn)

Tinnitus_array=dc_filter(Notch_array,a_dc)   

Tinnitus_array_fft,Tinnitus_fr,Tinnitus_t=get_fft(Tinnitus_array,fs)

# Saving a wav file with Scypi
rate=fs
data=np.asarray(Tinnitus_array, dtype=np.float32)*(10**(gain/20))
wav.write('Tinnitus.wav',rate,data)

# Plotting with Matplotlib
plt.figure()
plt.subplot(211)
plt.plot(Original_fr,20*np.log10(Original_array_fft*(10**(gain/20)))); plt.title('White Noise Signal')
plt.ylabel('Magnitude')
plt.ylim(-80+gain,-40+gain)
plt.subplot(212)
plt.plot(Tinnitus_fr,20*np.log10(Tinnitus_array_fft*(10**(gain/20))),'r'); plt.title('After user calibration')
plt.xlabel('Frequency(Hz)');plt.ylabel('Magnitude')
plt.ylim(-80+gain,-40+gain)
plt.show()
