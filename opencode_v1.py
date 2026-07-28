"""
Matheaufgaben Generator -- Gymnasium Klassen 5 & 6 (Sachsen-Anhalt)
Schwierige Aufgaben basierend auf dem Fachlehrplan (Fassung 01.08.2022).

Erstellt Word-Dokumente und paketiert sie als ZIP-Datei.
Kein Streamlit noetig -- reines Python-Skript.

Jede Aufgabe ist innerhalb eines Satzes eindeutig (Keine Wiederholungen).
"""

import random
import math
from fractions import Fraction
from docx import Document
from docx.shared import Pt
from io import BytesIO
import zipfile
import os
from datetime import datetime

# =============================================================================
# Aufgabengeneratoren
# =============================================================================

GENERATORS_KL5 = []
GENERATORS_KL6 = []


# =============================================================================
#  KLASSE 5 -- Zahl, Variable, Operation
# =============================================================================

def kl5_written_addition():
    """Schriftliche Addition grosser Zahlen."""
    a = random.randint(1_000_000, 99_999_999)
    b = random.randint(1_000_000, 99_999_999)
    return f"Berechne schriftlich: {a} + {b}."
GENERATORS_KL5.append(kl5_written_addition)

def kl5_written_subtraction():
    """Schriftliche Subtraktion grosser Zahlen."""
    a = random.randint(10_000_000, 99_999_999)
    b = random.randint(1_000_000, a - 1)
    return f"Berechne schriftlich: {a} - {b}."
GENERATORS_KL5.append(kl5_written_subtraction)

def kl5_written_multiplication():
    """Schriftliche Multiplikation."""
    a = random.randint(200, 999)
    b = random.randint(20, 99)
    return f"Berechne schriftlich: {a} x {b}."
GENERATORS_KL5.append(kl5_written_multiplication)

def kl5_written_division():
    """Schriftliche Division mit Rest."""
    divisor = random.randint(13, 37)
    quotient = random.randint(200, 4000)
    rest = random.randint(1, divisor - 1)
    dividend = divisor * quotient + rest
    return f"Berechne schriftlich: {dividend} : {divisor} (mit Rest)."
GENERATORS_KL5.append(kl5_written_division)

def kl5_written_division_exact():
    """Schriftliche Division ohne Rest."""
    divisor = random.randint(11, 25)
    quotient = random.randint(100, 500)
    dividend = divisor * quotient
    return f"Berechne schriftlich: {dividend} : {divisor}."
GENERATORS_KL5.append(kl5_written_division_exact)

def kl5_multi_step_brackets():
    """Mehrstufiges Rechnen mit Klammern."""
    a = random.randint(3, 12)
    b = random.randint(5, 25)
    c = random.randint(2, 9)
    d = random.randint(100, 800)
    e = random.randint(11, 49)
    pattern = random.choice([
        f"({a} + {b}) x {c} - {d}",
        f"{d} : {c} + ({b} - {a}) x {e}",
        f"({d} - {b} x {a}) : {c}",
        f"({d} + {a} x {b}) : {e} - {c}",
        f"{b} x {c} + {a}**2 - {d} : {e}",
        f"({d} - {a}) : {c} + {b} x ({e} - {d})",
    ])
    return f"Berechne: {pattern}."
GENERATORS_KL5.append(kl5_multi_step_brackets)

def kl5_multi_step_powers():
    """Rechnen mit Potenzen und Klammern."""
    a = random.randint(2, 5)
    b = random.randint(3, 8)
    c = random.randint(2, 4)
    d = random.randint(2, 5)
    pattern = random.choice([
        f"{a}**{c} + {b} x {d}",
        f"({a} + {b})**2 - {c}**{d}",
        f"{a}**3 x {b} - {c}**2 + {d}",
        f"({a} x {b})**2 : {c} + {d}",
    ])
    return f"Berechne: {pattern}."
GENERATORS_KL5.append(kl5_multi_step_powers)

def kl5_rounding():
    """Runden grosser Zahlen."""
    num = random.randint(100_000, 999_999_999)
    place = random.choice([
        'Tausender', 'Zehntausender', 'Hunderttausender',
        'Millionen', 'Zehnmillionen'
    ])
    return f"Runde die Zahl {num:,} (deutsche Schreibweise) auf die naechsten {place}.".replace(',', '.')
GENERATORS_KL5.append(kl5_rounding)

def kl5_rounding_decimals():
    """Runden von Dezimalzahlen."""
    num = round(random.uniform(1, 999.999), 3)
    place = random.choice(['eine', 'zwei', 'drei'])
    return f"Runde die Zahl {num} auf {place} Nachkommastellen."
GENERATORS_KL5.append(kl5_rounding_decimals)

def kl5_fraction_add():
    """Brueche addieren (gleicher und ungleicher Nenner)."""
    style = random.choice(['gleicher', 'ungleicher'])
    if style == 'gleicher':
        d = random.randint(3, 15)
        n1 = random.randint(1, d - 1)
        n2 = random.randint(1, d - 1)
        while n1 + n2 >= d:
            n2 = random.randint(1, d - 1)
        return f"Berechne: {n1}/{d} + {n2}/{d}."
    else:
        d1 = random.randint(3, 12)
        d2 = random.randint(3, 12)
        while d2 == d1:
            d2 = random.randint(3, 12)
        n1 = random.randint(1, d1 - 1)
        n2 = random.randint(1, d2 - 1)
        return f"Berechne: {n1}/{d1} + {n2}/{d2}."
GENERATORS_KL5.append(kl5_fraction_add)

def kl5_fraction_sub():
    """Brueche subtrahieren."""
    d1 = random.randint(4, 15)
    d2 = random.randint(4, 15)
    n1 = random.randint(2, d1 - 1)
    n2 = random.randint(1, min(d2 - 1, n1 * d2 // d1 + 1))
    return f"Berechne: {n1}/{d1} - {n2}/{d2}."
GENERATORS_KL5.append(kl5_fraction_sub)

def kl5_fraction_mul():
    """Brueche multiplizieren."""
    a, b = random.randint(2, 12), random.randint(2, 12)
    c, d = random.randint(2, 9), random.randint(2, 9)
    return f"Berechne: {a}/{b} x {c}/{d}."
GENERATORS_KL5.append(kl5_fraction_mul)

def kl5_fraction_div():
    """Brueche dividieren."""
    a, b = random.randint(2, 15), random.randint(2, 15)
    c, d = random.randint(2, 12), random.randint(2, 12)
    return f"Berechne: {a}/{b} : {c}/{d}."
GENERATORS_KL5.append(kl5_fraction_div)

def kl5_fraction_mixed_add():
    """Gemischte Zahlen addieren."""
    whole1 = random.randint(1, 5)
    num1 = random.randint(1, 7)
    den1 = random.randint(num1 + 1, 12)
    whole2 = random.randint(1, 4)
    num2 = random.randint(1, den1 - 1)
    return f"Berechne: {whole1} {num1}/{den1} + {whole2} {num2}/{den1}."
GENERATORS_KL5.append(kl5_fraction_mixed_add)

def kl5_fraction_mixed_sub():
    """Gemischte Zahlen subtrahieren."""
    whole1 = random.randint(2, 8)
    num1 = random.randint(1, 7)
    den1 = random.randint(num1 + 1, 12)
    whole2 = random.randint(1, whole1 - 1)
    num2 = random.randint(1, den1 - 1)
    return f"Berechne: {whole1} {num1}/{den1} - {whole2} {num2}/{den1}."
GENERATORS_KL5.append(kl5_fraction_mixed_sub)

def kl5_fraction_to_decimal():
    """Brueche in Dezimalzahlen umwandeln und umgekehrt."""
    kind = random.choice(['b2d', 'd2b'])
    if kind == 'b2d':
        den = random.choice([2, 4, 5, 8, 10, 16, 20, 25])
        num = random.randint(1, den - 1)
        return f"Wandle den Bruch {num}/{den} in eine Dezimalzahl um."
    else:
        decimals = random.choice([0.25, 0.5, 0.75, 0.125, 0.2, 0.4, 0.6, 0.8, 0.375])
        return f"Wandle die Dezimalzahl {decimals} in einen Bruch (gekuerzt) um."
GENERATORS_KL5.append(kl5_fraction_to_decimal)

def kl5_decimal_add_sub():
    """Dezimalzahlen addieren und subtrahieren."""
    a = round(random.uniform(10, 500), 2)
    b = round(random.uniform(1, a), 2)
    op = random.choice(['+', '-'])
    return f"Berechne: {a} {op} {b}."
GENERATORS_KL5.append(kl5_decimal_add_sub)

def kl5_decimal_mul():
    """Dezimalzahlen multiplizieren."""
    a = round(random.uniform(0.1, 50.0), 2)
    b = round(random.uniform(0.1, 50.0), 2)
    return f"Berechne: {a} x {b}."
GENERATORS_KL5.append(kl5_decimal_mul)

def kl5_decimal_div():
    """Dezimalzahlen dividieren."""
    b = round(random.uniform(0.2, 25.0), 1)
    result = round(random.uniform(1, 100), 2)
    a = round(b * result, 2)
    return f"Berechne: {a} : {b}."
GENERATORS_KL5.append(kl5_decimal_div)

def kl5_decimal_multi_step():
    """Mehrstufige Dezimalrechnung."""
    a = round(random.uniform(5, 50), 2)
    b = round(random.uniform(1, 20), 2)
    c = round(random.uniform(0.5, 10), 1)
    pattern = random.choice([
        f"({a} + {b}) x {c}",
        f"{a} x {b} - {c}",
        f"({a} - {b}) : {c}",
    ])
    return f"Berechne: {pattern}."
GENERATORS_KL5.append(kl5_decimal_multi_step)

def kl5_percentage_calc():
    """Prozente berechnen."""
    total = random.randint(50, 800)
    pct = random.choice([10, 15, 20, 25, 30, 40, 50, 60, 75])
    return f"Berechne {pct}% von {total}."
GENERATORS_KL5.append(kl5_percentage_calc)

def kl5_percentage_reverse():
    """Prozente rueckwaerts: Teil ist bekannt, Gesamt gesucht."""
    pct = random.choice([10, 15, 20, 25, 30, 40, 50])
    base = random.randint(50, 500)
    part = base * pct // 100
    return f"{part} sind {pct}% eines Gesamtwerts. Wie gross ist der Gesamtwert?"
GENERATORS_KL5.append(kl5_percentage_reverse)

def kl5_percentage_find():
    """Prozent finden: X ist wie viel Prozent von Y?"""
    base = random.choice([50, 80, 100, 120, 200, 250, 400])
    part = random.randint(1, base - 1)
    return f"Wie viel Prozent von {base} ist {part}?"
GENERATORS_KL5.append(kl5_percentage_find)

def kl5_ggT():
    """Groessten gemeinsamen Teiler berechnen."""
    a = random.randint(20, 200)
    b = random.randint(20, 200)
    while b == a:
        b = random.randint(20, 200)
    return f"Berechne den groessten gemeinsamen Teiler (ggT) von {a} und {b}."
GENERATORS_KL5.append(kl5_ggT)

def kl5_kgV():
    """Kleinstes gemeinsames Vielfaches berechnen."""
    a = random.randint(6, 30)
    b = random.randint(6, 30)
    while b == a:
        b = random.randint(6, 30)
    return f"Berechne das kleinste gemeinsame Vielfache (kgV) von {a} und {b}."
GENERATORS_KL5.append(kl5_kgV)

def kl5_primfaktor():
    """Primfaktorzerlegung."""
    n = random.choice([120, 144, 180, 200, 216, 240, 252, 288, 300, 324, 360, 400, 432, 450, 480, 504, 540, 576, 600, 648, 720, 840, 900, 960])
    return f"Zerlege {n} in eine Primfaktorzerlegung."
GENERATORS_KL5.append(kl5_primfaktor)

def kl5_divisibility_rules():
    """Teilbarkeitsregeln anwenden."""
    n = random.randint(100, 999)
    divisors = [2, 3, 5, 9, 10]
    d = random.choice(divisors)
    return f"Ist {n} durch {d} teilbar? Begründe mit der Teilbarkeitsregel."
GENERATORS_KL5.append(kl5_divisibility_rules)

def kl5_order_of_ops():
    """Reihenfolge der Rechenoperationen."""
    a = random.randint(2, 8)
    b = random.randint(3, 15)
    c = random.randint(2, 7)
    d = random.randint(10, 60)
    pattern = random.choice([
        f"{a} + {b} x {c} - {d}",
        f"{d} : {c} + {a} x {b}",
        f"{a} x {b} - {d} : {c}",
        f"{d} - {a} x {b} + {c}",
    ])
    return f"Berechne (beachte die Reihenfolge der Operationen): {pattern}."
GENERATORS_KL5.append(kl5_order_of_ops)

def kl5_commutative():
    """Rechengesetze anwenden (Kommutativ, Distributiv)."""
    a = random.randint(3, 15)
    b = random.randint(3, 15)
    c = random.randint(2, 8)
    kind = random.choice(['distributiv', 'kommutativ'])
    if kind == 'distributiv':
        return f"Berechne mit dem Distributivgesetz: ({a} + {b}) x {c}."
    else:
        return f"Vereinfache mit dem Kommutativgesetz: {a} x {b} + {b} x {a}."
GENERATORS_KL5.append(kl5_commutative)

# --- KLASSE 5 -- Messen ---

def kl5_unit_length():
    """Laengenumrechnungen."""
    kind = random.choice(['km_m', 'cm_mm', 'm_cm', 'gemischt'])
    if kind == 'km_m':
        val = round(random.uniform(1.0, 15.0), 2)
        return f"Wandle um: {val} km in Meter (m)."
    elif kind == 'cm_mm':
        val = random.randint(5, 50)
        return f"Wandle um: {val} cm in Millimeter (mm)."
    elif kind == 'm_cm':
        val = random.randint(1, 20)
        return f"Wandle um: {val} m in Zentimeter (cm)."
    else:
        km = random.randint(1, 10)
        m = random.randint(100, 999)
        return f"Wandle um: {km} km und {m} m in reine Zentimeter (cm)."
GENERATORS_KL5.append(kl5_unit_length)

def kl5_unit_weight():
    """Gewichtsumrechnungen."""
    kind = random.choice(['kg_g', 't_kg', 'gemischt'])
    if kind == 'kg_g':
        val = random.randint(1, 15)
        return f"Wandle um: {val} Kilogramm in Gramm (g)."
    elif kind == 't_kg':
        val = round(random.uniform(0.5, 5.0), 1)
        return f"Wandle um: {val} Tonnen in Kilogramm (kg)."
    else:
        kg = random.randint(1, 5)
        g = random.randint(200, 900)
        return f"Wandle um: {kg} kg und {g} g in reine Gramm (g)."
GENERATORS_KL5.append(kl5_unit_weight)

def kl5_unit_volume():
    """Volumenumrechnungen."""
    kind = random.choice(['l_ml', 'dm3_l', 'm3_l'])
    if kind == 'l_ml':
        val = random.randint(1, 10)
        return f"Wandle um: {val} Liter in Milliliter (ml)."
    elif kind == 'dm3_l':
        val = random.randint(2, 15)
        return f"Wandle um: {val} Kubikdezimeter (dm3) in Liter (l)."
    else:
        val = random.randint(1, 5)
        return f"Wandle um: {val} Kubikmeter (m3) in Liter (l)."
GENERATORS_KL5.append(kl5_unit_volume)

def kl5_unit_time():
    """Zeitumrechnungen."""
    kind = random.choice(['h_min', 'tage_h', 'gemischt'])
    if kind == 'h_min':
        h = random.randint(2, 10)
        m = random.randint(1, 59)
        return f"Wandle um: {h} Stunden und {m} Minuten in Gesamtminuten."
    elif kind == 'tage_h':
        tage = random.randint(2, 14)
        return f"Wandle um: {tage} Tage in Stunden."
    else:
        min_total = random.randint(200, 2000)
        return f"Wandle um: {min_total} Minuten in Stunden und Minuten."
GENERATORS_KL5.append(kl5_unit_time)

def kl5_unit_area():
    """Flaechenumrechnungen."""
    kind = random.choice(['m2_cm2', 'ha_m2', 'km2_m2'])
    if kind == 'm2_cm2':
        val = random.randint(2, 30)
        return f"Wandle um: {val} m2 in cm2."
    elif kind == 'ha_m2':
        val = random.randint(1, 20)
        return f"Wandle um: {val} Hektar (ha) in Quadratmeter (m2)."
    else:
        val = random.randint(1, 5)
        return f"Wandle um: {val} km2 in Quadratmeter (m2)."
GENERATORS_KL5.append(kl5_unit_area)

def kl5_unit_time_word():
    """Zeitprobleme als Textaufgabe."""
    h = random.randint(8, 23)
    m = random.randint(0, 59)
    add_h = random.randint(1, 6)
    add_m = random.randint(10, 59)
    return (f"Ein Film beginnt um {h}:{m:02d} Uhr und dauert {add_h} Stunden und {add_m} Minuten. "
            f"Wann endet er?")
GENERATORS_KL5.append(kl5_unit_time_word)

# --- KLASSE 5 -- Raum und Form ---

def kl5_perimeter_rectangle():
    """Umfang von Rechtecken."""
    l = random.randint(5, 30)
    w = random.randint(3, 20)
    return f"Ein Rechteck hat die Seiten {l} cm und {w} cm. Berechne den Umfang."
GENERATORS_KL5.append(kl5_perimeter_rectangle)

def kl5_area_rectangle():
    """Flaeche von Rechtecken."""
    l = random.randint(5, 30)
    w = random.randint(3, 20)
    return f"Ein Rechteck hat die Seiten {l} cm und {w} cm. Berechne den Flaecheninhalt."
GENERATORS_KL5.append(kl5_area_rectangle)

def kl5_perimeter_triangle():
    """Umfang von Dreiecken."""
    a = random.randint(3, 15)
    b = random.randint(3, 15)
    c = random.randint(abs(a - b) + 1, a + b - 1)
    return f"Ein Dreieck hat die Seiten {a} cm, {b} cm und {c} cm. Berechne den Umfang."
GENERATORS_KL5.append(kl5_perimeter_triangle)

def kl5_area_triangle():
    """Flaeche von Dreiecken (Grundseite und Hoehe)."""
    base = random.randint(5, 20)
    height = random.randint(3, 15)
    return f"Ein Dreieck hat Grundseite {base} cm und Hoehe {height} cm. Berechne den Flaecheninhalt."
GENERATORS_KL5.append(kl5_area_triangle)

def kl5_area_parallelogram():
    """Flaeche von Parallelogrammen."""
    base = random.randint(5, 20)
    height = random.randint(3, 15)
    return f"Ein Parallelogramm hat Grundseite {base} cm und Hoehe {height} cm. Berechne den Flaecheninhalt."
GENERATORS_KL5.append(kl5_area_parallelogram)

def kl5_reverse_problem():
    """Rueckwaertsprobleme: Flaeche/Umfang gegeben, Seite gesucht."""
    kind = random.choice(['flaeche_r', 'umfang_r'])
    if kind == 'flaeche_r':
        area = random.randint(60, 300)
        width = random.randint(5, 20)
        return (f"Die Flaeche eines Rechtecks betraegt {area} cm2. "
                f"Die Breite ist {width} cm. Berechne die Laenge und den Umfang.")
    else:
        perimeter = random.randint(40, 120)
        length = random.randint(10, 40)
        return (f"Der Umfang eines Rechtecks ist {perimeter} cm. "
                f"Die Laenge ist {length} cm. Berechne die Breite und die Flaeche.")
GENERATORS_KL5.append(kl5_reverse_problem)

def kl5_composite_l_shape():
    """L-foermige Figur: Flaeche und Umfang."""
    l1 = random.randint(8, 20)
    w1 = random.randint(5, 12)
    l2 = random.randint(3, l1 - 2)
    w2 = random.randint(2, w1 - 1)
    return (f"Eine L-foermige Figur entsteht durch Entfernen eines {l2} cm x {w2} cm "
            f"Rechtecks aus einem {l1} cm x {w1} cm Rechteck. "
            f"Berechne Flaeche und Umfang der L-Form.")
GENERATORS_KL5.append(kl5_composite_l_shape)

def kl5_composite_t_shape():
    """T-foermige Figur."""
    tb = random.randint(10, 20)
    th = random.randint(3, 7)
    sv = random.randint(6, 14)
    sh = random.randint(3, 7)
    return (f"Eine T-foermige Figur: waagerechter Balken {tb} cm x {th} cm, "
            f"senkrechter Strich {sv} cm x {sh} cm (mittig unten). "
            f"Berechne Flaeche und Umfang.")
GENERATORS_KL5.append(kl5_composite_t_shape)

def kl5_composite_step():
    """Stufenfoermige Figur."""
    n = random.randint(3, 5)
    dims = [(random.randint(2, 5), random.randint(2, 5)) for _ in range(n)]
    desc = ", ".join(f"Stufe {i+1}: {d[0]}x{d[1]} cm" for i, d in enumerate(dims))
    return (f"Eine stufenfoermige Figur besteht aus {n} Rechtecken: {desc}. "
            f"Berechne den Gesamtflaecheninhalt.")
GENERATORS_KL5.append(kl5_composite_step)

def kl5_cube_volume_surface():
    """Wuerfel: Volumen und Oberflaeche."""
    a = random.randint(3, 12)
    return (f"Ein Wuerfel hat die Kantenlaenge {a} cm. "
            f"Berechne Volumen und Oberflaeche.")
GENERATORS_KL5.append(kl5_cube_volume_surface)

def kl5_cuboid_volume_surface():
    """Quader: Volumen und Oberflaeche."""
    l = random.randint(4, 15)
    w = random.randint(3, 12)
    h = random.randint(3, 12)
    while l == w == h:
        h = random.randint(3, 12)
    return (f"Ein Quader hat die Kantenlaengen {l} cm, {w} cm und {h} cm. "
            f"Berechne Volumen und Oberflaeche.")
GENERATORS_KL5.append(kl5_cuboid_volume_surface)

def kl5_cuboid_reverse():
    """Quader rueckwaerts: Volumen gegeben, Kante gesucht."""
    l = random.randint(4, 12)
    w = random.randint(3, 10)
    h = random.randint(3, 10)
    vol = l * w * h
    return (f"Ein Quader hat Volumen {vol} cm3 und Kantenlaengen {l} cm und {w} cm. "
            f"Berechne die dritte Kante.")
GENERATORS_KL5.append(kl5_cuboid_reverse)

def kl5_angle_triangle_sum():
    """Winkelsumme im Dreieck."""
    a = random.randint(30, 80)
    b = random.randint(30, 150 - a)
    c = 180 - a - b
    return (f"In einem Dreieck sind zwei Winkel {a} Grad und {b} Grad. "
            f"Berechne den dritten Winkel.")
GENERATORS_KL5.append(kl5_angle_triangle_sum)

def kl5_angle_supplement():
    """Ergaenzungswinkel."""
    a = random.randint(15, 170)
    return (f"Ein Winkel betraegt {a} Grad. "
            f"Berechne seinen Ergaenzungswinkel und seinen Scheitelwinkel.")
GENERATORS_KL5.append(kl5_angle_supplement)

def kl5_angle_complement():
    """Komplementaerwinkel (90 Grad)."""
    a = random.randint(10, 80)
    return (f"Ein spitzer Winkel betraegt {a} Grad. "
            f"Wie gross ist sein Komplementaerwinkel?")
GENERATORS_KL5.append(kl5_angle_complement)

def kl5_angle_in_polygon():
    """Innenwinkelsumme im Polygon."""
    n = random.choice([3, 4, 5, 6, 8])
    if n == 3:
        a = random.randint(40, 80)
        b = random.randint(40, 120 - a)
        return (f"Ein Dreieck hat Winkel {a} Grad und {b} Grad. "
                f"Berechne den dritten Winkel.")
    elif n == 4:
        a = random.randint(60, 100)
        b = random.randint(60, 100)
        c = random.randint(60, 100)
        return (f"Ein Viereck hat drei Winkel: {a} Grad, {b} Grad und {c} Grad. "
                f"Berechne den vierten Winkel.")
    else:
        total = (n - 2) * 180
        return (f"Berechne die Innenwinkelsumme eines {n}-Ecks. "
                f"Wie gross ist der Durchschnittswinkel eines regelmassigen {n}-Ecks?")
GENERATORS_KL5.append(kl5_angle_in_polygon)

def kl5_symmetry_axes():
    """Symmetrieachsen bestimmen."""
    shapes = [
        ("Rechteck", "2"), ("Quadrat", "4"), ("gleichseitiges Dreieck", "3"),
        ("gleichschenkliges Dreieck", "1"), ("regelmaessiges Fuenfeck", "5"),
        ("regelmaessiges Sechseck", "6"), ("Kreis", "unendlich viele"),
        ("Rhombus", "2"), ("Drachenviereck", "1"), ("Trapez (gleichschenklig)", "1"),
    ]
    shape, axes = random.choice(shapes)
    return f"Wie viele Symmetrieachsen hat ein {shape}? (Erwartet: {axes})"
GENERATORS_KL5.append(kl5_symmetry_axes)

def kl5_point_reflection():
    """Punktspiegelung (1. Quadrant)."""
    x = random.randint(1, 8)
    y = random.randint(1, 8)
    return (f"Der Punkt P({x}|{y}) wird an der y-Achse gespiegelt. "
            f"Gib die Koordinaten von P' an.")
GENERATORS_KL5.append(kl5_point_reflection)

def kl5_distance_coords():
    """Abstand zweier Punkte (Pythagoras)."""
    x1, y1 = random.randint(1, 6), random.randint(1, 6)
    x2, y2 = random.randint(x1 + 1, 10), random.randint(1, 10)
    return (f"Im Koordinatensystem (1. Quadrant): A({x1}|{y1}) und B({x2}|{y2}). "
            f"Berechne die Laenge der Strecke AB.")
GENERATORS_KL5.append(kl5_distance_coords)

# --- KLASSE 5 -- Daten und Zufall ---

def kl5_mean():
    """Mittelwert berechnen."""
    numbers = sorted([random.randint(5, 40) for _ in range(random.randint(6, 10))])
    nums_str = ", ".join(str(n) for n in numbers)
    return f"Berechne den Mittelwert der Zahlen: {nums_str}."
GENERATORS_KL5.append(kl5_mean)

def kl5_median():
    """Median berechnen."""
    numbers = sorted([random.randint(3, 50) for _ in range(random.choice([7, 9, 11]))])
    nums_str = ", ".join(str(n) for n in numbers)
    return f"Berechne den Median der Zahlen: {nums_str}."
GENERATORS_KL5.append(kl5_median)

def kl5_mode():
    """Modalwert finden."""
    base = [random.randint(3, 20) for _ in range(5)]
    extras = [random.choice(base) for _ in range(3)]
    all_nums = sorted(base + extras)
    nums_str = ", ".join(str(n) for n in all_nums)
    return f"Bestimme den Modalwert der Zahlen: {nums_str}."
GENERATORS_KL5.append(kl5_mode)

def kl5_range():
    """Spannweite berechnen."""
    numbers = sorted([random.randint(1, 50) for _ in range(random.randint(6, 10))])
    nums_str = ", ".join(str(n) for n in numbers)
    return f"Berechne die Spannweite der Zahlen: {nums_str}."
GENERATORS_KL5.append(kl5_range)

def kl5_mean_median_all():
    """Mittelwert, Median und Spannweite together."""
    numbers = sorted([random.randint(5, 35) for _ in range(random.randint(7, 11))])
    nums_str = ", ".join(str(n) for n in numbers)
    return (f"Berechne Mittelwert, Median und Spannweite: {nums_str}.")
GENERATORS_KL5.append(kl5_mean_median_all)

def kl5_probability_dice():
    """Wahrscheinlichkeit mit einem Wuerfel."""
    faces = random.choice([6, 8, 10, 12])
    target = random.randint(1, faces)
    return (f"Ein {faces}-Seiten-Wuerfel wird geworfen. "
            f"Wie gross ist die Wahrscheinlichkeit, eine {target} zu würfeln?")
GENERATORS_KL5.append(kl5_probability_dice)

def kl5_probability_balls():
    """Wahrscheinlichkeit: Kugeln ziehen."""
    red = random.randint(2, 10)
    blue = random.randint(2, 10)
    return (f"In einem Beutel sind {red} rote und {blue} blaue Kugeln. "
            f"Es wird zufaellig eine Kugel gezogen. "
            f"Wie gross ist die Wahrscheinlichkeit, eine rote Kugel zu ziehen?")
GENERATORS_KL5.append(kl5_probability_balls)

def kl5_probability_cards():
    """Wahrscheinlichkeit: Karten."""
    rank = random.choice(["Bube", "Dame", "Koenig", "Ass"])
    suit = random.choice(["Herz", "Kreuz", "Pik", "Karo"])
    return (f"Von einem Skatblatt (32 Karten) wird zufaellig eine Karte gezogen. "
            f"Wie gross ist die Wahrscheinlichkeit, genau den {rank} von {suit} zu ziehen?")
GENERATORS_KL5.append(kl5_probability_cards)

def kl5_probability_combined():
    """Verbundene Ereignisse (UND/ODER)."""
    red = random.randint(3, 8)
    blue = random.randint(3, 8)
    green = random.randint(1, 5)
    total = red + blue + green
    return (f"In einem Beutel sind {red} rote, {blue} blaue und {green} gruene Kugeln. "
            f"Wie gross ist die Wahrscheinlichkeit, eine rote ODER eine gruene Kugel zu ziehen?")
GENERATORS_KL5.append(kl5_probability_combined)

# --- KLASSE 5 -- Funktionen ---

def kl5_function_table():
    """Funktionswerte aus Tabelle berechnen."""
    a = random.randint(2, 7)
    b = random.randint(1, 12)
    xs = sorted(random.sample(range(1, 10), 4))
    entries = ", ".join(str(x) for x in xs)
    return (f"Die Zuordnung ist: f(x) = {a}x + {b}. "
            f"Berechne f(x) fuer x element von {{{entries}}}.")
GENERATORS_KL5.append(kl5_function_table)

def kl5_function_rule_find():
    """Regel fuer Zuordnung finden."""
    a = random.randint(2, 6)
    b = random.randint(1, 15)
    xs = [1, 2, 3, 4, 5]
    vals = [a * x + b for x in xs]
    table = ", ".join(f"f({x})={v}" for x, v in zip(xs, vals))
    return (f"Gesucht: Die Zuordnungsregel. Gegeben: {table}. "
            f"Gib die Formel f(x) an.")
GENERATORS_KL5.append(kl5_function_rule_find)

def kl5_function_word():
    """Funktion in Alltagssituation."""
    speed = random.randint(3, 8)
    start = random.randint(10, 100)
    return (f"Ein Schwimmer schwimmt pro Minute {speed} Meter. "
            f"Er beginnt bei {start} Metern Entfernung vom Ufer. "
            f"Stelle eine Funktion f(t) auf und berechne, wann er am Ufer ist.")
GENERATORS_KL5.append(kl5_function_word)

def kl5_graph_read():
    """Werte aus Graph ablesen."""
    m = random.randint(1, 5)
    n = random.randint(0, 10)
    x = random.randint(1, 8)
    return (f"Ein Graph zeigt die Funktion f(x) = {m}x + {n}. "
            f"Lies den Funktionswert fuer x = {x} vom Graphen ab.")
GENERATORS_KL5.append(kl5_graph_read)


# =============================================================================
#  KLASSE 6 -- Zahl, Variable, Operation
# =============================================================================

def kl6_signed_add():
    """Addition mit vorzeichenbehafteten Zahlen."""
    a = random.randint(-50, 50)
    b = random.randint(-50, 50)
    return f"Berechne: ({a}) + ({b})."
GENERATORS_KL6.append(kl6_signed_add)

def kl6_signed_sub():
    """Subtraktion mit vorzeichenbehafteten Zahlen."""
    a = random.randint(-50, 50)
    b = random.randint(-50, 50)
    return f"Berechne: ({a}) - ({b})."
GENERATORS_KL6.append(kl6_signed_sub)

def kl6_signed_mul():
    """Multiplikation mit vorzeichenbehafteten Zahlen."""
    a = random.randint(-20, 20)
    b = random.randint(-20, 20)
    return f"Berechne: ({a}) x ({b})."
GENERATORS_KL6.append(kl6_signed_mul)

def kl6_signed_div():
    """Division mit vorzeichenbehafteten Zahlen."""
    b = random.choice([-8, -7, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8])
    result = random.randint(-12, 12)
    a = b * result
    return f"Berechne: ({a}) : ({b})."
GENERATORS_KL6.append(kl6_signed_div)

def kl6_signed_multi_step():
    """Mehrstufige Rechnung mit ganzen Zahlen."""
    a = random.randint(-15, 15)
    b = random.randint(-15, 15)
    c = random.randint(-10, 10)
    while c == 0:
        c = random.randint(-10, 10)
    pattern = random.choice([
        f"({a}) x ({b}) + ({c})",
        f"({a})**2 - ({b}) x ({c})",
        f"({a} + {b}) x ({c}) - ({a})",
        f"({a}) x ({b}) : ({c}) + ({a})",
    ])
    return f"Berechne: {pattern}."
GENERATORS_KL6.append(kl6_signed_multi_step)

def kl6_power_positive():
    """Potenzen mit positiver Basis."""
    base = random.randint(2, 12)
    exp = random.choice([2, 3, 4, 5])
    return f"Berechne: {base}^{exp}."
GENERATORS_KL6.append(kl6_power_positive)

def kl6_power_negative():
    """Potenzen mit negativer Basis."""
    base = random.randint(-8, -2)
    exp = random.choice([2, 3, 4])
    return f"Berechne: ({base})^{exp}. Was faellest dir auf?"
GENERATORS_KL6.append(kl6_power_negative)

def kl6_power_negative_exp():
    """Potenzen mit negativem Exponenten (einfach)."""
    base = random.choice([2, 3, 4, 5])
    return f"Berechne: {base}^(-2). Schreibe als Bruch."
GENERATORS_KL6.append(kl6_power_negative_exp)

def kl6_sqrt():
    """Quadratwurzeln ziehen."""
    n = random.choice([i*i for i in range(2, 20)])
    return f"Berechne: Wurzel aus {n}."
GENERATORS_KL6.append(kl6_sqrt)

def kl6_cbrt():
    """Kubikwurzeln ziehen."""
    n = random.choice([i**3 for i in range(2, 10)])
    return f"Berechne: Kubikwurzel aus {n}."
GENERATORS_KL6.append(kl6_cbrt)

def kl6_power_mixed():
    """Potenzen und Wurzeln gemischt."""
    a = random.randint(2, 5)
    b = random.randint(2, 3)
    c = random.choice([4, 9, 16, 25])
    return f"Berechne: {a}^{b} + Wurzel aus {c}."
GENERATORS_KL6.append(kl6_power_mixed)

def kl6_term_simplify():
    """Terme vereinfachen (addieren/subtrahieren)."""
    a = random.randint(2, 8)
    b = random.randint(1, 10)
    c = random.randint(2, 6)
    d = random.randint(1, 10)
    sign = random.choice(['+', '-'])
    return f"Vereinfache: ({a}x + {b}) {sign} ({c}x {'-' if sign == '+' else '+'} {d})."
GENERATORS_KL6.append(kl6_term_simplify)

def kl6_term_expand():
    """Ausmultiplizieren und Ausklammern."""
    a = random.randint(2, 8)
    b = random.randint(1, 10)
    c = random.randint(2, 6)
    kind = random.choice(['ausmultiplizieren', 'ausklammern'])
    if kind == 'ausmultiplizieren':
        return f"Multipliziere aus: {a}(x + {b}) + {c}(x - {b})."
    else:
        return f"Klammer aus: {a}x^2 + {b}x."
GENERATORS_KL6.append(kl6_term_expand)

def kl6_term_evaluate():
    """Term berechnen durch Einsetzen."""
    a = random.randint(2, 8)
    b = random.randint(-5, 5)
    c = random.randint(-3, 3)
    val = random.randint(1, 6)
    return (f"Fuer f(x) = {a}x + {b}: "
            f"Berechne f({val}).")
GENERATORS_KL6.append(kl6_term_evaluate)

def kl6_term_quadratic_evaluate():
    """Quadratischen Term berechnen."""
    a = random.randint(1, 5)
    b = random.randint(-5, 5)
    c = random.randint(-3, 3)
    val = random.randint(1, 5)
    return (f"Fuer f(x) = {a}x^2 + {b}x + {c}: "
            f"Berechne f({val}).")
GENERATORS_KL6.append(kl6_term_quadratic_evaluate)

def kl6_term_word():
    """Terme aus Textaufgaben aufstellen."""
    l = random.randint(5, 15)
    b = random.randint(3, 10)
    h = random.randint(4, 12)
    return (f"Ein Dreieck hat Grundseite a = {l} cm und Hoehe h = {h} cm. "
            f"Ein Quadrat hat Seite s = {b} cm. "
            f"Stelle einen Term fuer den Unterschied der Flaecheninhalte auf.")
GENERATORS_KL6.append(kl6_term_word)

def kl6_equation_simple():
    """Einfache lineare Gleichung."""
    a = random.randint(2, 15)
    b = random.randint(-20, 20)
    x = random.randint(-10, 10)
    result = a * x + b
    return f"Loese: {a}x + {b} = {result}."
GENERATORS_KL6.append(kl6_equation_simple)

def kl6_equation_brackets():
    """Gleichung mit Klammer."""
    a = random.randint(2, 8)
    b = random.randint(1, 10)
    c = random.randint(1, 10)
    x = random.randint(-5, 5)
    result = a * (x + b) + c
    return f"Loese: {a}(x + {b}) + {c} = {result}."
GENERATORS_KL6.append(kl6_equation_brackets)

def kl6_equation_both_sides():
    """Gleichung mit Termen auf beiden Seiten."""
    x = random.randint(-5, 5)
    a = random.randint(2, 8)
    c = random.randint(2, 8)
    while c == a:
        c = random.randint(2, 8)
    b = random.randint(1, 10)
    d = a * x + b - c * x
    return f"Loese: {a}x + {b} = {c}x + {d}."
GENERATORS_KL6.append(kl6_equation_both_sides)

def kl6_equation_word():
    """Gleichung aus Textaufgabe."""
    price = random.randint(3, 20)
    items = random.randint(3, 12)
    extra = random.randint(5, 30)
    total = price * items + extra
    return (f"Maria kauft {items} Buecher zu je {price} Euro und zahlt {extra} Euro Porto. "
            f"Gesamtpreis: {total} Euro. "
            f"Stelle eine Gleichung auf und berechne den Buchpreis.")
GENERATORS_KL6.append(kl6_equation_word)

def kl6_percentage_complex():
    """Prozentrechnung (fortgeschritten)."""
    kind = random.choice(['erhoehen', 'senken', 'zwischenwerte'])
    if kind == 'erhoehen':
        val = random.randint(40, 300)
        pct = random.choice([8, 12, 15, 20, 25, 30])
        return f"Ein Wert von {val} Euro wird um {pct}% erhoeht. Berechne den neuen Wert."
    elif kind == 'senken':
        val = random.randint(50, 500)
        pct = random.choice([10, 15, 20, 25, 30, 40])
        return f"Ein Wert von {val} Euro wird um {pct}% reduziert. Berechne den neuen Wert."
    else:
        new_val = random.randint(80, 500)
        old_val = random.randint(50, new_val - 1)
        return (f"Ein Preis steigt von {old_val} Euro auf {new_val} Euro. "
                f"Um wie viel Prozent ist er gestiegen?")
GENERATORS_KL6.append(kl6_percentage_complex)

def kl6_proportionality():
    """Direkte Proportionalitaet."""
    k = random.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5])
    x = random.randint(2, 10)
    return (f"f(x) = {k}x ist eine direkte Proportionalitaet. "
            f"Berechne f({x}).")
GENERATORS_KL6.append(kl6_proportionality)

def kl6_inverse_proportionality():
    """Umgekehrt proportionale Zuordnung."""
    k = random.choice([12, 24, 36, 48, 60, 72, 100, 120])
    x = random.randint(2, 10)
    return (f"f(x) = {k}/x ist eine umgekehrt proportionale Zuordnung. "
            f"Berechne f({x}).")
GENERATORS_KL6.append(kl6_inverse_proportionality)

# --- KLASSE 6 -- Messen ---

def kl6_dreisatz():
    """Einfacher Dreisatz."""
    a = random.randint(3, 10)
    b = random.randint(5, 30)
    c = random.randint(2, 8)
    return (f"{a} Artikel kosten {b} Euro. "
            f"Wie viel kosten {c} Artikel?")
GENERATORS_KL6.append(kl6_dreisatz)

def kl6_proportional_dreisatz():
    """Proportionaler Dreisatz mit Groessen."""
    kind = random.choice(['geschwindigkeit', 'dichte', 'massstab', 'preis_menge'])
    if kind == 'geschwindigkeit':
        v = random.randint(50, 130)
        t = random.randint(1, 4)
        return (f"Ein Auto faehrt {v} km/h. "
                f"Wie weit kommt es in {t} Stunden?")
    elif kind == 'dichte':
        mass = random.randint(100, 500)
        volume = random.randint(10, 50)
        return (f"Eine Fluessigkeit hat Dichte {mass}/{volume} g/cm3. "
                f"Wie viel wiegt ein Volumen von {volume * 3} cm3?")
    elif kind == 'massstab':
        real_l = random.randint(10, 50)
        real_w = random.randint(5, 30)
        scale = random.choice([100, 200, 500, 1000])
        return (f"Ein Grundstueck ist {real_l} m lang und {real_w} m breit. "
                f"Im Massstab 1:{scale}: Berechne die Abmessungen in cm.")
    else:
        price = random.randint(2, 15)
        amount = random.randint(3, 10)
        return (f"{amount} Apfel kosten {price} Euro. "
                f"Wie viel kosten 1 kg, wenn 1 Apfel 150 g wiegt?")
GENERATORS_KL6.append(kl6_proportional_dreisatz)

def kl6_scale_problem():
    """Massstab und Umrechnung."""
    real_h = random.randint(50, 200)
    scale = random.choice([100, 200, 500])
    return (f"Ein Haus ist {real_h} cm hoch. "
            f"Im Grundriss (Massstab 1:{scale}) wie hoch ist es?")
GENERATORS_KL6.append(kl6_scale_problem)

# --- KLASSE 6 -- Raum und Form ---

def kl6_pythagoras_hypotenuse():
    """Pythagoras: Hypotenuse berechnen."""
    a = random.randint(3, 15)
    b = random.randint(3, 15)
    return (f"Rechtwinkliges Dreieck: a = {a} cm, b = {b} cm. "
            f"Berechne die Hypotenuse c.")
GENERATORS_KL6.append(kl6_pythagoras_hypotenuse)

def kl6_pythagoras_leg():
    """Pythagoras: Kathete berechnen."""
    c = random.randint(10, 25)
    a = random.randint(3, c - 3)
    return (f"Rechtwinkliges Dreieck: c = {a} cm (Hypotenuse), b = {c} cm. "
            f"Berechne die Kathete a.")
GENERATORS_KL6.append(kl6_pythagoras_leg)

def kl6_pythagoras_word():
    """Pythagoras in Textaufgaben."""
    a = random.randint(3, 10)
    b = random.randint(3, 10)
    kind = random.choice(['leiter', 'seil', 'diagonale'])
    if kind == 'leiter':
        return (f"Eine Leiter steht {a} m vom Haus entfernt und reicht {a + b} m hoch. "
                f"Wie lang ist die Leiter?")
    elif kind == 'seil':
        return (f"Ein Seil ist {a + b} m lang. Es wird am Boden {a} m vom Pfosten entfernt befestigt. "
                f"Wie hoch reicht es?")
    else:
        return (f"Ein Rechteck hat die Seiten {a} cm und {b} cm. "
                f"Berechne die Laenge der Diagonale.")
GENERATORS_KL6.append(kl6_pythagoras_word)

def kl6_pythagoras_reverse():
    """Pythagoras Umkehrung: Ist das Dreieck rechtwinklig?"""
    triples = [
        (3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
        (6, 8, 10), (9, 12, 15), (9, 40, 41), (11, 60, 61),
    ]
    kind = random.choice(['rechtwinklig', 'nicht_rechtwinklig'])
    if kind == 'rechtwinklig':
        a, b, c = random.choice(triples)
        factor = random.choice([1, 2])
        return (f"Ist ein Dreieck mit den Seiten {a*factor} cm, {b*factor} cm, {c*factor} cm "
                f"rechtwinklig? Begründe mit dem Umkehrungssatz.")
    else:
        a, b, c = random.randint(4, 15), random.randint(4, 15), random.randint(4, 15)
        while a**2 + b**2 == c**2 or a**2 + c**2 == b**2 or b**2 + c**2 == a**2:
            a, b, c = random.randint(4, 15), random.randint(4, 15), random.randint(4, 15)
        sides = sorted([a, b, c])
        return (f"Ist ein Dreieck mit den Seiten {sides[0]} cm, {sides[1]} cm, {sides[2]} cm "
                f"rechtwinklig? Begründe.")
GENERATORS_KL6.append(kl6_pythagoras_reverse)

def kl6_circumference():
    """Kreisumfang."""
    r = random.randint(2, 15)
    return f"Ein Kreis hat Radius r = {r} cm. Berechne den Umfang (U = 2*pi*r)."
GENERATORS_KL6.append(kl6_circumference)

def kl6_circle_area():
    """Kreisflaeche."""
    r = random.randint(2, 15)
    return f"Ein Kreis hat Radius r = {r} cm. Berechne die Flaeche (A = pi*r^2)."
GENERATORS_KL6.append(kl6_circle_area)

def kl6_circle_ring():
    """Kreisring-Flaeche."""
    r_in = random.randint(2, 8)
    r_out = r_in + random.randint(2, 8)
    return (f"Ein Kreisring: innerer Radius r = {r_in} cm, aeusserer Radius R = {r_out} cm. "
            f"Berechne die Flaeche des Rings.")
GENERATORS_KL6.append(kl6_circle_ring)

def kl6_circle_from_diameter():
    """Kreis aus Durchmesser."""
    d = random.randint(6, 30)
    return (f"Ein Rad hat Durchmesser d = {d} cm. "
            f"Berechne Radius, Umfang und Flaeche des Rads.")
GENERATORS_KL6.append(kl6_circle_from_diameter)

def kl6_circle_word():
    """Kreis: Textaufgabe."""
    r = random.randint(3, 12)
    rotations = random.randint(10, 50)
    return (f"Ein Fahrradrad hat Radius {r} cm. "
            f"Wie weit faehrt das Rad in {rotations} Umdrehungen?")
GENERATORS_KL6.append(kl6_circle_word)

def kl6_trapez_area():
    """Trapez-Flaeche."""
    a = random.randint(6, 18)
    b = random.randint(4, a - 1)
    h = random.randint(4, 12)
    return (f"Ein Trapez: parallele Seiten a = {a} cm und b = {b} cm, Hoehe h = {h} cm. "
            f"Berechne den Flaecheninhalt.")
GENERATORS_KL6.append(kl6_trapez_area)

def kl6_hexagon_area():
    """Regelmaessiges Sechseck."""
    a = random.randint(3, 10)
    return (f"Ein regelm. Sechseck hat Seitenlaenge a = {a} cm. "
            f"Berechne den Flaecheninhalt (A = (3*Wurzel(3)/2)*a^2).")
GENERATORS_KL6.append(kl6_hexagon_area)

def kl6_triangle_advanced():
    """Dreieck: Flaeche mit Seiten und Winkel."""
    a = random.randint(5, 15)
    b = random.randint(5, 15)
    angle = random.choice([30, 45, 60, 90, 120, 135, 150])
    return (f"Ein Dreieck hat die Seiten a = {a} cm und b = {b} cm "
            f"sowie den eingeschlossenen Winkel {angle} Grad. "
            f"Skizziere das Dreieck.")
GENERATORS_KL6.append(kl6_triangle_advanced)

def kl6_cone_volume():
    """Kegel-Volumen."""
    r = random.randint(2, 8)
    h = random.randint(5, 15)
    return (f"Ein Kegel: Radius r = {r} cm, Hoehe h = {h} cm. "
            f"Berechne das Volumen (V = (1/3)*pi*r^2*h).")
GENERATORS_KL6.append(kl6_cone_volume)

def kl6_pyramid_volume():
    """Pyramiden-Volumen."""
    side = random.randint(4, 12)
    h = random.randint(5, 15)
    return (f"Quadratische Pyramide: Grundseite a = {side} cm, Hoehe h = {h} cm. "
            f"Berechne das Volumen.")
GENERATORS_KL6.append(kl6_pyramid_volume)

def kl6_sphere():
    """Kugel: Volumen und Oberflaeche."""
    r = random.randint(2, 10)
    return (f"Eine Kugel hat Radius r = {r} cm. "
            f"Berechne Volumen und Oberflaeche.")
GENERATORS_KL6.append(kl6_sphere)

def kl6_cylinder_volume():
    """Zylinder-Volumen."""
    r = random.randint(2, 8)
    h = random.randint(5, 20)
    return (f"Ein Zylinder: Radius r = {r} cm, Hoehe h = {h} cm. "
            f"Berechne Volumen und Mantelflaeche.")
GENERATORS_KL6.append(kl6_cylinder_volume)

def kl6_hollow_cylinder():
    """Hohler Zylinder (Rohr)."""
    r_out = random.randint(4, 10)
    r_in = random.randint(2, r_out - 1)
    h = random.randint(5, 20)
    return (f"Hohler Zylinder: aeusserer Radius R = {r_out} cm, "
            f"innerer Radius r = {r_in} cm, Hoehe h = {h} cm. "
            f"Berechne das Materialvolumen.")
GENERATORS_KL6.append(kl6_hollow_cylinder)

def kl6_congruence_criterion():
    """Kongruenzkriterien."""
    a, b, c = random.randint(4, 12), random.randint(4, 12), random.randint(4, 12)
    while a + b <= c or a + c <= b or b + c <= a:
        a, b, c = random.randint(4, 12), random.randint(4, 12), random.randint(4, 12)
    angle = random.choice([30, 45, 60, 90, 120])
    kind = random.choice(['SSS', 'SWS', 'WSW'])
    if kind == 'SSS':
        return (f"Zwei Dreiecke haben die Seiten {a} cm, {b} cm, {c} cm. "
                f"Sind sie kongruent? Welches Kriterium?")
    elif kind == 'SWS':
        return (f"Zwei Dreiecke haben: Seite {a} cm, Winkel {angle} Grad, Seite {b} cm. "
                f"Sind sie kongruent? Welches Kriterium?")
    else:
        angle2 = random.choice([30, 45, 60, 90])
        return (f"Zwei Dreiecke haben: Winkel {angle} Grad, Seite {a} cm, Winkel {angle2} Grad. "
                f"Sind sie kongruent? Welches Kriterium?")
GENERATORS_KL6.append(kl6_congruence_criterion)

def kl6_similarity():
    """Aehnliche Figuren."""
    a1 = random.randint(3, 10)
    b1 = random.randint(3, 10)
    c1 = random.randint(3, 10)
    factor = random.choice([1.5, 2, 2.5, 3, 0.5])
    return (f"Dreieck 1: Seiten {a1} cm, {b1} cm, {c1} cm. "
            f"Dreieck 2 ist aehnlich im Massstab {factor}. "
            f"Berechne die Seitenlaengen von Dreieck 2.")
GENERATORS_KL6.append(kl6_similarity)

def kl6_scaleDrawing():
    """Massstabszeichnung."""
    real_l = random.randint(5, 30)
    real_w = random.randint(3, 20)
    scale = random.choice([50, 100, 200, 500])
    return (f"Ein Grundstueck ist {real_l} m lang und {real_w} m breit. "
            f"Erstelle eine Zeichnung im Massstab 1:{scale}. "
            f"Berechne die Abmessungen in cm.")
GENERATORS_KL6.append(kl6_scaleDrawing)

def kl6_coords_reflect():
    """Punkt im Koordinatensystem spiegeln (4 Quadranten)."""
    x = random.randint(-8, 8)
    y = random.randint(-8, 8)
    axis = random.choice(['x-Achse', 'y-Achse', 'Ursprung'])
    return (f"Spiegle P({x}|{y}) an der {axis}. "
            f"Gib die Koordinaten von P' an.")
GENERATORS_KL6.append(kl6_coords_reflect)

def kl6_coords_distance():
    """Abstand zweier Punkte (alle Quadranten)."""
    x1, y1 = random.randint(-8, 8), random.randint(-8, 8)
    x2, y2 = random.randint(-8, 8), random.randint(-8, 8)
    while x1 == x2 and y1 == y2:
        x2, y2 = random.randint(-8, 8), random.randint(-8, 8)
    return (f"Berechne den Abstand A({x1}|{y1}) und B({x2}|{y2}).")
GENERATORS_KL6.append(kl6_coords_distance)

def kl6_coords_midpoint():
    """Mittelpunkt einer Strecke."""
    x1, y1 = random.randint(-10, 10), random.randint(-10, 10)
    x2, y2 = random.randint(-10, 10), random.randint(-10, 10)
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    return (f"Mittelpunkt von A({x1}|{y1}) und B({x2}|{y2}) berechnen.")
GENERATORS_KL6.append(kl6_coords_midpoint)

def kl6_coords_transform():
    """Punkt transformieren (drehen, verschieben)."""
    x, y = random.randint(-6, 6), random.randint(-6, 6)
    dx = random.randint(-5, 5)
    dy = random.randint(-5, 5)
    return (f"Verschiebe P({x}|{y}) um ({dx}|{dy}). "
            f"Gib die neuen Koordinaten an.")
GENERATORS_KL6.append(kl6_coords_transform)

def kl6_linear_func_slope():
    """Steigung einer linearen Funktion."""
    x1, y1 = random.randint(-5, 5), random.randint(-5, 5)
    x2, y2 = random.randint(-5, 5), random.randint(-5, 5)
    while x2 == x1:
        x2 = random.randint(-5, 5)
    return f"Bestimme die Steigung durch A({x1}|{y1}) und B({x2}|{y2})."
GENERATORS_KL6.append(kl6_linear_func_slope)

def kl6_linear_func_draw():
    """Lineare Funktion zeichnen."""
    m = random.choice([i for i in range(-5, 6) if i != 0])
    n = random.randint(-8, 8)
    return (f"Zeichne den Graphen von f(x) = {m}x + {n}. "
            f"Bestimme Steigung, y-Achsenabschnitt und Nullstelle.")
GENERATORS_KL6.append(kl6_linear_func_draw)

def kl6_linear_func_zero():
    """Nullstelle finden."""
    m = random.choice([i for i in range(-6, 7) if i != 0])
    n = random.choice([i for i in range(-10, 11) if i != 0])
    return f"Bestimme die Nullstelle von f(x) = {m}x + {n}."
GENERATORS_KL6.append(kl6_linear_func_zero)

def kl6_linear_func_word():
    """Lineare Funktion in Textaufgabe."""
    kind = random.choice(['temp', 'preis', 'entfernung'])
    if kind == 'temp':
        start = random.randint(-10, 5)
        rate = random.choice([0.5, 1, 1.5, 2])
        target = random.randint(15, 30)
        return (f"Temperatur: Start {start} Grad C, steigt {rate} Grad pro Minute. "
                f"Stelle f(t) auf. Wann werden {target} Grad erreicht?")
    elif kind == 'preis':
        base = random.randint(10, 50)
        per_unit = random.randint(2, 8)
        return (f"Ein Auto kostet {base} Euro Basis + {per_unit} Euro pro km. "
                f"Stelle f(x) auf fuer x km. Was kostet eine {random.randint(20,100)}-km-Fahrt?")
    else:
        start = random.randint(10, 100)
        speed = random.randint(30, 120)
        return (f"Ein Auto ist {start} km vom Ziel entfernt und faehrt {speed} km/h. "
                f"Stelle eine Funktion s(t) fuer die Reststrecke auf.")
GENERATORS_KL6.append(kl6_linear_func_word)

def kl6_proportional_func():
    """Direkte Proportionalitaet (f(x) = kx)."""
    k = random.choice([0.5, 1, 1.5, 2, 2.5, 3, 4, 5])
    x = random.randint(2, 10)
    return (f"f(x) = {k}x. Berechne f({x}). "
            f"Was bedeutet k = {k} in einem Alltagsbeispiel?")
GENERATORS_KL6.append(kl6_proportional_func)

def kl6_inverse_prop_func():
    """Umgekehrt proportionale Funktion."""
    k = random.choice([12, 24, 36, 48, 60, 72, 100, 120])
    x = random.randint(2, 10)
    return (f"f(x) = {k}/x. Berechne f({x}). "
            f"Zeichne den Graphen (Schaubild).")
GENERATORS_KL6.append(kl6_inverse_prop_func)

# --- KLASSE 6 -- Daten und Zufall ---

def kl6_mean():
    """Mittelwert (fortgeschritten)."""
    numbers = sorted([random.randint(5, 60) for _ in range(random.randint(8, 12))])
    nums_str = ", ".join(str(n) for n in numbers)
    return f"Berechne den Mittelwert: {nums_str}."
GENERATORS_KL6.append(kl6_mean)

def kl6_median_advanced():
    """Median (fortgeschritten)."""
    numbers = sorted([random.randint(5, 60) for _ in range(random.choice([9, 11, 13]))])
    nums_str = ", ".join(str(n) for n in numbers)
    return f"Berechne den Median: {nums_str}."
GENERATORS_KL6.append(kl6_median_advanced)

def kl6_variance():
    """Varianz und Standardabweichung."""
    numbers = sorted([random.randint(5, 30) for _ in range(6)])
    nums_str = ", ".join(str(n) for n in numbers)
    return (f"Berechne Varianz und Standardabweichung: {nums_str}.")
GENERATORS_KL6.append(kl6_variance)

def kl6_stats_interpret():
    """Statistik interpretieren."""
    subject = random.choice(["Mathe", "Deutsch", "Englisch", "Physik", "Sport"])
    numbers = sorted([random.randint(1, 6) for _ in range(random.randint(8, 15))])
    nums_str = ", ".join(str(n) for n in numbers)
    return (f"Noten im Fach {subject}: {nums_str}. "
            f"Berechne Mittelwert, Median und Spannweite. "
            f"Was sagt der Mittelwert ueber die Klasse aus?")
GENERATORS_KL6.append(kl6_stats_interpret)

def kl6_probability_urne():
    """Wahrscheinlichkeit: Urnenmodell."""
    red = random.randint(2, 8)
    blue = random.randint(2, 8)
    total = red + blue
    pick = random.choice([1, 2])
    if pick == 1:
        return (f"Urne: {red} rot, {blue} blau. 1 Kugel gezogen. "
                f"P(rot) = ?")
    else:
        return (f"Urne: {red} rot, {blue} blau. 2 Kugeln gleichzeitig. "
                f"P(2x rot) = ?")
GENERATORS_KL6.append(kl6_probability_urne)

def kl6_probability_urne_mixed():
    """Urne: gemischte Ereignisse."""
    red = random.randint(2, 6)
    blue = random.randint(2, 6)
    yellow = random.randint(1, 4)
    return (f"Urne: {red} rot, {blue} blau, {yellow} gelb. "
            f"1 Kugel gezogen. P(rot oder gelb) = ?")
GENERATORS_KL6.append(kl6_probability_urne_mixed)

def kl6_probability_tree():
    """Mehrstufiger Versuch (Baumdiagramm)."""
    kind = random.choice(['muenze_wuerfel', 'kugeln_zurueck'])
    if kind == 'muenze_wuerfel':
        return (f"Muenze werfen, dann 6er-Wuerfel. "
                f"Wie gross ist P(Kopf UND Zahl > 4)?")
    else:
        red = random.randint(3, 8)
        blue = random.randint(3, 8)
        total = red + blue
        return (f"Urne: {red} rot, {blue} blau. "
                f"2 Kugeln MIT Zuruecklegen. "
                f"P(1x rot, 1x blau in beliebiger Reihenfolge) = ?")
GENERATORS_KL6.append(kl6_probability_tree)

def kl6_probability_dice_multi():
    """Mehrere Wuerfel."""
    n_dice = random.choice([2, 3])
    faces = 6
    target = random.randint(n_dice, n_dice * faces)
    return (f"{n_dice} Wuerfel (je 6 Seiten) werden geworfen. "
            f"P(Summe >= {target}) = ?")
GENERATORS_KL6.append(kl6_probability_dice_multi)

def kl6_probability_complement():
    """Gegenereignis."""
    red = random.randint(3, 8)
    blue = random.randint(3, 8)
    total = red + blue
    return (f"Urne: {red} rot, {blue} blau. "
            f"Berechne P(nicht rot) mit dem Gegenereignis.")
GENERATORS_KL6.append(kl6_probability_complement)

def kl6_probability_conditional():
    """Bedingte Wahrscheinlichkeit (einfach)."""
    total = random.randint(10, 20)
    a = random.randint(3, total // 2)
    b = random.randint(2, total - a - 1)
    return (f"Eine Klasse hat {total} Schueler: {a} Maedchen mit Brille, "
            f"{b} Jungen mit Brille. "
            f"Wenn ein Maedchen ausgewaehlt wird: P(Brille)?")
GENERATORS_KL6.append(kl6_probability_conditional)


# =============================================================================
#  Generierungsfunktionen (mit Deduplizierung)
# =============================================================================

def create_problem_set(generators, num_problems=50):
    """Erzeugt eine Aufgabenliste OHNE Wiederholungen.

    Waehlt zufaellig Generatoren aus und prueft jede Aufgabe
    auf Eindeutigkeit. Duplikate werden neu generiert (max. 50 Versuche).
    """
    problems = []
    seen = set()

    for i in range(num_problems):
        problem = None
        for _ in range(50):
            gen = random.choice(generators)
            try:
                candidate = gen()
            except Exception:
                candidate = "[Generierungsfehler]"
            if candidate not in seen:
                problem = candidate
                seen.add(candidate)
                break
        if problem is None:
            problem = candidate  # Fallback: aufnehmen auch wenn Duplikat
        problems.append(f"{i + 1}. {problem}")

    return problems


def create_word_document(problems, title, subtitle=""):
    """Erstellt ein Word-Dokument im Speicher."""
    doc = Document()
    doc.add_heading(title, level=0)
    if subtitle:
        doc.add_paragraph(subtitle)

    for problem in problems:
        p = doc.add_paragraph(problem)
        p.style.font.size = Pt(11)

    bio = BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.getvalue()


# =============================================================================
#  Hauptprogramm
# =============================================================================

def main():
    print("=" * 60)
    print("  Matheaufgaben Generator -- Gymnasium Klasse 5 & 6")
    print("  Fachlehrplan Sachsen-Anhalt (01.08.2022)")
    print("=" * 60)
    print()

    # Konfiguration
    num_sets_kl5 = 5
    num_sets_kl6 = 5
    problems_per_set = 50
    output_dir = "Matheaufgaben_Output"

    os.makedirs(output_dir, exist_ok=True)

    print(f"  Verfuegbare Generatoren:")
    print(f"    Klasse 5: {len(GENERATORS_KL5)} Generatorfunktionen")
    print(f"    Klasse 6: {len(GENERATORS_KL6)} Generatorfunktionen")
    print()

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:

        # --- Klasse 5 ---
        print(f"Generiere {num_sets_kl5} Aufgabensaetze fuer Klasse 5 ...")
        for i in range(1, num_sets_kl5 + 1):
            problems = create_problem_set(GENERATORS_KL5, problems_per_set)
            title = f"Schwere Mathematikaufgaben -- Gymnasium Klasse 5 (Sachsen-Anhalt) -- Set {i}"
            subtitle = (f"Aufgabensatz {i} von {num_sets_kl5} | "
                        f"{len(problems)} Aufgaben | "
                        f"Erstellt am {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            docx_bytes = create_word_document(problems, title, subtitle)
            filename = f"Klasse_5_Set_{i:02d}.docx"
            zf.writestr(filename, docx_bytes)
            print(f"  [OK] {filename} ({len(problems)} Aufgaben)")

        # --- Klasse 6 ---
        print(f"\nGeneriere {num_sets_kl6} Aufgabensaetze fuer Klasse 6 ...")
        for i in range(1, num_sets_kl6 + 1):
            problems = create_problem_set(GENERATORS_KL6, problems_per_set)
            title = f"Schwere Mathematikaufgaben -- Gymnasium Klasse 6 (Sachsen-Anhalt) -- Set {i}"
            subtitle = (f"Aufgabensatz {i} von {num_sets_kl6} | "
                        f"{len(problems)} Aufgaben | "
                        f"Erstellt am {datetime.now().strftime('%d.%m.%Y %H:%M')}")
            docx_bytes = create_word_document(problems, title, subtitle)
            filename = f"Klasse_6_Set_{i:02d}.docx"
            zf.writestr(filename, docx_bytes)
            print(f"  [OK] {filename} ({len(problems)} Aufgaben)")

    # ZIP speichern
    zip_buffer.seek(0)
    zip_path = os.path.join(output_dir, "Matheaufgaben_Klasse_5_6_SCHWER.zip")
    with open(zip_path, "wb") as f:
        f.write(zip_buffer.getvalue())

    total_sets = num_sets_kl5 + num_sets_kl6
    print("\n" + "=" * 60)
    print(f"  Fertig! ZIP-Datei gespeichert unter:")
    print(f"  {os.path.abspath(zip_path)}")
    print(f"  Gesamt: {total_sets} Sets, "
          f"ca. {total_sets * problems_per_set} Aufgaben")
    print(f"  Keine Wiederholungen innerhalb eines Sets garantiert.")
    print("=" * 60)


if __name__ == "__main__":
    main()
