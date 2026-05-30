#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "genanki",
# ]
# ///
"""
Germana Rapidă — Anki Deck Generator
Generates an .apkg file from the flashcard data extracted from README.md
Run with: uv run create_anki_deck.py
"""

import genanki
import random

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
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": """
<div class="category">{{Category}}</div>
<div class="front">{{Front}}</div>
""",
            "afmt": """
<div class="category">{{Category}}</div>
<div class="front">{{Front}}</div>
<hr id="answer">
<div class="back">{{Back}}</div>
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


def card(front: str, back: str, category: str) -> genanki.Note:
    return genanki.Note(
        model=model,
        fields=[front, back, category],
        # deterministic guid so re-runs don't create duplicates
        guid=genanki.guid_for(front, category),
    )


# ---------------------------------------------------------------------------
# 1. ALPHABET
# ---------------------------------------------------------------------------
alphabet = [
    ("A", "[a:]"), ("B", "[be:]"), ("C", "[tse:]"), ("D", "[de:]"),
    ("E", "[e:]"), ("F", "[εf]"), ("G", "[ge:]"), ("H", "[ha:]"),
    ("I", "[εI:]"), ("J", "[jdɛt]"), ("K", "[ka:]"), ("L", "[εl]"),
    ("M", "[εm]"), ("N", "[εn]"), ("O", "[o:]"), ("P", "[pe:]"),
    ("Q", "[ku:]"), ("R", "[εr]"), ("S", "[εs]"), ("T", "[te:]"),
    ("U", "[u:]"), ("V", "[fa]"), ("W", "[ve:]"), ("X", "[iks]"),
    ("Y", "['ypsilon]"), ("Z", "[tsεt]"),
    ("ä", "[ε:]"), ("ö", "[ø:]"), ("ü", "[Y:]"),
]
for letter, pron in alphabet:
    deck.add_note(card(
        front=f"Litera germană: <b>{letter}</b>",
        back=f"Se pronunță: {pron}",
        category="Alfabet",
    ))

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
    # -ei words
    ("Rhein", "[rain]", "Rin (râu în Germania) — diftong <b>ei → [ai]</b>"),
    ("Reis", "[rais]", "orez — diftong <b>ei → [ai]</b>"),
    ("Seite", "[zaite]", "parte, față — diftong <b>ei → [ai]</b>"),
    ("Kleid", "[klaid]", "rochie — diftong <b>ei → [ai]</b>"),
    ("leise", "[laize]", "încet — diftong <b>ei → [ai]</b>"),
    # -ai words
    ("Mais", "[mais]", "porumb — diftong <b>ai → [ai]</b>"),
    ("Kaiser", "[kaizər]", "împărat — diftong <b>ai → [ai]</b>"),
    # -eu words
    ("Heu", "[hoY]", "fân — diftong <b>eu → [oY]</b>"),
    ("Freude", "[froYde]", "bucurie — diftong <b>eu → [oY]</b>"),
    ("heute", "[hoYte]", "azi — diftong <b>eu → [oY]</b>"),
    ("Feuer", "[foYər]", "foc — diftong <b>eu → [oY]</b>"),
    # -äu words
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
# 7. VOCABULARY — words extracted from pronunciation examples
# ---------------------------------------------------------------------------
vocabulary = [
    # from vowels section
    ("Macht", "puterea", "das"),
    ("Jahr", "anul", "das"),
    ("Tränen", "lacrimile", "die"),
    ("Etage", "etajul", "die"),
    ("Meer", "marea", "das"),
    ("Mehrheit", "majoritatea", "die"),
    ("Völker", "popoarele", "die"),
    ("Öl", "uleiul", "das"),
    ("Irre", "nebunul/nebuna", "der/die"),
    ("Sturm", "furtuna", "der"),
    ("Blume", "floarea", "die"),
    ("Ruhe", "liniștea", "die"),
    ("aber", "dar", "—"),
    # from consonants section
    ("Bier", "berea", "das"),
    ("Nacht", "noaptea", "die"),
    ("Fieber", "febra", "das"),
    ("Garage", "garajul", "die"),
    ("Genie", "geniul", "das"),
    ("Herz", "inima", "das"),
    ("Mutter", "mama", "die"),
    ("Name", "numele", "der"),
    ("Pause", "pauza", "die"),
    ("Essen", "mâncarea / a mânca", "das"),
    ("Soldat", "soldatul", "der"),
    ("Schwester", "sora", "die"),
    ("Tod", "moartea", "der"),
    ("Zucker", "zahărul", "der"),
    ("Wein", "vinul", "der"),
    # from double consonants
    ("Koffer", "bagajul", "der"),
    ("Kaffee", "cafeaua", "der"),
    ("Löffel", "lingura", "der"),
    ("Brille", "ochelarii", "die"),
    ("Unfall", "accidentul", "der"),
    ("Himmel", "cerul", "der"),
    ("Zimmer", "camera", "das"),
    ("Sonne", "soarele", "die"),
    ("Teppich", "covorul", "der"),
    ("Suppe", "supa", "die"),
    ("Wasser", "apa", "das"),
    ("Wetter", "vremea", "das"),
    # from diphthongs
    ("Haus", "casa", "das"),
    ("Leute", "oamenii", "die"),
    ("mein", "al meu", "—"),
    ("Reis", "orezul", "der"),
    ("Seite", "partea / fața", "die"),
    ("Kleid", "rochia", "das"),
    ("leise", "încet (adv.)", "—"),
    ("Mais", "porumbul", "der"),
    ("Kaiser", "împăratul", "der"),
    ("Heu", "fânul", "das"),
    ("Freude", "bucuria", "die"),
    ("heute", "azi", "—"),
    ("Feuer", "focul", "das"),
    ("Bäuerin", "țăranca", "die"),
    ("Häuschen", "căsuța", "das"),
    ("Geräusch", "zgomotul", "das"),
    ("häufig", "frecvent", "—"),
    # from accent section
    ("Lehrer", "profesorul", "der"),
    ("Vater", "tatăl", "der"),
    ("Bleistift", "creionul", "der"),
    ("Schreibtisch", "biroul", "der"),
    ("Jahrhundert", "secolul", "das"),
    ("Unterricht", "cursul / lecția", "der"),
    ("Widerstand", "opunerea", "der"),
    ("Widerspruch", "contradicția", "der"),
    ("Arznei", "medicamentul", "die"),
    # from [εf] section
    ("Elefant", "elefantul", "der"),
    ("viel", "mult", "—"),
    ("Asphalt", "asfaltul", "der"),
    ("voll", "plin", "—"),
    ("Sofa", "canapeaua", "das"),
    ("Vogel", "pasărea", "der"),
    ("Feder", "pana", "die"),
    ("Prophet", "profetul", "der"),
    ("Ufer", "malul / țărmul", "das"),
    ("vielleicht", "poate / probabil", "—"),
]
for german, romanian, article in vocabulary:
    article_str = f"<small>({article})</small> " if article != "—" else ""
    deck.add_note(card(
        front=f"🇩🇪 <b>{german}</b>",
        back=f"{article_str}<b>{romanian}</b>",
        category="Vocabular",
    ))
    # reverse card: Romanian → German
    deck.add_note(card(
        front=f"🇷🇴 <b>{romanian}</b>",
        back=f"{article_str}<b>{german}</b>",
        category="Vocabular — Invers",
    ))

# ---------------------------------------------------------------------------
# Write the package
# ---------------------------------------------------------------------------
output_path = "germana_rapida.apkg"
genanki.Package(deck).write_to_file(output_path)
print(f"✅  Deck creat cu succes: {output_path}")
print(f"   Carduri totale: {len(deck.notes)}")
print()
print("   Categorii:")
categories = {}
for note in deck.notes:
    cat = note.fields[2]
    categories[cat] = categories.get(cat, 0) + 1
for cat, count in sorted(categories.items()):
    print(f"   • {cat}: {count} carduri")
print()
print("   Importă fișierul în Anki: File → Import → germana_rapida.apkg")
