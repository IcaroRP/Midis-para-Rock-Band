import librosa
import mido
from mido import MidiTrack, MetaMessage
from sklearn.cluster import KMeans

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

def adicionar_trilha_beat(novo_midi, caminho_audio):
    y, sr = librosa.load(caminho_audio)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    beat_track = MidiTrack()
    beat_track.append(MetaMessage('track_name', name='BEAT', time=0))

    ticks_per_beat = novo_midi.ticks_per_beat
    last_tick = 0
    tick_pos = 0

    # Assume 4/4 como time signature padrão
    beat_track.append(MetaMessage('time_signature', numerator=4, denominator=4, time=0))

    for i, t in enumerate(beat_times):
        # Marca cada batida como um delta de tempo (em ticks)
        delta_time = t - (beat_times[i - 1] if i > 0 else 0)
        tick = int(delta_time * (ticks_per_beat * tempo / 60))
        beat_track.append(MetaMessage('marker', text=f'BAR {i+1}', time=tick))
        tick_pos += tick

    novo_midi.tracks.insert(1, beat_track)
    print(f"Trilha de BEAT com compassos adicionada.")

def adicionar_marcadores_eventos(novo_midi, caminho_audio):
    y, sr = librosa.load(caminho_audio)
    y_harmonic, _ = librosa.effects.hpss(y)
    chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)

    n_secoes = 6
    kmeans = KMeans(n_clusters=n_secoes, random_state=0).fit(chroma.T)
    boundaries = librosa.segment.agglomerative(chroma.T, k=n_secoes)
    bound_times = librosa.frames_to_time(boundaries, sr=sr)

    nomes_secoes = ['[intro]', '[verse]', '[chorus]', '[verse2]', '[solo]', '[outro]']

    events_track = MidiTrack()
    events_track.append(MetaMessage('track_name', name='EVENTS', time=0))

    last_tick = 0
    ticks_per_beat = novo_midi.ticks_per_beat
    tempo = 120

    for i, t in enumerate(bound_times[:len(nomes_secoes)]):
        tick = int(t * (ticks_per_beat * tempo / 60))
        delta = tick - last_tick
        events_track.append(MetaMessage('marker', text=nomes_secoes[i], time=delta))
        last_tick = tick

    novo_midi.tracks.append(events_track)
    print("Trilha de EVENTS com marcadores por IA adicionada.")

def adicionar_trilha_venue(novo_midi, caminho_audio):
    y, sr = librosa.load(caminho_audio)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='frames')
    boundaries = librosa.segment.agglomerative(onset_env.reshape(-1, 1), k=6)
    bound_times = librosa.frames_to_time(boundaries, sr=sr)

    nomes_secoes = ['verse', 'verse', 'chorus', 'verse', 'bridge', 'outro']
    efeitos_camera = ['[camera_closeup]', '[camera_pan]', '[camera_zoom]', '[camera_closeup]', '[camera_pan]', '[camera_zoom]']
    efeitos_luz = [f'[lighting ({nome})]' for nome in nomes_secoes]

    venue_track = MidiTrack()
    venue_track.append(MetaMessage('track_name', name='VENUE', time=0))

    ticks_per_beat = novo_midi.ticks_per_beat
    last_tick = 0

    for i, t in enumerate(bound_times[:len(nomes_secoes)]):
        tick = int(t * (ticks_per_beat * tempo / 60))
        delta = tick - last_tick

        venue_track.append(MetaMessage('marker', text=efeitos_luz[i], time=delta))
        venue_track.append(MetaMessage('marker', text=efeitos_camera[i], time=0))
        last_tick = tick

    novo_midi.tracks.append(venue_track)
    print("Trilha de VENUE adicionada.")