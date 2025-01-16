'''
Before you start, make sure you have session file and the structure.oebin file has been read
'''
import numpy as np
from kilosort4_loadmat import kilosort4Wrapper
from pathlib import Path

# Define the base path for the session
basePath = Path(r"path\to\your\base")

# Define paths for both probe data files
probeA_path = Path(r"path\to\your\file\ProbeA.dat")
probeB_path = Path(r"path\to\your\file\ProbeB.dat")

# Set time parameters
tmin = 0
tmax = np.inf

# Process Probe A
print("Processing Probe A...")
kilosort4Wrapper(basePath, probeA_path, tmin, tmax, 'A')

# Process Probe B
print("Processing Probe B...")
kilosort4Wrapper(basePath, probeB_path, tmin, tmax, 'B')