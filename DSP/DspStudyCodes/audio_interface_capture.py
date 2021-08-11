
######### Testing audio capture from audio interface ###########

import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)


# Variables
device=(1,3)
samplerate=44100
blocksize=2048
latency="low"
channels=1


def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata*2
    # print(type(indata), indata.shape)
    # print("time.inputBufferAdcTime: ",time.inputBufferAdcTime,"time.outputBufferDacTime: ",time.outputBufferDacTime,"time.currentTime: ",time.currentTime )
    # print("frames: "+str(frames)+" indata len: "+str(len(indata))+" outdata len: "+str(len(outdata)))
    # print(indata[0:10],type(indata))
    print(len(indata))


with sd.Stream(device=device,
               samplerate=samplerate, blocksize=blocksize,
               dtype=None, latency=latency,
               channels=channels, callback=callback):
    print('#' * 80)
    print('press Return to quit')
    print('#' * 80)
    input()
