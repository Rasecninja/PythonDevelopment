#################################################################################
#                                                                               #
#                         Correlation with different signals                    #
#     																			#
#################################################################################

################# Imports #########################
import math
import numpy as np
import scipy.io.wavfile as wav
import sys
from pylab import *

#Importing files from different directory
sys.path.append('../Libraries')

from real_time_dsp import *

####################### Variables ############################
#Frequency domain
num_ch=56
frame_counter=0
previous_freq_frame=[0]*num_ch
num_corr=(num_ch*2)-1
#Time domain
num_samples=64
auto_frames=8
previous_time_frame=[[0]*num_samples]*auto_frames

####################### AUTOCORRELATION TESTS ############################
#Main freq process function from real-time lib
def pre_proc_func(input_data):
	autocorrelation_time(input_data.copy())
	return input_data

def autocorrelation_time(input_data):
	global frame_counter
	global previous_time_frame
	for i in range(auto_frames,-1,-1):
		if(i==0): previous_time_frame[0]=input_data
		else:
			previous_time_frame[i-1]=previous_time_frame[i-2]

	total_buffer=[]
	for i in range(auto_frames):
		for j in range(num_samples):
			total_buffer.append(previous_time_frame[i][j])

	if(frame_counter%1000==0):
		x=[(frame_counter*num_samples)+i for i in range(auto_frames*num_samples)]
		figure()
		subplot(121)
		plot(x,total_buffer,"-x")
		title("Input signal (512 samples)")
		grid()
		subplot(122)
		plot(np.correlate(total_buffer,total_buffer,"full")[511:],"-*r")
		title("Autocorrelated signal")
		grid()
		show()
	frame_counter=frame_counter+1




####################### CROSS CORRELATION TESTS ############################
def freq_proc_func(freq_data):
	#correlation_frames(freq_data.copy())
	return freq_data

def correlation_frames(freq_data):
	global frame_counter
	global previous_freq_frame

	x=[freq_data[i]/128 for i in range(num_ch)]
	y=previous_freq_frame
	correlation=abs(np.correlate(x,y,"full"))

	if(frame_counter==3000): 
		figure()
		plot(abs(np.asarray([freq_data[i]/128 for i in range(num_ch)])),"-x")
		plot(abs(np.asarray(previous_freq_frame)),"-x")
		title("Current and previous frequency frames")
		grid()
		figure()
		plot(abs(correlation),"-x")
		title("Correlation between 2 frequency frames")
		grid()
	previous_freq_frame=x
	frame_counter=frame_counter+1
	corr_sum=np.asarray(num_corr)

####################### Calling ############################
wave_file_process("../Example Music/Speech Stereo.wav",progress_bar=True,nfft=256,zero_pad=False,stereo=False,pre_proc_func=pre_proc_func,freq_proc_func=freq_proc_func)
show()