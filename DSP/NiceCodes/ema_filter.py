##########################################################################
#                                                                        #
#                Exponential Moving Average Filter                       #
#                                                                        #
##########################################################################

"""

LP:
Y(n)=aX(n)+(1-a)Y(n-1)
HP:
Y(n)=(1-a)X(n)-(1-a)Y(n-1)
BP:
Y(n)=(1-ah-al)X(n)-(2-ah-al)Y(n-1)
BR:
Y(n)=(ah+al)X(n)+(2-ah-al)Y(n-1)

Calculating cutoff frequency:
alpha=(-beta+sqrt((beta^2)+4*beta))/2
beta=2-2*cos(2*pi*Fc_L/Fs)

"""

import math
import matplotlib.pyplot as plt
import numpy as np
import os

###################### Imput variables ###################

Fc_L=2000 #Low cut-off frequency

Fc_H=2000 #High cut-off frequency

Fs=16000 #Sampling frequency

seeds=[65321,12043,2769] #Seeds (1,2 and 3)

size=16000 #Output samples


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
def get_fft(array,Fs):
    ts=1/(int(Fs))
    t=np.arange(0,(len(array)*ts),ts)
    n=np.size(t)
    fr=(int(Fs)/2)*np.linspace(0,1,int(n/2))
    resp=np.fft.fft(array)
    freq=(2/n)*abs(resp[0:np.size(fr)])
    return freq,fr,t #Array, frequency in hz, time in sec


#Get function for alpha (depends on the Fc)
def get_alpha(Fc,Fs):
    beta=2-2*math.cos(2*math.pi*Fc/Fs)
    alpha=(-beta+math.sqrt((beta**2)+4*beta))/2
    return alpha


####################### FILTERS ######################

#Low pass filter ( Y(n)=aX(n)+(1-a)Y(n-1) )
def low_pass(array,alpha):
    output=[]
    for i in range(len(array)):
        if i==0:
            output.append(alpha*array[i])
        else:
            output.append(alpha*array[i]+(1-alpha)*output[i-1])
    return output

#High pass filter ( Y(n)=(1-a)X(n)-(1-a)Y(n-1) )
def high_pass(array,alpha):
    output=[]
    hp_array=low_pass(array,alpha)
    for i in range(len(hp_array)):
        output.append(array[i]-hp_array[i])
    return output


########################## FFTs ##################################
#Original Random Array
Original_array=get_random(seeds,size)
Original_array_fft,O_fr,O_t=get_fft(Original_array,Fs)

#Low pass array
LP_array=low_pass(Original_array,get_alpha(Fc_L,Fs))
LP_array_fft,LP_fr,LP_t=get_fft(LP_array,Fs)

#High pass array
HP_array=high_pass(Original_array,get_alpha(Fc_H,Fs))
HP_array_fft,HP_fr,HP_t=get_fft(HP_array,Fs)


########################## Ploting ##################################
plt.figure()
plt.subplot(121)
plt.plot(LP_fr/(Fs/2),20 * np.log10(LP_array_fft/(max(LP_array_fft))),); plt.title('Low Pass Filter')
plt.ylabel('Amplitude [dB]'); plt.xlabel('Frequency [pi*rad/sample]')
plt.ylim(-15,0)
plt.subplot(122)
plt.plot(HP_fr/(Fs/2),20 * np.log10(HP_array_fft/(max(HP_array_fft))),'r'); plt.title('High Pass Filter')
plt.ylabel('Amplitude [dB]'); plt.xlabel('Frequency [pi*rad/sample]')
plt.ylim(-15,0)
plt.show()
