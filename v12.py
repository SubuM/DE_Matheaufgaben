import streamlit as st
import random
from docx import Document
from io import BytesIO
import zipfile
import time
from datetime import datetime

# =============================================================================
#  v12 -- 50 harte Denkaufgaben aus dem Lehrplan Klasse 5 & 6
#  Gymnasium Sachsen-Anhalt (Fachlehrplan 01.08.2022)
#
#  Ziel: Nicht Buchwissen abfragen, sondern "out of the box"-Denken.
#  Jede Aufgabe ist randomisiert und fordert Begruendung / Strategie.
# =============================================================================

GENERATORS = []


# -----------------------------------------------------------------------------
#  A. ZAHLEN & DENKSPORT
# -----------------------------------------------------------------------------

def g_missing_digit():
    x = random.randint(11, 49)
    y = random.randint(3, 9)
    product = x * y
    s = str(x)
    i = random.randint(0, 1)
    masked = s[:i] + "_" + s[i + 1:]
    return (f"Ergaenze die fehlende Ziffer: {masked} * {y} = {product}. "
            f"Welche Ziffer gehoert an die Stelle des Unterstrichs? Begruende kurz.")


def g_consecutive():
    k = random.randint(8, 40)
    total = 3 * k + 3
    return (f"Die Summe von drei aufeinanderfolgenden natuerlichen Zahlen betraegt {total}. "
            f"Wie heissen die drei Zahlen? Beschreibe deinen Loesungsweg.")


def g_gauss():
    n = random.choice([30, 40, 50, 60, 80, 99, 100, 101, 200])
    return (f"Berechne die Summe 1 + 2 + 3 + ... + {n} moeglichst geschickt "
            f"(Gauss-Trick) und erklaere das Prinzip.")


def g_think_number():
    x = random.randint(3, 25)
    shown = 2 * x + 3
    return (f"Ich denke an eine Zahl. Ich multipliziere sie mit 4, addiere 6 und teile "
            f"das Ergebnis durch 2. Dabei erhalte ich {shown}. An welche Zahl habe ich gedacht?")


def g_digit_reverse():
    hi = random.randint(3, 9)
    lo = random.randint(0, hi - 1)
    q = hi + lo
    diff = 9 * (hi - lo)
    return (f"Eine zweistellige Zahl hat die Quersumme {q}. Vertauscht man ihre beiden Ziffern, "
            f"so ist die entstehende Zahl um {diff} kleiner als die urspruengliche Zahl. "
            f"Wie lautet die urspruengliche Zahl?")


def g_units_digit():
    b = random.randint(2, 9)
    e = random.randint(4, 20)
    return (f"Welche Einerstelle (letzte Ziffer) hat {b}^{e}? Finde einen Trick fuer das "
            f"zyklische Muster, ohne den gesamten Wert auszurechnen.")


def g_trailing_zeros():
    n = random.choice([10, 15, 20, 25, 30, 40, 45, 50])
    return (f"Wie viele Nullen stehen am Ende der Zahl {n}! (Fakultaet: {n}*{n-1}*...*1)? "
            f"Begruende deine Antwort.")


def g_divisors_count():
    n = random.choice([36, 48, 60, 72, 84, 90, 96, 108, 120, 144, 180, 200, 210, 360])
    return (f"Wie viele verschiedene Teiler hat die Zahl {n}? Finde einen systematischen Weg "
            f"(z. B. ueber die Primfaktorzerlegung).")


def g_div9():
    while True:
        a = random.randint(1, 9)
        b = random.randint(0, 9)
        if (a + b) % 9 != 0:
            break
    return (f"Bestimme die fehlende Ziffer, sodass die dreistellige Zahl {a}_{b} durch 9 teilbar "
            f"ist. Warum ist die Loesung eindeutig?")


def g_repdigit_proof():
    d = random.randint(1, 9)
    n = d * 111
    return (f"Beweise, dass jede dreistellige Zahl mit drei gleichen Ziffern (z. B. {n}) durch 37 "
            f"teilbar ist. Zerlege die Zahl dazu geschickt.")


def g_goldbach():
    n = random.choice([20, 24, 28, 30, 34, 38, 40, 42, 46, 50, 54, 60])
    return (f"Zerlege die gerade Zahl {n} als Summe zweier Primzahlen (Goldbachsche Vermutung). "
            f"Gib eine Moeglichkeit an und pruefe beide Zahlen auf Primalitaet.")


def g_divisible_by_9_proof():
    return ("Waehle eine beliebige zweistellige Zahl und subtrahiere ihre Umkehrung. "
            "Warum ist das Ergebnis immer durch 9 teilbar? Pruefe mit zwei Beispielen "
            "und begruende es allgemein.")


def g_sum_odd():
    n = random.choice([10, 20, 30, 40, 50])
    return (f"Berechne die Summe der ersten {n} ungeraden Zahlen: 1 + 3 + 5 + ... "
            f"Welche Gesetzmaessigkeit erkennst du?")


def g_binary():
    n = random.randint(5, 60)
    b = bin(n)[2:]
    return (f"Die Zahl {b} ist im Binaersystem (Zweiersystem) geschrieben. "
            f"Wie lautet ihr Wert im Dezimalsystem?")


def g_signed_trick():
    a = random.randint(2, 6)
    return (f"Vergleiche die beiden Ausdruecke (-{a})^2 und -{a}^2. Berechne beide und "
            f"erklaere den Unterschied.")


GENERATORS += [
    g_missing_digit, g_consecutive, g_gauss, g_think_number, g_digit_reverse,
    g_units_digit, g_trailing_zeros, g_divisors_count, g_div9, g_repdigit_proof,
    g_goldbach, g_divisible_by_9_proof, g_sum_odd, g_binary, g_signed_trick,
]


# -----------------------------------------------------------------------------
#  B. BRUECHE, PROZENTE, VERHAELTNISSE
# -----------------------------------------------------------------------------

def g_fraction_remaining():
    a, b, c, d = random.choice([
        (3, 4, 2, 3), (2, 3, 1, 4), (4, 5, 1, 2),
        (5, 6, 2, 5), (3, 5, 1, 3), (7, 8, 3, 7),
    ])
    return (f"Ein Behaelter ist zu {a}/{b} gefuellt. Man entnimmt {c}/{d} des vorhandenen Inhalts. "
            f"Welcher Anteil des Behaelters bleibt gefuellt? Berechne.")


def g_successive_percent():
    p = random.choice([10, 20, 25, 50])
    base = random.choice([200, 400, 500, 800, 1000, 1200])
    final = round(base * (1 + p / 100) * (1 - p / 100), 2)
    return (f"Der Preis eines Artikels von {base} Euro wird zuerst um {p} % erhoeht und "
            f"anschliessend um {p} % gesenkt. Wie hoch ist der Endpreis? Ist er gleich dem "
            f"Ausgangspreis? Warum (nicht)?")


def g_double_discount():
    p1, p2 = random.choice([(20, 10), (25, 20), (30, 10), (40, 20)])
    base = random.choice([200, 300, 500, 800, 1000])
    final = round(base * (1 - p1 / 100) * (1 - p2 / 100), 2)
    return (f"Ein Artikel kostet {base} Euro. Zuerst gibt es {p1} % Rabatt, danach auf den neuen "
            f"Preis nochmals {p2} % Rabatt. Ein Kunde glaubt, der Preis sinkt um {p1 + p2} %. "
            f"Berechne den tatsaechlichen Endpreis und den wahren Gesamtrabatt in Prozent.")


def g_ratio_sharing():
    r = random.choice([(1, 2, 3), (2, 3, 5), (1, 1, 2), (3, 4, 5), (1, 2, 4), (2, 3, 4)])
    unit = random.randint(5, 50)
    total = sum(r) * unit
    return (f"Teile {total} Euro im Verhaeltnis {' : '.join(map(str, r))} auf. "
            f"Wie viel erhaelt jeder Anteil?")


def g_reverse_discount():
    orig = random.choice([80, 120, 150, 200, 250, 400, 500])
    p = random.choice([10, 20, 25, 50])
    final = round(orig * (100 - p) / 100, 2)
    return (f"Nach einem Rabatt von {p} % kostet ein Artikel noch {final} Euro. Wie hoch war der "
            f"urspruengliche Preis? Achtung: Einfaches Addieren von {p} % liefert ein falsches "
            f"Ergebnis - erklaere den Unterschied.")


def g_unit_fraction():
    n = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
    return (f"Schreibe den Stammbruch 1/{n} als Summe zweier verschiedener Stammbrueche: "
            f"1/{n} = 1/{n + 1} + 1/___. Bestimme die fehlende Zahl und begruende die Identitaet.")


def g_recipe():
    persons = random.randint(3, 6)
    target = persons + random.choice([1, 2, 3, 5])
    sugar = random.randint(2, 8) * persons
    return (f"Ein Rezept fuer {persons} Personen benoetigt {sugar} g Zucker. "
            f"Wie viel Zucker braucht man fuer {target} Personen? Erklaere den Rechenweg (Dreisatz).")


GENERATORS += [
    g_fraction_remaining, g_successive_percent, g_double_discount, g_ratio_sharing,
    g_reverse_discount, g_unit_fraction, g_recipe,
]


# -----------------------------------------------------------------------------
#  C. TERME, GLEICHUNGEN, FUNKTIONEN
# -----------------------------------------------------------------------------

def g_term_trick():
    x = random.randint(5, 25)
    return (f"Berechne ({x + 1})^2 - ({x - 1})^2 geschickt, ohne beide Quadrate vollstaendig "
            f"auszurechnen. Welcher Term vereinfacht den Ausdruck?")


def g_linear_two_points():
    x1 = random.randint(0, 3)
    x2 = x1 + random.randint(1, 4)
    m = random.choice([i for i in range(-4, 5) if i != 0])
    n = random.randint(-6, 6)
    y1 = m * x1 + n
    y2 = m * x2 + n
    return (f"Eine Gerade verlaeuft durch die Punkte A({x1}|{y1}) und B({x2}|{y2}). "
            f"Bestimme die Funktionsgleichung f(x) = m*x + n und die Nullstelle.")


def g_function_riddle():
    m = random.randint(2, 6)
    n = random.choice([i for i in range(-8, 9) if i != 0])
    x0 = random.randint(-5, 5)
    y0 = m * x0 + n
    return (f"Gegeben ist f(x) = {m}x {n:+d}. Fuer welchen Wert von x liefert die Funktion den "
            f"Wert {y0}? Loese durch Rueckwaertsrechnen.")


def g_age_puzzle():
    k = random.randint(3, 6)
    t = random.randint(2, 6)
    son = t * (k - 2)
    return (f"Ein Vater ist heute {k}-mal so alt wie sein Sohn. In {t} Jahren ist er nur noch "
            f"{k - 1}-mal so alt. Wie alt ist der Sohn heute?")


def g_inverse_proportion():
    workers = random.randint(3, 12)
    new_workers = random.randint(2, 9)
    k = random.randint(2, 8)
    base_days = new_workers * k
    return (f"Fuer eine Arbeit benoetigen {workers} Arbeiter {base_days} Tage. Wie viele Tage "
            f"brauchen {new_workers} Arbeiter, wenn alle gleich schnell arbeiten?")


GENERATORS += [
    g_term_trick, g_linear_two_points, g_function_riddle, g_age_puzzle, g_inverse_proportion,
]


# -----------------------------------------------------------------------------
#  D. RAUM UND FORM
# -----------------------------------------------------------------------------

def g_angle_clock():
    h = random.randint(1, 12)
    m = random.choice([0, 10, 20, 30, 40, 50])
    angle = abs(30 * h - 5.5 * m)
    angle = min(angle, 360 - angle)
    return (f"Welchen (kleineren) Winkel schliessen der Stunden- und der Minutenzeiger einer Uhr "
            f"um {h}:{m:02d} Uhr ein?")


def g_angle_ratio_triangle():
    ratio = random.choice([(1, 2, 3), (2, 3, 4), (1, 1, 2), (3, 4, 5), (1, 2, 6), (2, 2, 5)])
    return (f"Die Winkel eines Dreiecks verhalten sich wie {' : '.join(map(str, ratio))}. "
            f"Berechne alle drei Winkel und pruefe die Winkelsumme.")


def g_optimize_area():
    P = random.choice([20, 24, 32, 36, 40, 48, 60])
    return (f"Ein Rechteck hat den Umfang {P} cm. Wie muessen Laenge und Breite gewaehlt werden, "
            f"damit der Flaecheninhalt maximal wird? Wie gross ist dann die Flaeche? Begruende.")


def g_similar_shadow():
    ph = random.choice([1.5, 1.6, 1.8, 2.0])
    sh1 = round(random.uniform(1.0, 3.0), 1)
    sh2 = round(random.uniform(4.0, 12.0), 1)
    return (f"Ein {ph} m grosser Mensch wirft bei Sonnenlicht einen Schatten von {sh1} m. "
            f"Zur gleichen Zeit wirft ein Baum einen Schatten von {sh2} m. Wie hoch ist der Baum? "
            f"(Strahlensatz)")


def g_circle_in_square():
    s = random.choice([4, 6, 8, 10, 12, 16, 20])
    return (f"Einem Quadrat mit der Seitenlaenge {s} cm wird ein Kreis einbeschrieben. "
            f"Wie gross ist der Flaecheninhalt der Restflaeche zwischen Quadrat und Kreis? "
            f"(pi ~ 3,14)")


def g_volume_displacement():
    a = random.randint(6, 15)
    b = random.randint(6, 15)
    h = random.randint(1, 5)
    return (f"In ein quaderfoermiges Gefaess mit der Grundflaeche {a} cm x {b} cm wird ein Stein "
            f"vollstaendig eingetaucht. Der Wasserspiegel steigt dabei um {h} cm. "
            f"Wie gross ist das Volumen des Steins?")


def g_pythagoras_ladder():
    p, q, r = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)])
    return (f"Eine Leiter lehnt an einer Hauswand. Ihr Fuss steht {p} m von der Wand entfernt; "
            f"die Spitze reicht {q} m hoch. Wie lang ist die Leiter? "
            f"Berechne mit dem Satz des Pythagoras.")


def g_regular_polygon():
    n = random.randint(5, 12)
    total = (n - 2) * 180
    return (f"Wie gross ist jeder Innenwinkel eines regelmaessigen {n}-Ecks? "
            f"Gib auch die Innenwinkelsumme an.")


GENERATORS += [
    g_angle_clock, g_angle_ratio_triangle, g_optimize_area, g_similar_shadow,
    g_circle_in_square, g_volume_displacement, g_pythagoras_ladder, g_regular_polygon,
]


# -----------------------------------------------------------------------------
#  E. KOMBINATORIK, WAHRSCHEINLICHKEIT, LOGIK
# -----------------------------------------------------------------------------

def g_handshake():
    n = random.randint(6, 15)
    return (f"Bei einer Feier begruessen sich {n} Personen, jede mit jeder genau einmal per "
            f"Handschlag. Wie viele Handschlaege gibt es insgesamt? Finde eine Formel.")


def g_count_rectangles():
    rows = random.randint(2, 4)
    cols = random.randint(2, 5)
    return (f"Wie viele verschiedene Rechtecke (einschliesslich Quadrate) lassen sich in einem "
            f"{rows} x {cols}-Raster aus Einheitsquadraten zaehlen? Entwickle eine Zaehlstrategie.")


def g_grid_paths():
    r = random.randint(2, 5)
    u = random.randint(2, 5)
    return (f"Ein Roboter bewegt sich auf einem Gitter nur nach Osten oder Norden. "
            f"Wie viele verschiedene Wege fuehren von (0|0) zu ({r}|{u})? Berechne die Anzahl.")


def g_socks():
    colors = random.randint(3, 6)
    return (f"In einer Schublade liegen Socken in {colors} verschiedenen Farben. "
            f"Wie viele Socken muss man im Dunkeln mindestens herausnehmen, um sicher ein Paar "
            f"gleicher Farbe zu haben? Begruende mit dem Schubfachprinzip.")


def g_prob_without_replacement():
    r = random.randint(3, 7)
    b = random.randint(3, 7)
    return (f"In einer Urne sind {r} rote und {b} blaue Kugeln. Es werden zwei Kugeln gleichzeitig "
            f"gezogen. Wie gross ist die Wahrscheinlichkeit, dass beide rot sind? (als Bruch)")


def g_two_dice():
    k = random.randint(4, 10)
    return (f"Zwei faire Wuerfel werden geworfen. Wie gross ist die Wahrscheinlichkeit, dass die "
            f"Augensumme genau {k} betraegt? Gib den Bruch und den Prozentwert an.")


def g_fair_game():
    payout = random.choice([6, 12, 18, 24])
    target = random.randint(1, 6)
    return (f"Bei einem Gluecksspiel gewinnt man {payout} Euro, wenn mit einem fairen Wuerfel eine "
            f"{target} faellt, sonst nichts. Welcher Einsatz waere fair "
            f"(Erwartungswert = 0)?")


def g_venn():
    a = random.randint(8, 15)
    b = random.randint(8, 15)
    both = random.randint(2, min(a, b) - 1)
    neither = random.randint(1, 6)
    total = (a - both) + (b - both) + both + neither
    return (f"In einer Klasse mit {total} Kindern moegen {a} Mathematik und {b} Englisch; "
            f"{both} moegen beide Faecher. Wie viele Kinder moegen keines der beiden Faecher? "
            f"Beschreibe deinen Loesungsweg.")


def g_password_pin():
    return ("Wie viele verschiedene 4-stellige Geheimzahlen (PINs) gibt es, bei denen sich keine "
            "Ziffer wiederholt? Begruende mit dem Zaehlprinzip.")


def g_weighing():
    n = random.choice([3, 9, 27])
    return (f"Unter {n} aeusserlich gleichen Muenzen ist genau eine leichtere Faelschung. "
            f"Wie viele Waegungen mit einer Balkenwaage braucht man mindestens, um sie sicher zu "
            f"finden? Erklaere das Vorgehen.")


GENERATORS += [
    g_handshake, g_count_rectangles, g_grid_paths, g_socks, g_prob_without_replacement,
    g_two_dice, g_fair_game, g_venn, g_password_pin, g_weighing,
]


# -----------------------------------------------------------------------------
#  F. MESSEN, BEWEGUNG, MUSTER
# -----------------------------------------------------------------------------

def g_work_rate():
    a, b, _ = random.choice([(4, 12, 3), (6, 12, 4), (8, 24, 6), (10, 15, 6),
                             (12, 6, 4), (20, 30, 12), (6, 3, 2)])
    return (f"Ein Rohr fuellt ein Becken in {a} Stunden, ein zweites Rohr in {b} Stunden. "
            f"Wie lange dauert es, wenn beide Rohre zusammen geoeffnet sind? "
            f"(Begruende, warum man die Zeiten nicht einfach addieren darf.)")


def g_speed_meeting():
    v1 = random.randint(30, 90)
    v2 = random.randint(30, 90)
    t = random.randint(1, 4)
    d = (v1 + v2) * t
    return (f"Zwei Staedte sind {d} km voneinander entfernt. Zwei Fahrzeuge starten gleichzeitig "
            f"mit {v1} km/h bzw. {v2} km/h aufeinander zu. Nach welcher Zeit und in welcher "
            f"Entfernung von Stadt A treffen sie sich?")


def g_scale_map():
    scale = random.choice([25000, 50000, 100000, 200000])
    cm = random.choice([2, 3, 4, 5, 6, 8])
    km = (cm * scale) / 100000
    return (f"Zwei Orte sind auf einer Karte im Massstab 1:{scale} genau {cm} cm voneinander "
            f"entfernt. Wie weit sind sie in Wirklichkeit (in km)?")


def g_clock_overlap():
    h = random.randint(1, 10)
    return (f"Zwischen {h} und {h + 1} Uhr ueberholen sich Minuten- und Stundenzeiger. "
            f"Zu welcher Uhrzeit (auf die Minute gerundet) geschieht das? Erklaere deine Rechnung.")


def g_sequence_law():
    return ("Setze die Folge fort: 2, 6, 12, 20, 30, ... Bestimme die naechsten zwei Zahlen und "
            "beschreibe das Bildungsgesetz.")


GENERATORS += [
    g_work_rate, g_speed_meeting, g_scale_map, g_clock_overlap, g_sequence_law,
]


# =============================================================================
#  Generierungsfunktionen (zufaellige Aufgabentypen, ohne Wiederholungen)
# =============================================================================

def create_single_problem_set(num_problems=50):
    """Erzeugt eine Liste von Aufgaben mit voellig zufaellig gemixten Typen."""
    problems = []
    seen = set()
    attempts = 0
    limit = num_problems * 60

    while len(problems) < num_problems and attempts < limit:
        attempts += 1
        generator = random.choice(GENERATORS)
        try:
            candidate = generator()
        except Exception:
            continue
        if candidate not in seen:
            seen.add(candidate)
            problems.append(candidate)

    while len(problems) < num_problems:
        problems.append(random.choice(GENERATORS)())

    return problems


def create_word_document(problems, set_number):
    """Erstellt ein Word-Dokument (im Speicher) und gibt es als Bytes zurueck."""
    document = Document()
    document.add_heading(
        f'50 haerteste Mathematikaufgaben - Gymnasium Kl. 5 & 6 '
        f'(Sachsen-Anhalt) - Set {set_number}', 0
    )
    document.add_paragraph(
        "Denkaufgaben mit erhoehtem Schwierigkeitsgrad. "
        "Begruende jeden Loesungsweg - nicht nur das Ergebnis zaehlt."
    )
    document.add_paragraph(
        f"Erstellt am {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )
    for i, problem in enumerate(problems, 1):
        document.add_paragraph(f"{i}. {problem}")

    bio = BytesIO()
    document.save(bio)
    bio.seek(0)
    return bio.getvalue()


# =============================================================================
#  Streamlit Login und Hauptprogramm (Operabilitaet aus streamlit_app.py)
# =============================================================================

def login_form():
    """Zeigt das Login-Formular an und prueft die Anmeldedaten aus st.secrets."""
    try:
        STATIC_USER = st.secrets["auth"]["username"]
        STATIC_PASS = st.secrets["auth"]["password"]
    except KeyError:
        st.error("Konfigurationsfehler: Bitte stellen Sie sicher, dass die Datei "
                 "'.streamlit/secrets.toml' mit der Sektion [auth] existiert.")
        return

    st.sidebar.header("Login erforderlich")
    with st.sidebar.form("login_form"):
        username = st.text_input("Benutzername")
        password = st.text_input("Passwort", type="password")
        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            if username == STATIC_USER and password == STATIC_PASS:
                st.session_state["authenticated"] = True
                st.success("Login erfolgreich!")
            else:
                st.error("Ungueltiger Benutzername oder Passwort.")


def main_app():
    """Die Hauptanwendung, die nur nach erfolgreichem Login angezeigt wird."""
    st.title("Matheaufgaben-Generator v12 (Denksport)")
    st.markdown("Generiert bis zu **10 Saetze** mit je **50 haertesten, zufaellig "
                "gemischten Denkaufgaben** aus Klasse 5 & 6.")
    st.markdown("---")

    # Vorschau einer zufaellig gemischten Aufgabe
    st.subheader("Vorschau")
    if st.button("Zufaellige Denkaufgabe anzeigen", key="preview_v12"):
        st.info(random.choice(GENERATORS)())
    st.markdown("---")

    num_sets = st.number_input(
        "1. Anzahl der benoetigten Aufgabensaetze:",
        min_value=1,
        max_value=10,
        value=5,
        help="Maximal 10 Sets empfohlen, um die Einzigartigkeit zu garantieren."
    )

    download_location = st.text_input(
        "2. Gewuenschter lokaler Speicherpfad (zur Information):",
        value="C:/Users/IhrName/Downloads/Matheaufgaben_Schwer/",
        help="Der Pfad dient nur als Hinweis, der Download erfolgt ueber den Browser."
    )

    st.markdown("---")

    if st.button(f"Starte Generierung von {num_sets} Saetzen und erstelle ZIP-Datei",
                 type="primary"):

        zip_buffer = BytesIO()

        with st.status("Starte die Generierung...", expanded=True) as status:
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                for i in range(1, int(num_sets) + 1):
                    status.write(f"Set {i}/{num_sets}: Erstelle 50 Denkaufgaben...")
                    problems = create_single_problem_set(num_problems=50)
                    docx_bytes = create_word_document(problems, i)
                    filename = f"Denkaufgaben_Set_{i:02d}.docx"
                    zf.writestr(filename, docx_bytes)
                    status.write(f"OK - {filename} zur ZIP-Datei hinzugefuegt.")

                status.update(label="Komprimiere und finalisiere das ZIP-Archiv...",
                              state="running")
                time.sleep(1)

            zip_buffer.seek(0)
            status.update(
                label=f"{num_sets} Aufgabensaetze sind bereit zum Download!",
                state="complete",
                expanded=False,
            )

        st.markdown("---")
        st.markdown(f"**Hinweis:** Die Dateien waeren lokal unter dem Pfad "
                    f"`{download_location}` gespeichert worden.")

        st.download_button(
            label="Alle Saetze als ZIP-Datei herunterladen",
            data=zip_buffer,
            file_name="Matheaufgaben_Klasse_5_6_DENKSPORT.zip",
            mime="application/zip",
            key="download_zip_button_v12"
        )


if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        main_app()
    else:
        login_form()
