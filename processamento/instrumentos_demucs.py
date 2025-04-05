import os
import subprocess

def separar_com_demucs(arquivo_audio, pasta_saida="saida_demucs"):
    os.makedirs(pasta_saida, exist_ok=True)
    comando = [
        "demucs",
        "--two-stems=vocals",
        "--out", pasta_saida,
        "--device", "cuda",
        arquivo_audio
    ]
    subprocess.run(["demucs", "--device", "cuda", arquivo_audio], check=True)
    print(f"✅ Separação concluída: {arquivo_audio}")
