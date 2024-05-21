# Python Third-Party Imports
from mido import MidiFile, MidiTrack, tempo2bpm
from midi2audio import FluidSynth
###############################################################################
def note_onFilter(midiFile):
    mid = MidiFile(midiFile)
    new_mid = MidiFile(ticks_per_beat=mid.ticks_per_beat)
    new_track = MidiTrack()
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == "note_on" and msg.velocity == 0:
                new_track.append(msg.copy(type = "note_off"))
            else:
                new_track.append(msg)
            
    new_mid.tracks.append(new_track)
    return new_mid

###############################################################################
def MIDInoCheck(note: int, min: int = 0, max: int = 127):
    if note > max:
        new_note = MIDInoCheck(note - 12)
        return new_note
    elif note < min:
        new_note = MIDInoCheck(note + 12)
        return new_note
    else: return note
    
###############################################################################
def changePitchHeight(midiFile: str, octave = 1, min: int = 0, max: int = 127):
    """
    """
    midiFile = MidiFile (midiFile)
    new = MidiFile(type=0, ticks_per_beat = midiFile.ticks_per_beat)
    track = MidiTrack()
    new.tracks.append(track)
    for i in range(len(midiFile.tracks)):
        for msg in midiFile.tracks[i]:
            if msg.type in ["note_on", "note_off"]:
                new_note = MIDInoCheck(msg.note + (int(12 * octave)), min = min, max = max)
                track.append(msg.copy(note = new_note))
            else:
                track.append(msg)   
    return new

###############################################################################
def changeVelocity(midiFile: str, velocity = 64):
    """
    """
    midiFile = MidiFile(midiFile)
    new = MidiFile(type=0, ticks_per_beat = midiFile.ticks_per_beat)
    track = MidiTrack()
    new.tracks.append(track)
    for i in range(len(midiFile.tracks)):
        for msg in midiFile.tracks[i]:
            if msg.type == "note_on":
                track.append(msg.copy(velocity = int(velocity)))
            else:
                track.append(msg)   
    return new

###############################################################################
def changeTempo(midiFile: str, tempo: float = 2.0):
    """
        MIDI tempo is given in microseconds per quarter note
        when multiplying the tempo of a file:
        numbers below 1 will decrease the microseconds per quarter note, 
        speeding up the file
        numbers above 1 will increse the microseconds per quarter note, 
        slowing down the file
        Intuitively, we thinking of a number above 1 increasing the tempo, 
        and below decreasing.
        Therefore, we take 1/a of the tempo multiplier argument 
        so it makes sense to the user.
    """
    midiFile = MidiFile (midiFile)
    new = MidiFile(type=0, ticks_per_beat = midiFile.ticks_per_beat)
    track = MidiTrack()
    new.tracks.append(track)
    for i in range(len(midiFile.tracks)):
        for msg in midiFile.tracks[i]:
            if msg.type == "set_tempo":
                newTempo = int(msg.tempo * (1/tempo))
                track.append(msg.copy(tempo = (newTempo)))
            else:
                track.append(msg)
    return new

###############################################################################
def exportMIDI(midiFile, filename):
    """
    """
    midiFile.save(filename)

###############################################################################
def synthMIDI(midiFile,
              sf = "sf/GrandPiano.sf2",
              sampleRate = 44100,
              ext = ".wav",
              filename = "output"):
    """
    """
    FluidSynth(sample_rate = sampleRate)
    FluidSynth(sf).midi_to_audio(midiFile, filename + ext)

###############################################################################
def maniMIDI(midiFile, manipulation = "tempo", filename = "audio/test3.wav"):
    """
    """
    org = MidiFile(midiFile)
    new = changePitchHeight(org, octave = 2)
    file = "midi/test.mid"
    exportMIDI(new, filename = file)
    synthMIDI(file, filename = filename)

###############################################################################
def swierckj_pcd(midiFile, timebase = "seconds", velocity = "False"):
    """"""
    # TODO: Add vleocity weightings
    midiFile = MidiFile(midiFile)
    tpb = midiFile.ticks_per_beat
    if "set_tempo" in [msg.type for msg in midiFile.tracks[0]]:
        bpm = tempo2bpm([msg.tempo for msg in midiFile.tracks[0] if 
                            msg.type == "set_tempo"][0])
    else:
        bpm = 120
    if timebase == "seconds":
        temp = 0
        new = MidiFile(type=0, ticks_per_beat = midiFile.ticks_per_beat)
        track = MidiTrack()
        new.tracks.append(track)
        for i in range(len(midiFile.tracks)):
                for msg in midiFile.tracks[i]:
                    tick_time = ((msg.time / tpb) / bpm) * 60
                    abs_time = tick_time + temp
                    track.append(msg.copy(time = abs_time))
                    temp = abs_time
    elif timebase == "ticks":
        temp = 0
        new = MidiFile(type=0, ticks_per_beat = midiFile.ticks_per_beat)
        track = MidiTrack()
        new.tracks.append(track)
        for i in range(len(midiFile.tracks)):
                for msg in midiFile.tracks[i]:
                    tick_time = msg.time
                    abs_time = tick_time + temp
                    track.append(msg.copy(time = abs_time))
                    temp = abs_time
    out = []
    for i, msg in enumerate(new.tracks[0]):
        if msg.type == "note_on":
            for next in range(i + 1, len(new.tracks[0])):
                if new.tracks[0][next].type in ["note_off", "note_on"] and new.tracks[0][next].note == msg.note:
                    out.append({"note": msg.note,
                                "velocity": msg.velocity,
                                "time_on": msg.time,
                                "time_off": new.tracks[0][next].time,
                                "length": (new.tracks[0][next].time - msg.time)})
                    break
    pcd = dict.fromkeys(range(0,12), 0)
    for msg in out:
        pc = msg["note"]%12
        pcd[pc] = pcd[pc] + msg["length"]
    return [pcd[pc]/sum(pcd.values()) for pc in range(0,12)]

###############################################################################
def absTime(file):
    midiFile = MidiFile(file)
    temp = 0
    new = MidiFile(type=0, ticks_per_beat = midiFile.ticks_per_beat)
    track = MidiTrack()
    new.tracks.append(track)
    for i in range(len(midiFile.tracks)):
            for msg in midiFile.tracks[i]:
                tick_time = msg.time
                abs_time = tick_time + temp
                track.append(msg.copy(time = abs_time))
                temp = abs_time
    out = []
    for i, msg in enumerate(new.tracks[0]):
        if msg.type == "note_on":
            for next in range(i + 1, len(new.tracks[0])):
                if new.tracks[0][next].type in ["note_off", "note_on"] and new.tracks[0][next].note == msg.note:
                    out.append({"note": msg.note,
                                "velocity": msg.velocity,
                                "time_on": msg.time,
                                "time_off": new.tracks[0][next].time,
                                "length": (new.tracks[0][next].time - msg.time)})
                    break
    return out    

###############################################################################
def ambitus(file):
    """"""
    number_list = []
    for track in MidiFile(file).tracks:
        for msg in track:
            if msg.type == "note_on":
                number_list.append(msg.note)
    return min(number_list), max(number_list)

###############################################################################
def pitchHeight(file):
    """"""
    abs = absTime(file)
    return pitchHeight
