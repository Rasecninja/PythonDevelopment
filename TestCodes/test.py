import curses
import math
import numpy as np
import scipy.io.wavfile as wav
from scipy import signal
import sys

# from test_callback import *
sys.path.append('../Libraries')
from real_time_dsp import *


screen = curses.initscr()
num_rows, num_cols = screen.getmaxyx()

screen.nodelay(1)
curses.noecho()
# curses.halfdelay(1)


# screen.addstr("#"*(num_cols*num_rows))
screen.addstr("#"*10)
screen.refresh()
curses.napms(2000)



def drawVline(start,size,charact):
    for i in range(size):
        screen.addch(start[0]+i,start[1],charact)
    screen.refresh()

def drawInVline(start,size,charact):
    for i in range(size):
        screen.addch(start[0]-i,start[1],charact)
    screen.refresh()

def drawHline(start,size,charact):
    for i in range(size):
        screen.addch(start[0],start[1]+i,charact)
    screen.refresh()

def drawspect(input_data):
    size=0
    if(num_cols>len(input_data)): size=len(input_data)
    else: size=num_cols

    # c=screen.getch()
    # if(c):
    #     screen.clear()
    #     curses.endwin()

    for i in range(size):
        val=20*math.log10(abs(input_data[i])/len(input_data*2))
        num=int((val+96)/3)   #Assume 10 rows and input normalized to 1
        if(num>30): num=30
        drawInVline((30,i),num,"#")

# def freq_proc_func(input_data):
#     screen.clear()
#     drawspect(input_data.copy())
#     return (np.zeros(len(input_data)))

# # wave_file_process(in_file_name="../ExampleMusic/Bad Guy Stereo.wav",
# #                       progress_bar=False,
# #                       stereo=False,
# #                       overlap=75,
# #                       block_size=128,
# #                       zero_pad=True,
# #                       pre_proc_func=None,
# #                       freq_proc_func=freq_proc_func,
# #                       post_proc_func=None)

# real_time_stream(device=(1,3),
#          samplerate=16000,
#          stereo=False,
#          overlap=75,
#          block_size=64,
#          zero_pad=False,
#          pre_proc_func=None,
#          freq_proc_func=freq_proc_func)



