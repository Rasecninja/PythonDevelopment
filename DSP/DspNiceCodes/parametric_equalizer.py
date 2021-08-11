#################################################################################
#                                                                               #
#                    Parametric EQ with cascaded IIR filters                    #
#                                                                               #
#################################################################################

"""
--------------------   The Parametric EQ Algorithm   -------------------------
  Implements 2 types of order 2 IIR filters:
  
  - Shelf filter
  	Filter that can boost or cut the corners of the frequency band. It can be
	applied to the low or high corner.
	Inputs:
	- fs: sample frequency
	- fc: cut-off frequency
	- gain: filter gain in dB (positive or negative)
	- f_type: low or high (accepts only "LP" and "HP")
  
  - Peak filter
  	Similar to narrow band pass, this filter can boost or cut a specific band
	determined by Q factor
	Inputs: 
	- fs: sample frequency
	- fc: cut-off frequency
	- gain: filter gain in dB (positive or negative)
	- Q: makes the filter band wide (small values) or narrow (large values)
  
  The filters are cascaded in order to form a multi-band EQ. There can be only
  2 shelf filter (low and high) but the number of peak filters is up to user.

  The time domain filter have the advantage of variable bandwith and also
  are resistant to input buffer size. That means even for variable input
  buffer size for every frame this EQ will work normally.
  
"""

################################ Imports #####################################
from math import pi
from math import tan
from math import sqrt
#Importing files from different directory
import sys
sys.path.append('../Libraries')
from real_time_dsp import *


############################# The coeficients struct #############################
class Coeficients:
	def __init__(self):
		self.b0=0.0
		self.b1=0.0
		self.b2=0.0
		self.a1=0.0
		self.a2=0.0

###########################  Coeficients class #############################
#Shelf Coeficients class
class ShelfCoeficients:
	def __init__(self,g_type="boost",K=0.5,Vo=1.0,f_type="LP"):
		self._g_type=g_type
		self._K=K
		self._Vo=Vo
		self._f_type=f_type
		self.coeficients=Coeficients()
		self._set_coef()

	def _set_coef(self):
		self.coeficients=Coeficients()
		if(self._f_type=="LP"):
			if(self._g_type=="boost"):
				self.coeficients.b0=(1+sqrt(2*self._Vo)*self._K+self._Vo*(self._K**2))/(1+sqrt(2)*self._K+self._K**2)
				self.coeficients.b1=(2*(self._Vo*(self._K**2)-1))/(1+sqrt(2)*self._K+self._K**2)
				self.coeficients.b2=(1-sqrt(2*self._Vo)*self._K+self._Vo*(self._K**2))/(1+sqrt(2)*self._K+self._K**2)
				self.coeficients.a1=(2*((self._K**2)-1))/(1+sqrt(2)*self._K+self._K**2)
				self.coeficients.a2=(1-sqrt(2)*self._K+(self._K**2))/(1+sqrt(2)*self._K+self._K**2)
			elif(self._g_type=="cut"):
				self.coeficients.b0=(self._Vo*(1+sqrt(2)*self._K+(self._K**2)))/(self._Vo+sqrt(2*self._Vo)*self._K+(self._K**2))
				self.coeficients.b1=(2*self._Vo*((self._K**2)-1))/(self._Vo+sqrt(2*self._Vo)*self._K+(self._K**2))
				self.coeficients.b2=(self._Vo*(1-sqrt(2)*self._K+(self._K**2)))/(self._Vo+sqrt(2*self._Vo)*self._K+(self._K**2))
				self.coeficients.a1=(2*((self._K**2)-self._Vo))/(self._Vo+sqrt(2*self._Vo)*self._K+(self._K**2))
				self.coeficients.a2=(self._Vo-sqrt(2*self._Vo)*self._K+(self._K**2))/(self._Vo+sqrt(2*self._Vo)*self._K+(self._K**2))
		elif(self._f_type=="HP"):
			if(self._g_type=="boost"):
				self.coeficients.b0=(self._Vo+sqrt(2*self._Vo)*self._K+(self._K**2))/(1+sqrt(2)*self._K+(self._K**2))
				self.coeficients.b1=(2*((self._K**2)-self._Vo))/(1+sqrt(2)*self._K+(self._K**2))
				self.coeficients.b2=(self._Vo-sqrt(2*self._Vo)*self._K+(self._K**2))/(1+sqrt(2)*self._K+(self._K**2))
				self.coeficients.a1=(2*((self._K**2)-1))/(1+sqrt(2)*self._K+(self._K**2))
				self.coeficients.a2=(1-sqrt(2)*self._K+(self._K**2))/(1+sqrt(2)*self._K+(self._K**2))
			elif(self._g_type=="cut"):
				self.coeficients.b0=(self._Vo*(1+sqrt(2)*self._K+(self._K**2)))/(1+sqrt(2*self._Vo)*self._K+self._Vo*(self._K**2))
				self.coeficients.b1=(2*self._Vo*((self._K**2)-1))/(1+sqrt(2*self._Vo)*self._K+self._Vo*(self._K**2))
				self.coeficients.b2=(self._Vo*(1-sqrt(2)*self._K+(self._K**2)))/(1+sqrt(2*self._Vo)*self._K+self._Vo*(self._K**2))
				self.coeficients.a1=(2*(self._Vo*(self._K**2)-1))/(1+sqrt(2*self._Vo)*self._K+self._Vo*(self._K**2))
				self.coeficients.a2=(1-sqrt(2*self._Vo)*self._K+self._Vo*(self._K**2))/(1+sqrt(2*self._Vo)*self._K+self._Vo*(self._K**2))

#Peak Coeficients class
class PeakCoeficients:
	def __init__(self,g_type="boost",K=0.5,Vo=1.0,Q=1.0):
		self._g_type=g_type
		self._K=K
		self._Vo=Vo
		self._Q=Q
		self._set_coef()

	def _set_coef(self):
		self.coeficients=Coeficients()
		if(self._g_type=="boost"):
			self.coeficients.b0=(1+(self._Vo/self._Q)*self._K+(self._K**2))/(1+(1/self._Q)*self._K+(self._K**2))
			self.coeficients.b1=(2*((self._K**2)-1))/(1+(1/self._Q)*self._K+(self._K**2))
			self.coeficients.b2=(1-(self._Vo/self._Q)*self._K+(self._K**2))/(1+(1/self._Q)*self._K+(self._K**2))
			self.coeficients.a1=(2*((self._K**2)-1))/(1+(1/self._Q)*self._K+(self._K**2))
			self.coeficients.a2=(1-(1/self._Q)*self._K+(self._K**2))/(1+(1/self._Q)*self._K+(self._K**2))
		elif(self._g_type=="cut"):
			self.coeficients.b0=(1+(1/self._Q)*self._K+(self._K**2))/(1+(1/(self._Vo*self._Q))*self._K+(self._K**2))
			self.coeficients.b1=(2*((self._K**2)-1))/(1+(1/(self._Vo*self._Q))*self._K+(self._K**2))
			self.coeficients.b2=(1-(1/self._Q)*self._K+(self._K**2))/(1+(1/(self._Vo*self._Q))*self._K+(self._K**2))
			self.coeficients.a1=(2*((self._K**2)-1))/(1+(1/(self._Vo*self._Q))*self._K+(self._K**2))
			self.coeficients.a2=(1-(1/(self._Vo*self._Q))*self._K+(self._K**2))/(1+(1/(self._Vo*self._Q))*self._K+(self._K**2))

###########################  Filters class #############################
#Filter used in the corner of frequency range
class ShelfFilter:
	#Called when the instance is created
	def __init__(self,fs=48000,fc=1000,gain=-12,f_type="LP"):
		self._fs=fs
		self._fc=fc
		self._gain=gain
		self._f_type=f_type
		self._previous_input_samples=[0]*2  #y[n]=b0x[n]+b1x[n-1]+b2x[n-2]-a1y[n-1]-a2y[n-2]
		self._previous_output_samples=[0]*2
		self._coeficients=Coeficients()
		self._get_coef()

	@property
	def coeficients(self):
		b=[self._coeficients.b0,self._coeficients.b1,self._coeficients.b2]
		a=[1,self._coeficients.a1,self._coeficients.a2]
		return b,a

	#Called when the class object is called like an function
	def __call__(self,input_data):
		self._input_data=input_data.copy()
		self._output_data=self._apply_filter()
		self._update_previous_samples()
		return(self._output_data)

	#Apply the filter to input data
	def _apply_filter(self):
		#Assign class variables to local variable
		b=[self._coeficients.b0,self._coeficients.b1,self._coeficients.b2]
		a=[1,self._coeficients.a1,self._coeficients.a2]
		#Output local array
		output=[]
		for n in range(len(self._input_data)):
			#FF and FB values holder
			Feedback=0
			Feedforward=0
			#Calculating the Feedback values
			for i in range(1,len(a)):
				#Check if the previous output frame data is used 
				if(n-i<0): Feedback=Feedback-(a[i]*self._previous_output_samples[-i+n])
				#If n>len(a)-1 then only current output frame data is used
				else: Feedback=Feedback-(a[i]*output[n-i])
			#Calculating the Feedforward values
			for i in range(len(b)):
				#Check if the previous input frame data is used 
				if(n-i<0): Feedforward=Feedforward+(b[i]*self._previous_input_samples[-i+n])
				#If n>len(b)-1 then only current input frame data is used
				else: Feedforward=Feedforward+(b[i]*self._input_data[n-i])	
			output.append((Feedforward+Feedback)/a[0])
		return output

	#Update the previous samples buffers
	def _update_previous_samples(self):\
		#Updating feedback buffers
		self._previous_output_samples[0]=self._output_data[-2]
		self._previous_output_samples[1]=self._output_data[-1]
		#Updating feedforward buffers
		self._previous_input_samples[0]=self._input_data[-2]
		self._previous_input_samples[1]=self._input_data[-1]

	#Private setter for the coeficients
	def _get_coef(self):
		#Check if filter is boost or cut type
		self._g_type="boost"
		if(self._gain<0): self._g_type="cut"
		#Calculates the K value
		self._K=tan(pi*(self._fc/self._fs))
		#Calculates the gain in amplitude from dB value
		self._Vo=10**(self._gain/20)
		#Getting the coeficients
		self._shelf_coef=ShelfCoeficients(self._g_type,self._K,self._Vo,self._f_type)
		self._coeficients=self._shelf_coef.coeficients

#Filter used in middle of frequency range
class PeakFilter:
	#Called when the instance is created
	def __init__(self,fs=48000,fc=1000,gain=-12,Q=1.0):
		self._fs=fs
		self._fc=fc
		self._gain=gain
		self._Q=Q
		self._previous_input_samples=[0]*2  #y[n]=b0x[n]+b1x[n-1]+b2x[n-2]-a1y[n-1]-a2y[n-2]
		self._previous_output_samples=[0]*2
		self._coeficients=Coeficients()
		self._get_coef()
	
	@property
	def coeficients(self):
		b=[self._coeficients.b0,self._coeficients.b1,self._coeficients.b2]
		a=[1,self._coeficients.a1,self._coeficients.a2]
		return b,a

	#Called when the class object is called like an function
	def __call__(self,input_data):
		self._input_data=input_data.copy()
		self._output_data=self._apply_filter()
		self._update_previous_samples()
		return(self._output_data)

	#Apply the filter to input data
	def _apply_filter(self):
		#Assign class variables to local variable
		b=[self._coeficients.b0,self._coeficients.b1,self._coeficients.b2]
		a=[1,self._coeficients.a1,self._coeficients.a2]
		#Output local array
		output=[]
		for n in range(len(self._input_data)):
			#FF and FB values holder
			Feedback=0
			Feedforward=0
			#Calculating the Feedback values
			for i in range(1,len(a)):
				#Check if the previous output frame data is used 
				if(n-i<0): Feedback=Feedback-(a[i]*self._previous_output_samples[-i+n])
				#If n>len(a)-1 then only current output frame data is used
				else: Feedback=Feedback-(a[i]*output[n-i])
			#Calculating the Feedforward values
			for i in range(len(b)):
				#Check if the previous input frame data is used 
				if(n-i<0): Feedforward=Feedforward+(b[i]*self._previous_input_samples[-i+n])
				#If n>len(b)-1 then only current input frame data is used
				else: Feedforward=Feedforward+(b[i]*self._input_data[n-i])	
			output.append((Feedforward+Feedback)/a[0])
		return output

	#Update the previous samples buffers
	def _update_previous_samples(self):
		#Updating feedback buffers
		self._previous_output_samples[0]=self._output_data[-2]
		self._previous_output_samples[1]=self._output_data[-1]
		#Updating feedforward buffers
		self._previous_input_samples[0]=self._input_data[-2]
		self._previous_input_samples[1]=self._input_data[-1]
		
	#Private setter for the coeficients
	def _get_coef(self):
		#Check if filter is boost or cut type
		self._g_type="boost"
		if(self._gain<0): self._g_type="cut"
		#Calculates the K value
		self._K=tan(pi*(self._fc/self._fs))
		#Calculates the gain in amplitude from dB value
		self._Vo=10**(self._gain/20)
		#Getting the coeficients
		self._peak_coef=PeakCoeficients(self._g_type,self._K,self._Vo,self._Q)
		self._coeficients=self._peak_coef.coeficients


###########################  Creating the Filters  #############################
#Sampling frequency is the same for all filters
fs=44100
#High shelf filter instance
HPShelf=ShelfFilter(fs=fs,fc=15000,gain=-6,f_type="HP")
#Low shelf filter instance
LPShelf=ShelfFilter(fs=fs,fc=40,gain=6,f_type="LP")
# First peak filter instance
MidPeak1=PeakFilter(fs=fs,fc=2000,gain=6,Q=10.0)
# Second peak filter instance
MidPeak2=PeakFilter(fs=fs,fc=400,gain=6,Q=0.5)
# Third peak filter instance
MidPeak3=PeakFilter(fs=fs,fc=6000,gain=-3,Q=5.0)

###########################  Applying to signal  #############################
#Getting coeficients using decorators
b,a=HPShelf.coeficients
print("High Shelf Filter Coeficients")
print("b=",b)
print("a=",a)

#Calling real time process lib
def pre_proc_func(input_data):
	#Return the cascaded filters instances call method
	return MidPeak3(MidPeak2(MidPeak1(HPShelf(LPShelf(input_data)))))

wave_file_process("../ExampleMusic/White Noise.wav",
					"ParametricEQ.wav",
					progress_bar=True,
					block_size=128,
					zero_pad=False,
					stereo=False,
					pre_proc_func=pre_proc_func)









		


