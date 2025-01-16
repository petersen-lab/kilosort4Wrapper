from kilosort.io import save_probe
from find_and_load_session_mat import findAndLoadSessionMat, extractSessionData, plotChannelMap
from pathlib import Path
import os


def generate_probe_json(basePath, probeLetter=None):
    # Load session data
    session, dataReader = findAndLoadSessionMat(basePath, probeLetter=probeLetter)

    # Extract probe information
    chanMap, xc, yc, kcoords, nChan, sampleRate, badChannels = extractSessionData(session, dataReader)

    # Plot channel maps (optional, can be commented out if not needed)
    plotChannelMap(xc, yc, kcoords, plotAllElectrodes=True)
    plotChannelMap(xc, yc, kcoords, plotAllElectrodes=False)

    # Create probe dictionary
    probe = {
        'chanMap': chanMap,
        'xc': xc,
        'yc': yc,
        'kcoords': kcoords,
        'n_chan': nChan
    }

    # Save probe to JSON file
    if probeLetter:
        save_probe(probe, basePath / f"probe{probeLetter}.json")
    else:
        save_probe(probe, basePath / "probe.json")

    print(f"Probe JSON file saved to {basePath}")


# Example usage
basePath = Path(r"path\to\your\base")  # Replace with your actual base path
probeLetter = ""  # Replace with your probe letter or None if not applicable
generate_probe_json(basePath, probeLetter)