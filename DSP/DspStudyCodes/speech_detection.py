#!/usr/bin/env python3
#
# Released under the HOT-BEVERAGE-OF-MY-CHOICE LICENSE: Bastian Rieck wrote
# this script. As long you retain this notice, you can do whatever you want
# with it. If we meet some day, and you feel like it, you can buy me a hot
# beverage of my choice in return.

################# Imports #########################
import numpy
import scipy.io.wavfile
import scipy.stats
import sys
import math
import scipy.io.wavfile as wav
from pylab import *

#Importing files from different directory
sys.path.append('../Libraries')

from real_time_dsp import *

####################### Variables ############################
downsample_order=4  # Number of times for downsample
samples_frame=16  # Number of samples per frame
acc_frames=8     # Number of frames to accumulate
total_frame=[0]*(samples_frame*acc_frames) # Previous frame holder
frame_counter=0   # Counter for input frames
previous_flag=0 # Save the previous frame flag
#Flag will only change if 10 (best value from tests) frames have the same state 
flag_tracker=10 # Check frames are noise or speech (0<Noise<10  10<Speech<20)
#Start as 1 to not update NR profile
vad_flag=1


####################### Helper functions ############################
def chunks(l, k):
  """
  Yields chunks of size k from a given list.
  """
  for i in range(0, len(l), k):
    yield l[i:i+k]

def shortTermEnergy(frame):
  """
  Calculates the short-term energy of an audio frame. The energy value is
  normalized using the length of the frame to make it independent of said
  quantity.
  """
  return sum( [ abs(x)**2 for x in frame ] ) / len(frame)

def rateSampleByVariation(frame):
  """
  Rates an audio sample using the coefficient of variation of its short-term
  energy.
  """
  energy = shortTermEnergy(frame)
  return energy
  # return scipy.stats.variation(energy)

def zeroCrossingRate(frame):
  """
  Calculates the zero-crossing rate of an audio frame.
  """
  signs             = numpy.sign(frame)
  signs[signs == 0] = -1

  return len(numpy.where(numpy.diff(signs))[0])/len(frame)

def rateSampleByCrossingRate(frame):
  """
  Rates an audio sample using the standard deviation of its zero-crossing rate.
  """
  zcr = zeroCrossingRate(frame) 
  return zcr
  # return numpy.std(zcr)

def entropyOfEnergy(frame, numSubFrames):
  """
  Calculates the entropy of energy of an audio frame. For this, the frame is
  partitioned into a number of sub-frames.
  """
  lenSubFrame = int(numpy.floor(len(frame) / numSubFrames))
  shortFrames = list(chunks(frame, lenSubFrame))
  energy      = [ shortTermEnergy(s) for s in shortFrames ]
  totalEnergy = sum(energy)
  energy      = [ e / totalEnergy for e in energy ]

  entropy = 0.0
  for e in energy:
    if e != 0:
      entropy = entropy - e * numpy.log2(e)

  return entropy

def rateSampleByEntropy(frame):
  """
  Rates an audio sample using its minimum entropy.
  """
  entropy = entropyOfEnergy(frame, 16)
  return entropy
  # return numpy.min(entropy)

####################### Main ############################

def pre_proc_func(input_data):
  return speech_detection(input_data.copy())


def speech_detection(input_data):
  global downsample_order
  global samples_frame
  global acc_frames
  global total_frame
  global frame_counter
  global flag_tracker
  global vad_flag
  global previous_flag
  
  ############### Speech recognition algorithm ##########
  counter=0
  current_flag=0
  variation = rateSampleByVariation(total_frame)
  zcr       = rateSampleByCrossingRate(total_frame)
  entropy   = rateSampleByEntropy(total_frame)

  # print("variation: ",variation)
  # print("zcr: ",zcr)
  # print("entropy: ",entropy)

  # Original values
  # if variation >= 1.0: counter=counter+1
  # if  zcr >= 0.05: counter=counter+1
  # if entropy < 2.5: counter=counter+1

  # First tuning 
  # if variation >= 0.002: counter=counter+1
  # if  zcr >= 0.2: counter=counter+1
  # if entropy < 4: counter=counter+1

  # Second tunning 
  # if variation >= 0.0015: counter=counter+1
  # if  zcr >= 0.1: counter=counter+1
  # if entropy < 4: counter=counter+1

  # Last tuning
  if variation >= 0.0015: counter=counter+1
  if  zcr >= 0.10: counter=counter+1
  if entropy < 4: counter=counter+1

  if counter>2: current_flag=1

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
  for i in range((samples_frame*acc_frames)-samples_frame):
    total_frame[i]=total_frame[i+samples_frame]
  for i in range(samples_frame):
    total_frame[-i]=current_frame[-i]

  # Updating frame counter
  frame_counter=frame_counter+1
  # VAD=1 (Output Bypass)  VAD=0 (Output zero)
  if(vad_flag==0): input_data=[0]*(samples_frame*downsample_order)
  return input_data


####################### Calling ############################
original_wav=wave_file_process("../Example Music/Female Speech Train 5dB SNR.wav",progress_bar=True,nfft=256,zero_pad=False,stereo=False,pre_proc_func=pre_proc_func,freq_proc_func=None)

data=np.asarray(original_wav, dtype=np.float32)

wav.write("Test.wav",44100,data)