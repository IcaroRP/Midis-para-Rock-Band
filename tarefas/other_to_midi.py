import os
import crepe
import librosa
import numpy as np
import pretty_midi
import soundfile as sf

# Caminho para o arquivo do stem 'other'
audio_path = 'separated/htdemucs/No Way Through/other.wav'

# Carrega o áudio
print("Carregando áudio...")
y, sr = librosa.load(audio_path, sr=16000, mono=True)

# Usa o CREPE para detectar o pitch
timestamps, frequencies, confidences, activation = crepe.predict(y, sr, viterbi=True, step_size=10)

# Parâmetros de segmentação
confidence_threshold = 0.4
min_note_length = 0.1

# Notas usadas nas lanes de guitarra (Green a Orange)
lane_notes = [60, 61, 62, 63, 64]  # C4 to E4

def map_to_lane(pitch_hz):
    """Mapeia o pitch detectado para uma das 5 lanes padrão Rock Band."""
    if pitch_hz <= 196:     # G3
        return lane_notes[0]
    elif pitch_hz <= 247:   # B3
        return lane_notes[1]
    elif pitch_hz <= 330:   # E4
        return lane_notes[2]
    elif pitch_hz <= 440:   # A4
        return lane_notes[3]
    else:
        return lane_notes[4]

notes = []
current_pitch = None
start_time = None

print("Segmentando e mapeando notas...")
for i in range(len(frequencies)):
    pitch = frequencies[i]
    conf = confidences[i]
    time = timestamps[i]

    if conf < confidence_threshold:
        pitch = 0

    if pitch > 0:
        midi_note = map_to_lane(pitch)
    else:
        midi_note = None

    if current_pitch is None:
        if midi_note is not None:
            current_pitch = midi_note
            start_time = time
    else:
        if midi_note != current_pitch:
            end_time = time
            duration = end_time - start_time
            if duration >= min_note_length:
                notes.append((current_pitch, start_time, duration))
            current_pitch = midi_note
            start_time = time if midi_note is not None else None

# Finaliza última nota
if current_pitch is not None and start_time is not None:
    end_time = timestamps[-1]
    duration = end_time - start_time
    if duration >= min_note_length:
        notes.append((current_pitch, start_time, duration))

print(f"Total de notas mapeadas para lanes: {len(notes)}")

# Cria o arquivo MIDI
midi = pretty_midi.PrettyMIDI()
other_instr = pretty_midi.Instrument(program=81, is_drum=False, name="GUITAR_EXPERT")

for note_num, start, dur in notes:
    note = pretty_midi.Note(velocity=100, pitch=note_num, start=start, end=start + dur)
    other_instr.notes.append(note)

midi.instruments.append(other_instr)

output_midi_path = 'guitar_chart_output.mid'
midi.write(output_midi_path)
print(f"MIDI salvo como: {output_midi_path}")