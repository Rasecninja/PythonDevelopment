#################################################################################
#                                                                               #
#                  NR using VAD flag to update noise profile                    #
#                                                                               #
#################################################################################

"""
------------------------------  VAD -------------------------------------------
  Uses the algorithm proposed by Bastian Rieck in 
  https://bastian.rieck.ru/blog/posts/2014/simple_experiments_speech_detection/
  This algorithm uses time domain approach with 3 variables:
  - Zero crossing rate
  - Short term energy
  - Entropy of energy
  I changed the original algorithm to downsample the original sampling frequency
  by 4 times. The frame total frame is 256 with every new frame of 16 samples.
  Also the subframes of entropy were changed to 16 to avoid division.
  The tuning parameters were set based on various samples.

------------------------------  NR -------------------------------------------
  Uses the algorithm described in Audacity documentation (Effect ->Noise Reduction)
  This algorithm uses a frequency domain approach. The main parts are:
  - Noise profiling
  - Decision making
  - Filtering and frequency smoothing
  The change from the original Audacity NR is that this code uses the VAD flag to
  update the noise profile instead of noise profile selected manually by the user.
  Also the profile will be averaged 2 times, one for short accumulation and then
  the longer accumulation. The long accumulation will retain previous noisy frames 
  data and it will update the noise profile slowly.
  Another change is that the noise profiling will start only if the VAD flag is 
  zero for over half a second.

"""

##################################### Imports #####################################
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

############################### Tuning Variables ####################################
########## NR #############
num_acc_frames=4 #Noise frames saved to get average 
short_num_acc_frames=32 #Noise frames that are accumulated to same buffer
sensitivity=4 #Increase or decrease noise profile
nr_gain_db=-18 #Value set by user (from 0dB to -30dB reduction)
num_non_speech_frames=350 #Number of noise frames need to start noise update

########## VAD #############
energy_threshold=0.0015 #Frame energy threshold
zcr_threshold=0.10 #Zero crossing rate threshold
entropy_threshold=4 #Energy entropy threshold


############################### General Variables ####################################
frame_counter=0   # Counter for input frames
########## VAD #############
downsample_order=4  # Number of times for downsample
samples_frame=16  # Number of samples per frame
acc_frames=8     # Number of frames to accumulate
total_frame=[0]*(samples_frame*acc_frames) # Previous frame holder
previous_flag=0 # Save the previous frame flag
#Flag will only change if 10 (best value from tests) frames have the same state 
flag_tracker=10 # Check frames are noise or speech (0<Noise<10  10<Speech<20)
#Start as 1 to not update NR profile
vad_flag=1
########## NR #############
freq_frame_size=129 #Freq domain frame
nr_gain=10**(nr_gain_db/20) #Convert to amplitude
num_previous_input_frames=3
#Buffers
previous_input_frames=[0]*(freq_frame_size*num_previous_input_frames)
noise_profile=[0]*freq_frame_size 
short_acc_frames=[0]*freq_frame_size
previous_noise_frames=[0]*(freq_frame_size*num_acc_frames)
#Counters
short_frames_counter=0
non_speech_counter=0

###################################### Main ######################################
def pre_proc_func(input_data):
  speech_detection(input_data.copy())
  return input_data

def freq_proc_func(input_data):
  return noise_reduction(input_data.copy())

def noise_reduction(input_data):
  global num_acc_frames
  global short_num_acc_frames
  global sensitivity
  global nr_gain_db
  global freq_frame_size
  global nr_gain
  global noise_profile
  global short_acc_frames
  global previous_noise_frames
  global short_frames_counter
  global non_speech_counter
  global vad_flag
  global num_non_speech_frames
  global previous_input_frames
  global frame_counter
  # Update frame counter
  frame_counter=frame_counter+1
  ############### Noise Profiling #############
  #Noise frame detected
  if(vad_flag==0):
    non_speech_counter=non_speech_counter+1
    #Noise ready to be updated
    if(non_speech_counter>=num_non_speech_frames):
      #Check if short frame accumation is ready
      if(short_frames_counter<short_num_acc_frames):
        #Accumulate short frame
        for i in range(freq_frame_size):
          short_acc_frames[i]=short_acc_frames[i]+(abs(input_data[i])/short_num_acc_frames)
        #Update short frame counter
        short_frames_counter=short_frames_counter+1
      #Short accumulation done, read to update profile
      else:
        #Reset short frame accumulation counter
        short_frames_counter=0
        #Update the noise profile by one average
        for i in range(len(previous_noise_frames)-freq_frame_size):
          previous_noise_frames[i]=previous_noise_frames[i+freq_frame_size]
        #Add the new short frame to the noise accumulation buffer
        for i in range(freq_frame_size):
          previous_noise_frames[i+((num_acc_frames-1)*freq_frame_size)]=short_acc_frames[i]
          #Cleaning the short accumulation buffer
          short_acc_frames[i]=0
          #cleaning noise profile before update
          noise_profile[i]=0
        #Updating noise profile
        for i in range(freq_frame_size):
          for j in range(num_acc_frames):
            noise_profile[i]=noise_profile[i]+(previous_noise_frames[i+(j*freq_frame_size)]/num_acc_frames)
  #If speech frame reset non speech counter and clean the short frame accumulator
  else: 
    non_speech_counter=0
    short_frames_counter=0
    for i in range(freq_frame_size): short_acc_frames[i]=0

  ############### Decision Making #############
  #Updating the input data holder buffer
  for i in range(len(previous_input_frames)-freq_frame_size):
    previous_input_frames[i]=previous_input_frames[i+freq_frame_size]
  for i in range(freq_frame_size):
    previous_input_frames[i+(2*freq_frame_size)]=abs(input_data[i])
  #Buffer with gains
  gain_buffer=[0]*freq_frame_size
  for i in range(freq_frame_size):
    #Finding the input frames median for each bin
    median=find_median(previous_input_frames[i+(2*freq_frame_size)],previous_input_frames[i+freq_frame_size],previous_input_frames[i])
    #Check if input signal is below or above noise level
    if(median<=noise_profile[i]*sensitivity): gain_buffer[i]=nr_gain #noisy bin (apply negative gain)
    else: gain_buffer[i]=1 #speech bin (0dB gain)

  ############### Frequency Smoothing #############
  # 2 bands smoothing
  for i in range(freq_frame_size-1): #last sample does not apply smoothing
    gain_buffer[i]=(gain_buffer[i]+gain_buffer[i+1])/2

  #Applying gain to input buffer
  output_data=array_multiply(input_data,gain_buffer)

  #Output filtered data
  return output_data

def speech_detection(input_data):
  global downsample_order
  global samples_frame
  global acc_frames
  global total_frame
  global flag_tracker
  global vad_flag
  global previous_flag
  global energy_threshold
  global zcr_threshold
  global entropy_threshold
  ############### Speech recognition algorithm ##########
  counter=0
  current_flag=0
  energy = rateSampleByEnergy(total_frame)
  zcr       = rateSampleByCrossingRate(total_frame)
  entropy   = rateSampleByEntropy(total_frame)
  # Checking threshold values
  if energy >= energy_threshold: counter=counter+1
  if  zcr >= zcr_threshold: counter=counter+1
  if entropy < entropy_threshold: counter=counter+1
  # Only if all values are true VAD flag is true
  if counter>2: current_flag=1
  ############## Flag decision making ##################
  # Check previous flags
  if(current_flag!=previous_flag):
    flag_tracker=10
  # Only change status if continuous 10 frames
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


############################### Helper functions ###################################
########## VAD #############
def chunks(l, k):
  for i in range(0, len(l), k):
    yield l[i:i+k]

def shortTermEnergy(frame):
  return sum( [ abs(x)**2 for x in frame ] ) / len(frame)

def rateSampleByEnergy(frame):
  energy = shortTermEnergy(frame)
  return energy

def zeroCrossingRate(frame):
  signs             = numpy.sign(frame)
  signs[signs == 0] = -1
  return len(numpy.where(numpy.diff(signs))[0])/len(frame)

def rateSampleByCrossingRate(frame):
  zcr = zeroCrossingRate(frame) 
  return zcr

def entropyOfEnergy(frame, numSubFrames):
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
  entropy = entropyOfEnergy(frame, 16)
  return entropy

########## NR #############
def find_median(in1,in2,in3):
  val=0
  if(in1>in2):
    if(in2>in3): val=in2
    else: val=in3
  else:
    if(in1>in3): val=in1
    else: val=in2
  return val

def array_multiply(in1,in2):
  out=[0]*len(in1)
  for i in range(len(in1)):
    out[i]=in1[i]*in2[i]
  return out

  

################################################### Calling ################################################
wave_file_process("../ExampleMusic/Female Speech Office 15dB SNR.wav",
                  "NR_with_VAD.wav",
                  progress_bar=True,
                  block_size=64,
                  zero_pad=False,
                  stereo=False,
                  pre_proc_func=pre_proc_func,
                  freq_proc_func=freq_proc_func)

# real_time_stream(device=(1,3),
#          samplerate=16000,
#          stereo=False,
#          overlap=75,
#          block_size=64,
#          zero_pad=False,
#          pre_proc_func=pre_proc_func,
#          freq_proc_func=freq_proc_func)
