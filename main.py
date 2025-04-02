import separador
import transcrever

instrumentos = separador('teste.mp3')

midis = {}

for nome, caminho_wav in instrumentos.items():
    midi_path = transcrever(caminho_wav)
    midis[nome] = midi_path
    print(f'{nome} -> {midi_path}')