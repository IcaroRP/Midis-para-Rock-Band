import transcrever, midis, separador

def pipeline_completo(audio_mp3):
    instrumentos = separador(audio_mp3)

    midis_gerados = {}
    for nome, caminho_wav in instrumentos.items():
        midi_path = transcrever(caminho_wav)
        midis_gerados[nome] = midi_path

    midis(midis_gerados, audio_mp3, saida='saida_final_c3.mid')