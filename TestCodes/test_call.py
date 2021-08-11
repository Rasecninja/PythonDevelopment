import math
import numpy as np
import scipy.io.wavfile as wav
from scipy import signal
import sys

# from test_callback import *
sys.path.append('../Libraries')
from real_time_dsp import *

# data=wave_file_process("../ExampleMusic/Clean Male Speech Stereo.wav",True)
# print(data)

# def pre_proc_func(left,right):
# 	print("\n\n\n\n",left)
# 	print("\n\n\n\n",right)
# 	# for i in range(100):
# 	# 	np.fft.fft(input_data)
# 	return left,right



# real_time_stream(device=(1,3),
# 				 samplerate=16000,
# 				 stereo=True,
# 				 overlap=75,
# 				 block_size=576,
# 				 zero_pad=True,
# 				 pre_proc_func=None,
# 				 freq_proc_func=None,
# 				 post_proc_func=None)

wave_file_process(in_file_name="../ExampleMusic/Bad Guy Stereo.wav",
                      out_file_name="outfile.wav",
                      progress_bar=True,
                      stereo=False,
                      overlap=75,
                      block_size=128,
                      zero_pad=True,
                      pre_proc_func=None,
                      freq_proc_func=None,
                      post_proc_func=None)

# class rtparams:
# 	a=0
# 	b=10
# 	c=[1,2,3]

# rtinstance=rtparams()

# def test():
# 	pass

# def change():
# 	global rtinstance

# 	print(rtinstance.a)
# 	rtinstance.a=[0]*10
# 	print(rtinstance.a)
# 	rtinstance.b=0
# 	print(rtinstance.b)
# 	rtinstance.c=test

# print(rtinstance.a)

# print(rtinstance.b)

# change()

# print(rtinstance.a)

# print(rtinstance.b)

# print(rtinstance.c)