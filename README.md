# Kilosort 4 Wrapper

## Overview
Python wrapper for Kilosort 4 that processes Neuropixels probe data.

## Installation
```bash
# Create and activate conda environment
conda create -n myenv python=3.9.19 -y
conda activate myenv

# Install requirements
pip install -r requirements.txt
```

## Main Functions

### kilosort4Wrapper
Processes neural data through Kilosort 4.

```python
from kilosort4_loadmat import kilosort4Wrapper
from pathlib import Path

basePath = Path("path/to/base")
dataPath = Path("path/to/data.dat")
tmin = 0
tmax = np.inf
probeLetter = 'A'  # Optional: 'A', 'B', etc.

kilosort4Wrapper(basePath, dataPath, tmin, tmax, probeLetter)
```

### generate_probe_json
Creates probe configuration file.

```python
from kilosort4_loadmat import generate_probe_json
from pathlib import Path

basePath = Path("path/to/base")
probeLetter = 'A'  # Optional

generate_probe_json(basePath, probeLetter)
```

### Helper Functions

#### findAndLoadSessionMat
Loads MATLAB session files (supports .mat and v7.3 formats).

#### extractSessionData
Extracts probe information:
- Channel mapping
- Channel coordinates
- Shank assignments
- Channel count
- Sample rate
- Bad channels

#### plotChannelMap
Visualizes probe layout with options for:
- All electrode sites
- Active channels only
- Color-coded shanks

## Required Packages
Key dependencies (see requirements.txt for full list):
- kilosort==4.0.17
- numpy==1.26.4
- scipy==1.13.1
- torch==2.4.1
- mat73==0.65

## Output
Results are saved in timestamped directories:
```
kilosort4_ProbeX_YYYYMMDD-HHMMSS/
```