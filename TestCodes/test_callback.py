##################################################################################################
#                                                                                                #
#                                 Real time DSP process Lib                                      #
#                                                                                                #
##################################################################################################

''' 
    Real time capture and reproduction of audio using SoundDevice Lib

'''

import sounddevice as sd
import numpy as np  # Make sure NumPy is loaded before it is used in the callback
# assert numpy  # avoid "imported but unused" message (W0611)


# Variables
class _RealTimeStreamParams:
    #User input data
    device=(1,3)
    samplerate=44100
    stereo=True
    overlap=75
    block_size=128
    zero_pad=True
    pre_proc_func=None
    freq_proc_func=None
    post_proc_func=None
    #Wola static data
    windowed_frame_left=[0]
    windowed_frame_right=[0]
    input_frames_left=[0]
    input_frames_right=[0]

RealTimeStreamInstance=_RealTimeStreamParams()


def real_time_stream(device=(1,3),
                    samplerate=44100,
                    stereo=True,
                    overlap=75,
                    block_size=128,
                    zero_pad=True,
                    pre_proc_func=None,
                    freq_proc_func=None,
                    post_proc_func=None): 
    print('#' * 80)
    print("#                           Real Time Stream                                   #") 
    global RealTimeStreamInstance
    RealTimeStreamInstance.pre_proc_func=pre_proc_func
    channels=0
    if(stereo): channels=2
    else: channels=1
    with sd.Stream(device=device,
                   samplerate=samplerate, blocksize=block_size,
                   dtype=None, latency="low",
                   channels=channels, callback=callback):
        print('#' * 80)
        print('press Return to quit')
        print('#' * 80)
        input()


def callback(indata, outdata, frames, time, status):
    global RealTimeStreamInstance

    input_left=[indata[i][0] for i in range(indata.shape[0])]
    input_right=[indata[i][1] for i in range(indata.shape[0])]

    # print(indata,type(indata),indata.shape)
    # x=np.vstack((input_left,input_left)).T
    # print(x,type(x),x.shape)

    output_left,output_right=RealTimeStreamInstance.pre_proc_func(input_left,input_right)

    left=np.asarray(output_left, dtype=np.float32)
    right=np.asarray(output_right, dtype=np.float32)
    data=np.vstack((left, right)).T



    outdata[:] = data
    # if status:
        # print(status)
    # print(type(indata), indata.shape[0],indata.shape[1])
    # print(left)
    # print(type(left),type(left[0]))
    # print("time.inputBufferAdcTime: ",time.inputBufferAdcTime,"time.outputBufferDacTime: ",time.outputBufferDacTime,"time.currentTime: ",time.currentTime )
    # print("frames: "+str(frames)+" indata len: "+str(len(indata))+" outdata len: "+str(len(outdata)))
    # print(indata[0:10],type(indata))
    # print(len(indata))




