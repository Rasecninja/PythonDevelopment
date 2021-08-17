#################################################################################
#                                                                               #
#               High Pass filtering tests for Hearing aid use                   #
#     																			#
#################################################################################

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


########################### Filter Design ############################
""" 
	Creating a IIR HPF using Scipy and using the results to apply 
	in the real time process function
"""
plot_filter=True
order=4
fs=48000
fcut=500
fc=fcut/(fs/2)
filter_type="butter"
output_type="ba"
#Getting the coeficients
b, a = signal.iirfilter(order, fc, btype='high',analog=False,ftype=filter_type,output=output_type)
"""
            jw                 -jw              -jwM
   jw    B(e  )    b[0] + b[1]e    + ... + b[M]e
H(e  ) = ------ = -----------------------------------
            jw                 -jw              -jwN
         A(e  )    a[0] + a[1]e    + ... + a[N]e
"""
#Checking filter performance and stability
if(plot_filter): 
	zplane(b,a)
	w, h = signal.freqz(b, a, worN=2048)
	freq=w * fs * 1.0 / (2 * np.pi)
	amp=20*np.log10(abs(h)) #Convert to dB
	angle=180 * np.angle(h) / np.pi 	# Convert to degrees

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

####################### Variables ############################
#All filters
wav_out=False
frame_counter=0
previous_input_frame=[]
previous_output_frame=[]


####################### Functions ############################
def pre_proc_func(input_data):
	global filter_type
	output_data=custom_high_pass(input_data)
	return output_data


########## IIR HP Filter made with Scipy design tool  #############
def custom_high_pass(array):
	#Denominator
	global a
	#Numerator
	global b
	#Holder of the previous input frame (X(n))
	global previous_input_frame
	#Holder of the previous output frame (Y(n))
	global previous_output_frame
	#The frame counter
	global frame_counter
	#Output array
	output=[]
	#Check if the input array is bigger than the filter order
	if((len(array)<len(b)) or (len(array)<len(a))): return None
	#Check if previous frame is empty
	if(frame_counter==0):
		previous_input_frame=[0]*len(array)
		previous_output_frame=[0]*len(array)
	#Samples loop
	for n in range(len(array)):
		#FF and FB values holder
		Feedback=0
		Feedforward=0
		#Calculating the Feedback values
		for i in range(1,len(a)):
			#Check if the previous output frame data is used 
			if(n-i<0): Feedback=Feedback-(a[i]*previous_output_frame[-i+n])
			#If n>len(a)-1 then only current output frame data is used
			else: Feedback=Feedback-(a[i]*output[n-i])
		#Calculating the Feedforward values
		for i in range(len(b)):
			#Check if the previous input frame data is used 
			if(n-i<0): Feedforward=Feedforward+(b[i]*previous_input_frame[-i+n])
			#If n>len(b)-1 then only current input frame data is used
			else: Feedforward=Feedforward+(b[i]*array[n-i])	
		output.append((Feedforward+Feedback)/a[0])
	previous_input_frame=array
	previous_output_frame=output
	frame_counter=frame_counter+1
	return output

####################### Calling ############################
if(wav_out): wave_file_process("../Example Music/White Noise.wav","HPF_"+filter_type+".wav",progress_bar=True,nfft=256,zero_pad=False,stereo=False,pre_proc_func=pre_proc_func,freq_proc_func=None)
