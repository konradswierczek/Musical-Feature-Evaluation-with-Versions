from os import walk, path
from time import time
###############################################################################
from soundfile import read, write
###############################################################################
def parser(dir, extension: str = None):
    """Accepts folder directory, returns root paths of all MIDI files."""
    if ('PARSER_EXTENSION' in globals()) and (extension == None):
        extension = PARSER_EXTENSION
    elif extension == None:
        extension = '.mid'
    start_time = time()
    data = []
    for root, dirs, files in walk(dir):
        for filename in files:
            nm, ext = path.splitext(filename)
            if ext.lower().endswith((extension)):
                data.append((root + "/" + filename))
    end_time = time()
    elapsed_time = end_time - start_time
    print("Elapsed Time: " + str(round(elapsed_time/60,2)) + " Minutes")
    return data

###############################################################################
def cut_audio(audio_file, output, seconds: float = 2):
    """
    """
    data, sr = read(audio_file)
    write(output, data[ :len(data) - sr * seconds], 
             sr, subtype = 'PCM_16')
    return(len(data)/sr, len(data[ :len(data) - sr * seconds])/sr)

###############################################################################