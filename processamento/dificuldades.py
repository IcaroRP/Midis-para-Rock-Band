from copy import deepcopy


def simplificar_dificuldade(track, nivel='easy'):
    """
    Reduz a densidade de notas de uma track para uma dificuldade específica.
    easy = 25% das notas
    medium = 50%
    hard = 75%
    """
    nivel_map = {
        'easy': 0.25,
        'medium': 0.5,
        'hard': 0.75,
        'expert': 1.0
    }
    fator = nivel_map.get(nivel, 0.5)

    notas_originais = [msg for msg in track if msg.type == 'note_on' and msg.velocity > 0]
    total = len(notas_originais)
    manter = int(total * fator)

    notas_filtradas = set(notas_originais[i] for i in range(0, total, max(1, total // manter)))

    nova_track = []
    for msg in track:
        if msg.type == 'note_on' and msg.velocity > 0:
            if msg in notas_filtradas:
                nova_track.append(msg)
            else:
                nova_track.append(msg.copy(velocity=0))  # mute nota
        else:
            nova_track.append(msg)

    return nova_track


def gerar_dificuldades(midi):
    """
    Cria trilhas duplicadas com nomes como PART GUITAR EASY, MEDIUM, HARD
    com densidade de notas reduzida.
    """
    novas_tracks = []
    for track in midi.tracks:
        nome = None
        for msg in track:
            if msg.type == 'track_name' and msg.name.startswith('PART'):
                nome = msg.name
                break
        if not nome:
            continue

        for nivel in ['easy', 'medium', 'hard']:
            nova = deepcopy(track)
            nova_nome = f"{nome} {nivel.upper()}"
            for msg in nova:
                if msg.type == 'track_name':
                    msg.name = nova_nome
            nova_msgs = simplificar_dificuldade(nova, nivel)
            nova[:] = nova_msgs
            novas_tracks.append(nova)

    midi.tracks.extend(novas_tracks)
    print("🎮 Dificuldades EASY/MEDIUM/HARD geradas com sucesso.")