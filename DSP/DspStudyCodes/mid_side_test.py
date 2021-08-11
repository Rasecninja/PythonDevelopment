#################################################################################
#                                                                               #
#                         Mid-Side tests code                                   #
#                                                                               #
#################################################################################

################# Imports #########################
import math
import numpy as np
import scipy.io.wavfile as wav
import sys

#Importing files from different directory
sys.path.append('../Libraries')

from real_time_dsp import *

####################### Variables ############################
#Sample frequency of the original wav file
fs=44100
#MidSide gain  
gain=0.5

####################### Functions ############################
#Time domain
# def sub_left_right(left_data,right_data):
# 	global frame
# 	global gain
# 	frame+=1
# 	print_progress(frame, total_frames, decimals = 0, barLength = 50)
# 	output_left=[]
# 	output_right=[]
# 	side=0
# 	for i in range(len(left_data)):
# 		side=left_data[i]-right_data[i]
# 		output_left.append((1-gain)*left_data[i]+side*gain)
# 		output_right.append((1-gain)*right_data[i]-side*gain)
# 		# output_left.append(left_data[i]+side*gain)
# 		# output_right.append(right_data[i]-side*gain)
# 	return output_left,output_right

def sub_left_right(left_data,right_data):
	global gain
	output_left=[]
	output_right=[]
	side=0
	for i in range(len(left_data)):
		side=left_data[i]-right_data[i]
		output_left.append((1-gain)*left_data[i]+side*gain)
		output_right.append((1-gain)*right_data[i]-side*gain)
		# output_left.append(left_data[i]+side*gain)
		# output_right.append(right_data[i]-side*gain)
	return output_left,output_right


####################### Calling ############################
# left_in,right_in=wave_file_process("../Example Music/Bad Guy Stereo.wav",nfft=1024,stereo=True,pre_proc_func=sub_left_right)
# left=np.asarray(left_in, dtype=np.float32)
# right=np.asarray(right_in, dtype=np.float32)
# data=np.vstack((left, right)).T
# wav.write("test_out.wav",fs,data)

wave_file_process("../Example Music/Bad Guy Stereo.wav","Mid_side_out.wav",block_size=256,zero_pad=False,stereo=True,pre_proc_func=sub_left_right)