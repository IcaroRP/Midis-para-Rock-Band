# Midis para Rock Band 🎸

Este projeto tem como objetivo converter áudios em arquivos MIDI compatíveis com jogos estilo Rock Band/Guitar Hero. Ele realiza:

- Separação de instrumentos com **Demucs**
- Transcrição com **CREPE** (alta qualidade de pitch) - Ainda não funcional
- Geração de tracks MIDI (vocals, bass, drums, other)
- Adição de tempo dinâmico, compassos e marcadores de eventos - Quebrado
- Exportação de arquivos `.mid` prontos para charting

---

## ✅ Pré-requisitos

- Python 3.9 ou superior
- [ffmpeg](https://ffmpeg.org/) instalado (para leitura de .mp3/.wav)
- GPU (opcional) com CUDA para acelerar o Demucs

---

## 🚀 Instalação

Crie um ambiente virtual e instale as dependências:

```bash
python -m venv env
call env\Scripts\activate  # no Windows

pip install -r requirements.txt
```

> ⚠️ Para suporte a GPU, instale o PyTorch com CUDA conforme seu driver: [https://pytorch.org/get-started/locally/](https://pytorch.org/get-started/locally/)

---

## 🎧 Separando os instrumentos

Use o script de separação:

```bash
separar_audio_demucs.bat caminho\para\audio.mp3
```

Os stems (vocals, bass, drums, other) serão salvos em:

```
saida_demucs/htdemucs/NOME_DO_ARQUIVO/
```

---

## 🎼 Rodando a pipeline principal

Edite o caminho no `main.py` e execute:

```bash
python main.py
```

O MIDI final será salvo em:

```
saida_midis/NOME_DO_ARQUIVO_final.mid
```

---

## 🎮 Compatibilidade Rock Band

As notas do stem `other` podem ser mapeadas para lanes Rock Band (Green to Orange) usando:

- C4 (60) = Green
- C#4 (61) = Red
- D4 (62) = Yellow
- D#4 (63) = Blue
- E4 (64) = Orange

Esse mapeamento pode ser usado em REAPER + Magma/EOF para criar charts jogáveis.

---

## 📁 Estrutura

```
Midis-para-Rock-Band/
├── main.py
├── requirements.txt
├── separar_audio_demucs.bat
├── processamento/
│   ├── crepe_transcriber.py
│   ├── tempo.py
│   ├── eventos.py
│   ├── instrumentos.py
│   ├── utils.py
├── saida_demucs/
├── saida_midis/
├── tarefas/
│   ├── vocal_to_midi.py
│   ├── other_to_midi.py
│   ├── bass_to_midi.py
```

---

## 📄 Licença

Este projeto é livre para fins educacionais e artísticos. Não é afiliado a Harmonix, Rock Band ou Guitar Hero.

---

## ✉️ Contato

Para dúvidas, entre em contato via GitHub ou e-mail.
