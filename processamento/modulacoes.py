import librosa
import numpy as np
import music21
from mido import MetaMessage, MidiTrack


def detectar_modulacoes(audio_path, janela=2.0):
    """
    Divide o áudio em janelas e estima a tonalidade local de cada uma.
    Retorna uma lista de (tempo_em_segundos, tonalidade, modo).
    """
    y, sr = librosa.load(audio_path, sr=22050)
    dur = librosa.get_duration(y=y, sr=sr)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

    hop_length = int(janela * sr)
    steps = int(dur // janela)
    resultados = []

    for i in range(steps):
        inicio = int(i * janela * sr / 512)
        fim = int((i + 1) * janela * sr / 512)
        trecho = chroma[:, inicio:fim]

        if trecho.shape[1] < 3:
            continue

        media = np.mean(trecho, axis=1)
        notas = [music21.note.Note(music21.pitch.Pitch(i))
                 for i, val in enumerate(media) if val > np.max(media) * 0.3]

        stream = music21.stream.Stream(notas)
        try:
            key = stream.analyze('key')
            tempo_inicio = i * janela
            resultados.append((tempo_inicio, key.tonic.name, key.mode))
        except:
            continue

    return resultados


def adicionar_marcadores_modulacoes(midi, modulacoes, ticks_per_beat, bpm=120):
    """
    Adiciona eventos de modulação ao MIDI como marcadores.
    """
    track = MidiTrack()
    track.append(MetaMessage('track_name', name='MODULACOES', time=0))

    last_tick = 0
    for tempo, tonica, modo in modulacoes:
        tick = int(tempo * (ticks_per_beat * bpm / 60))
        delta = tick - last_tick
        texto = f"Key: {tonica} {modo}"
        track.append(MetaMessage('marker', text=texto, time=delta))
        last_tick = tick

    midi.tracks.append(track)
    print("🎼 Marcadores de modulação adicionados ao MIDI.")
