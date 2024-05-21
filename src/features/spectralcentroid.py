from statistics import mean
from librosa import load, get_samplerate
from librosa.feature import spectral_centroid
from essentia.standard import MonoLoader, SpectralCentroidTime
from src import eng
###############################################################################
def librosa_centroid(filename: str):
    """"""
    y, sr = load(filename, sr = get_samplerate(filename))
    return mean(spectral_centroid(y=y, sr=sr)[0])

###############################################################################
def essentia_centroid(filename: str):
    """"""
    audio = MonoLoader(filename = filename)()
    SpectralCentroid = SpectralCentroidTime()
    return SpectralCentroid(audio)

###############################################################################
def mircentroid(filename: str):
    """"""
    eng.eval("mircentroid_val = mirgetdata(mircentroid('" +
    filename +
    "'))", nargout = 0)
    return eng.workspace['mircentroid_val']

###############################################################################