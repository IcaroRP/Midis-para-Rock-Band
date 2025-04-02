from basic_pitch.inference import predict_and_save
from pathlib import Path

def transcrever_para_midi(audio_path, pasta_saida='midis'):
    audio_path = Path(audio_path)
    pasta_saida = Path(pasta_saida)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    predict_and_save(
        [audio_path],
        output_directory=pasta_saida,
        save_midi=True,
        save_model_outputs=False,
        save_notes=False,
    )

    return pasta_saida / (audio_path.stem + '.mid')