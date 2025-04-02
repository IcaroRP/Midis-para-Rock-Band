import librosa
from mido import MidiTrack, MetaMessage
from sklearn.cluster import KMeans

def adicionar_marcadores_eventos(midi, audio_path):
    y, sr = librosa.load(audio_path)
    y_harmonic, _ = librosa.effects.hpss(y)
    chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)

    n_secoes = 6
    kmeans = KMeans(n_clusters=n_secoes, random_state=0).fit(chroma.T)
    boundaries = librosa.segment.agglomerative(chroma.T, k=n_secoes)
    bound_times = librosa.frames_to_time(boundaries, sr=sr)

    nomes_secoes = ['[intro]', '[verse]', '[chorus]', '[verse2]', '[solo]', '[outro]']

    track = MidiTrack()
    track.append(MetaMessage('track_name', name='EVENTS', time=0))

    last_tick = 0
    ticks_per_beat = midi.ticks_per_beat
    tempo = 120

    for i, t in enumerate(bound_times[:len(nomes_secoes)]):
        tick = int(t * (ticks_per_beat * tempo / 60))
        delta = tick - last_tick
        track.append(MetaMessage('marker', text=nomes_secoes[i], time=delta))
        last_tick = tick

    midi.tracks.append(track)
    print("Trilha de EVENTS com marcadores por IA adicionada.")

def adicionar_trilha_venue(midi, audio_path):
    y, sr = librosa.load(audio_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    boundaries = librosa.segment.agglomerative(onset_env.reshape(-1, 1), k=6)
    bound_times = librosa.frames_to_time(boundaries, sr=sr)

    nomes_secoes = ['verse', 'verse', 'chorus', 'verse', 'bridge', 'outro']
    efeitos_camera = ['[camera_closeup]', '[camera_pan]', '[camera_zoom]', '[camera_closeup]', '[camera_pan]', '[camera_zoom]']
    efeitos_luz = [f'[lighting ({nome})]' for nome in nomes_secoes]

    track = MidiTrack()
    track.append(MetaMessage('track_name', name='VENUE', time=0))

    ticks_per_beat = midi.ticks_per_beat
    last_tick = 0

    for i, t in enumerate(bound_times[:len(nomes_secoes)]):
        tick = int(t * (ticks_per_beat * tempo / 60))
        delta = tick - last_tick
        track.append(MetaMessage('marker', text=efeitos_luz[i], time=delta))
        track.append(MetaMessage('marker', text=efeitos_camera[i], time=0))
        last_tick = tick

    midi.tracks.append(track)
    print("Trilha de VENUE adicionada.")
