# Germana Rapidă — Anki Flashcard Generator

Study aid for the book **[Germana Rapidă by Corina Dragomir](./GERMANA_RAPIDA.md)** — a practical German course for Romanian speakers (Editura Steaua Nordului, 2012).

The script extracts vocabulary, pronunciation rules, diphthongs, consonant patterns, and accent rules from the book and packages them as an Anki deck ready to import.

---

## Requirements

- [uv](https://docs.astral.sh/uv/) — Python package manager (handles dependencies automatically)
- [Anki](https://apps.ankiweb.net/) — to import and study the generated deck

Install `uv` if you don't have it:

```bash
pip install uv
# or via Homebrew
brew install uv
```

---

## Usage

```bash
uv run create_anki_deck.py
```

That's it. `uv` installs `genanki` on first run (into an isolated environment) and generates `germana_rapida.apkg` in the current directory.

### Import into Anki

1. Open Anki
2. `File → Import`
3. Select `germana_rapida.apkg`
4. The deck **"Germana Rapidă :: Corina Dragomir"** will appear in your collection

Re-running the script and re-importing is safe — card GUIDs are deterministic, so Anki updates existing cards instead of creating duplicates.

---

## What's in the deck

260 cards across 8 categories:

| Category | Cards | Description |
|---|---|---|
| Alfabet | 29 | All 26 letters + ä, ö, ü with IPA pronunciation |
| Pronunție — Vocale | 16 | Vowel length and quality rules with examples |
| Pronunție — Diftongi | 18 | Diphthong patterns: ei/ai, au, eu/äu |
| Pronunție — Consoane | 26 | Consonant rules including ch, sch, st, sp, z, w |
| Pronunție — Consoane duble | 10 | Double consonant behaviour |
| Accent | 9 | Stress rules for compounds, suffixes, separable verbs |
| Vocabular | 76 | German → Romanian (with grammatical gender) |
| Vocabular — Invers | 76 | Romanian → German |

---

## Files

```
.
├── create_anki_deck.py   # the generator script
├── germana_rapida.apkg   # generated Anki deck (after running the script)
├── GERMANA_RAPIDA.md     # book content: alphabet, pronunciation, accent rules
└── README.md             # this file
```

---

## Source material

**Germana Rapidă** — Corina Dragomir  
Editura Steaua Nordului, Constanța, 2012 (Ed. a 6-a)  
ISBN 978-606-511-372-5  
[Ediția 2005 pe Scribd](https://www.scribd.com/document/397842541/Corina-Dragomir-Germana-Rapida-2005-Steaua-Nordului-pdf)
