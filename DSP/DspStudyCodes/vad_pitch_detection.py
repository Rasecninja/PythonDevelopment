#################################################################################
#                                                                               #
#               VAD using Pitch Detection with Autocorrelation                  #
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
downsample_order=4	# Number of times for downsample
samples_frame=16  # Number of samples per frame
auto_frames=8 	  # Number of frames to accumulate
total_frame=[0]*(samples_frame*auto_frames) # Previous frame holder
frame_counter=0   # Counter for input frames
fs=44100	# Sampling frequency
previous_flag=0 # Save the previous frame flag
#Flag will only change if 10 (best value from tests) frames have the same state 
flag_tracker=10 # Check frames are noise or speech (0<Noise<10  10<Speech<20)
#Start as 1 to not update NR profile
vad_flag=1

####################### AUTOCORRELATION TESTS ############################
#Main freq process function from real-time lib
def pre_proc_func(input_data):
	return autocorrelation_time(input_data.copy())
	

def autocorrelation_time(input_data):
	global downsample_order
	global samples_frame
	global auto_frames
	global total_frame
	global frame_counter
	global fs
	global flag_tracker
	global vad_flag
	global previous_flag
	
	########## Calculating the Fundamental frequency ############
	#Calculate Autocorrelation
	auto_out=np.correlate(total_frame,total_frame,"full")
	#Retrive only second half
	auto_out_half=(auto_out[128:]).tolist()
	#Local variables
	valley_flag=0
	tao=0
	pitch=0
	current_flag=0
	#Checking the T value (index of autocorrelation for second peak)
	for i in range(1,len(auto_out_half)):
		if(auto_out_half[i]>auto_out_half[i-1]): valley_flag=1
		if((auto_out_half[i]<auto_out_half[i-1]) and valley_flag==1): 
			tao=i
			break
	#Checking pitch flag
	#If frame is empty (all zeros)
	if(tao==0):
		current_flag=0
	else:
		#Pitch=Sampling Frequency/ Tao index
		pitch=(fs/downsample_order)/tao
		#Human voice fundamental frequency range (best values in tests)
		if(pitch>80 and pitch<500):
			current_flag=1
		else: 
			current_flag=0

	############## Flag decision making ##################
	if(current_flag!=previous_flag):
		flag_tracker=10
	else:
		if(current_flag==0):
			if(flag_tracker>0):
				flag_tracker=flag_tracker-1
			else:
				vad_flag=0
		else:
			if(flag_tracker<20):
				flag_tracker=flag_tracker+1
			else:
				vad_flag=1

	########### Updating variables ##########	
	#Updating previous flag
	previous_flag=current_flag
	#Updating the current downsampled frame
	current_frame=[0]*samples_frame
	for i in range(samples_frame):
		current_frame[i]=input_data[downsample_order*i]
	#Updating the total frames buffer
	for i in range((samples_frame*auto_frames)-samples_frame):
		total_frame[i]=total_frame[i+samples_frame]
	for i in range(samples_frame):
		total_frame[-i]=current_frame[-i]

	# Updating frame counter
	frame_counter=frame_counter+1
	# VAD=1 (Output Bypass)  VAD=0 (Output zero)
	if(vad_flag==0): input_data=[0]*(samples_frame*downsample_order)
	return input_data


####################### Calling ############################
original_wav=wave_file_process("../Example Music/Male Speech Train 10dB SNR.wav",progress_bar=True,nfft=256,zero_pad=False,stereo=False,pre_proc_func=pre_proc_func,freq_proc_func=None)

data=np.asarray(original_wav, dtype=np.float32)

wav.write("Test.wav",44100,data)
