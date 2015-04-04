# OpenBCI EEG Classifier
Runs in the background comparing waveforms across each of the sensors to samples from a file.

So far there are no ideal waveforms to compare against yet and this is still prototype code.

## Requirements
* [OpenBCI's python library](https://github.com/OpenBCI/OpenBCI_Python) for simplifying accessing OpenBCI access
* [serial](https://pypi.python.org/pypi/pyserial) because the OpenBCI python library needs it
* [numpy](http://numpy.org) for FFT transformations
