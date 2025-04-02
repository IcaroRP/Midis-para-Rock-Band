import os
from spleeter.separator import Separator

def separar_instrumentos(arquivo_audio, pasta_saida='saida_spleeter'):
    separator = Separator('spleeter:5stems')
    separator.separate_to_file(arquivo_audio, pasta_saida)

    base = os.path.splitext(os.path.basename(arquivo_audio))[0]
    caminho = os.path.join(pasta_saida, base)

    instrumentos = {
        'vocal': os.path.join(caminho, 'vocal.wav'),
        'drums': os.path.join(caminho, 'drums.wav'),
        'bass': os.path.join(caminho, 'bass.wav'),
        'guitar': os.path.join(caminho, 'guitar.wav'),
    }
    return instrumentos