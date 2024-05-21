"""
"""
###############################################################################
# Third Party Imports
import essentia.standard as es
import essentia.streaming as ess
from essentia import Pool, run
from librosa import feature, load, get_samplerate
from numpy import array
from src import eng
###############################################################################
def essentia_hpcp(audio_file, output: str = "proportion", method: str = "cqt"):
    """
    """
    outputs = ['proportion', 'original']
    methods = ['cqt', 'stft']
    if output not in outputs:
        raise ValueError("Invalid output argument. Expected one of: %s" % outputs)
    if method not in methods:
        raise ValueError("Invalid method argument. Expected one of: %s" % methods)
    audio = es.MonoLoader(filename = audio_file)()
    windowing = es.Windowing(type='blackmanharris62')
    hpcp_out = [0] * 12
    if method == 'cqt':
        hpcp = es.Chromagram(normalizeType = 'none')
        for frame in es.FrameGenerator(audio, frameSize= 32768, hopSize = 2048):
            buffer = list(hpcp(windowing(frame)))
            hpcp_out = [new + total for (new, total) in zip(buffer, hpcp_out)]
    elif method == 'stft':
        hpcp = es.HPCP(normalized = 'none')
        spectrum = es.Spectrum()
        spectralpeaks = es.SpectralPeaks(orderBy='magnitude',
                                        magnitudeThreshold=0.00001,
                                        minFrequency=20,
                                        maxFrequency=3500,
                                        maxPeaks=60)
        for frame in es.FrameGenerator(audio, frameSize= 4096, hopSize = 2048):
            peaks, magnitudes = spectralpeaks(spectrum(windowing(frame)))
            buffer = list(hpcp(peaks, magnitudes))
            hpcp_out = [new + total for (new, total) in zip(buffer, hpcp_out)]
    hpcp_out = [hpcp_out[(i + 3)%12] for i in range (0,12)]
    if output == 'original':
        return hpcp_out
    else:
        return [pc/sum(hpcp_out) for pc in hpcp_out]
    """
    outputs = ['proportion', 'original']
    methods = ['cqt', 'stft']
    if output not in outputs:
        raise ValueError("Invalid output argument. Expected one of: %s" % outputs)
    if method not in methods:
        raise ValueError("Invalid method argument. Expected one of: %s" % methods)
    loader = ess.MonoLoader(filename=audio_file)
    framecutter = ess.FrameCutter(frameSize=4096, hopSize=2048, silentFrames='noise')
    windowing = ess.Windowing(type='blackmanharris62')
    spectrum = ess.Spectrum()
    spectralpeaks = ess.SpectralPeaks(orderBy='magnitude',
                                      magnitudeThreshold=0.00001,
                                      minFrequency=20,
                                      maxFrequency=3500,
                                      maxPeaks=60)
    if method == "constantQ":
        hpcp = ess.Chromagram()
    else:
        hpcp = ess.HPCP()
    pool = Pool()
    loader.audio >> framecutter.signal
    framecutter.frame >> windowing.frame >> spectrum.frame
    spectrum.spectrum >> spectralpeaks.spectrum
    spectralpeaks.magnitudes >> hpcp.magnitudes
    spectralpeaks.frequencies >> hpcp.frequencies
    hpcp.hpcp >> (pool, 'tonal.hpcp')
    run(loader)
    hpcp = [sum(pc) for pc in pool['tonal.hpcp'].T]
    hpcp = [hpcp[(i + 3)%12] for i in range (0,12)]
    if output == "original":
        return hpcp
    elif output == "proportion":
        return [pc/sum(hpcp) for pc in hpcp]
#import essentia.standard as es
#audio = es.AudioLoader(filename = file)()
#SpectralCentroid = es.Chromagram()
#SpectralCentroid(audio)
loader = es.MonoLoader(filename=audio_file)
framecutter = es.FrameCutter(frameSize=4096, hopSize=2048)
windowing = es.Windowing(type='blackmanharris62')
spectrum = es.Spectrum()
# Refer http://essentia.upf.edu/documentation/reference/std_SpectralPeaks.html
spectralPeaks = es.SpectralPeaks(orderBy='magnitude',
                                    magnitudeThreshold=0.00001,
                                    minFrequency=20,
                                    maxFrequency=3500,
                                    maxPeaks=60)
# http://essentia.upf.edu/documentation/reference/std_SpectralWhitening.html
#spectralWhitening = es.SpectralWhitening(maxFrequency= maxFrequency,
#                                        sampleRate=sampleRate)
# http://essentia.upf.edu/documentation/reference/std_HPCP.html
hpcp = es.HPCP()
pool = essentia.Pool()
#compute hpcp for each frame and add the results to the pool
for frame in framecutter:
    spectrum_mag = spectrum(windowing(frame))
    frequencies, magnitudes = spectralPeaks(spectrum_mag)
    #if whitening:
        #   w_magnitudes = spectralWhitening(spectrum_mag,
    #                                    frequencies,
        #                                   magnitudes)
        #   hpcp_vector = hpcp(frequencies, w_magnitudes)
    #else:
    hpcp_vector = hpcp(frequencies, magnitudes)
    pool.add('tonal.hpcp', hpcp_vector)
        sampleRate=sampleRate,
                   maxFrequency=maxFrequency,
                   minFrequency=minFrequency,
                   size=numBins, **kwargs
"""
###############################################################################
def librosa_chromagram(audio_file: str, output: str = "proportion", method: str = "cqt"):
    """
    """
    outputs = ['proportion', 'original']
    methods = ['cqt', 'stft', 'cens', 'vqt']
    if output not in outputs:
        raise ValueError("Invalid output argument. Expected one of: %s" % outputs)
    if method not in methods:
        raise ValueError("Invalid method argument. Expected one of: %s" % methods)
    y, sr = load(audio_file, sr = get_samplerate(audio_file))
    if method == 'vqt':
        chromagram = feature.chroma_vqt(y = y, sr = sr, intervals = 'equal', norm = None)
    else:
        chromagram = eval("feature.chroma_" +
                        method +
                        "(y = y, sr = sr, n_chroma = 12)")
    chromagram = [sum(pc) for pc in chromagram]
    if output == "original":
        return chromagram
    elif output == "proportion":
        return [pc/sum(chromagram) for pc in chromagram]
    
###############################################################################
def mirchromagram(filename, output: str = "proportion"):
    """
    """
    outputs = ['proportion', 'original']
    if output not in outputs:
        raise ValueError("Invalid output argument. Expected one of: %s" % outputs)
    eng.eval("mirchromagram_val = mirgetdata(mirchromagram('" +
             filename +
             "'))", nargout = 0)
    out = array(eng.workspace['mirchromagram_val']).tolist()
    hpcp = [i for sublist in out for i in sublist]
    if output == "original":
        return hpcp
    elif output == "proportion":
        return [pc/sum(hpcp) for pc in hpcp]

###############################################################################