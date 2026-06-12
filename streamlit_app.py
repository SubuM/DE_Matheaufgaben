import streamlit as st
import random
from docx import Document
from io import BytesIO
import zipfile
import os
import time
import math

# --- Page configuration ---
st.set_page_config(
    page_title="Matheaufgaben-Generator | Gymnasium Sachsen-Anhalt",
    page_icon="🎓",
    layout="centered"
)

# --- Inject Custom Styling for Rich Premium Look ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    background: radial-gradient(circle at 10% 20%, rgba(90, 92, 234, 0.05) 0%, rgba(253, 222, 230, 0.05) 90%);
}

h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    color: #1E293B;
}

/* Custom card container styling */
.premium-card {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    box-shadow: 0 10px 30px rgba(30, 41, 59, 0.04);
    margin-bottom: 24px;
}

/* Accent header gradient */
.gradient-text {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* Customize buttons */
div.stButton > button {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%) !important;
    color: white !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
    transition: all 0.2s ease-in-out !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.4) !important;
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
}

/* Sidebar layout */
[data-testid="stSidebar"] {
    background: rgba(248, 250, 252, 0.95);
    border-right: 1px solid #E2E8F0;
}
</style>
""", unsafe_allow_html=True)

# --- Generator Functions (Tough Problems - DEFINED HERE) ---

GENERATORS = []

# 1. Zahlen und Operationen (Large Numbers, Divisibility Rules, Prime Factorization, ggT/kgV)
def generate_zahlen_operationen_tough():
    sub_type = random.choice(['schriftlich_mul_div', 'teilbarkeit', 'primfaktorzerlegung', 'ggt_kgv'])
    if sub_type == 'schriftlich_mul_div':
        if random.choice([True, False]):
            num1 = random.randint(123456, 9876543)
            num2 = random.randint(1234, 98765)
            return f"Berechne schriftlich: {num1} x {num2}."
        else:
            divisor = random.randint(23, 999)
            quotient = random.randint(12345, 98765)
            remainder = random.randint(1, divisor - 1)
            num1 = divisor * quotient + remainder
            return f"Berechne schriftlich: {num1} : {divisor} (Gib das Ergebnis mit Rest an)."
    elif sub_type == 'teilbarkeit':
        num = random.randint(100000, 9999999)
        d_choices = [3, 4, 6, 8, 9]
        random.shuffle(d_choices)
        ds = sorted(d_choices[:4])
        ds_str = ", ".join(map(str, ds[:-1])) + " und " + str(ds[-1])
        return f"Überprüfe die Zahl {num} auf Teilbarkeit durch {ds_str}. Begründe deine Entscheidung mithilfe der jeweiligen Teilbarkeitsregeln."
    elif sub_type == 'primfaktorzerlegung':
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        num_factors = random.randint(4, 6)
        factors = [random.choice(primes) for _ in range(num_factors)]
        num = 1
        for f in factors:
            num *= f
        while not (500 <= num <= 20000):
            factors = [random.choice(primes) for _ in range(num_factors)]
            num = 1
            for f in factors:
                num *= f
        return f"Bestimme die Primfaktorzerlegung der Zahl {num}."
    else: # ggt_kgv
        base = random.choice([12, 15, 18, 24, 36, 48])
        a = base * random.randint(3, 12)
        b = base * random.randint(3, 12)
        while a == b:
            b = base * random.randint(3, 12)
        return f"Bestimme den größten gemeinsamen Teiler (ggT) und das kleinste gemeinsame Vielfache (kgV) der Zahlen {a} und {b}."

GENERATORS.append(generate_zahlen_operationen_tough)

# 2. Rounding
def generate_rounding_tough():
    if random.choice([True, False]):
        # Large integer rounding
        num = random.randint(10000000, 999999999)
        place = random.choice(['Millionen', 'Zehnmillionen', 'Hunderttausender'])
        return f"Runde die Zahl {num} auf die nächsten {place}."
    else:
        # Decimal rounding
        num = round(random.uniform(0.1234, 9.8765), 4)
        place = random.choice(['Zehntel', 'Hundertstel', 'Tausendstel'])
        return f"Runde die Dezimalzahl {num} auf {place}."

GENERATORS.append(generate_rounding_tough)

# 3. Order of Operations (Rechengesetze & Klammern)
def generate_order_of_operations_tough():
    pattern_choice = random.choice([1, 2, 3])
    if pattern_choice == 1:
        base = random.choice([2, 3, 5])
        exp = 2 if base == 5 else (3 if base == 3 else random.choice([3, 4, 5]))
        val = base ** exp
        c = random.randint(2, val - 2)
        d = random.randint(3, 8)
        f = random.randint(15, 40)
        g = random.randint(2, f - 3)
        e = random.randint(4, 9)
        return f"Berechne den Wert des Terms: ({base} hoch {exp} - {c}) x {d} + {e} x ({f} - {g})"
    elif pattern_choice == 2:
        d = random.randint(4, 10)
        e = random.randint(2, d*d - 2)
        c = random.randint(2, 5)
        b = random.randint(5, 20)
        a = random.randint(2, 6)
        return f"Berechne: {a} x [{b} + {c} x ({d}² - {e})]"
    else:
        d = random.randint(2, 10)
        c = d + random.randint(3, 12)
        b = random.randint(3, 8)
        inner = b * (c - d)
        a = random.randint(5, 20)
        total = a + inner
        divisors = [i for i in range(2, 11) if total % i == 0]
        if divisors:
            e = random.choice(divisors)
        else:
            e = random.choice([3, 5])
            a = e * random.randint(2, 10) - inner
            while a <= 0:
                a += e
            total = a + inner
        return f"Berechne den Wert des Terms: {{{a} + [{b} x ({c} - {d})]}} : {e}"

GENERATORS.append(generate_order_of_operations_tough)

# 4. Fractions & Decimals (Gemeine Brüche und Dezimalbrüche - Class 6 focus)
def generate_fractions_decimals_tough():
    sub_type = random.choice(['kuerzen_erweitern', 'bruch_rechnung', 'dezimal_rechnung', 'umwandlung'])
    if sub_type == 'kuerzen_erweitern':
        if random.choice([True, False]):
            common = random.choice([12, 15, 18, 24, 36])
            num_base = random.choice([2, 3, 5, 7, 11])
            den_base = random.choice([3, 4, 5, 7, 11])
            while num_base == den_base:
                den_base = random.choice([3, 4, 5, 7, 11])
            num = num_base * common
            den = den_base * common
            return f"Kürze den Bruch {num}/{den} so weit wie möglich."
        else:
            num = random.randint(2, 9)
            den = random.randint(num + 1, 12)
            factor = random.randint(3, 12)
            target_den = den * factor
            return f"Erweitere den Bruch {num}/{den} so, dass der Nenner {target_den} beträgt. Welcher Zähler ergibt sich?"
    elif sub_type == 'bruch_rechnung':
        den1, den2, den3 = random.choice([
            (2, 3, 4), (3, 4, 6), (2, 5, 10), (4, 5, 10), (3, 5, 15), (4, 6, 8)
        ])
        num1 = random.randint(1, den1 - 1)
        num2 = random.randint(1, den2 - 1)
        num3 = random.randint(1, den3 - 1)
        whole1 = random.randint(1, 3)
        whole2 = random.randint(1, 2)
        op = random.choice(['+', '-'])
        if op == '+':
            return f"Berechne und gib das Ergebnis als gemischte Zahl an: {whole1} {num1}/{den1} + {whole2} {num2}/{den2} - {num3}/{den3}"
        else:
            return f"Berechne und gib das Ergebnis als gekürzten Bruch oder gemischte Zahl an: {whole1} {num1}/{den1} - {num2}/{den2} + {whole2} {num3}/{den3}"
    elif sub_type == 'dezimal_rechnung':
        if random.choice([True, False]):
            val1 = round(random.uniform(1.1, 15.9), random.choice([1, 2]))
            val2 = round(random.uniform(0.1, 2.9), random.choice([1, 2]))
            return f"Berechne schriftlich: {val1} x {val2}"
        else:
            quotient = round(random.uniform(1.2, 8.5), 1)
            val2 = round(random.uniform(0.2, 1.5), 1)
            val1 = round(quotient * val2, 2)
            return f"Berechne schriftlich: {val1} : {val2}"
    else: # umwandlung
        if random.choice([True, False]):
            den = random.choice([8, 16, 20, 25, 40, 50, 125, 250])
            num = random.randint(1, den - 1)
            while math.gcd(num, den) != 1:
                num = random.randint(1, den - 1)
            return f"Wandle den gemeinen Bruch {num}/{den} in eine Dezimalzahl um."
        else:
            dec = round(random.uniform(0.04, 0.96), random.choice([2, 3]))
            dec_str = f"{dec:.3f}" if dec * 1000 % 10 != 0 else f"{dec:.2f}"
            return f"Wandle den Dezimalbruch {dec_str} in einen vollständig gekürzten gemeinen Bruch um."

GENERATORS.append(generate_fractions_decimals_tough)

# 5. Units & Conversions
def generate_units_conversion_tough():
    unit_choice = random.choice(['Länge', 'Zeit', 'Masse', 'Fläche', 'Volumen'])
    if unit_choice == 'Länge':
        km = round(random.uniform(0.5, 5.0), 2)
        m = random.randint(100, 800)
        dm = random.randint(1000, 10000)
        target = random.choice(['Metern (m)', 'Dezimetern (dm)'])
        return f"Berechne und gib das Ergebnis in {target} an: {km} km - {m} m + {dm} dm."
    elif unit_choice == 'Masse':
        t = round(random.uniform(1.0, 4.0), 3)
        kg = random.randint(100, 900)
        g = random.randint(5000, 25000)
        target = random.choice(['Kilogramm (kg)', 'Gramm (g)'])
        return f"Berechne und gib das Ergebnis in {target} an: {t} t - {kg} kg + {g} g."
    elif unit_choice == 'Zeit':
        h1 = random.randint(2, 6)
        m1 = random.randint(10, 50)
        s1 = random.randint(60, 300)
        h2 = round(random.choice([0.5, 1.5, 2.5]), 1)
        return f"Berechne und gib das Ergebnis in Minuten (min) an: {h1} h {m1} min + {s1} s - {h2} h."
    elif unit_choice == 'Fläche':
        ha = round(random.uniform(0.1, 2.0), 2)
        a = random.randint(5, 80)
        m2 = random.randint(100, 900)
        target = random.choice(['Quadratmetern (m²)', 'Ar (a)'])
        return f"Berechne und gib das Ergebnis in {target} an: {ha} ha + {a} a - {m2} m²."
    else: # Volumen
        m3 = round(random.uniform(0.5, 3.0), 2)
        dm3 = random.randint(100, 800)
        l = random.randint(50, 400)
        target = random.choice(['Litern (l)', 'Dezimetern³ (dm³)'])
        return f"Berechne und gib das Ergebnis in {target} an: {m3} m³ - {dm3} dm³ + {l} Liter."

GENERATORS.append(generate_units_conversion_tough)

# 6. Geometry
def generate_geometry_perimeter_area_tough():
    sub_choice = random.choice(['flaeche_rueck', 'compound_shape', 'koordinaten', 'quader'])
    if sub_choice == 'flaeche_rueck':
        side1 = random.randint(8, 25)
        side2 = random.randint(12, 40)
        area = side1 * side2
        return f"Ein Rechteck hat einen Flächeninhalt von {area} cm². Seine Breite beträgt {side1} cm. Berechne die Länge dieses Rechtecks und seinen Umfang."
    elif sub_choice == 'compound_shape':
        l1 = random.randint(8, 15)
        w1 = random.randint(6, 10)
        l2 = random.randint(4, 7)
        w2 = random.randint(3, 5)
        return f"Eine L-förmige Figur setzt sich aus zwei rechteckigen Teilflächen zusammen. Teilfläche 1 ist {l1} cm lang und {w1} cm breit. Teilfläche 2 ist {l2} cm lang und {w2} cm breit. Berechne den Gesamtflächeninhalt und den Umfang der zusammengesetzten Figur, wenn sie an den kürzeren Seiten aneinandergrenzen."
    elif sub_choice == 'koordinaten':
        x1, y1 = random.randint(1, 5), random.randint(1, 5)
        w = random.randint(4, 8)
        h = random.randint(3, 6)
        x2, y2 = x1 + w, y1
        x3, y3 = x1 + w, y1 + h
        mirror_axis = random.choice(['y-Achse', 'x-Achse'])
        return f"Im Koordinatensystem bilden die Punkte A({x1}|{y1}), B({x2}|{y2}) und C({x3}|{y3}) drei Eckpunkte eines Rechtecks. Bestimme zuerst die Koordinaten des vierten Punktes D. Spiegele anschließend den Punkt D an der {mirror_axis} und gib die Koordinaten des Bildpunktes D' an."
    else: # quader
        l = random.randint(40, 100)
        w = random.randint(20, 50)
        h = random.randint(30, 60)
        fill_percent = random.choice([50, 60, 75, 80, 90])
        return f"Ein Aquarium ist {l} cm lang, {w} cm breit und {h} cm hoch. Es wird zu {fill_percent}% mit Wasser gefüllt. Berechne: a) Das maximale Volumen des Aquariums in Litern. b) Die Wassermenge, die sich aktuell im Aquarium befindet (in Litern)."

GENERATORS.append(generate_geometry_perimeter_area_tough)

# 7. Percentages (Class 6 introduction)
def generate_percentages_tough():
    choice = random.choice(['discount', 'increase', 'share'])
    if choice == 'discount':
        orig_price = random.choice([80, 120, 150, 200, 250, 300, 450, 600])
        discount = random.choice([5, 10, 15, 20, 25, 30, 40, 50])
        return f"Ein Tablet-PC kostet regulär {orig_price} €. Wegen einer Sonderaktion wird der Preis um {discount}% gesenkt. Wie viel Geld spart der Käufer und wie hoch ist der neue Verkaufspreis?"
    elif choice == 'increase':
        orig_price = random.choice([50, 80, 100, 120, 160, 200, 240])
        increase = random.choice([5, 10, 15, 20])
        return f"Die Jahresgebühr für den Sportverein betrug bisher {orig_price} €. Ab dem nächsten Monat erhöht sich der Beitrag um {increase}%. Wie hoch ist die neue Jahresgebühr?"
    else:
        total_people = random.choice([200, 250, 400, 500, 600, 800, 1000])
        pct = random.choice([12, 15, 24, 28, 35, 45])
        return f"An einer Schule lernen {total_people} Schülerinnen und Schüler. Davon nehmen {pct}% an einer freiwilligen Mathematik-Olympiade teil. Berechne die genaue Anzahl der Teilnehmenden."

GENERATORS.append(generate_percentages_tough)

# 8. Sachaufgaben & Dreisatz
def generate_word_problem_tough():
    sub_choice = random.choice(['dreisatz_prop', 'dreisatz_antiprop', 'speed_problem', 'cost_compare'])
    if sub_choice == 'dreisatz_prop':
        factor = random.randint(4, 12)
        u1 = random.randint(3, 9)
        price1 = u1 * factor
        u2 = u1 + random.randint(3, 10)
        return f"Für {u1} Schulbücher müssen insgesamt {price1} € bezahlt werden. Berechne mithilfe des Dreisatzes, wie viel {u2} Schulbücher derselben Art kosten."
    elif sub_choice == 'dreisatz_antiprop':
        p1 = random.randint(3, 8)
        h1 = random.randint(6, 20)
        total_work = p1 * h1
        divisors = [i for i in range(2, 13) if total_work % i == 0 and i != p1]
        p2 = random.choice(divisors) if divisors else p1 + 2
        if not divisors:
            total_work = p2 * h1
            p1 = total_work // h1
        h2 = total_work // p2
        return f"Um ein Schwimmbecken zu entleeren, benötigen {p1} baugleiche Pumpen genau {h1} Stunden. Wie viele Stunden benötigen {p2} dieser Pumpen, um dasselbe Becken zu leeren?"
    elif sub_choice == 'speed_problem':
        speed = random.choice([60, 80, 90, 100, 120])
        hours = random.randint(2, 5)
        mins = random.choice([0, 15, 30, 45])
        time_str = f"{hours} Stunden" if mins == 0 else f"{hours} Stunden und {mins} Minuten"
        return f"Ein ICE-Zug fährt mit einer durchschnittlichen Geschwindigkeit von {speed} km/h. Welche Strecke (in Kilometern) legt der Zug in {time_str} zurück?"
    else:
        p1_cents = random.choice([150, 180, 200, 250, 300])
        p1_str = f"{p1_cents / 100.0:.2f}".replace('.', ',')
        p2_cents = p1_cents * 4 - random.choice([50, 100, 150])
        p2_str = f"{p2_cents / 100.0:.2f}".replace('.', ',')
        return f"In einem Supermarkt wird Erdbeermarmelade in zwei verschiedenen Gläsern angeboten: Glas A enthält 500 g und kostet {p1_str} €; Glas B enthält 2 kg und kostet {p2_str} €. Welches Angebot ist für den Kunden auf ein Kilogramm gerechnet günstiger und wie viel spart man pro kg?"

GENERATORS.append(generate_word_problem_tough)

# --- Document and Helper Functions ---

def create_single_problem_set(num_problems=50):
    """Generiert eine Liste von 50 Aufgaben, die völlig zufällig aus den Generatoren gezogen werden."""
    problems = []
    for i in range(1, num_problems + 1):
        generator = random.choice(GENERATORS)
        problem = generator()
        problems.append(f"{i}. {problem}")
    return problems

def create_word_document(problems, set_number):
    """Erstellt ein Word-Dokument (im Speicher) und gibt es als Bytes zurück."""
    document = Document()
    document.add_heading(f'Schwere Mathematikaufgaben Gymnasium Kl. 5/6 (Sachsen-Anhalt) - Set {set_number}', 0)
    document.add_paragraph("Dies sind Übungen mit erhöhtem Schwierigkeitsgrad.")
    for problem in problems:
        document.add_paragraph(problem)
    bio = BytesIO()
    document.save(bio)
    bio.seek(0)
    return bio.getvalue()

# --- Streamlit Login and Main Program ---

def login_form():
    """Zeigt das Login-Formular an und prüft die Anmeldedaten aus st.secrets."""
    try:
        STATIC_USER = st.secrets["auth"]["username"]
        STATIC_PASS = st.secrets["auth"]["password"]
    except KeyError:
        st.error("❌ Konfigurationsfehler: Bitte stellen Sie sicher, dass die Datei '.streamlit/secrets.toml' mit der Sektion [auth] existiert.")
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
                st.rerun()
            else:
                st.error("Ungültiger Benutzername oder Passwort.")

def main_app():
    """Die Hauptanwendung, die nur nach erfolgreichem Login angezeigt wird."""
    st.title("🎓 Matheaufgaben-Generator")
    st.markdown("<h3 class='gradient-text'>Gymnasium Klasse 5 & 6 (Sachsen-Anhalt)</h3>", unsafe_allow_html=True)
    st.markdown("Generiert bis zu **20 völlig zufällige und anspruchsvolle** Übungsblätter.")
    st.markdown("---")

    # Wrap inputs in a premium styled container
    st.markdown("""
        <div class="premium-card">
            <h4>⚙️ Einstellungen für die Generierung</h4>
            Stellen Sie ein, wie viele Aufgabensätze Sie generieren möchten. Jeder Satz enthält 50 völlig zufällige, schwere Aufgaben.
        </div>
    """, unsafe_allow_html=True)

    # User Inputs
    num_sets = st.number_input(
        "Anzahl der benötigten Aufgabensätze:", 
        min_value=1, 
        max_value=20, 
        value=5,
        help="Maximal 20 Sets empfohlen, um die Einzigartigkeit zu garantieren."
    )
    
    st.markdown("---")

    if st.button(f"Starte Generierung von {num_sets} Sätzen und erstelle ZIP-Datei", type="primary"):
        zip_buffer = BytesIO()
        
        with st.status("🛠️ Starte die Generierung...", expanded=True) as status:
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                for i in range(1, int(num_sets) + 1):
                    status.write(f"➡️ **Set {i}/{num_sets}:** Erstelle 50 schwere Aufgaben...")
                    
                    problems = create_single_problem_set(num_problems=50)
                    docx_bytes = create_word_document(problems, i)
                    filename = f"Matheaufgaben_Set_SCHWER_{i}.docx"
                    
                    zf.writestr(filename, docx_bytes)
                    status.write(f"✅ **Set {i}/{num_sets}:** Erfolgreich zur ZIP-Datei hinzugefügt.")
                
                status.update(label="📦 Komprimiere und finalisiere das ZIP-Archiv...", state="running")
                time.sleep(1) # Simulate compression time
            
            zip_buffer.seek(0)
            status.update(label=f"🎉 {num_sets} Aufgabensätze sind bereit zum Download!", state="complete", expanded=False)
        
        st.markdown("---")
        
        st.download_button(
            label="Alle Sätze als ZIP-Datei herunterladen",
            data=zip_buffer,
            file_name="Matheaufgaben_Gymnasium_5_6_SCHWER.zip",
            mime="application/zip",
            key='download_zip_button'
        )

# Hauptfunktion, die den Login-Zustand verwaltet
if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        main_app()
    else:
        login_form()
        st.title("🎓 Matheaufgaben Generator (Klassen 5/6)")
        st.markdown("""
            Willkommen beim Aufgaben-Generator für das **Gymnasium in Sachsen-Anhalt** (Schuljahrgänge 5 und 6).
            
            Bitte loggen Sie sich in der linken Seitenleiste ein, um Aufgabensätze zu generieren.
        """)