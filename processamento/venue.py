from mido import MidiTrack, MetaMessage


def adicionar_trilha_venue(midi, duracao_musica, ticks_per_beat, bpm=120):
    """
    Cria uma trilha VENUE com efeitos visuais para Rock Band.
    Adiciona luzes, câmeras e fogos automaticamente ao longo da música.
    """
    print("🎥 Adicionando efeitos visuais na trilha VENUE...")
    efeitos = [
        "lighting (verse)", "lighting (chorus)", "lighting (ambient)",
        "camera_close", "camera_pan_up", "camera_pan_down",
        "fog_on", "fog_off", "blackout"
    ]

    intervalo = 4.0  # segundos entre efeitos
    total_eventos = int(duracao_musica // intervalo)

    track = MidiTrack()
    track.append(MetaMessage('track_name', name='VENUE', time=0))

    last_tick = 0
    for i in range(total_eventos):
        tempo = i * intervalo
        tick = int(tempo * (ticks_per_beat * bpm / 60))
        delta = tick - last_tick
        efeito = efeitos[i % len(efeitos)]
        track.append(MetaMessage('text', text=efeito, time=delta))
        last_tick = tick

    midi.tracks.append(track)
    print(f"✅ {total_eventos} efeitos visuais adicionados na trilha VENUE.")
