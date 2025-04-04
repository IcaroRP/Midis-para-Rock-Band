import os
from spleeter.separator import Separator

def separar_instrumentos(arquivo_audio):
    # Cria o separador com multiprocessing desativado para evitar erro no Windows
    separator = Separator("spleeter:5stems")

    # Nome base do arquivo (sem extensão)
    nome_base = os.path.splitext(os.path.basename(arquivo_audio))[0]

    # Pasta base onde o Spleeter salvará os resultados
    pasta_saida = os.path.join("saida_spleeter")

    # Roda o separador (Spleeter criará subpasta com nome_base automaticamente)
    separator.separate_to_file(arquivo_audio, pasta_saida)

    # Caminho final onde os arquivos separados estarão
    pasta_final = os.path.join(pasta_saida, nome_base)

    # Lista de instrumentos gerados pelo modelo 5stems
    instrumentos = ["vocals", "drums", "bass", "piano", "other"]

    # Cria dicionário com os caminhos para cada .wav
    caminhos = {
        inst: os.path.abspath(os.path.join(pasta_final, f"{inst}.wav"))
        for inst in instrumentos
    }

    return caminhos