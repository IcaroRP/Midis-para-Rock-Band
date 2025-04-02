import librosa
import mido
from mido import MidiTrack, MetaMessage

def detectar_tempos(audio_path, ticks_per_beat=480):
    y, sr = librosa.load(audio_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    tempos_bpm = []
    for i in range(1, len(beat_times)):
        intervalo = beat_times[i] - beat_times[i - 1]
        bpm = 60.0 / intervalo if intervalo > 0 else tempo
        tempos_bpm.append(bpm)

    tempos_midi = []
    ticks = 0
    last_tick = 0
    last_time = 0

    for i, t in enumerate(beat_times[:len(tempos_bpm)]):
        delta_time = t - last_time
        tick = int(delta_time * (ticks_per_beat * tempo / 60)) + last_tick
        midi_tempo = mido.bpm2tempo(tempos_bpm[i])
        tempos_midi.append((tick, midi_tempo))
        last_tick = tick
        last_time = t

    return tempos_midi

def adicionar_trilha_tempo_dinamico(novo_midi, caminho_audio):
    tempos = detectar_tempos(caminho_audio, ticks_per_beat=novo_midi.ticks_per_beat)
    tempo_track = MidiTrack()
    tempo_track.append(MetaMessage('track_name', name='TEMPO', time=0))

    last_tick = 0
    for tick, tempo_valor in tempos:
        delta = tick - last_tick
        tempo_track.append(MetaMessage('set_tempo', tempo=tempo_valor, time=delta))
        last_tick = tick

    novo_midi.tracks.insert(0, tempo_track)
    print("Trilha de tempo dinâmica adicionada.")