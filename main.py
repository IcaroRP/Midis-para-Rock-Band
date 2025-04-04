
from processamento.instrumentos import separar_instrumentos
from processamento.transcricao import transcrever_para_midi
from processamento.harmonias import separar_vocais_em_harmonias
from processamento.tempo import adicionar_trilha_tempo_dinamico, adicionar_trilha_beat
from processamento.eventos import adicionar_marcadores_eventos, adicionar_trilha_venue
from processamento.utils import importar_trilha

import mido
from mido import MidiFile, MidiTrack, MetaMessage

trilhas_nomeadas = {
    'bass': 'PART BASS',
    'drums': 'PART DRUMS',
    'piano': 'PART KEYS',
    'other': 'PART GUITAR',  # assumindo que a guitarra está em "other"
}

def criar_midi_c3(midis_entrada, caminho_audio_original, saida='c3_chart.mid'):
    novo_midi = MidiFile(ticks_per_beat=480)

    for nome_instr, caminho_midi in midis_entrada.items():
        if nome_instr == 'vocals':
            notas, harm1, harm2 = separar_vocais_em_harmonias(caminho_midi)

            pista_principal = MidiTrack()
            pista_principal.append(MetaMessage('track_name', name='PART VOCALS', time=0))
            pista_principal.extend(notas)
            novo_midi.tracks.append(pista_principal)

            pista_h1 = MidiTrack()
            pista_h1.append(MetaMessage('track_name', name='HARM1', time=0))
            pista_h1.extend(harm1)
            novo_midi.tracks.append(pista_h1)

            pista_h2 = MidiTrack()
            pista_h2.append(MetaMessage('track_name', name='HARM2', time=0))
            pista_h2.extend(harm2)
            novo_midi.tracks.append(pista_h2)

            print("Vocais principais e harmonias adicionados.")
        elif nome_instr in trilhas_nomeadas:
            trilha = importar_trilha(caminho_midi)
            if trilha:
                nova_trilha = MidiTrack()
                nova_trilha.append(MetaMessage('track_name', name=trilhas_nomeadas[nome_instr], time=0))
                nova_trilha.extend(trilha)
                novo_midi.tracks.append(nova_trilha)
                print(f"Adicionada trilha: {trilhas_nomeadas[nome_instr]}")

    adicionar_trilha_tempo_dinamico(novo_midi, caminho_audio_original)
    adicionar_trilha_beat(novo_midi, caminho_audio_original)
    adicionar_marcadores_eventos(novo_midi, caminho_audio_original)
    adicionar_trilha_venue(novo_midi, caminho_audio_original)

    novo_midi.save(saida)
    print(f"MIDI combinado salvo como: {saida}")

def pipeline_completo(audio_mp3):
    instrumentos = separar_instrumentos(audio_mp3)

    midis_gerados = {}
    for nome, caminho_wav in instrumentos.items():
        print(f"Transcrevendo {nome}: {caminho_wav}")
        midi_path = transcrever_para_midi(caminho_wav)
        if midi_path:
            midis_gerados[nome] = midi_path

    criar_midi_c3(midis_gerados, audio_mp3, saida='saida_final_c3.mid')

if __name__ == "__main__":
    pipeline_completo("audio_example_mono.mp3")
