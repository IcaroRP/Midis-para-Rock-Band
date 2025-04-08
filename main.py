import os
import pretty_midi
from mido import MidiFile
import io

from processamento.instrumentos import separar_instrumentos
from processamento.crepe_transcriber import transcrever_audio_para_instrumento
from processamento.tempo import adicionar_trilha_tempo_dinamico, adicionar_trilha_beat
from processamento.eventos import adicionar_marcadores_eventos
from processamento.utils import get_ticks_per_beat_from_pretty_midi
from processamento.key_estimation import detectar_escala_musical
from processamento.musical_tuning import afinar_midi_para_escala


def pipeline_completo(audio_original):
    print(f"\n🎬 Iniciando pipeline para: {audio_original}")

    # 1. Separar instrumentos com Demucs
    instrumentos = separar_instrumentos(audio_original)
    if not instrumentos:
        print("❌ Nenhum instrumento separado. Encerrando pipeline.")
        return

    # 2. Iniciar objeto PrettyMIDI final
    midi_pretty = pretty_midi.PrettyMIDI()

    # 3. Transcrever cada instrumento encontrado
    mapa_programas = {
        "vocals": 0,    # Piano
        "bass": 34,     # Fingered Bass
        "drums": 118,   # Synth Drum
        "other": 81     # Lead 2
    }

    for nome, caminho in instrumentos.items():
        program = mapa_programas.get(nome, 0)
        instrumento_midi = transcrever_audio_para_instrumento(
            caminho,
            instrument_name=nome.upper(),
            program_number=program
        )
        midi_pretty.instruments.append(instrumento_midi)

    # 4. Detectar escala musical com base no stem 'other' (caso exista)
    if "other" in instrumentos:
        tonica, modo = detectar_escala_musical(instrumentos["other"])
        midi_pretty = afinar_midi_para_escala(midi_pretty, tonica, modo)

    # 5. Converter PrettyMIDI para mido.MidiFile para adicionar tempo/eventos
    buffer = io.BytesIO()
    midi_pretty.write(buffer)
    buffer.seek(0)
    midi_mido = MidiFile(file=buffer)

    # 6. Obter ticks_per_beat dinamicamente via mido
    ticks_per_beat = midi_mido.ticks_per_beat

    # 7. Adicionar trilhas extras com mido
    adicionar_trilha_tempo_dinamico(midi_mido, audio_original, ticks_per_beat)
    adicionar_trilha_beat(midi_mido, audio_original, ticks_per_beat)
    adicionar_marcadores_eventos(midi_mido, audio_original)

    # 8. Salvar MIDI final
    nome_base = os.path.splitext(os.path.basename(audio_original))[0]
    output_path = f"saida_midis/{nome_base}_final.mid"
    os.makedirs("saida_midis", exist_ok=True)
    midi_mido.save(output_path)
    print(f"\n✅ Pipeline finalizado! MIDI salvo em: {output_path}\n")


# Execução direta
if __name__ == "__main__":
    pipeline_completo("audio_example_mono.mp3")