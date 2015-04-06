#!/usr/bin/env python2
from __future__ import print_function

from open_bci_v3 import OpenBCIBoard
import numpy as np
import threading
import Queue
import atexit

# http://www.devshed.com/c/a/Python/Basic-Threading-in-Python/
# https://github.com/OpenBCI/OpenBCI_Python/blob/master/user.py

samples =  Queue.Queue(0)
waveforms = []
def handle_sample(sample):
	print(sample.id)
	samples.put(sample)

def classify_waveform(sensor_data):
	print("Classifying waveforms on sensors")
	#run an np.fft.rfft on it, since those're ideal for values that are only real
	# http://docs.scipy.org/doc/numpy/reference/generated/numpy.fft.rfft.html
	fftified = np.fft.rfft(sensor_data)
	for w in waveforms:
		# http://docs.scipy.org/doc/numpy/reference/generated/numpy.allclose.html#numpy-allclose
		if np.allclose(fftified, w):
			pass
		#check how similar the contents are by comparing with each waveform type
		#write the result to the serial for the cart board
		#optional: if we get a new sample, then we should discard our current data
		#          and try to re-evaluate with new data
	pass
	#return unknown here

#let's load up our wave form classificiations
def load_waveform_samples():
	print("Loading data for ideal waveforms like blinking")
	pass

class FFTBCIThread(threading.Thread):
	def __init__(self):
		self.sample_counter = 0
		threading.Thread.__init__(self)
		# placeholders since samples are per channel
		self.samples = ([], [], [], [], [], [], [], [])
		self.prev_id = -1
		#number of packets to collect before running an FFT
		self.max_packets = 1024

	def run(self):
		while True:
			sample = samples.get()
			if sample != None:
				if sample.id - self.prev_id > 1:
					print("Warning, packets may've been skipped!")
				self.prev_id = sample.id
				for i in xrange(8):
					self.samples[i].append(sample.channel_data[i])
				self.sample_counter += 1
				if self.sample_counter == self.max_packets:
					#analyse
					for i in xrange(8):
						result = classify_waveform(self.samples[i])
						# write this over serial
					for changather in self.samples:
						del changather[:]
					self.sample_counter = 0

load_waveform_samples()
# make flexible

board = OpenBCIBoard(port="/dev/ttyUSB0")
#board.print_register_settings()

atexit.register(board.disconnect)

# collect the data in a separate thread
# to prevent blocking
classifying_thread = FFTBCIThread()
classifying_thread.daemon = True
classifying_thread.start()

# handle grabbing board data on main thread
board.start_streaming(handle_sample)
