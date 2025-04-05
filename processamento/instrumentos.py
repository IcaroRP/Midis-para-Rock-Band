import os
import subprocess

def separar_instrumentos(arquivo_audio):
    nome_base = os.path.splitext(os.path.basename(arquivo_audio))[0]
    pasta_saida = os.path.join("separated", "htdemucs", nome_base)

    if not os.path.exists(pasta_saida):
        print(f"🎧 Rodando Demucs para separar: {arquivo_audio}")
        try:
            subprocess.run(["demucs", arquivo_audio], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao rodar Demucs: {e}")
            return {}

    if not os.path.exists(pasta_saida):
        print(f"❌ Pasta de saída do Demucs não encontrada: {pasta_saida}")
        return {}

    instrumentos = ["vocals", "drums", "bass", "other"]

    caminhos = {}
    for inst in instrumentos:
        caminho = os.path.join(pasta_saida, f"{inst}.wav")
        if os.path.exists(caminho):
            caminhos[inst] = os.path.abspath(caminho)
        else:
            print(f"⚠️ Arquivo não encontrado: {caminho}")

    return caminhos
