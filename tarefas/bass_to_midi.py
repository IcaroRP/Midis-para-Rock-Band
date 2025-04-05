import os
import crepe
import librosa
import numpy as np
import pretty_midi
import soundfile as sf

# Caminho para o baixo isolado
bass_path = 'separated/htdemucs/Seven Rings In Hand/bass.wav'

print("Carregando áudio de baixo...")
y, sr = librosa.load(bass_path, sr=16000, mono=True)

print("Analisando pitch com CREPE...")
timestamps, frequencies, confidences, activation = crepe.predict(y, sr, viterbi=True, step_size=10)

confidence_threshold = 0.4
min_note_length = 0.1

notes = []
current_pitch = None
start_time = None

print("Segmentando notas de baixo...")
for i in range(len(frequencies)):
    pitch = frequencies[i]
    conf = confidences[i]
    time = timestamps[i]

    if conf < confidence_threshold:
        pitch = 0

    midi_note = int(np.round(69 + 12 * np.log2(pitch / 440))) if pitch > 0 else None

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

if current_pitch is not None and start_time is not None:
    end_time = timestamps[-1]
    duration = end_time - start_time
    if duration >= min_note_length:
        notes.append((current_pitch, start_time, duration))

print(f"Notas detectadas: {len(notes)}")

# Cria o MIDI
midi = pretty_midi.PrettyMIDI()
bass_instr = pretty_midi.Instrument(program=34, is_drum=False, name="BASS")  # 34 = Fingered Bass

for note_num, start, dur in notes:
    note = pretty_midi.Note(velocity=100, pitch=note_num, start=start, end=start+dur)
    bass_instr.notes.append(note)

midi.instruments.append(bass_instr)

output_midi_path = 'bass_output.mid'
midi.write(output_midi_path)
print(f"MIDI de baixo salvo como: {output_midi_path}")