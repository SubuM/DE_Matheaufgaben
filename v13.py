import streamlit as st
import random
import time
from datetime import datetime
from groq import Groq
from docx import Document
from io import BytesIO
import zipfile

# =============================================================================
#  v13 -- Zero-Cost AI Math Generator (Groq Free Tier)
#  Generates tough, syllabus-aligned transfer tasks dynamically.
# =============================================================================

SYLLABUS_TOPICS = [
    # Klasse 5
    "Schriftliche Addition/Subtraktion grosser Zahlen", "Schriftliche Multiplikation und Division",
    "Mehrstufiges Rechnen mit Klammern und Potenzen", "Runden grosser Zahlen und Dezimalzahlen",
    "Brueche: Addieren, Subtrahieren, Multiplizieren, Dividieren", "Bruch/Dezimal Umwandlung", 
    "Prozentrechnung (Anteil, Gesamtwert)", "ggT, kgV, Primfaktorzerlegung",
    "Umrechnungen: Laenge, Gewicht, Volumen, Zeit", "Zeitrechnung als Textaufgabe",
    "Umfang und Flaeche von Rechtecken und Dreiecken", "Zusammengesetzte Figuren (L-Form, T-Form)",
    "Volumen und Oberflaeche von Wuerfel und Quader", "Symmetrieachsen und Punktspiegelung",
    "Mittelwert, Median, Spannweite", "Wahrscheinlichkeit (Wuerfel, Kugeln)",
    # Klasse 6
    "Ganze Zahlen: alle Grundrechenarten", "Potenzen und Wurzeln (Quadrat, Kubik)",
    "Terme vereinfachen und berechnen durch Einsetzen", "Lineare Gleichungen mit Klammern",
    "Proportionalitaet (direkt/umgekehrt) und Dreisatz", "Massstab und Umrechnung",
    "Pythagoras (Hypotenuse, Kathete, Textaufgaben)", "Kreis (Umfang, Flaeche, Kreisring)",
    "Flaeche von Trapez", "Volumen/Oberflaeche von Zylinder und Prisma",
    "Kongruenzkriterien und aehnliche Figuren", "Koordinatensystem (Spiegeln, Abstand)",
    "Lineare Funktionen (Steigung, Nullstelle)", "Wahrscheinlichkeit (Urnenmodell, Baumdiagramm)"
]

def generate_problems_with_groq(api_key, topics_sample, num_problems=50):
    """
    Uses the free Groq API to generate unique math problems based on the syllabus.
    """
    client = Groq(api_key=api_key)
    topics_list_str = "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(topics_sample)])
    
    system_prompt = (
        "Du bist ein anspruchsvoller Mathematik-Lehrer an einem Gymnasium in Sachsen-Anhalt. "
        "Deine Aufgabe ist es, komplexe Denkaufgaben und Transferaufgaben zu erstellen."
    )
    
    user_prompt = f"""
    Erstelle genau {num_problems} einzigartige, extrem schwere Denkaufgaben für die Klassen 5 und 6.
    Nutze dafür diese zugewiesenen Lehrplanthemen in der gleichen Reihenfolge:
    {topics_list_str}

    Anforderungen:
    - Verknüpfe verschiedene Konzepte (z.B. Geometrie mit Brüchen).
    - Erfinde komplexe Sachsituationen.
    - Formatiere die Ausgabe als reine, nummerierte Liste (1. Aufgabe..., 2. Aufgabe...).
    - Verwende KEIN Markdown (kein Fettdruck, keine Sterne).
    - Gib NUR die Aufgaben zurück. Keine Einleitung, keine Lösungen.
    """

    try:
        # llama-3.1-70b-versatile is excellent and fully supported on the free tier
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            # model="llama-3.1-70b-versatile",
            # model = "qwen/qwen3.8-27b",
            model = "mixtral-8x7b-32768",
            # model = "openai/gpt-oss-20b",

            temperature=0.7,
        )
        
        content = response.choices[0].message.content
        problems = [line.strip() for line in content.split('\n') if line.strip() and (line[0].isdigit() or line.startswith('-'))]
        
        # Fallback parsing
        if len(problems) < num_problems / 2:
            problems = [p for p in content.split('\n\n') if p.strip()]
            
        return problems
    except Exception as e:
        return [f"API-Fehler (Groq): {str(e)}"]

def create_word_document(problems, set_number):
    document = Document()
    document.add_heading(f'Gymnasium Kl. 5 & 6 (Sachsen-Anhalt) - Set {set_number}', 0)
    document.add_paragraph("Dynamische Denkaufgaben mit erhoehtem Schwierigkeitsgrad.")
    document.add_paragraph(f"Erstellt am {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    
    for i, problem in enumerate(problems, 1):
        clean_prob = problem.lstrip('0123456789.- ')
        document.add_paragraph(f"{i}. {clean_prob}")

    bio = BytesIO()
    document.save(bio)
    bio.seek(0)
    return bio.getvalue()

def main_app():
    # Attempt to load the free Groq key from secrets
    api_key = None
    if "groq" in st.secrets and "api_key" in st.secrets["groq"]:
        api_key = st.secrets["groq"]["api_key"]
    else:
        st.error("Groq API Key fehlt. Bitte in .streamlit/secrets.toml eintragen.")
        return

    st.title("🧠 Zero-Cost Mathe-Generator (Groq)")
    st.markdown("Generiert völlig einzigartige Denkaufgaben aus Klasse 5 & 6[cite: 1, 2] – 100% kostenlos via Groq[cite: 3].")
    st.markdown("---")

    num_sets = st.number_input(
        "Anzahl der benoetigten Aufgabensaetze:",
        min_value=1,
        max_value=20, # Generous free limits allow up to 20 sets comfortably
        value=3
    )

    if st.button(f"Starte Generierung ({num_sets} Sätze)", type="primary"):
        zip_buffer = BytesIO()

        with st.status("Verbinde mit Groq API (Kostenloser Tarif)...", expanded=True) as status:
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                for i in range(1, int(num_sets) + 1):
                    status.write(f"Set {i}/{num_sets}: Generiere 50 Aufgaben via Llama 3...")
                    
                    # Randomly sample topics to ensure uniqueness in every set
                    sampled_topics = random.choices(SYLLABUS_TOPICS, k=50)
                    problems = generate_problems_with_groq(api_key, sampled_topics, num_problems=50)
                    
                    docx_bytes = create_word_document(problems, i)
                    filename = f"Groq_Set_{i:02d}.docx"
                    zf.writestr(filename, docx_bytes)
                    status.write(f"✅ {filename} fertiggestellt.")
                    
                    # Brief pause to respect rate limits on the free tier
                    time.sleep(2)

            zip_buffer.seek(0)
            status.update(label="Generierung abgeschlossen!", state="complete", expanded=False)

        st.download_button(
            label="Alle Saetze als ZIP-Datei herunterladen",
            data=zip_buffer,
            file_name="Mathe_Kl_5_6_Groq_Free.zip",
            mime="application/zip",
            key="download_zip_groq"
        )

if __name__ == "__main__":
    st.set_page_config(page_title="Free Groq Math Generator")
    main_app()