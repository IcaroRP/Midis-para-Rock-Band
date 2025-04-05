import librosa
from mido import MidiTrack, MetaMessage
from sklearn.cluster import KMeans

def adicionar_marcadores_eventos(midi, audio_path):
    y, sr = librosa.load(audio_path)
    y_harmonic, _ = librosa.effects.hpss(y)
    chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)

    n_secoes = 6
    kmeans = KMeans(n_clusters=n_secoes, random_state=0, n_init=10).fit(chroma.T)
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
    import librosa
    import numpy as np
    from mido import MidiTrack, MetaMessage
    from sklearn.cluster import AgglomerativeClustering

    y, sr = librosa.load(audio_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_env = onset_env.reshape(-1, 1)

    if onset_env.shape[0] < 2:
        print("⚠️ Número insuficiente de amostras para clusterização. Evento único adicionado.")
        boundaries = [0, onset_env.shape[0] - 1]  # Apenas um início e fim
    else:
        # Aplica clusterização
        clusterer = AgglomerativeClustering(n_clusters=6)
        clusterer.fit(onset_env)
        labels = clusterer.labels_
        # Encontra as fronteiras
        boundaries = [0]
        for i in range(1, len(labels)):
            if labels[i] != labels[i-1]:
                boundaries.append(i)
        boundaries.append(len(labels) - 1)

    times = librosa.frames_to_time(boundaries, sr=sr)
    ticks_per_beat = midi.ticks_per_beat

    track = MidiTrack()
    track.append(MetaMessage('track_name', name='EVENTS', time=0))

    last_tick = 0
    for i, t in enumerate(times):
        tick = int(librosa.time_to_frames(t, sr=sr) * ticks_per_beat / 43)  # 43 ≈ hop_length
        delta = tick - last_tick
        track.append(MetaMessage('marker', text=f'EVENT {i+1}', time=delta))
        last_tick = tick

    midi.tracks.append(track)
    print("Trilha de EVENTS com marcadores por IA adicionada.")