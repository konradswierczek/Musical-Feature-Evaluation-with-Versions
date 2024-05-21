"""
MAPLE Module May/June 2022
Konrad Swierczek
Replication of mirmode algorithm from MIRtoolbox for symbolic notation using music21.
Used for comparison of results of mirmode for symbolic notation and audio files.
"""
# Requires music21
import csv
import os
import fnmatch
from music21 import *

# music21 method.
def music21_pcd(sStream, output = 'proportion'):
    """ Pitch Class Distribution weighted with quarter length durations. """
    a = analysis.discrete.KrumhanslSchmuckler()
    flatstream = sStream.flatten().notesAndRests
    pcd = a._getPitchClassDistribution(flatstream)
    if output == 'quarterLength':
        return {key: pcd[key] for key in range(0,12)}
    elif output == 'proportion':
        pcd = [key/sum(pcd) for key in pcd]
        return {key: round(pcd[key],3) for key in range(0,12)}
    else:
        # make an error
        return "Specify method 'proportion' or 'quarterLength'"

def music21_krumhanslschmuckler(sStream):
    """ Full output of Krumhansl Schmuckler keyfinding algorithm. """
    krumhanslschmuckler = analysis.discrete.KrumhanslSchmuckler(sStream)
    krumhanslschmuckler.getSolution(sStream)
    key_coefficients = krumhanslschmuckler.alternativeSolutions
    key_coefficients.append(krumhanslschmuckler.getSolutionsUsed()[0])
    return {str(key_coefficients[ind][0].pitchClass) + 
                " " + 
                key_coefficients[ind][1]:round(key_coefficients[ind][2],3)
                for ind, val in enumerate(key_coefficients)}

def music21_mirmode(sStream, method = 'top'):
    """ Mode based on mirmode in MIRtoolbox 1.8. """
    key_coefficients = music21_krumhanslschmuckler(sStream)
    if method == 'top':
        mirmode = max([value for key, value in key_coefficients.items() if 'major' in key.lower()]) - max([value for key, value in key_coefficients.items() if 'minor' in key.lower()])
        return round(mirmode,3)
    elif method == 'sum':
        mirmode = sum([value for key, value in key_coefficients.items() if 'major' in key.lower()]) - sum([value for key, value in key_coefficients.items() if 'minor' in key.lower()])
        return round(mirmode,3)
    else:
        # Make this an error
        return "Specify method 'top' or 'sum'"

###############################################################################

class mirmodeMAPLE:
    def __init__(self,filepath):
        """  """
        self.name = os.path.basename(filepath)
        self.sStream = converter.parse(filepath).measures(1,8)
        self.pcd = music21_pcd(self.sStream)
        self.krum = music21_krumhanslschmuckler(self.sStream)
        self.mirmode_val = music21_mirmode(self.sStream)
        self.mirmode_valsum = music21_mirmode(self.sStream, method = 'sum')

###############################################################################

def corpus_analyze(corpus_path, mirmode_method = 'top', pcd_output = 'proportion'):
    """ Corpus analysis tool. """
    # Extract file names.
    corpus_folder = os.listdir(corpus_path)

    # Filter out files with unuasble extensions.
    corpus_filepaths = []
    extensions =  ['*.krn','*.mid','*.mxl']
    for extension in extensions:
        for name in fnmatch.filter(corpus_folder,extension):
            corpus_filepaths.append(corpus_path+'/'+name)

    # Analyze corpus
    corpus_analyzed={}
    for file in corpus_filepaths:
        pass
        corpus_analyzed.update({os.path.basename(file):mirmodeMAPLE(file)})
    return corpus_analyzed