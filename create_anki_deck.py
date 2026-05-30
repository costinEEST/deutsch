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
Generates an .apkg file from the flashcard data extracted from README.md.
Alphabet cards include audio pronunciation sourced from:
  https://tsimpliarakis.github.io/German-Cheat-Sheet/alphabet
  (CC BY-NC-SA 4.0 — Michail Tsimpliarakis)

Run with: uv run create_anki_deck.py
"""

import os
import sys
import urllib.parse
import requests
import genanki

# ---------------------------------------------------------------------------
# Audio — download .m4a files from the German Cheat Sheet repo
# ---------------------------------------------------------------------------
AUDIO_BASE_URL = (
    "https://github.com/Tsimpliarakis/German-Cheat-Sheet"
    "/raw/main/docs/assets/audio/"
)
AUDIO_CACHE_DIR = ".audio_cache"

# letter → filename mapping (ß uses SS.m4a)
LETTER_AUDIO: dict[str, str] = {
    **{l: f"{l}.m4a" for l in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
    "Ä": "Ä.m4a",
    "Ö": "Ö.m4a",
    "Ü": "Ü.m4a",
    "ß": "SS.m4a",
}


def fetch_audio_files() -> dict[str, str]:
    """Download audio files to a local cache dir. Returns {letter: local_path}."""
    os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)
    result: dict[str, str] = {}
    total = len(LETTER_AUDIO)
    print(f"⬇️  Downloading {total} audio files …")
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
# Deck & Model IDs — fixed so re-runs update cards rather than duplicate them
# ---------------------------------------------------------------------------
DECK_ID  = 1_234_567_890
MODEL_ID = 9_876_543_210

model = genanki.Model(
    MODEL_ID,
    "Germana Rapidă",
    fields=[
        {"name": "Front"},
        {"name": "Back"},
        {"name": "Category"},
        {"name": "Audio"},   # [sound:X.m4a] or empty
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": """
<div class="category">{{Category}}</div>
<div class="front">{{Front}}</div>
{{Audio}}
""",
            "afmt": """
<div class="category">{{Category}}</div>
<div class="front">{{Front}}</div>
<hr id="answer">
<div class="back">{{Back}}</div>
{{Audio}}
""",
        }
    ],
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

deck = genanki.Deck(DECK_ID, "Germana Rapidă :: Corina Dragomir")


def card(front: str, back: str, category: str, audio: str = "") -> genanki.Note:
    return genanki.Note(
        model=model,
        fields=[front, back, category, audio],
        guid=genanki.guid_for(front, category),
    )


# ---------------------------------------------------------------------------
# 1. ALPHABET  (with audio)
# ---------------------------------------------------------------------------
def build_alphabet_cards(audio_map: dict[str, str]) -> list[str]:
    """Add alphabet cards and return list of local audio file paths to bundle."""
    alphabet = [
        ("A", "[a:]"),   ("B", "[be:]"),  ("C", "[tse:]"), ("D", "[de:]"),
        ("E", "[e:]"),   ("F", "[εf]"),   ("G", "[ge:]"),  ("H", "[ha:]"),
        ("I", "[εI:]"),  ("J", "[jdɛt]"), ("K", "[ka:]"),  ("L", "[εl]"),
        ("M", "[εm]"),   ("N", "[εn]"),   ("O", "[o:]"),   ("P", "[pe:]"),
        ("Q", "[ku:]"),  ("R", "[εr]"),   ("S", "[εs]"),   ("T", "[te:]"),
        ("U", "[u:]"),   ("V", "[fa]"),   ("W", "[ve:]"),  ("X", "[iks]"),
        ("Y", "['ypsilon]"), ("Z", "[tsεt]"),
        ("ä", "[ε:]"),   ("ö", "[ø:]"),   ("ü", "[Y:]"),
    ]
    media_files: list[str] = []
    for letter, pron in alphabet:
        upper = letter.upper()
        audio_key = upper  # Ä/Ö/Ü stay as-is; a-z → A-Z
        local_path = audio_map.get(audio_key)
        if local_path:
            filename = os.path.basename(local_path)
            sound_tag = f"[sound:{filename}]"
            media_files.append(local_path)
        else:
            sound_tag = ""
        deck.add_note(card(
            front=f"Litera germană: <b>{letter}</b>",
            back=f"Se pronunță: {pron}",
            category="Alfabet",
            audio=sound_tag,
        ))
    return media_files


# ---------------------------------------------------------------------------
# 2. VOWELS — pronunciation rules
# ---------------------------------------------------------------------------
vowels = [
    ("Macht", "[maxt]", "putere — <b>a</b> scurt, ca în rom. <i>pact</i>"),
    ("Saale / Jahr", "[sa:le] / [ja:r]", "<b>a</b> lung [a:] — ca în rom. <i>vale</i>; h prelungește vocala"),
    ("betten", "[betən]", "<b>e</b> scurt — urmat de mai multe consoane, ca în rom. <i>sec</i>"),
    ("Tränen", "[trenən]", "<b>e</b> lung deschis [e:] — ca în rom. <i>plăcere</i>"),
    ("Etage / Meer", "[eta:ʒe] / [me:r]", "<b>e</b> lung închis [e:] — ca în rom. <i>soare</i>"),
    ("offen", "[ofən]", "<b>o</b> scurt — ca în rom. <i>foc</i>"),
    ("Ozon", "[o:tson]", "<b>o</b> lung [o:] — ca în rom. <i>soră</i>"),
    ("Völker", "[foelkər]", "<b>ö</b> scurt [oe] — ca în rom. <i>bleu</i>"),
    ("Goethe / Öl", "[goe:te] / [oe:l]", "<b>ö</b> lung [oe:] — ca în rom. <i>Phoenix</i>"),
    ("Irre", "[ire]", "<b>i</b> scurt — ca în rom. <i>nivel</i>"),
    ("mir / riesig", "[mi:r] / [ri:zç]", "<b>i</b> lung [i:] — ca în rom. <i>ie, mie</i>"),
    ("Sturm", "[ʃturm]", "<b>u</b> scurt — ca în rom. <i>ulm</i>"),
    ("Blume / Ruhe", "[blu:me] / [ru:e]", "<b>u</b> lung [u:] — ca în rom. <i>lume</i>; h prelungește vocala"),
    ("Schüsse", "[ʃYse]", "<b>ü</b> scurt [Y] — ca în rom. <i>mure</i>"),
    ("drüben / führen", "[drYbən] / [fY:rən]", "<b>ü</b> lung [Y:] — ca în rom. <i>prelung</i>; h prelungește vocala"),
    ("aber", "[abər]", "<b>e</b> neaccentuat [ə] — ca în rom. <i>băiat</i>"),
]
for word, pron, rule in vowels:
    deck.add_note(card(
        front=f"Pronunție: <b>{word}</b>",
        back=f"{pron}<br><small>{rule}</small>",
        category="Pronunție — Vocale",
    ))

# ---------------------------------------------------------------------------
# 3. DIPHTHONGS
# ---------------------------------------------------------------------------
diphthongs = [
    ("ei / ai / ey / ay", "[ai]", "ca în rom. <i>mai</i> — ex: <b>mein</b> (al meu), <b>Mayer</b>"),
    ("au", "[au]", "ca în rom. <i>flaut</i> — ex: <b>Haus</b> (casă)"),
    ("eu / äu", "[oY]", "ca în rom. <i>ploi</i> — ex: <b>Leute</b> (oameni), <b>äußern</b> (a exprima)"),
    ("Rhein", "[rain]", "Rin (râu în Germania) — diftong <b>ei → [ai]</b>"),
    ("Reis", "[rais]", "orez — diftong <b>ei → [ai]</b>"),
    ("Seite", "[zaite]", "parte, față — diftong <b>ei → [ai]</b>"),
    ("Kleid", "[klaid]", "rochie — diftong <b>ei → [ai]</b>"),
    ("leise", "[laize]", "încet — diftong <b>ei → [ai]</b>"),
    ("Mais", "[mais]", "porumb — diftong <b>ai → [ai]</b>"),
    ("Kaiser", "[kaizər]", "împărat — diftong <b>ai → [ai]</b>"),
    ("Heu", "[hoY]", "fân — diftong <b>eu → [oY]</b>"),
    ("Freude", "[froYde]", "bucurie — diftong <b>eu → [oY]</b>"),
    ("heute", "[hoYte]", "azi — diftong <b>eu → [oY]</b>"),
    ("Feuer", "[foYər]", "foc — diftong <b>eu → [oY]</b>"),
    ("Bäuerin", "[boYərin]", "țărancă — diftong <b>äu → [oY]</b>"),
    ("Häuschen", "[hoYsxən]", "căsuță — diftong <b>äu → [oY]</b>"),
    ("Geräusch", "[geroYʃ]", "zgomot — diftong <b>äu → [oY]</b>"),
    ("häufig", "[hoYfiç]", "frecvent — diftong <b>äu → [oY]</b>"),
]
for word, pron, rule in diphthongs:
    deck.add_note(card(
        front=f"Pronunție: <b>{word}</b>",
        back=f"{pron}<br><small>{rule}</small>",
        category="Pronunție — Diftongi",
    ))

# ---------------------------------------------------------------------------
# 4. CONSONANTS
# ---------------------------------------------------------------------------
consonants = [
    ("b", "[b]", "ca în rom. <i>bun</i> — ex: <b>Bier</b> (bere)"),
    ("ch / -ig", "[ç]", "ca în rom. <i>Mihnea</i> — ex: <b>nicht</b> (nu), <b>riesig</b> (uriaș)"),
    ("ch (după a, o, u)", "[x]", "ca în rom. <i>hală</i> — ex: <b>Nacht</b> (noapte)"),
    ("d", "[d]", "ca în rom. <i>direcție</i> — ex: <b>das</b>"),
    ("f", "[f]", "ca în rom. <i>față</i> — ex: <b>Fieber</b> (febră)"),
    ("g", "[g]", "ca în rom. <i>gard</i> — ex: <b>Garage</b> (garaj)"),
    ("g (urmat de e)", "[ʒ]", "ca în rom. <i>jidan</i> — ex: <b>Genie</b> (geniu)"),
    ("h", "[h]", "ca în rom. <i>haită</i> — ex: <b>Herz</b> (inimă); după vocală nu se pronunță, doar prelungește"),
    ("j", "[j]", "ca în rom. <i>iese</i> — ex: <b>jagen</b> (a vâna)"),
    ("k", "[k]", "ca în rom. <i>cal</i> — ex: <b>klar</b> (clar)"),
    ("l", "[l]", "ca în rom. <i>leu</i> — ex: <b>langsam</b> (încet)"),
    ("m", "[m]", "ca în rom. <i>miel</i> — ex: <b>Mutter</b> (mama)"),
    ("n", "[n]", "ca în rom. <i>nou</i> — ex: <b>Name</b> (nume)"),
    ("n (înainte de g/k)", "[ŋ]", "nazal, ca în rom. <i>tanc</i> — ex: <b>fangen</b> (a prinde)"),
    ("p", "[p]", "ca în rom. <i>pară</i> — ex: <b>Pause</b> (pauză)"),
    ("r", "[r]", "ca în rom. <i>rândunică</i> — ex: <b>Ruhe</b> (liniște)"),
    ("S / ss / ß", "[s]", "ca în rom. <i>râs</i> — ex: <b>Essen</b> (a mânca), <b>Fluß</b> (râu)"),
    ("s (la început de cuvânt)", "[z]", "ca în rom. <i>ziuă</i> — ex: <b>Soldat</b> (soldat)"),
    ("sch", "[ʃ]", "ca în rom. <i>șanț</i> — ex: <b>Schwester</b> (soră)"),
    ("st (la început)", "[ʃt]", "ca în rom. <i>știe</i> — ex: <b>Stehlen</b> (a fura)"),
    ("sp (la început)", "[ʃp]", "ca în rom. <i>șp</i> — ex: <b>Spinat</b> (spanac)"),
    ("t", "[t]", "ca în rom. <i>tânăr</i> — ex: <b>Tod</b> (moarte)"),
    ("z", "[ts]", "ca în rom. <i>țar</i> — ex: <b>Zucker</b> (zahăr)"),
    ("w", "[v]", "ca în rom. <i>vineri</i> — ex: <b>Wein</b> (vin)"),
    ("v", "[f]", "ca în rom. <i>față</i> — ex: <b>Vater</b> (tată), <b>viel</b> (mult)"),
    ("ph", "[f]", "ca în rom. <i>față</i> — ex: <b>Asphalt</b> (asfalt), <b>Prophet</b> (profet)"),
]
for cons, pron, rule in consonants:
    deck.add_note(card(
        front=f"Consoana germană: <b>{cons}</b>",
        back=f"{pron}<br><small>{rule}</small>",
        category="Pronunție — Consoane",
    ))

# ---------------------------------------------------------------------------
# 5. DOUBLE CONSONANTS
# ---------------------------------------------------------------------------
double_consonants = [
    ("bb", "Rabbi [rabi]", "rabin — vocala dinaintea consoanei duble este scurtă"),
    ("dd", "Pudding [pudiŋ]", "budincă"),
    ("ff", "Koffer [kofər], Kaffee, Löffel [loefel]", "bagaj, cafea, lingură"),
    ("gg", "Bagger [bagər]", "excavator"),
    ("ll", "Brille [brile], Unfall [unfal]", "ochelari, accident"),
    ("mm", "Himmel [himel], Zimmer [tsimər]", "cer, cameră"),
    ("nn", "Sonne [zone]", "soare"),
    ("pp", "Teppich [tepix], Suppe [zupe]", "covor, supă"),
    ("ss", "Wasser [vasər], interessant [interesant]", "apă, interesant"),
    ("tt", "Schlitten [ʃlitən], Wetter [vetər]", "sanie, vreme"),
]
for cons, example, meaning in double_consonants:
    deck.add_note(card(
        front=f"Consoană dublă: <b>{cons}</b>",
        back=f"{example}<br><small>{meaning}</small>",
        category="Pronunție — Consoane duble",
    ))

# ---------------------------------------------------------------------------
# 6. ACCENT RULES
# ---------------------------------------------------------------------------
accent_rules = [
    (
        "Unde cade accentul în cuvintele germane simple?",
        "Pe <b>rădăcina cuvântului</b> — accentul este fix.<br>"
        "<small>Ex: der Le̲hrer (profesor), die Mu̲tter (mama), der Va̲ter (tata)</small>",
    ),
    (
        "Unde cade accentul în substantivele compuse?",
        "Pe <b>cuvântul determinativ</b> (primul element).<br>"
        "<small>Ex: der Ble̲istift (creion), der Schre̲ibtisch (birou), das Ja̲hrhundert (secol)</small>",
    ),
    (
        "Excepții — accentul NU cade pe rădăcină",
        "der U̲nterricht (curs), der Wi̲derstand (opunere), der Wi̲derspruch (contradicție)",
    ),
    (
        "Accentul la substantive cu sufixe străine (-ismus, -ar, -al, -ier, -är, -ik, -ion, -eur)",
        "Accentul cade pe <b>sufix</b>.<br>"
        "<small>Ex: Sekretärin, Kapitän, Bibliothekar, General, Offizier, Optimismus, Deklination, Ingenieur, Politik</small>",
    ),
    (
        "Accentul la sufixele -ist, -ant, -oph, -oge, -ment, -et, -iv, -em",
        "Accentul cade pe <b>sufix</b>.<br>"
        "<small>Ex: Aspirant, Philosoph, Philologe, Dokument, Dekret, Substantiv, Problem</small>",
    ),
    (
        "Accentul la verbele cu particulă separabilă",
        "Accentul cade pe <b>particulă</b>.<br>"
        "<small>Ex: e̲inladen (a invita), te̲ilnehmen (a lua parte)</small>",
    ),
    (
        "Accentul la verbele cu sufixul -ieren",
        "Accentul cade pe <b>sufix (-ie-)</b>.<br>"
        "<small>Ex: spazieren (a se plimba), studieren (a studia), reparieren (a repara)</small>",
    ),
    (
        "Accentul la adjectivele compuse",
        "Accentul cade pe <b>vocala din rădăcina fiecărui cuvânt component</b>.<br>"
        "<small>Ex: e̲iskalt (rece ca gheața), schne̲eweiß (alb ca zăpada)</small>",
    ),
    (
        "Sufixul -ei la substantive derivate",
        "Accentul cade pe <b>sufix -ei</b>.<br>"
        "<small>Ex: die Arznei (medicament) [artsnai]</small>",
    ),
]
for front, back in accent_rules:
    deck.add_note(card(front=front, back=back, category="Accent"))

# ---------------------------------------------------------------------------
# 7. VOCABULARY
# ---------------------------------------------------------------------------
vocabulary = [
    ("Macht", "puterea", "das"), ("Jahr", "anul", "das"),
    ("Tränen", "lacrimile", "die"), ("Etage", "etajul", "die"),
    ("Meer", "marea", "das"), ("Mehrheit", "majoritatea", "die"),
    ("Völker", "popoarele", "die"), ("Öl", "uleiul", "das"),
    ("Irre", "nebunul/nebuna", "der/die"), ("Sturm", "furtuna", "der"),
    ("Blume", "floarea", "die"), ("Ruhe", "liniștea", "die"),
    ("aber", "dar", "—"), ("Bier", "berea", "das"),
    ("Nacht", "noaptea", "die"), ("Fieber", "febra", "das"),
    ("Garage", "garajul", "die"), ("Genie", "geniul", "das"),
    ("Herz", "inima", "das"), ("Mutter", "mama", "die"),
    ("Name", "numele", "der"), ("Pause", "pauza", "die"),
    ("Essen", "mâncarea / a mânca", "das"), ("Soldat", "soldatul", "der"),
    ("Schwester", "sora", "die"), ("Tod", "moartea", "der"),
    ("Zucker", "zahărul", "der"), ("Wein", "vinul", "der"),
    ("Koffer", "bagajul", "der"), ("Kaffee", "cafeaua", "der"),
    ("Löffel", "lingura", "der"), ("Brille", "ochelarii", "die"),
    ("Unfall", "accidentul", "der"), ("Himmel", "cerul", "der"),
    ("Zimmer", "camera", "das"), ("Sonne", "soarele", "die"),
    ("Teppich", "covorul", "der"), ("Suppe", "supa", "die"),
    ("Wasser", "apa", "das"), ("Wetter", "vremea", "das"),
    ("Haus", "casa", "das"), ("Leute", "oamenii", "die"),
    ("mein", "al meu", "—"), ("Reis", "orezul", "der"),
    ("Seite", "partea / fața", "die"), ("Kleid", "rochia", "das"),
    ("leise", "încet (adv.)", "—"), ("Mais", "porumbul", "der"),
    ("Kaiser", "împăratul", "der"), ("Heu", "fânul", "das"),
    ("Freude", "bucuria", "die"), ("heute", "azi", "—"),
    ("Feuer", "focul", "das"), ("Bäuerin", "țăranca", "die"),
    ("Häuschen", "căsuța", "das"), ("Geräusch", "zgomotul", "das"),
    ("häufig", "frecvent", "—"), ("Lehrer", "profesorul", "der"),
    ("Vater", "tatăl", "der"), ("Bleistift", "creionul", "der"),
    ("Schreibtisch", "biroul", "der"), ("Jahrhundert", "secolul", "das"),
    ("Unterricht", "cursul / lecția", "der"), ("Widerstand", "opunerea", "der"),
    ("Widerspruch", "contradicția", "der"), ("Arznei", "medicamentul", "die"),
    ("Elefant", "elefantul", "der"), ("viel", "mult", "—"),
    ("Asphalt", "asfaltul", "der"), ("voll", "plin", "—"),
    ("Sofa", "canapeaua", "das"), ("Vogel", "pasărea", "der"),
    ("Feder", "pana", "die"), ("Prophet", "profetul", "der"),
    ("Ufer", "malul / țărmul", "das"), ("vielleicht", "poate / probabil", "—"),
]
for german, romanian, article in vocabulary:
    article_str = f"<small>({article})</small> " if article != "—" else ""
    deck.add_note(card(
        front=f"🇩🇪 <b>{german}</b>",
        back=f"{article_str}<b>{romanian}</b>",
        category="Vocabular",
    ))
    deck.add_note(card(
        front=f"🇷🇴 <b>{romanian}</b>",
        back=f"{article_str}<b>{german}</b>",
        category="Vocabular — Invers",
    ))

# ---------------------------------------------------------------------------
# Main — fetch audio, build alphabet cards, write package
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    audio_map = fetch_audio_files()
    media_files = build_alphabet_cards(audio_map)

    output_path = "germana_rapida.apkg"
    genanki.Package(deck, media_files=media_files).write_to_file(output_path)

    print(f"✅  Deck creat cu succes: {output_path}")
    print(f"   Carduri totale: {len(deck.notes)}")
    print(f"   Fișiere audio incluse: {len(media_files)}")
    print()
    print("   Categorii:")
    categories: dict[str, int] = {}
    for note in deck.notes:
        cat = note.fields[2]
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in sorted(categories.items()):
        print(f"   • {cat}: {count} carduri")
    print()
    print("   Importă fișierul în Anki: File → Import → germana_rapida.apkg")
    print()
    print("   Audio source: tsimpliarakis.github.io/German-Cheat-Sheet")
    print("   License: CC BY-NC-SA 4.0 — Michail Tsimpliarakis")
