from mido import MidiFile

def importar_trilha(midi_path):
    midi = MidiFile(midi_path)
    for track in midi.tracks:
        if any(msg.type in ['note_on', 'note_off'] for msg in track):
            return track
    return None