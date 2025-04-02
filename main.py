import separador
import paramidi

instrumentos = separador('teste.mp3')

midis = {}

for nome, caminho_wav in instrumentos.items():
    midi_path = paramidi(caminho_wav)
    midis[nome] = midi_path
    print(f'{nome} -> {midi_path}')