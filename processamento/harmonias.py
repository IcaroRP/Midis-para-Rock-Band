from mido import MidiFile, MidiTrack

def separar_vocais_em_harmonias(midi_path):
    midi = MidiFile(midi_path)
    track = midi.tracks[1]  # basic-pitch geralmente coloca as notas na segunda track

    notas_principais = MidiTrack()
    harmonia_1 = MidiTrack()
    harmonia_2 = MidiTrack()

    notas_por_tempo = {}

    for msg in track:
        if msg.type in ['note_on', 'note_off']:
            pitch = msg.note
            if pitch not in notas_por_tempo:
                notas_por_tempo[pitch] = 0
            notas_por_tempo[pitch] += 1

    principais = sorted(notas_por_tempo, key=notas_por_tempo.get, reverse=True)[:1]
    harm_1 = sorted(notas_por_tempo, key=notas_por_tempo.get, reverse=True)[1:2]
    harm_2 = sorted(notas_por_tempo, key=notas_por_tempo.get, reverse=True)[2:3]

    for msg in track:
        if msg.type in ['note_on', 'note_off']:
            if msg.note in principais:
                notas_principais.append(msg)
            elif msg.note in harm_1:
                harmonia_1.append(msg)
            elif msg.note in harm_2:
                harmonia_2.append(msg)

    return notas_principais, harmonia_1, harmonia_2