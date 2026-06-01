# Resurse pentru învățat germana

Colecție de cursuri, cărți și unelte pentru a învăța limba germană — cu focus pe vorbitori de română.

---

## Cursuri video

| Resursă | Nivel | Limbă | Descriere |
|---|---|---|---|
| [Călin Ardelean — Profu' de Germană](./calin-ardelean-profu-de-germana.md) | A1–B1+ | Română | Cursuri gratuite pe YouTube, structurate progresiv |

---

## Cărți

| Resursă | Nivel | Limbă | Descriere |
|---|---|---|---|
| [Germana Rapidă — Corina Dragomir](./corina-dragomir-germana-rapida.md) | A1–A2 | Română | Curs practic, 34 de lecții, gramatică, vocabular |

---

## Unelte

### Generator de carduri Anki — Germana Rapidă

Script Python care extrage vocabularul, regulile de pronunție și accentul din cartea **Germana Rapidă** și generează un deck Anki cu 260 de carduri. Cardurile pentru alfabet includ audio nativ.

**Cerințe:**

- [uv](https://docs.astral.sh/uv/) — manager de pachete Python
- [Anki](https://apps.ankiweb.net/) — pentru studiat deck-ul generat

Instalează `uv` dacă nu îl ai:

```bash
# via pip
pip install uv

# sau via Homebrew
brew install uv
```

**Opțiunea 1 — Export în fișier, import manual**

Folosește când Anki este închis sau ca setup inițial.

```bash
uv run create_anki_deck.py
```

Generează `germana_rapida.apkg` în directorul curent. Apoi în Anki: `File → Import → germana_rapida.apkg`.

Re-importul după regenerare este sigur — GUID-urile cardurilor sunt deterministe, deci Anki actualizează cardurile existente fără să creeze duplicate. Progresul de studiu se păstrează.

**Opțiunea 2 — Push direct în Anki via AnkiConnect**

Folosește pentru actualizări zilnice, fără import manual.

```bash
uv run create_anki_deck.py --push
```

Cerințe: Anki deschis + add-on-ul AnkiConnect instalat.

**Instalare AnkiConnect:**

1. Deschide Anki
2. `Tools → Add-ons → Get Add-ons…`
3. Introdu codul [**`2055492159`**](https://github.com/ankicommunity/anki-desktop-addon-connect#installation) și click OK
4. Repornește Anki

Verifică că rulează accesând [http://localhost:8765](http://localhost:8765) — ar trebui să apară textul `AnkiConnect`.

> **macOS:** App Nap poate suspenda AnkiConnect când Anki nu e în prim-plan. Dezactivează-l o singură dată:
> ```bash
> defaults write net.ankiweb.dtop NSAppSleepDisabled -bool true
> defaults write net.ichi2.anki NSAppSleepDisabled -bool true
> defaults write org.qt-project.Qt.QtWebEngineCore NSAppSleepDisabled -bool true
> ```
> Apoi repornește Anki.

**Ce conține deck-ul:**

260 de carduri în 8 categorii:

| Categorie | Carduri | Descriere |
|---|---|---|
| Alfabet | 29 | Toate cele 26 de litere + ä, ö, ü cu pronunție IPA și audio |
| Pronunție — Vocale | 16 | Reguli de lungime și calitate a vocalelor cu exemple |
| Pronunție — Diftongi | 18 | Tipare de diftongi: ei/ai, au, eu/äu |
| Pronunție — Consoane | 26 | Reguli pentru ch, sch, st, sp, z, w |
| Pronunție — Consoane duble | 10 | Comportamentul consoanelor duble |
| Accent | 9 | Reguli de accent pentru compuse, sufixe, verbe separabile |
| Vocabular | 76 | Germană → Română (cu gen gramatical) |
| Vocabular — Invers | 76 | Română → Germană |

Audio pentru alfabet provine din [German Cheat Sheet](https://tsimpliarakis.github.io/German-Cheat-Sheet/alphabet) de Michail Tsimpliarakis, licențiat sub [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

---

## Structura repository-ului

```
.
├── README.md                              # acest fișier
├── calin-ardelean-profu-de-germana.md     # lecții YouTube — Profu' de Germană
├── corina-dragomir-germana-rapida.md     # conținut carte: alfabet, pronunție, accent, lecții
└── create_anki_deck.py                    # script generator deck Anki
```

Directorul `.audio_cache/` se creează la prima rulare a scriptului pentru a stoca fișierele `.m4a` local. Rulările ulterioare refolosesc cache-ul. Atât `germana_rapida.apkg` cât și `.audio_cache/` sunt în `.gitignore`.
