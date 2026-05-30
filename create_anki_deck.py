#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "genanki",
#   "requests",
# ]
# ///
"""
Germana Rapidă — Anki Deck Generator

Usage:
  uv run create_anki_deck.py           # write germana_rapida.apkg
  uv run create_anki_deck.py --push    # push directly to running Anki via AnkiConnect

AnkiConnect (add-on 2055492159) must be installed and Anki must be open for --push.
Audio source: tsimpliarakis.github.io/German-Cheat-Sheet (CC BY-NC-SA 4.0)
"""

import base64
import json
import os
import sys
import urllib.parse
import urllib.request
import argparse
import requests
import genanki

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ANKI_CONNECT_URL = "http://127.0.0.1:8765"
DECK_NAME        = "Germana Rapidă :: Corina Dragomir"
MODEL_NAME       = "Germana Rapidă"
DECK_ID          = 1_234_567_890
MODEL_ID         = 9_876_543_210

AUDIO_BASE_URL = (
    "https://github.com/Tsimpliarakis/German-Cheat-Sheet"
    "/raw/main/docs/assets/audio/"
)
AUDIO_CACHE_DIR = ".audio_cache"

LETTER_AUDIO: dict[str, str] = {
    **{l: f"{l}.m4a" for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
    "Ä": "Ä.m4a", "Ö": "Ö.m4a", "Ü": "Ü.m4a", "ß": "SS.m4a",
}


# ---------------------------------------------------------------------------
# AnkiConnect helpers
# ---------------------------------------------------------------------------
def ac_invoke(action: str, **params) -> object:
    """Call AnkiConnect and return the result, raising on error."""
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode()
    req = urllib.request.Request(ANKI_CONNECT_URL, payload)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = json.load(resp)
    except OSError as e:
        raise SystemExit(
            f"\n❌  Cannot reach AnkiConnect at {ANKI_CONNECT_URL}\n"
            f"   Make sure Anki is open and AnkiConnect (add-on 2055492159) is installed.\n"
            f"   Error: {e}"
        )
    if body.get("error"):
        raise RuntimeError(f"AnkiConnect error [{action}]: {body['error']}")
    return body["result"]


def ac_is_running() -> bool:
    try:
        ac_invoke("version")
        return True
    except SystemExit:
        return False


def ac_store_media(path: str) -> None:
    """Upload a local file to Anki's media folder."""
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ac_invoke("storeMediaFile", filename=os.path.basename(path), data=data)


def ac_upsert_notes(notes_payload: list[dict]) -> dict:
    """Add new notes; update fields of existing ones. Returns counts."""
    added = updated = skipped = 0
    for note in notes_payload:
        # Try to find an existing note by its first field value in the deck
        front = note["fields"]["Front"]
        query = f'deck:"{DECK_NAME}" "Front:{front}"'
        existing = ac_invoke("findNotes", query=query)
        if existing:
            note_id = existing[0]
            ac_invoke("updateNoteFields", note={"id": note_id, "fields": note["fields"]})
            updated += 1
        else:
            result = ac_invoke("addNote", note=note)
            if result:
                added += 1
            else:
                skipped += 1
    return {"added": added, "updated": updated, "skipped": skipped}


# ---------------------------------------------------------------------------
# Audio download
# ---------------------------------------------------------------------------
def fetch_audio_files() -> dict[str, str]:
    """Download .m4a files to local cache. Returns {LETTER: local_path}."""
    os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)
    result: dict[str, str] = {}
    print(f"⬇️  Checking {len(LETTER_AUDIO)} audio files …")
    for letter, filename in LETTER_AUDIO.items():
        local_path = os.path.join(AUDIO_CACHE_DIR, filename)
        if not os.path.exists(local_path):
            url = AUDIO_BASE_URL + urllib.parse.quote(filename)
            try:
                resp = requests.get(url, timeout=15)
                resp.raise_for_status()
                with open(local_path, "wb") as f:
                    f.write(resp.content)
                print(f"   ✓ {filename}")
            except requests.RequestException as e:
                print(f"   ✗ {filename} — {e}", file=sys.stderr)
                continue
        else:
            print(f"   · {filename} (cached)")
        result[letter] = local_path
    print()
    return result


# ---------------------------------------------------------------------------
# genanki model (used for .apkg export)
# ---------------------------------------------------------------------------
GENANKI_MODEL = genanki.Model(
    MODEL_ID,
    MODEL_NAME,
    fields=[
        {"name": "Front"}, {"name": "Back"},
        {"name": "Category"}, {"name": "Audio"},
    ],
    templates=[{
        "name": "Card 1",
        "qfmt": '<div class="category">{{Category}}</div>'
                '<div class="front">{{Front}}</div>{{Audio}}',
        "afmt": '<div class="category">{{Category}}</div>'
                '<div class="front">{{Front}}</div>'
                '<hr id="answer">'
                '<div class="back">{{Back}}</div>{{Audio}}',
    }],
    css="""
.card { font-family: Arial, sans-serif; font-size: 20px; text-align: center;
        color: #222; background-color: #fafafa; padding: 20px; }
.category { font-size: 12px; color: #888; text-transform: uppercase;
            letter-spacing: 1px; margin-bottom: 8px; }
.front { font-size: 26px; font-weight: bold; color: #1a1a2e; margin: 10px 0; }
.back  { font-size: 22px; color: #16213e; margin-top: 10px; }
hr     { border: none; border-top: 1px solid #ddd; margin: 16px 0; }
""",
)


# ---------------------------------------------------------------------------
# Card data
# ---------------------------------------------------------------------------
def build_cards(audio_map: dict[str, str]) -> tuple[list[dict], list[str]]:
    """
    Returns (notes_list, media_file_paths).
    Each note dict is compatible with both genanki and AnkiConnect payloads.
    """
    notes: list[dict] = []
    media_files: list[str] = []

    def note(front: str, back: str, category: str, audio: str = "") -> dict:
        return {"front": front, "back": back, "category": category, "audio": audio}

    # 1. ALPHABET
    alphabet = [
        ("A","[a:]"),("B","[be:]"),("C","[tse:]"),("D","[de:]"),
        ("E","[e:]"),("F","[εf]"),("G","[ge:]"),("H","[ha:]"),
        ("I","[εI:]"),("J","[jdɛt]"),("K","[ka:]"),("L","[εl]"),
        ("M","[εm]"),("N","[εn]"),("O","[o:]"),("P","[pe:]"),
        ("Q","[ku:]"),("R","[εr]"),("S","[εs]"),("T","[te:]"),
        ("U","[u:]"),("V","[fa]"),("W","[ve:]"),("X","[iks]"),
        ("Y","['ypsilon]"),("Z","[tsεt]"),
        ("ä","[ε:]"),("ö","[ø:]"),("ü","[Y:]"),
    ]
    for letter, pron in alphabet:
        local_path = audio_map.get(letter.upper())
        if local_path:
            filename = os.path.basename(local_path)
            sound_tag = f"[sound:{filename}]"
            media_files.append(local_path)
        else:
            sound_tag = ""
        notes.append(note(
            front=f"Litera germană: <b>{letter}</b>",
            back=f"Se pronunță: {pron}",
            category="Alfabet",
            audio=sound_tag,
        ))

    # 2. VOWELS
    for word, pron, rule in [
        ("Macht","[maxt]","putere — <b>a</b> scurt, ca în rom. <i>pact</i>"),
        ("Saale / Jahr","[sa:le] / [ja:r]","<b>a</b> lung [a:] — ca în rom. <i>vale</i>; h prelungește vocala"),
        ("betten","[betən]","<b>e</b> scurt — urmat de mai multe consoane, ca în rom. <i>sec</i>"),
        ("Tränen","[trenən]","<b>e</b> lung deschis [e:] — ca în rom. <i>plăcere</i>"),
        ("Etage / Meer","[eta:ʒe] / [me:r]","<b>e</b> lung închis [e:] — ca în rom. <i>soare</i>"),
        ("offen","[ofən]","<b>o</b> scurt — ca în rom. <i>foc</i>"),
        ("Ozon","[o:tson]","<b>o</b> lung [o:] — ca în rom. <i>soră</i>"),
        ("Völker","[foelkər]","<b>ö</b> scurt [oe] — ca în rom. <i>bleu</i>"),
        ("Goethe / Öl","[goe:te] / [oe:l]","<b>ö</b> lung [oe:] — ca în rom. <i>Phoenix</i>"),
        ("Irre","[ire]","<b>i</b> scurt — ca în rom. <i>nivel</i>"),
        ("mir / riesig","[mi:r] / [ri:zç]","<b>i</b> lung [i:] — ca în rom. <i>ie, mie</i>"),
        ("Sturm","[ʃturm]","<b>u</b> scurt — ca în rom. <i>ulm</i>"),
        ("Blume / Ruhe","[blu:me] / [ru:e]","<b>u</b> lung [u:] — ca în rom. <i>lume</i>; h prelungește vocala"),
        ("Schüsse","[ʃYse]","<b>ü</b> scurt [Y] — ca în rom. <i>mure</i>"),
        ("drüben / führen","[drYbən] / [fY:rən]","<b>ü</b> lung [Y:] — ca în rom. <i>prelung</i>; h prelungește vocala"),
        ("aber","[abər]","<b>e</b> neaccentuat [ə] — ca în rom. <i>băiat</i>"),
    ]:
        notes.append(note(f"Pronunție: <b>{word}</b>", f"{pron}<br><small>{rule}</small>", "Pronunție — Vocale"))

    return notes, media_files


def build_remaining_cards() -> list[dict]:
    """Build diphthong, consonant, accent and vocabulary cards (no audio)."""
    notes: list[dict] = []

    def note(front, back, category):
        return {"front": front, "back": back, "category": category, "audio": ""}

    # 3. DIPHTHONGS
    for word, pron, rule in [
        ("ei / ai / ey / ay","[ai]","ca în rom. <i>mai</i> — ex: <b>mein</b> (al meu)"),
        ("au","[au]","ca în rom. <i>flaut</i> — ex: <b>Haus</b> (casă)"),
        ("eu / äu","[oY]","ca în rom. <i>ploi</i> — ex: <b>Leute</b> (oameni)"),
        ("Rhein","[rain]","Rin — diftong <b>ei → [ai]</b>"),
        ("Reis","[rais]","orez — diftong <b>ei → [ai]</b>"),
        ("Seite","[zaite]","parte, față — diftong <b>ei → [ai]</b>"),
        ("Kleid","[klaid]","rochie — diftong <b>ei → [ai]</b>"),
        ("leise","[laize]","încet — diftong <b>ei → [ai]</b>"),
        ("Mais","[mais]","porumb — diftong <b>ai → [ai]</b>"),
        ("Kaiser","[kaizər]","împărat — diftong <b>ai → [ai]</b>"),
        ("Heu","[hoY]","fân — diftong <b>eu → [oY]</b>"),
        ("Freude","[froYde]","bucurie — diftong <b>eu → [oY]</b>"),
        ("heute","[hoYte]","azi — diftong <b>eu → [oY]</b>"),
        ("Feuer","[foYər]","foc — diftong <b>eu → [oY]</b>"),
        ("Bäuerin","[boYərin]","țărancă — diftong <b>äu → [oY]</b>"),
        ("Häuschen","[hoYsxən]","căsuță — diftong <b>äu → [oY]</b>"),
        ("Geräusch","[geroYʃ]","zgomot — diftong <b>äu → [oY]</b>"),
        ("häufig","[hoYfiç]","frecvent — diftong <b>äu → [oY]</b>"),
    ]:
        notes.append(note(f"Pronunție: <b>{word}</b>", f"{pron}<br><small>{rule}</small>", "Pronunție — Diftongi"))

    # 4. CONSONANTS
    for cons, pron, rule in [
        ("b","[b]","ca în rom. <i>bun</i> — ex: <b>Bier</b> (bere)"),
        ("ch / -ig","[ç]","ca în rom. <i>Mihnea</i> — ex: <b>nicht</b> (nu), <b>riesig</b> (uriaș)"),
        ("ch (după a, o, u)","[x]","ca în rom. <i>hală</i> — ex: <b>Nacht</b> (noapte)"),
        ("d","[d]","ca în rom. <i>direcție</i> — ex: <b>das</b>"),
        ("f","[f]","ca în rom. <i>față</i> — ex: <b>Fieber</b> (febră)"),
        ("g","[g]","ca în rom. <i>gard</i> — ex: <b>Garage</b> (garaj)"),
        ("g (urmat de e)","[ʒ]","ca în rom. <i>jidan</i> — ex: <b>Genie</b> (geniu)"),
        ("h","[h]","ca în rom. <i>haită</i> — ex: <b>Herz</b> (inimă); după vocală nu se pronunță"),
        ("j","[j]","ca în rom. <i>iese</i> — ex: <b>jagen</b> (a vâna)"),
        ("k","[k]","ca în rom. <i>cal</i> — ex: <b>klar</b> (clar)"),
        ("l","[l]","ca în rom. <i>leu</i> — ex: <b>langsam</b> (încet)"),
        ("m","[m]","ca în rom. <i>miel</i> — ex: <b>Mutter</b> (mama)"),
        ("n","[n]","ca în rom. <i>nou</i> — ex: <b>Name</b> (nume)"),
        ("n (înainte de g/k)","[ŋ]","nazal, ca în rom. <i>tanc</i> — ex: <b>fangen</b> (a prinde)"),
        ("p","[p]","ca în rom. <i>pară</i> — ex: <b>Pause</b> (pauză)"),
        ("r","[r]","ca în rom. <i>rândunică</i> — ex: <b>Ruhe</b> (liniște)"),
        ("S / ss / ß","[s]","ca în rom. <i>râs</i> — ex: <b>Essen</b> (a mânca)"),
        ("s (la început de cuvânt)","[z]","ca în rom. <i>ziuă</i> — ex: <b>Soldat</b> (soldat)"),
        ("sch","[ʃ]","ca în rom. <i>șanț</i> — ex: <b>Schwester</b> (soră)"),
        ("st (la început)","[ʃt]","ca în rom. <i>știe</i> — ex: <b>Stehlen</b> (a fura)"),
        ("sp (la început)","[ʃp]","ca în rom. <i>șp</i> — ex: <b>Spinat</b> (spanac)"),
        ("t","[t]","ca în rom. <i>tânăr</i> — ex: <b>Tod</b> (moarte)"),
        ("z","[ts]","ca în rom. <i>țar</i> — ex: <b>Zucker</b> (zahăr)"),
        ("w","[v]","ca în rom. <i>vineri</i> — ex: <b>Wein</b> (vin)"),
        ("v","[f]","ca în rom. <i>față</i> — ex: <b>Vater</b> (tată), <b>viel</b> (mult)"),
        ("ph","[f]","ca în rom. <i>față</i> — ex: <b>Asphalt</b>, <b>Prophet</b>"),
    ]:
        notes.append(note(f"Consoana germană: <b>{cons}</b>", f"{pron}<br><small>{rule}</small>", "Pronunție — Consoane"))

    # 5. DOUBLE CONSONANTS
    for cons, example, meaning in [
        ("bb","Rabbi [rabi]","rabin — vocala dinaintea consoanei duble este scurtă"),
        ("dd","Pudding [pudiŋ]","budincă"),
        ("ff","Koffer [kofər], Kaffee, Löffel [loefel]","bagaj, cafea, lingură"),
        ("gg","Bagger [bagər]","excavator"),
        ("ll","Brille [brile], Unfall [unfal]","ochelari, accident"),
        ("mm","Himmel [himel], Zimmer [tsimər]","cer, cameră"),
        ("nn","Sonne [zone]","soare"),
        ("pp","Teppich [tepix], Suppe [zupe]","covor, supă"),
        ("ss","Wasser [vasər], interessant [interesant]","apă, interesant"),
        ("tt","Schlitten [ʃlitən], Wetter [vetər]","sanie, vreme"),
    ]:
        notes.append(note(f"Consoană dublă: <b>{cons}</b>", f"{example}<br><small>{meaning}</small>", "Pronunție — Consoane duble"))

    return notes


def build_accent_and_vocab_cards() -> list[dict]:
    notes: list[dict] = []

    def note(front, back, category):
        return {"front": front, "back": back, "category": category, "audio": ""}

    # 6. ACCENT RULES
    for front, back in [
        ("Unde cade accentul în cuvintele germane simple?",
         "Pe <b>rădăcina cuvântului</b> — accentul este fix.<br><small>Ex: der Le̲hrer, die Mu̲tter, der Va̲ter</small>"),
        ("Unde cade accentul în substantivele compuse?",
         "Pe <b>cuvântul determinativ</b> (primul element).<br><small>Ex: der Ble̲istift, der Schre̲ibtisch, das Ja̲hrhundert</small>"),
        ("Excepții — accentul NU cade pe rădăcină",
         "der U̲nterricht, der Wi̲derstand, der Wi̲derspruch"),
        ("Accentul la substantive cu sufixe străine (-ismus, -ar, -al, -ier, -är, -ik, -ion, -eur)",
         "Accentul cade pe <b>sufix</b>.<br><small>Ex: Sekretärin, Kapitän, Bibliothekar, General, Offizier, Politik</small>"),
        ("Accentul la sufixele -ist, -ant, -oph, -oge, -ment, -et, -iv, -em",
         "Accentul cade pe <b>sufix</b>.<br><small>Ex: Aspirant, Philosoph, Dokument, Dekret, Substantiv, Problem</small>"),
        ("Accentul la verbele cu particulă separabilă",
         "Accentul cade pe <b>particulă</b>.<br><small>Ex: e̲inladen (a invita), te̲ilnehmen (a lua parte)</small>"),
        ("Accentul la verbele cu sufixul -ieren",
         "Accentul cade pe <b>sufix (-ie-)</b>.<br><small>Ex: spazieren, studieren, reparieren</small>"),
        ("Accentul la adjectivele compuse",
         "Accentul cade pe <b>vocala din rădăcina fiecărui cuvânt</b>.<br><small>Ex: e̲iskalt, schne̲eweiß</small>"),
        ("Sufixul -ei la substantive derivate",
         "Accentul cade pe <b>sufix -ei</b>.<br><small>Ex: die Arznei (medicament) [artsnai]</small>"),
    ]:
        notes.append(note(front, back, "Accent"))

    # 7. VOCABULARY
    vocabulary = [
        ("Macht","puterea","das"),("Jahr","anul","das"),("Tränen","lacrimile","die"),
        ("Etage","etajul","die"),("Meer","marea","das"),("Mehrheit","majoritatea","die"),
        ("Völker","popoarele","die"),("Öl","uleiul","das"),("Irre","nebunul/nebuna","der/die"),
        ("Sturm","furtuna","der"),("Blume","floarea","die"),("Ruhe","liniștea","die"),
        ("aber","dar","—"),("Bier","berea","das"),("Nacht","noaptea","die"),
        ("Fieber","febra","das"),("Garage","garajul","die"),("Genie","geniul","das"),
        ("Herz","inima","das"),("Mutter","mama","die"),("Name","numele","der"),
        ("Pause","pauza","die"),("Essen","mâncarea / a mânca","das"),("Soldat","soldatul","der"),
        ("Schwester","sora","die"),("Tod","moartea","der"),("Zucker","zahărul","der"),
        ("Wein","vinul","der"),("Koffer","bagajul","der"),("Kaffee","cafeaua","der"),
        ("Löffel","lingura","der"),("Brille","ochelarii","die"),("Unfall","accidentul","der"),
        ("Himmel","cerul","der"),("Zimmer","camera","das"),("Sonne","soarele","die"),
        ("Teppich","covorul","der"),("Suppe","supa","die"),("Wasser","apa","das"),
        ("Wetter","vremea","das"),("Haus","casa","das"),("Leute","oamenii","die"),
        ("mein","al meu","—"),("Reis","orezul","der"),("Seite","partea / fața","die"),
        ("Kleid","rochia","das"),("leise","încet (adv.)","—"),("Mais","porumbul","der"),
        ("Kaiser","împăratul","der"),("Heu","fânul","das"),("Freude","bucuria","die"),
        ("heute","azi","—"),("Feuer","focul","das"),("Bäuerin","țăranca","die"),
        ("Häuschen","căsuța","das"),("Geräusch","zgomotul","das"),("häufig","frecvent","—"),
        ("Lehrer","profesorul","der"),("Vater","tatăl","der"),("Bleistift","creionul","der"),
        ("Schreibtisch","biroul","der"),("Jahrhundert","secolul","das"),
        ("Unterricht","cursul / lecția","der"),("Widerstand","opunerea","der"),
        ("Widerspruch","contradicția","der"),("Arznei","medicamentul","die"),
        ("Elefant","elefantul","der"),("viel","mult","—"),("Asphalt","asfaltul","der"),
        ("voll","plin","—"),("Sofa","canapeaua","das"),("Vogel","pasărea","der"),
        ("Feder","pana","die"),("Prophet","profetul","der"),
        ("Ufer","malul / țărmul","das"),("vielleicht","poate / probabil","—"),
    ]
    for german, romanian, article in vocabulary:
        art = f"<small>({article})</small> " if article != "—" else ""
        notes.append(note(f"🇩🇪 <b>{german}</b>", f"{art}<b>{romanian}</b>", "Vocabular"))
        notes.append(note(f"🇷🇴 <b>{romanian}</b>", f"{art}<b>{german}</b>", "Vocabular — Invers"))

    return notes


# ---------------------------------------------------------------------------
# Export modes
# ---------------------------------------------------------------------------
def export_apkg(all_notes: list[dict], media_files: list[str]) -> None:
    """Write a self-contained .apkg file."""
    genanki_deck = genanki.Deck(DECK_ID, DECK_NAME)
    for n in all_notes:
        genanki_deck.add_note(genanki.Note(
            model=GENANKI_MODEL,
            fields=[n["front"], n["back"], n["category"], n["audio"]],
            guid=genanki.guid_for(n["front"], n["category"]),
        ))
    output = "germana_rapida.apkg"
    genanki.Package(genanki_deck, media_files=media_files).write_to_file(output)
    print(f"✅  Fișier creat: {output}")
    print(f"   Carduri: {len(genanki_deck.notes)}  |  Audio: {len(media_files)} fișiere")
    print("   Importă în Anki: File → Import → germana_rapida.apkg")


def push_to_anki(all_notes: list[dict], media_files: list[str]) -> None:
    """Push notes directly to a running Anki instance via AnkiConnect."""
    print("🔌  Connecting to AnkiConnect …")
    version = ac_invoke("version")
    print(f"   AnkiConnect v{version} — OK")

    # Ensure deck exists
    ac_invoke("createDeck", deck=DECK_NAME)
    print(f"   Deck: {DECK_NAME}")

    # Ensure model exists (createModel is a no-op if name already exists)
    existing_models = ac_invoke("modelNames")
    if MODEL_NAME not in existing_models:
        ac_invoke("createModel",
            modelName=MODEL_NAME,
            inOrderFields=["Front", "Back", "Category", "Audio"],
            css=GENANKI_MODEL.css,
            cardTemplates=[{
                "Name": "Card 1",
                "Front": GENANKI_MODEL.templates[0]["qfmt"],
                "Back":  GENANKI_MODEL.templates[0]["afmt"],
            }],
        )
        print(f"   Model '{MODEL_NAME}' created")
    else:
        print(f"   Model '{MODEL_NAME}' already exists")

    # Upload audio files
    if media_files:
        print(f"\n🔊  Uploading {len(media_files)} audio files …")
        for path in media_files:
            ac_store_media(path)
            print(f"   ✓ {os.path.basename(path)}")

    # Upsert notes
    print(f"\n📇  Syncing {len(all_notes)} cards …")
    ac_notes = [
        {
            "deckName": DECK_NAME,
            "modelName": MODEL_NAME,
            "fields": {
                "Front":    n["front"],
                "Back":     n["back"],
                "Category": n["category"],
                "Audio":    n["audio"],
            },
            "options": {"allowDuplicate": False, "duplicateScope": "deck"},
            "tags": [n["category"].replace(" ", "_").replace("—", "")],
        }
        for n in all_notes
    ]
    counts = ac_upsert_notes(ac_notes)
    print(f"\n✅  Sync complete:")
    print(f"   Added:   {counts['added']}")
    print(f"   Updated: {counts['updated']}")
    print(f"   Skipped: {counts['skipped']}")

    # Print category breakdown
    categories: dict[str, int] = {}
    for n in all_notes:
        categories[n["category"]] = categories.get(n["category"], 0) + 1
    print("\n   Categorii:")
    for cat, count in sorted(categories.items()):
        print(f"   • {cat}: {count} carduri")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Germana Rapidă — Anki deck generator")
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push cards directly to running Anki via AnkiConnect (port 8765)",
    )
    args = parser.parse_args()

    audio_map = fetch_audio_files()
    alphabet_notes, media_files = build_cards(audio_map)
    remaining_notes = build_remaining_cards()
    accent_vocab_notes = build_accent_and_vocab_cards()
    all_notes = alphabet_notes + remaining_notes + accent_vocab_notes

    if args.push:
        push_to_anki(all_notes, media_files)
    else:
        export_apkg(all_notes, media_files)
        print()
        print("💡  Tip: run with --push to sync directly to a running Anki instance.")
        print("   Audio source: tsimpliarakis.github.io/German-Cheat-Sheet")
        print("   License: CC BY-NC-SA 4.0 — Michail Tsimpliarakis")
