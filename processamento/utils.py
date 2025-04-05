from mido import MidiFile
import io

def importar_trilha(midi_path):
    midi = MidiFile(midi_path)
    for track in midi.tracks:
        if any(msg.type in ['note_on', 'note_off'] for msg in track):
            return track
    return None

def get_ticks_per_beat_from_pretty_midi(pretty):
    buffer = io.BytesIO()
    pretty.write(buffer)
    buffer.seek(0)
    midi = MidiFile(file=buffer)
    return midi.ticks_per_beat