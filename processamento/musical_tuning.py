import numpy as np
import pretty_midi
from music21 import scale, pitch


def obter_notas_da_escala(tonica: str, modo: str):
    """Retorna uma lista de notas válidas (em string) para a escala fornecida."""
    modo = modo.lower()
    if modo == "major":
        esc = scale.MajorScale(tonica)
    elif modo == "minor":
        esc = scale.MinorScale(tonica)
    else:
        raise ValueError("Modo musical inválido. Use 'major' ou 'minor'.")

    notas = [esc.pitchFromDegree(i+1).name for i in range(7)]
    return notas


def ajustar_nota_para_escala(nota_midi, notas_validas):
    """Corrige a nota MIDI para a nota mais próxima dentro da escala."""
    p = pitch.Pitch()
    p.midi = nota_midi
    nome_original = p.name

    if nome_original in notas_validas:
        return nota_midi  # já está na escala

    # Caso contrário, encontra a nota da escala mais próxima
    menor_dif = float('inf')
    nota_ajustada = nota_midi
    for nome in notas_validas:
        alvo = pitch.Pitch(nome)
        dif = abs(alvo.midi - nota_midi)
        if dif < menor_dif:
            menor_dif = dif
            nota_ajustada = alvo.midi

    return nota_ajustada


def afinar_midi_para_escala(midi: pretty_midi.PrettyMIDI, tonica: str, modo: str):
    """Modifica as notas do MIDI para pertencerem à escala informada."""
    notas_validas = obter_notas_da_escala(tonica, modo)
    print(f"🎯 Afinando para escala: {tonica} {modo} → notas válidas: {notas_validas}")

    for instr in midi.instruments:
        for note in instr.notes:
            original = note.pitch
            ajustada = ajustar_nota_para_escala(note.pitch, notas_validas)
            if original != ajustada:
                print(f"♫ Corrigido: {original} → {ajustada}")
                note.pitch = int(ajustada)

    return midi
