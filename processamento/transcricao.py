import soundfile as sf
from pathlib import Path

def transcrever_para_midi(caminho_audio):
    caminho_audio = Path(caminho_audio).resolve()
    print("🔍 Recebido para transcrição:", caminho_audio)
    print("📂 Existe:", caminho_audio.exists())
    print("📁 É arquivo:", caminho_audio.is_file())

    try:
        audio, sr = sf.read(str(caminho_audio))
        print(f"✅ Áudio carregado com sucesso ({sr} Hz, {audio.shape})")
    except RuntimeError as e:
        print("❌ Erro ao carregar com soundfile:", e)
        return None
