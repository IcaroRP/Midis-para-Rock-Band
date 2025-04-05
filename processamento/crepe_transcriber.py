import crepe
import librosa
import numpy as np
import pretty_midi


def transcrever_audio_para_instrumento(audio_path, instrument_name="INSTRUMENT", program_number=0,
                                       confidence_threshold=0.4, min_note_length=0.1):
    """
    Transcreve um arquivo de áudio para uma track MIDI usando CREPE.

    :param audio_path: Caminho para o arquivo .wav
    :param instrument_name: Nome da trilha MIDI (ex: VOCALS, BASS)
    :param program_number: Programa MIDI (instrumento General MIDI)
    :param confidence_threshold: Confiança mínima para considerar pitch
    :param min_note_length: Duração mínima da nota (em segundos)
    :return: pretty_midi.Instrument
    """
    print(f"🎧 Carregando áudio: {audio_path}")
    y, sr = librosa.load(audio_path, sr=16000, mono=True)
    dur_audio = len(y) / sr

    # Parâmetros especiais para vocais
    if instrument_name.lower() == "vocals":
        confidence_threshold = 0.6
        min_note_length = 0.15
        start_offset = -0.05
        smoothing_window = 5
    else:
        start_offset = 0.0
        smoothing_window = 1

    print(f"🎼 Rodando CREPE para: {instrument_name}")
    timestamps, frequencies, confidences, activation = crepe.predict(
        y, sr, viterbi=True, step_size=10
    )

    if smoothing_window > 1:
        frequencies = np.convolve(frequencies, np.ones(smoothing_window)/smoothing_window, mode='same')

    notes = []
    current_pitch = None
    start_time = None
    last_valid_time = 0

    print("🎵 Segmentando notas...")
    for i in range(len(frequencies)):
        pitch = frequencies[i]
        conf = confidences[i]
        time = timestamps[i]

        if conf < confidence_threshold:
            pitch = 0

        midi_note = int(np.round(69 + 12 * np.log2(pitch / 440))) if pitch > 0 else None

        if pitch > 0:
            last_valid_time = time

        if current_pitch is None:
            if midi_note is not None:
                current_pitch = midi_note
                start_time = time + start_offset
        else:
            if midi_note != current_pitch:
                end_time = time
                duration = end_time - start_time
                if duration >= min_note_length:
                    notes.append((current_pitch, max(start_time, 0.0), duration))
                current_pitch = midi_note
                start_time = time + start_offset if midi_note is not None else None

    if current_pitch is not None and start_time is not None:
        end_time = last_valid_time + 0.05
        duration = end_time - start_time
        if duration >= min_note_length and end_time <= dur_audio:
            notes.append((current_pitch, max(start_time, 0.0), duration))

    print(f"🎹 Total de notas detectadas para {instrument_name} (pré-processamento): {len(notes)}")

    notas_filtradas = []
    for note in notes:
        if not notas_filtradas:
            notas_filtradas.append(note)
            continue
        last_note = notas_filtradas[-1]
        if note[0] == last_note[0] and note[1] - (last_note[1] + last_note[2]) < 0.03:
            nova_dur = (note[1] + note[2]) - last_note[1]
            notas_filtradas[-1] = (last_note[0], last_note[1], nova_dur)
        elif note[1] - (last_note[1] + last_note[2]) >= 0.03:
            notas_filtradas.append(note)

    print(f"✅ Notas após pós-processamento: {len(notas_filtradas)}")

    instrument = pretty_midi.Instrument(program=program_number, is_drum=False, name=instrument_name)

    for note_num, start, dur in notas_filtradas:
        end = start + dur
        if start < dur_audio and end > start:
            instrument.notes.append(pretty_midi.Note(velocity=100, pitch=note_num, start=start, end=end))

    return instrument