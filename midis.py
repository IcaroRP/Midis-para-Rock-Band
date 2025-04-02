import mido

from mido import MidiFile, MidiTrack, MetaMessage

def importar_trilha(midi_path):
    #Carrega a primeira trilha com eventos de nota de um midi básico.
    midi = MidiFile(midi_path)
    for track in midi.tracks:
        if any(msg.type in ['note_on', 'note_off'] for msg in track):
            return track
    return None

def criar_midi(midis_entrada, saida = 'c3_chart.mid'):
    novo_midi = MidiFile(ticks_per_beat=480) #padrão Rock Band

    trilhas = {
        'guitar': 'PART GUITAR',
        'bass': 'PART BASS',
        'drums': 'PART DRUMS',
        'vocals': 'PART VOCALS',
    }

    for nome_instr, caminho_midi in midis_entrada.items():
        if nome_instr not in trilhas:
            continue

        trilha = importar_trilha(caminho_midi)
        if trilha:
            nova_trilha = MidiTrack()
            nova_trilha.append(MetaMessage('track_name', name=trilhas[nome_instr], time=0))
            nova_trilha.tracks.append(nova_trilha)
            print(f'Adicionada trilha: {trilhas[nome_instr]}')
    
    #Adiciona trilha vazia para tempo ou marcações
    tempo_track = MidiTrack()
    tempo_track.append(MetaMessage('track_name', name='TEMPO', time=0))
    tempo_track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(120), time=0)) # define o tempo base (120 BPM)
    novo_midi.tracks.insert(0, tempo_track)

    novo_midi.save(saida)
    print(f"MIDI combinado salvo com {saida}")