import os
from spleeter.separator import Separator

def separar_instrumentos(audio, saida='saida_spleeter'):
    separator = Separator('spleeter:5stems')
    separator.separate_to_file(audio, saida)

    base = os.path.splitext(os.path.basename(audio))[0]
    caminho = os.path.join(saida, base)

    instrumentos = {
        'vocal': os.path.join(caminho, 'vocal.wav'),
        'drums': os.path.join(caminho, 'drums.wav'),
        'bass': os.path.join(caminho, 'bass.wav'),
        'guitar': os.path.join(caminho, 'guitar.wav'),
    }
    return instrumentos