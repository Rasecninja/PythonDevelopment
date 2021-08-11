#################################################################################
#                                                                               #
#                        		 Mid-Side                                       #
#                                                                               #
#################################################################################

'''
	Mid-Side technique applied to Music
	- This technique is used to increase the stereo image
	- Increases or decreases the stereo image using the gain variable
	- Documentation shows the results

'''

################# Imports #########################
import math
import numpy as np
import scipy.io.wavfile as wav
import sys

#Importing files from different directory
sys.path.append('../Libraries')

from real_time_dsp import *

####################### Variables ############################
#MidSide gain  
gain=0.5

####################### Functions ############################
def sub_left_right(input_data):
	global gain
	left_data=input_data[0]
	right_data=input_data[1]
	output_left=[]
	output_right=[]
	side=0
	for i in range(len(left_data)):
		side=left_data[i]-right_data[i]
		output_left.append((1-gain)*left_data[i]+side*gain)
		output_right.append((1-gain)*right_data[i]-side*gain)
	output_data=[output_left,output_right]
	return output_data


####################### Calling ############################
wave_file_process("../ExampleMusic/Bad Guy Stereo.wav","Mid_side_out.wav",block_size=256,zero_pad=False,stereo=True,pre_proc_func=sub_left_right)
