from mido import MidiTrack, MetaMessage


def renomear_trilhas_para_rockband(midi):
    """
    Renomeia trilhas existentes no MIDI para padrão Rock Band customs.
    Exemplo: VOCALS → PART VOCALS, BASS → PART BASS, etc.
    """
    mapa_nomes = {
        'VOCALS': 'PART VOCALS',
        'BASS': 'PART BASS',
        'DRUMS': 'PART DRUMS',
        'OTHER': 'PART GUITAR',
        'BEAT': 'BEAT',
        'EVENTS': 'EVENTS',
        'MODULACOES': 'EVENTS'  # Opcional: consolidar em EVENTS
    }

    for track in midi.tracks:
        for msg in track:
            if msg.type == 'track_name':
                nome_original = msg.name.upper()
                nome_novo = mapa_nomes.get(nome_original, msg.name)
                msg.name = nome_novo
                break

    print("🎮 Trilhas renomeadas para formato Rock Band.")
    return midi
