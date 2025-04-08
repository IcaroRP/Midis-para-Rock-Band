import librosa
import numpy as np
import music21


def detectar_escala_musical(audio_path):
    """
    Analisa o áudio e retorna a tonalidade estimada (ex: C major, G# minor).
    Usa análise de cromas e o music21 para maior precisão musical.
    """
    print(f"🎼 Estimando escala musical de: {audio_path}")
    
    y, sr = librosa.load(audio_path, sr=22050)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)

    # Média ao longo do tempo para obter perfil harmônico geral
    chroma_avg = np.mean(chroma, axis=1)

    # Cria uma partitura com base nas notas mais frequentes
    s = music21.stream.Stream()
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 
                  'F#', 'G', 'G#', 'A', 'A#', 'B']

    for i, intensity in enumerate(chroma_avg):
        if intensity > np.max(chroma_avg) * 0.3:
            n = music21.note.Note(note_names[i])
            s.append(n)

    # Usa o analisador de tonalidade do music21
    key = s.analyze('key')
    print(f"🔍 Tonalidade estimada: {key.tonic.name} {key.mode}")
    return key.tonic.name, key.mode


# Exemplo de uso direto
if __name__ == "__main__":
    caminho = "saida_demucs/htdemucs/audio_example_mono/other.wav"
    detectar_escala_musical(caminho)