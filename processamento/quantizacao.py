import pretty_midi
import librosa
import numpy as np


def quantizar_notas_midi(midi: pretty_midi.PrettyMIDI, audio_path: str, tolerancia_ms=50):
    """
    Ajusta levemente o tempo das notas para alinhá-las aos tempos detectados no áudio.
    tolerancia_ms: distância máxima para aplicar a correção (em milissegundos)
    """
    print("🔧 Iniciando quantização leve das notas...")
    y, sr = librosa.load(audio_path, sr=22050)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    tolerancia = tolerancia_ms / 1000.0  # converter para segundos

    for instr in midi.instruments:
        for note in instr.notes:
            tempos_candidatos = [t for t in beat_times if abs(note.start - t) <= tolerancia]
            if tempos_candidatos:
                mais_proximo = min(tempos_candidatos, key=lambda t: abs(t - note.start))
                deslocamento = mais_proximo - note.start
                note.start += deslocamento
                note.end += deslocamento

    print("✅ Quantização concluída. Notas ajustadas para batidas próximas.")
    return midi
