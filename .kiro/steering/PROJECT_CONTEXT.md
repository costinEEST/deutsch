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

## Formatarea conținutului de lecții

Când utilizatorul adaugă conținut brut dintr-o lecție (text copiat, transcriere, note), formatează-l urmând acest pattern stabilit în lecția 10 din `calin-ardelean-profu-de-germana.md`.

### Structura unei lecții

```markdown
### Lecția N — Titlu subiect

📺 [Vezi pe YouTube](URL)

**Salut / expresie cheie** — traducere

---

#### Secțiunea principală — concept gramatical

Scurtă explicație a conceptului (1-3 propoziții).

| Tabel rezumat dacă există mai multe variante |
|---|---|
| **termen** | sens |

**Subsecțiune — verb sau concept specific**

| Germană | Română |
|---|---|
| Exemplu german. | Traducere română. |

---

#### Exerciții — grupate pe verb/concept

**verb/concept — exerciții**

| Germană | Română |
|---|---|
| Propoziție. | Traducere. |

---

**Danke** — Mulțumesc
```

### Reguli de formatare

- **Nu folosi blocuri de cod indentat** (`    text`) pentru propoziții — folosește tabele
- **Grupează exemplele pe verb sau concept**, nu le lăsa amestecate într-o listă plată
- **Adaugă un tabel rezumat** când există mai multe variante ale unui concept (ex: toate verbele modale)
- **Separă cu `---`** secțiunile principale (teorie vs. exerciții)
- **Bifează lecția** în lista playlist-ului după ce conținutul e adăugat (`- [x]`)
- **Link-ul YouTube** al lecției apare imediat sub titlul lecției
- Titlul lecției folosește anchor intern pentru a putea fi referit din lista de checkboxuri

### Checklist playlist

Fiecare playlist are o listă de checkboxuri deasupra conținutului lecțiilor. Lecțiile cu conținut adăugat sunt bifate (`[x]`) și au un link anchor către secțiunea lor.

Exemplu:
```markdown
- [ ] Lecția 1
- [x] [Lecția 10 — Verbe modale](#lecția-10--verbe-modale)
```

## Limbă

Documentația și fișierele `.md` sunt în **română**. Codul Python poate avea comentarii în engleză sau română.
