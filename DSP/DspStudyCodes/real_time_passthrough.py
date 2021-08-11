##################################################################################################
#                                                                                                #
#                                 Real time DSP process Lib                                      #
#                                                                                                #
##################################################################################################

''' 
    Real time capture and reproduction of audio using SoundDevice Lib

'''

import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback
# assert numpy  # avoid "imported but unused" message (W0611)


# Variables
device=(1,3)
samplerate=48000
blocksize=64
latency="low"
channels=1



# def real_time_stream(device=(1,3),samplerate=44100,stereo=True,overlap=75,nfft=1024,zero_pad=True,pre_proc_func=None,freq_proc_func=None,post_proc_func=None):
    


def _callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata*2
    a=0
    for i in range(100):
        numpy.fft.fft(indata)
    # print(type(indata), indata.shape)
    # print("time.inputBufferAdcTime: ",time.inputBufferAdcTime,"time.outputBufferDacTime: ",time.outputBufferDacTime,"time.currentTime: ",time.currentTime )
    # print("frames: "+str(frames)+" indata len: "+str(len(indata))+" outdata len: "+str(len(outdata)))
    # print(indata[0:10],type(indata))
    print(len(indata))


with sd.Stream(device=device,
               samplerate=samplerate, blocksize=blocksize,
               dtype=None, latency=latency,
               channels=channels, callback=_callback):
    print('#' * 80)
    print('press Return to quit')
    print('#' * 80)
    input()

