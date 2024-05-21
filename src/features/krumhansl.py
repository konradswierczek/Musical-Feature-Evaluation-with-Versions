from csv import reader
from scipy.stats import pearsonr
from src import eng
###############################################################################
with open('data/weights.csv', mode='r') as file:
    reader = list(reader(file))
    profiles = {row[0]: {"major": [float(i) for i in row[1:13]],
                         "minor": [float(i) for i in row[13:25]]} \
                         for row in reader[2:]}

for profile in profiles:
    buffer = {}
    for key in profiles[profile]:
        org = profiles[profile][key]
        for pc in range(0,12):
            buffer[str(pc) + "_" + key] = [org[(ind - pc)%12] \
                                           for (ind, val) in enumerate(org)]
    profiles[profile] = buffer

###############################################################################
def keyfinding(pitchDistribution: list,
               profile: str = "KrumhanslKessler",
               similarity: str = 'pearsonr'):
    """ """
    if not isinstance(pitchDistribution, list):
        raise TypeError("must be pitch distribution.")
    if profile not in profiles.keys():
        raise TypeError("Invalid profile name")
    coefis = {}
    for key in profiles[profile]:
        coefis[key] = pearsonr(profiles[profile][key], 
                               pitchDistribution).statistic
    return coefis

###############################################################################
def mirmode(pitchDistribution: list,
            weights: str = "KrumhanslKessler",
            method: str = "best"):
    """ """
    if not isinstance(pitchDistribution, list):
        raise TypeError("coefis must be list of integers")
    if weights not in profiles.keys():
        raise TypeError("Invalid profile name")
    if method not in ["best", "sum"]:
        raise TypeError("method must be 'best' or 'sum'.")
    coefis = keyfinding(pitchDistribution, profile = weights)
    if method == "best":
        max_major = max([coefis[key] for key in coefis if 'major' in key])
        max_minor = max([coefis[key] for key in coefis if 'minor' in key])
        return max_major - max_minor
    elif method == "sum":
        sum_major = sum([coefis[key] for key in coefis if 'major' in key])
        sum_minor = sum([coefis[key] for key in coefis if 'minor' in key])
        return sum_major + sum_minor

###############################################################################
def mirmode_dir(filename, method: str = "best"):
    """
    """
    if method not in ['best', 'sum']:
        raise ValueError("Invalid method argument. Expected one of: %s" % methods)
    eng.eval("mirmode_val = mirgetdata(mirmode('" +
             filename +
             "'))", nargout = 0)
    return eng.workspace['mirmode_val']

###############################################################################
def mirkeystrength(filename, method: str = "best"):
    """
    """
    if method not in ['best', 'sum']:
        raise ValueError("Invalid method argument. Expected one of: %s" % methods)
    eng.eval("mirkeystrength_val = mirgetdata(mirkeystrength('" +
             filename +
             "'))", nargout = 0)
    modes = ["major", "minor"]
    keystrength = {}
    for pc, vals in enumerate(np.array(eng.workspace['mirkeystrength_val']).tolist()):
        for mode, val in enumerate(vals[0][0]):
            keystrength[str(pc) + "_" + modes[mode]] = val
    return keystrength

###############################################################################