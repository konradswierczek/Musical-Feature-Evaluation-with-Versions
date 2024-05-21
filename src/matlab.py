from matlab.engine import start_matlab
# matlab engine
eng = start_matlab()
# Import MIRtoolbox
eng.addpath(eng.genpath('src/mirtoolbox1.8.1'), nargout= 0)