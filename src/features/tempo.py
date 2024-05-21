# Third Party Imports
import essentia.standard as es
import librosa
from src import eng
###############################################################################
def librosa_tempo(filename: str, method: str = "beat_track"):
    """"""
    methods = ["beat_track", "onsets"]
    if method not in methods:
        raise ValueError("Invalid method argument. \
                          Expected one of: %s" % methods)
    y, sr = librosa.load(filename, sr = librosa.get_samplerate(filename))
    if method == "beat_track":
        return librosa.beat.beat_track(y=y, sr=sr)[0]
    else:
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        return librosa.feature.tempo(onset_envelope=onset_env, sr=sr)[0]

###############################################################################
def essentia_tempo(filename: str, method: str = 'percival'):
    """"""
    methods = ["percival", "degara", 'multifeature']
    if method not in methods:
        raise ValueError("Invalid method argument. \
                          Expected one of: %s" % methods)
    audio = es.MonoLoader(filename = filename)()
    if method == 'percival':
        return es.PercivalBpmEstimator()(audio)
    elif method == 'degara':
        return es.RhythmExtractor2013(method = 'degara')(audio)[0]
    else:
        return es.RhythmExtractor2013()(audio)[0]

###############################################################################
def mirtempo(filename: str, method: str = "Classical"):
    """
    """
    methods = ['Classical', 'Metre']
    if method not in methods:
        raise ValueError("Invalid method argument. \
                          Expected one of: %s" % methods)
    if method == 'Classical':
        eng.eval("mirtempo_val = mirgetdata(mirtempo('" +
                 filename +
                 "'))", nargout = 0)
    else:
        eng.eval("mirtempo_val = mean(mirgetdata(mirtempo('" +
                 filename +
                 "', 'Metre')))", nargout = 0)
    return eng.workspace['mirtempo_val']

###############################################################################