from kilosort import run_kilosort
from kilosort.io import save_probe
from find_and_load_session_mat import findAndLoadSessionMat, extractSessionData, plotChannelMap
from datetime import datetime
from pathlib import Path
import os


def kilosort4Wrapper(basePath, dataPath, tmin, tmax, probeLetter=None):
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
    currentTime = datetime.now().strftime("%Y%m%d-%H%M%S")
    if probeLetter:
        resultPath = basePath / f'kilosort4_Probe{probeLetter}_{currentTime}'
    else:
        resultPath = basePath / f'kilosort4_{currentTime}'
    session, dataReader = findAndLoadSessionMat(basePath, probeLetter=probeLetter)

    chanMap, xc, yc, kcoords, nChan, sampleRate, badChannels = extractSessionData(session, dataReader)
    plotChannelMap(xc, yc, kcoords, plotAllElectrodes=True)
    plotChannelMap(xc, yc, kcoords, plotAllElectrodes=False)

    Th_universal = 9
    Th_learned = 8
    # Th_universal = 7
    # Th_learned = 6
    probe = {
        'chanMap': chanMap,
        'xc': xc,
        'yc': yc,
        'kcoords': kcoords,
        'n_chan': nChan
    }
    # print(len(probe['chanMap']), len(probe['xc']), len(probe['yc']), len(probe['kcoords']))
    # print(probe)
    save_probe(probe, basePath / f"probe{probeLetter}.json")

    settings = {
        'n_chan_bin': probe['n_chan'], 'fs': sampleRate,
        'Th_universal': Th_universal, 'Th_learned': Th_learned,
        'tmin': tmin, 'tmax': tmax
    }

    ops, st, clu, tF, Wall, similar_templates, is_ref, est_contam_rate, kept_spikes = \
        run_kilosort(
            settings=settings, filename=dataPath, results_dir=resultPath, bad_channels=badChannels, probe=probe,
            device='cuda'
            # save_preprocessed_copy=True
            )