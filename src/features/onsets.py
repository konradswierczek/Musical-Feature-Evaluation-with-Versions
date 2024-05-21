# Third Party Imports
import essentia.standard as es
import essentia
from librosa import load, get_samplerate
from librosa.onset import onset_detect
from src import eng
###############################################################################
def mirevents(filename):
    """
    """
    eng.eval("mirevents_val = mirgetdata(mirevents('" +
             filename +
             "'))", nargout = 0)
    return len(eng.workspace['mirevents_val'])

###############################################################################
def essentia_Onsets(filename: str, method: str = "hfc"):
    """
    """
    methods = ['hfc', 'complex', 'complex_phase', 'flux', 'melflux', 'rms']
    if method not in methods:
        raise ValueError("Invalid method argument. \
                            Expected one of: %s" % methods)
    audio = es.MonoLoader(filename = filename)()
    od = es.OnsetDetection(method = method)
    pool = essentia.Pool()
    for frame in es.FrameGenerator(audio, frameSize = 1024, hopSize = 512):
        magnitude, phase = es.CartesianToPolar()(es.FFT() \
                           (es.Windowing(type = 'hann')(frame)))
        pool.add('onsets', od(magnitude, phase))
    return len(es.Onsets()(essentia.array([pool['onsets']]), [1]))

###############################################################################
def librosa_onset_detect(filename):
    """"""
    y, sr = load(filename, sr = get_samplerate(filename))
    return len(onset_detect(y = y, sr = sr))

###############################################################################