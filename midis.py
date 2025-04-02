from tempo import adicionar_trilha_tempo_dinamico
from mido import MidiFile, MidiTrack, MetaMessage

def importar_trilha(midi_path):
    midi = MidiFile(midi_path)
    for track in midi.tracks:
        if any(msg.type in ['note_on', 'note_off'] for msg in track):
            return track
    return None

def criar_midi_c3(midis_entrada, caminho_audio_original, saida='c3_chart.mid'):
    novo_midi = MidiFile(ticks_per_beat=480)

    trilhas_nomeadas = {
        'guitar': 'PART GUITAR',
        'bass': 'PART BASS',
        'drums': 'PART DRUMS',
        'vocals': 'PART VOCALS',
        'piano': 'PART KEYS',
        'other': 'PART KEYS 2',
    }

    for nome_instr, caminho_midi in midis_entrada.items():
        if nome_instr not in trilhas_nomeadas:
            continue

        trilha = importar_trilha(caminho_midi)
        if trilha:
            nova_trilha = MidiTrack()
            nova_trilha.append(MetaMessage('track_name', name=trilhas_nomeadas[nome_instr], time=0))
            nova_trilha.extend(trilha)
            novo_midi.tracks.append(nova_trilha)
            print(f"Adicionada trilha: {trilhas_nomeadas[nome_instr]}")

    adicionar_trilha_tempo_dinamico(novo_midi, caminho_audio_original)
    novo_midi.save(saida)
    print(f"MIDI combinado salvo como: {saida}")