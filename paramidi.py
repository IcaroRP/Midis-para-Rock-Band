from basic_pitch.inference import predict_and_save
from pathlib import Path

def to_midi(audio, saida='midis'):
    audio = Path(audio)
    saida = Path(saida)
    saida.mkdir(parents=True, exist_ok=True)

    predict_and_save(
        [audio],
        output_directory=saida,
        save_midi=True,
        save_model_outputs=False,
        save_notes=False,
    )

    return saida / (audio.stem + '.mid')