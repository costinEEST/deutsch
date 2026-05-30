# Germana Rapidă — Anki Flashcard Generator

Study aid for the book **[Germana Rapidă by Corina Dragomir](./GERMANA_RAPIDA.md)** — a practical German course for Romanian speakers (Editura Steaua Nordului, 2012).

The script extracts vocabulary, pronunciation rules, diphthongs, consonant patterns, and accent rules from the book and packages them as an Anki deck. Alphabet cards include native audio pronunciation.

---

## Requirements

- [uv](https://docs.astral.sh/uv/) — Python package manager (handles all dependencies automatically)
- [Anki](https://apps.ankiweb.net/) — to study the generated deck

Install `uv` if you don't have it:

```bash
# via pip
pip install uv

# or via Homebrew
brew install uv
```

---

## Two ways to get cards into Anki

### Option 1 — Export to file, import manually

Use this when Anki is closed, or as a one-time setup.

```bash
uv run create_anki_deck.py
```

This generates `germana_rapida.apkg` in the current directory. Then in Anki:

1. `File → Import`
2. Select `germana_rapida.apkg`
3. The deck **"Germana Rapidă :: Corina Dragomir"** appears in your collection

Re-importing after regenerating is safe — card GUIDs are deterministic, so Anki updates existing cards instead of creating duplicates. Your study progress and review history are preserved.

---

### Option 2 — Push directly to Anki via AnkiConnect

Use this for day-to-day updates. No manual import step needed.

```bash
uv run create_anki_deck.py --push
```

This connects to a running Anki instance, uploads the audio files, and adds or updates all 260 cards in place. Study progress is fully preserved.

**Requirements for `--push`:**
- Anki must be open
- The AnkiConnect add-on must be installed (see below)

---

## What is AnkiConnect?

AnkiConnect is an Anki add-on that starts a local HTTP server (on port 8765) whenever Anki is running. External tools — like this script — can talk to it to create decks, add or update cards, and upload media files, all without touching the Anki UI.

Think of it as a REST API for your local Anki collection.

### Installing AnkiConnect

1. Open Anki
2. Go to `Tools → Add-ons → Get Add-ons…`
3. Enter the code **`2055492159`** and click OK
4. Restart Anki

You can verify it's running by opening [http://localhost:8765](http://localhost:8765) in your browser — you should see the text `AnkiConnect`.

### Extra step for macOS

macOS has a feature called App Nap that suspends background apps, which breaks AnkiConnect when Anki is not the focused window. Disable it for Anki by running these three commands once in Terminal:

```bash
defaults write net.ankiweb.dtop NSAppSleepDisabled -bool true
defaults write net.ichi2.anki NSAppSleepDisabled -bool true
defaults write org.qt-project.Qt.QtWebEngineCore NSAppSleepDisabled -bool true
```

Then restart Anki.

---

## What's in the deck

260 cards across 8 categories:

| Category | Cards | Description |
|---|---|---|
| Alfabet | 29 | All 26 letters + ä, ö, ü with IPA pronunciation and audio |
| Pronunție — Vocale | 16 | Vowel length and quality rules with examples |
| Pronunție — Diftongi | 18 | Diphthong patterns: ei/ai, au, eu/äu |
| Pronunție — Consoane | 26 | Consonant rules including ch, sch, st, sp, z, w |
| Pronunție — Consoane duble | 10 | Double consonant behaviour |
| Accent | 9 | Stress rules for compounds, suffixes, separable verbs |
| Vocabular | 76 | German → Romanian (with grammatical gender) |
| Vocabular — Invers | 76 | Romanian → German |

Audio pronunciation for the alphabet is sourced from [German Cheat Sheet](https://tsimpliarakis.github.io/German-Cheat-Sheet/alphabet) by Michail Tsimpliarakis, licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

---

## Files

```
.
├── create_anki_deck.py   # the generator script
├── germana_rapida.apkg   # generated Anki deck (after running the script)
├── GERMANA_RAPIDA.md     # book content: alphabet, pronunciation, accent rules
└── README.md             # this file
```

The `.audio_cache/` directory is created on first run to store downloaded `.m4a` files locally. Subsequent runs reuse the cache. Both `germana_rapida.apkg` and `.audio_cache/` are gitignored.

---

## Source material

**Germana Rapidă** — Corina Dragomir  
Editura Steaua Nordului, Constanța, 2012 (Ed. a 6-a)  
ISBN 978-606-511-372-5  
[Ediția 2005 pe Scribd](https://www.scribd.com/document/397842541/Corina-Dragomir-Germana-Rapida-2005-Steaua-Nordului-pdf)
