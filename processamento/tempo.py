import librosa
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
    last_tick = 0
    last_time = 0

    for i, t in enumerate(beat_times[:len(tempos_bpm)]):
        delta_time = t - last_time
        tick = int(delta_time * (ticks_per_beat * tempo / 60)) + last_tick
        midi_tempo = int(60_000_000 / tempos_bpm[i])
        tempos_midi.append((tick, midi_tempo))
        last_tick = tick
        last_time = t

    return tempos_midi

def adicionar_trilha_tempo_dinamico(midi, audio_path):
    tempos = detectar_tempos(audio_path, ticks_per_beat=midi.ticks_per_beat)
    tempo_track = MidiTrack()
    tempo_track.append(MetaMessage('track_name', name='TEMPO', time=0))

    last_tick = 0
    for tick, tempo in tempos:
        delta = tick - last_tick
        tempo_track.append(MetaMessage('set_tempo', tempo=tempo, time=delta))
        last_tick = tick

    midi.tracks.insert(0, tempo_track)
    print("Trilha de tempo dinâmica adicionada.")

def adicionar_trilha_beat(midi, audio_path):
    y, sr = librosa.load(audio_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    beat_track = MidiTrack()
    beat_track.append(MetaMessage('track_name', name='BEAT', time=0))
    beat_track.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    ticks_per_beat = midi.ticks_per_beat
    last_tick = 0

    for i, t in enumerate(beat_times):
        delta_time = t - (beat_times[i - 1] if i > 0 else 0)
        tick = int(delta_time * (ticks_per_beat * tempo / 60))
        beat_track.append(MetaMessage('marker', text=f'BAR {i+1}', time=tick))
        last_tick += tick

    midi.tracks.insert(1, beat_track)
    print("Trilha de BEAT com compassos adicionada.")
