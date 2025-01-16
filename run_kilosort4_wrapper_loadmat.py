'''
Before you start, make sure you have session file and the structure.oebin file has been read
'''
import numpy as np
from kilosort4_loadmat import kilosort4Wrapper
from pathlib import Path

basePath = Path(r"path\to\your\base")
dataPath = Path(r"path\to\your\file")

tmin = 0
tmax = np.inf
probeLetter = ''

kilosort4Wrapper(basePath, dataPath, tmin, tmax, probeLetter)

# kilosort4Wrapper(basePath, dataPath, tmin, tmax)

