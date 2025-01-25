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

## How to Use

### **File Structure Preparation**
```
basepath/
├── structure.oebin              # Open Ephys metadata
└── concatenated_data.dat        # Binary data (all epochs merged)
```

*Note:* Use your preferred method (e.g., `preprocessOpenEphysData` in cellExplorer, custom script) to concatenate epoch files from `continuous/Neuropix-PXI-...` folders into one `concatenated_data.dat` in the basepath.

### **MATLAB Processing Code**
```matlab
% 1. Set paths and load session
basepath = '/path/to/your/basepath';
[~, basename] = fileparts(basepath);
session = loadSession(basepath, basename); 

% 2. Load Open Ephys metadata (critical for chanCoords)
session = loadOpenEphysSettingsFile(fullfile(basepath, 'structure.oebin'),...
                                   session, 'probeLetter', 'A');

% 3. Handle missing chanCoords
if ~isfield(session.extracellular, 'chanCoords') || isempty(session.extracellular.chanCoords)
    warning('Generating Neuropixels channel coordinates from first principles');
end

% 4. Save session file
saveStruct(session);
```
*Requirements:* MATLAB with newest CellExplorer toolkit installed

### **Python Processing Code**

```python
from kilosort4_loadmat import kilosort4Wrapper, generate_probe_json
from pathlib import Path

# Define paths
basePath = Path("/path/to/your/basepath")
dataPath = basePath / "concatenatedData.dat"

# Optional: Generate probe config JSON
generate_probe_json(basePath, probeLetter='A')  # Match probeLetter from MATLAB step

# Run Kilosort 4
kilosort4Wrapper(
    basePath=basePath,
    dataPath=dataPath,
    tmin=0,          # Start time (seconds)
    tmax=np.inf,     # End time (seconds; use np.inf for full duration)
    probeLetter='A'  # Must match probe ID used earlier
)
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