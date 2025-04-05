import os
import crepe
import librosa
import numpy as np
import pretty_midi
import soundfile as sf

# Caminho para o arquivo de voz isolada (vocals.wav)
audio_path = 'saida_demucs/htdemucs/audio_example_mono/vocals.wav'

# Carrega o áudio
print("Carregando áudio...")
y, sr = librosa.load(audio_path, sr=16000, mono=True)  # CREPE funciona melhor com 16kHz

# Usa o CREPE para detectar o pitch
timestamps, frequencies, confidences, activation = crepe.predict(y, sr, viterbi=True, step_size=10)

# Parâmetros de segmentação
confidence_threshold = 0.4  # Confiança mínima para considerar uma nota
min_note_length = 0.1       # Em segundos

notes = []
current_pitch = None
start_time = None

print("Segmentando notas...")
for i in range(len(frequencies)):
    pitch = frequencies[i]
    conf = confidences[i]
    time = timestamps[i]

    if conf < confidence_threshold:
        pitch = 0  # Considera como silêncio

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

# Finaliza a última nota
if current_pitch is not None and start_time is not None:
    end_time = timestamps[-1]
    duration = end_time - start_time
    if duration >= min_note_length:
        notes.append((current_pitch, start_time, duration))

print(f"Total de notas detectadas: {len(notes)}")

# Cria o arquivo MIDI
midi = pretty_midi.PrettyMIDI()
voice_instr = pretty_midi.Instrument(program=0, is_drum=False, name="VOCALS")

for note_num, start, dur in notes:
    note = pretty_midi.Note(velocity=100, pitch=note_num, start=start, end=start+dur)
    voice_instr.notes.append(note)

midi.instruments.append(voice_instr)

output_midi_path = 'vocal_output.mid'
midi.write(output_midi_path)
print(f"MIDI salvo como: {output_midi_path}")