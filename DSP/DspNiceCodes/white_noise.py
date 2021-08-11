##########################################################################
#                                                                        #
#                           White Noise                                  #
#                                                                        #
##########################################################################
'''
    Random number generation with 16 bit variable
- Using 3 seeds
- Just 2 counters
- Only one squared, one addition operation and one shift
- Only 10 bytes need for RAM

                          THE ALGORITHM

1- Take the seed using counter to select between the 3. The counter is 
increased by 1 every loop. Here is an example of 3 seeds.

seeds=[65321,12043,2769]

val=seeds[seed_counter]=65321= 1111111100101001

2- Square the current "val"  value to get twice the size (32 bit now)

val=val*val= 11111110010100101011010010010001

3- Select the output based on the gama factor. Gama, same as seed counter,
gets updated every loop, being that the maximum is the number of bits
precision, this case 16 (0 to 15)

11111110010100101011010010010001
|     gama=0    |
 |     gama=1    |
  |     gama=2    |
            ...
               |     gama=15    |

For gama=0, the output value will be 1111111001010010 or 65106

4- Next step is to update the seeds. Using the output value, 
add this value to the next seed. Hence the values will be 
even more likely to immitate random behaviour. 

seeds[seed_counter]=val+seeds[seed_counter+1]

For seed_counter=0

seeds[0]=65106+12043= 11613 = 0010110101011101*

* Note that the value overflew and there is no
problem with overflow

'''

import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wav
import os

###################### Imput variables ###################

fs=44100 #Sampling frequency

seeds=[65321,12043,2769] #Seeds (1,2 and 3)

size=4410000 #Output samples for the random code 

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

########################## Ploting ##################################

white_noise=get_random(seeds,size)

# Saving a wav file with Scypi
data=np.asarray(white_noise, dtype=np.float32) #Normalized
wav.write('White Noise.wav',fs,data)

