#Built-in Imports
import os
import requests
import shutil
from zipfile import ZipFile
# Third Party Imports
import pandas as pd
from music21 import *
# Constants
PARSER_EXTENSION = '.wav'
# Local Imports
from src import *

# Cut
url = 'https://mcmasteru365-my.sharepoint.com/:u:/g/personal/swierckj_mcmaster_ca/ESm13Lzrt-9JuexJf57ZwwUB3S50v9jMKueiCdR2kB6v1A?e=hYQjbt'
r = requests.get(url, allow_redirects=True)
open('org_audio.zip', 'wb').write(r.content)

os.mkdir('temp')
with ZipFile("org_audio.zip", 'r') as zipped:
    zipped.extractall(path = "temp")

log = []
os.mkdir('audio')
for file in parser('temp/org_audio', extension = '.wav'):
        folder = file.split('/')[2]
        if not os.path.isdir('audio/' + folder):
            os.mkdir('audio/' + folder)
        log.append([cut_audio(file, output = 'audio/' + folder + '/'+ \
                                             os.path.basename(file))])

set([round(i[0][0] - i[0][1], 10) for i in log])
os.remove('org_audio.zip')
shutil.rmtree('temp')


for file in parser("midi", extension = '.mid'):
    converter.parse(file).measures(1,8).write("midi", file[:-6] + "flatMIDI_cut.mid")
    new_file = file[:-4] + "_flatV.mid"
    exportMIDI(changeVelocity(file[:-6] + "flatMIDI_cut.mid"), filename = new_file)
    synthMIDI(new_file, filename = "audio/" + file[4:-6] + "flatMIDI")
    os.remove(new_file)
    os.remove(file[:-6] + "flatMIDI_cut.mid")



# Mode Extraction
# TODO: Include cqt essentia.
df = pd.DataFrame()
for file in parser('audio', extension = '.wav'):
    mode = {"filename": [file], 
            "mirmode_essentia-cqt": [mirmode(essentia_hpcp(file,
                                                            output = "original",
                                                            method = "cqt"),
                                      weights = "Gomez_MIRtoolbox")],
            "mirmode_essentia-sftf": [mirmode(essentia_hpcp(file,
                                                             output = "original",
                                                             method = "stft"),
                                       weights = "Gomez_MIRtoolbox")],
            "mirmode_MIRtoolbox-std": [mirmode(mirchromagram(file, 
                                                          output = "original"),
                                     weights = "Gomez_MIRtoolbox")],
            "mirmode_MIRtoolbox-dir": [mirmode_dir(file)],
            "mirmode_librosa-cqt": [mirmode(librosa_chromagram(file,
                                                                output = "original"),
                                     weights = "Gomez_MIRtoolbox")],
            "mirmode_librosa-stft": [mirmode(librosa_chromagram(file,
                                                                 output = "original",
                                                                 method = "stft"), 
                                      weights = "Gomez_MIRtoolbox")],
            "mirmode_librosa-cens": [mirmode(librosa_chromagram(file,
                                                                 output = "original",
                                                                 method = "cens"),
                                      weights = "Gomez_MIRtoolbox")],
            "mirmode_librosa-vqt": [mirmode(librosa_chromagram(file,
                                                                output = "original",
                                                                method = "vqt"),
                                    weights = "Gomez_MIRtoolbox")]}
    df = pd.concat([df, pd.DataFrame(mode)])
 
#
df.to_csv("data/_mode.csv")

# Onsets Extraction
df = pd.DataFrame()
for file in parser('audio', extension = '.wav'):
    onsets = {"filename": [file], 
              "onsets_essentia-hfc": [essentia_Onsets(file)],
              "onsets_essentia-complex": [essentia_Onsets(file,
                                                         method = "complex")],
              "onsets_essentia-phase": [essentia_Onsets(file,
                                                         method = "complex_phase")],
              "onsets_essentia-flux": [essentia_Onsets(file,
                                                         method = "flux")],                    
              "onsets_essentia-melflux": [essentia_Onsets(file,
                                                         method = "melflux")],    
              "onsets_essentia-rms": [essentia_Onsets(file,
                                                         method = "rms")],         
              "onsets_mirtoolbox-std": [mirevents(file)],
              "onsets_librosa-std": [librosa_onset_detect(file)]}
    df = pd.concat([df, pd.DataFrame(onsets)])

#
df.to_csv("data/_onsets.csv")

# Spectral Centroid Extraction
df = pd.DataFrame()
for file in parser('audio', extension = '.wav'):
    centroid = {"filename": [file], 
                "centroid_essentia-std": [essentia_centroid(file)],
                "centroid_mirtoolbox-std": [mircentroid(file)],
                "centroid_librosa-std": [librosa_centroid(file)]}
    df = pd.concat([df, pd.DataFrame(centroid)])

#
df.to_csv("data/_centroid.csv")

# BPM Extraction
df = pd.DataFrame()
for file in parser('audio', extension = '.wav'):
    bpm = {"filename": [file], 
           "bpm_essentia-percival": [essentia_tempo(file)],
           "bpm_essentia-degara": [essentia_tempo(file, method = 'degara')],
           "bpm_essentia-multifeature": [essentia_tempo(file,
                                                        method = 'multifeature')],
           "bpm_mirtoolbox-classical": [mirtempo(file)],
           "bpm_mirtoolbox-metre": [mirtempo(file, method = "Metre")],
           "bpm_librosa-beattrack": [librosa_tempo(file)],
           "bpm_librosa-onsets": [librosa_tempo(file, method = 'onsets')]}
    df = pd.concat([df, pd.DataFrame(bpm)])

#
df.to_csv("data/_bpm.csv")