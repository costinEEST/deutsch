# Context — Repository de resurse pentru germană

## Ce este acest repository

O colecție personală de resurse pentru învățat limba germană, adresată vorbitorilor de română. Conține:
- note și conținut extras din cărți
- referințe către cursuri video
- un script Python care generează carduri Anki

## Structura fișierelor

```
.
├── README.md                              # index principal al colecției
├── calin-ardelean-profu-de-germana.md     # lecții YouTube — @ProfudeGermana
├── GERMANA_RAPIDA.md                      # conținut extras din cartea Corina Dragomir
├── create_anki_deck.py                    # script generator deck Anki
└── .kiro/steering/PROJECT_CONTEXT.md     # acest fișier
```

## Convenții pentru fișiere de resurse

Fiecare resursă (carte, canal YouTube, site) primește un fișier `.md` dedicat, cu numele în format `kebab-case` descriptiv (ex: `calin-ardelean-profu-de-germana.md`).

Structura unui fișier de resursă:
1. Titlu și link către sursă
2. Scurtă descriere
3. Conținut structurat (lecții, capitole, note)
4. Secțiune pentru note personale
5. Resurse suplimentare menționate

Orice resursă nouă adăugată trebuie menționată și în `README.md`, în tabelul corespunzător categoriei (Cursuri video / Cărți / Unelte).

## Scriptul Anki (`create_anki_deck.py`)

- Rulat cu `uv run create_anki_deck.py` (fără `--push`) → generează `germana_rapida.apkg`
- Rulat cu `--push` → trimite cardurile direct în Anki deschis via AnkiConnect (port 8765)
- Sursă de date: conținutul din `GERMANA_RAPIDA.md`
- Cache audio în `.audio_cache/` (gitignored)
- Output `germana_rapida.apkg` (gitignored)

## Limbă

Documentația și fișierele `.md` sunt în **română**. Codul Python poate avea comentarii în engleză sau română.
