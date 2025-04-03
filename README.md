# 🥁🎸 Gerador de MIDI para Rock Band (C3 Tools Format)

Este projeto em Python automatiza a criação de arquivos `.mid` compatíveis com o formato da **C3 Tools** para charts do jogo **Rock Band**. Ele extrai automaticamente os instrumentos e vocais de uma música e gera pistas MIDI para cada um deles, incluindo tempo, compassos, eventos, luzes, câmeras e até harmonias vocais.

---

## 🚀 Funcionalidades

- 🎧 Separação de instrumentos com **Spleeter**
- 🎹 Transcrição automática para **MIDI** com **basic-pitch**
- 🎼 Geração de pistas MIDI para:
  - `PART VOCALS` (com `HARM1`, `HARM2`)
  - `PART GUITAR`, `PART BASS`, `PART DRUMS`, `PART KEYS`
- 🕒 Tempo dinâmico e compassos sincronizados
- 🎤 Análise de seções com IA (`EVENTS`)
- 🎬 Animações automáticas de palco (`VENUE`)
- 📦 Pronto para uso com **Reaper + C3 CON Tools**

---

## 📁 Estrutura do Projeto

```
projeto/
├── main.py
├── requirements.txt
├── processamento/
│   ├── __init__.py
│   ├── instrumentos.py
│   ├── transcricao.py
│   ├── harmonias.py
│   ├── tempo.py
│   ├── eventos.py
│   └── utils.py
```

---

## ⚙️ Requisitos

- Python 3.10 (recomendado)
- Pip
- Ambiente virtual (opcional, mas recomendado)

---

## 🧩 Instalação

```bash
# Clone o projeto
git clone https://github.com/IcaroRP/Midis-para-Rock-Band
cd projeto-chart

# Crie e ative o ambiente virtual
python -m venv env
env\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

---

## 🛠️ Uso

1. Coloque a música `.mp3` na raiz do projeto.
2. Execute o script:

```bash
python main.py
```

3. Isso irá:
   - Separar os instrumentos
   - Transcrever os MIDIs
   - Gerar o arquivo `saida_final_c3.mid` com todas as trilhas
4. Importe o `.mid` no **REAPER + C3 Tools** para finalizar o chart.

---

## 📌 Dependências

Veja todas em [requirements.txt](./requirements.txt), incluindo:

- `spleeter`
- `librosa`
- `mido`
- `scikit-learn`
- `basic-pitch`

---

## 💡 Futuras melhorias

- Sincronização labial automática (`lyric` + `phrase_start`)
- Classificação por gênero musical
- Validador automático de qualidade do chart
- Exportador para outros formatos (Clone Hero, Osu!)

---

## 📜 Licença

MIT © 2025 — por kentjpg
