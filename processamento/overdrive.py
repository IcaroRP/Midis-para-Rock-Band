from mido import MetaMessage, MidiTrack


def adicionar_star_power(midi, ticks_per_beat, bpm=120, duracao_minima=2.0):
    """
    Adiciona seções de star power/overdrive como marcadores na track EVENTS.
    Escolhe regiões com poucas notas e sustains longos para marcar.
    """
    print("⚡ Adicionando star power/overdrive...")

    # Criar nova track ou encontrar EVENTS existente
    track_eventos = None
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'track_name' and msg.name.upper() == 'EVENTS':
                track_eventos = track
                break

    if not track_eventos:
        track_eventos = MidiTrack()
        track_eventos.append(MetaMessage('track_name', name='EVENTS', time=0))
        midi.tracks.append(track_eventos)

    # Recolher possíveis seções com base nos instrumentos
    marcadores = []
    for track in midi.tracks:
        if any(msg.type == 'track_name' and msg.name.startswith("PART") for msg in track):
            tempo_aberto = None
            ticks = 0
            for msg in track:
                if msg.type == 'note_on' and msg.velocity > 0:
                    if tempo_aberto is None:
                        tempo_aberto = ticks
                if msg.type in ['note_off', 'note_on'] and msg.velocity == 0:
                    if tempo_aberto is not None:
                        dur = ticks - tempo_aberto
                        dur_seg = dur / (ticks_per_beat * bpm / 60)
                        if dur_seg >= duracao_minima:
                            marcadores.append((tempo_aberto, "[prc_sp]"))
                        tempo_aberto = None
                ticks += msg.time

    # Adiciona marcadores de SP à track EVENTS
    marcadores.sort()
    last_tick = 0
    for tick, texto in marcadores:
        delta = tick - last_tick
        track_eventos.append(MetaMessage('marker', text=texto, time=delta))
        last_tick = tick

    print(f"✅ {len(marcadores)} star power adicionados na track EVENTS.")