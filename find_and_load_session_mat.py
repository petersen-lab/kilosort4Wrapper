import os
import glob
import scipy.io
import mat73
import numpy as np
import matplotlib.pyplot as plt


def findAndLoadSessionMat(basePath, probeLetter=None):
    if probeLetter:
        searchPattern = os.path.join(basePath, f'*Probe{probeLetter}.session.mat')
    else:
        searchPattern = os.path.join(basePath, '*session*.mat')

    sessionFiles = glob.glob(searchPattern)

    if not sessionFiles:
        print(f"No session files found in {basePath}")
        return None, None

    if len(sessionFiles) > 1:
        print(f"Multiple files found: {sessionFiles}")
        print("Loading the first file in the list.")

    fileToLoad = sessionFiles[0]
    print(f"Loading file: {fileToLoad}")

    try:
        matData = scipy.io.loadmat(fileToLoad)
        return matData, 'scipy'
    except NotImplementedError as e:
        if "Please use HDF reader for matlab v7.3" in str(e):
            print("Detected MATLAB v7.3 file. Attempting to load with mat73.")
            try:
                matData = mat73.loadmat(fileToLoad)
                return matData, 'mat73'
            except Exception as mat73_error:
                print(f"Error loading with mat73: {mat73_error}")
                return None, None
        else:
            print(f"Unexpected error: {e}")
            return None, None
    except Exception as e:
        print(f"Error loading file: {e}")
        return None, None


def extractSessionData(session, dataReader):
    try:
        if dataReader == 'scipy':
            sessionData = session['session'][0, 0]

            # Extract chanMap and concatenate into a 1D list
            chanMap = np.concatenate(
                [group[0] for group in sessionData['extracellular'][0, 0]['electrodeGroups'][0, 0]['channels'][0]])
            chanMap = (chanMap.flatten() - 1).astype(np.int32)
            chanMapSorted = np.sort(chanMap)

            # Extract other data
            xc = sessionData['extracellular'][0, 0]['chanCoords'][0, 0]['x'].flatten().astype(np.float64)
            yc = sessionData['extracellular'][0, 0]['chanCoords'][0, 0]['y'].flatten().astype(np.float64)
            kcoords = sessionData['extracellular'][0, 0]['chanCoords'][0, 0]['shank'].flatten().astype(np.int32)
            nChan = int(sessionData['extracellular'][0, 0]['nChannels'][0, 0])
            sampleRate = float(sessionData['extracellular'][0, 0]['sr'][0, 0])
            try:
                badChannels = list(sessionData['channelTags'][0, 0]['bad'][0, 0]['channels'][0])
            except Exception:
                badChannels = []

        elif dataReader == 'mat73':
            sessionData = session['session'] if 'session' in session else session

            try:
                electrodeGroups = sessionData['extracellular']['electrodeGroups']

                # Handle the list of dictionaries format
                if isinstance(electrodeGroups, list):
                    # Each group has {'channels': array(...), 'label': 'shanksN'}
                    chanMap = np.concatenate([group['channels'].flatten() for group in electrodeGroups])
                elif isinstance(electrodeGroups, dict):
                    # If it's in dictionary format
                    channels_list = electrodeGroups['channels']
                    if isinstance(channels_list, list):
                        chanMap = np.concatenate([np.array(group).flatten() for group in channels_list])
                    else:
                        chanMap = np.array(channels_list).flatten()
                else:
                    raise ValueError(f"Unexpected electrodeGroups format: {type(electrodeGroups)}")

            except Exception as e:
                print(f"Error in channel extraction: {e}")
                print("electrodeGroups structure:", electrodeGroups)
                raise Exception("Failed to extract channels properly")

            chanMap = (chanMap - 1).astype(np.int32)
            chanMapSorted = np.sort(chanMap)

            # Extract other data
            xc = sessionData['extracellular']['chanCoords']['x'].flatten().astype(np.float64)
            yc = sessionData['extracellular']['chanCoords']['y'].flatten().astype(np.float64)
            kcoords = sessionData['extracellular']['chanCoords']['shank'].flatten().astype(np.int32)
            nChan = int(sessionData['extracellular']['nChannels'])
            sampleRate = float(sessionData['extracellular']['sr'])
            try:
                temp = sessionData['channelTags']['bad']['channels']
                badChannels = [temp[()]] if temp.shape == () else list(temp)
            except Exception:
                badChannels = []

        else:
            raise ValueError(f"Unsupported dataReader: {dataReader}")

        return chanMapSorted, xc, yc, kcoords, nChan, sampleRate, badChannels

    except KeyError as e:
        raise KeyError(f"Missing key in session data: {e}")
    except IndexError as e:
        raise IndexError(f"Index out of range. Possible mismatch in data structure: {e}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error occurred while extracting session data: {e}")

def plotChannelMap(activeX, activeY, activeShanks, plotAllElectrodes=False):
    fig, ax = plt.subplots(figsize=(6, 8))

    xSubsets = np.array([0, 32, 250, 282, 500, 532, 750, 782])
    yScale = np.arange(0, 640 * 15, 15)

    if plotAllElectrodes:
        allX, allY = np.meshgrid(xSubsets, yScale)
        plt.scatter(allX, allY, c='lightgray', marker='o', alpha=0.3, s=10, label='All Electrodes')

    # Color map for the four shanks
    colors = ['red', 'blue', 'green', 'purple']

    for shank in range(1, 5):  # We have 4 shanks
        mask = activeShanks == shank
        plt.scatter(activeX[mask], activeY[mask], c=colors[shank - 1], marker='o', s=20, label=f'Shank {shank}')

    if plotAllElectrodes:
        plt.xlim(min(xSubsets) - 15, max(xSubsets) + 15)
        plt.ylim(min(yScale) - 16, max(yScale) + 16)
    else:
        # Adjust limits for active sites only
        xMargin = (max(activeX) - min(activeX)) * 0.1
        yMargin = (max(activeY) - min(activeY)) * 0.1
        plt.xlim(min(activeX) - xMargin, max(activeX) + xMargin)
        plt.ylim(min(activeY) - yMargin, max(activeY) + yMargin)

    plt.title(f"{'All Electrodes' if plotAllElectrodes else 'Active Channels'} Visualization")
    plt.xlabel('X coordinate (µm)')
    plt.ylabel('Y coordinate (µm)')
    plt.grid(True)
    plt.legend()
    plt.show()