import streamlit as st
import random
import time
import json
import re
from datetime import datetime
from groq import Groq
from docx import Document
from io import BytesIO
import zipfile

# =============================================================================
#  v14 -- Zero-Cost AI Math Generator (Groq Free Tier Optimized)
#  Dynamic Model Fetching + Regex Text Cleaning + Failsafes
# =============================================================================

SYLLABUS_TOPICS = [
    "Schriftliche Addition/Subtraktion grosser Zahlen", "Schriftliche Multiplikation und Division",
    "Mehrstufiges Rechnen mit Klammern und Potenzen", "Runden grosser Zahlen und Dezimalzahlen",
    "Brueche: Addieren, Subtrahieren, Multiplizieren, Dividieren", "Bruch/Dezimal Umwandlung", 
    "Prozentrechnung (Anteil, Gesamtwert)", "ggT, kgV, Primfaktorzerlegung",
    "Umrechnungen: Laenge, Gewicht, Volumen, Zeit", "Zeitrechnung als Textaufgabe",
    "Umfang und Flaeche von Rechtecken und Dreiecken", "Zusammengesetzte Figuren (L-Form, T-Form)",
    "Volumen und Oberflaeche von Wuerfel und Quader", "Symmetrieachsen und Punktspiegelung",
    "Mittelwert, Median, Spannweite", "Wahrscheinlichkeit (Wuerfel, Kugeln)",
    "Ganze Zahlen: alle Grundrechenarten", "Potenzen und Wurzeln (Quadrat, Kubik)",
    "Terme vereinfachen und berechnen durch Einsetzen", "Lineare Gleichungen mit Klammern",
    "Proportionalitaet (direkt/umgekehrt) und Dreisatz", "Massstab und Umrechnung",
    "Pythagoras (Hypotenuse, Kathete, Textaufgaben)", "Kreis (Umfang, Flaeche, Kreisring)",
    "Flaeche von Trapez", "Volumen/Oberflaeche von Zylinder und Prisma",
    "Kongruenzkriterien und aehnliche Figuren", "Koordinatensystem (Spiegeln, Abstand)",
    "Lineare Funktionen (Steigung, Nullstelle)", "Wahrscheinlichkeit (Urnenmodell, Baumdiagramm)"
]

@st.cache_data(ttl=3600)
def get_available_models(api_key):
    """Fetches the live list of active models available to this API key."""
    try:
        client = Groq(api_key=api_key)
        models = client.models.list()
        # Filter for likely text models (excluding whisper/audio if present)
        return sorted([m.id for m in models.data if "whisper" not in m.id])
    except Exception as e:
        st.error(f"Fehler beim Laden der Modelle: {e}")
        return []

def generate_problems_with_groq_json(api_key, model_id, topics_sample, expected_count):
    client = Groq(api_key=api_key)
    topics_list_str = "\n".join([f"- {topic}" for topic in topics_sample])
    
    system_prompt = (
        "Du bist ein anspruchsvoller Mathematik-Lehrer an einem Gymnasium in Sachsen-Anhalt. "
        "Du gibst deine Antworten ausschließlich im validen JSON-Format aus."
    )
    
    user_prompt = f"""
    Erstelle exakt {expected_count} einzigartige, schwere Denkaufgaben.
    Nutze dafür diese Lehrplanthemen:
    {topics_list_str}

    WICHTIG: Gib das Ergebnis AUSSCHLIESSLICH als JSON-Objekt mit einem einzigen Schlüssel "problems" zurück, der ein Array von Strings enthält.
    Beispiel:
    {{
      "problems": [
        "Aufgabe 1 Text...",
        "Aufgabe 2 Text..."
      ]
    }}
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model=model_id, 
            temperature=0.7,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        problems = data.get("problems", [])
        
        return [str(p).strip() for p in problems if len(str(p).strip()) > 15]
    
    except Exception as e:
        return [f"API-Fehler: {str(e)}"]

def create_word_document(problems, set_number):
    document = Document()
    document.add_heading(f'Gymnasium Kl. 5 & 6 (Sachsen-Anhalt) - Set {set_number}', 0)
    document.add_paragraph("Dynamische Denkaufgaben mit erhoehtem Schwierigkeitsgrad.")
    document.add_paragraph(f"Erstellt am {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    
    for i, problem in enumerate(problems[:50], 1):
        clean_prob = re.sub(r'^(\d+[\.\-)]?\s*|Aufgabe\s*\d*:?\s*)+', '', problem).strip()
        document.add_paragraph(f"{i}. {clean_prob}")

    bio = BytesIO()
    document.save(bio)
    bio.seek(0)
    return bio.getvalue()

def login_form():
    try:
        STATIC_USER = st.secrets["auth"]["username"]
        STATIC_PASS = st.secrets["auth"]["password"]
    except KeyError:
        st.error("Konfigurationsfehler: Bitte stellen Sie sicher, dass '.streamlit/secrets.toml' die Sektion [auth] enthält.")
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
    api_key = None
    if "groq" in st.secrets and "api_key" in st.secrets["groq"]:
        api_key = st.secrets["groq"]["api_key"]
    else:
        st.error("Groq API Key fehlt. Bitte in .streamlit/secrets.toml eintragen.")
        return

    st.title("🧠 Zero-Cost Mathe-Generator (Groq)")
    st.markdown("Generiert 50 Aufgaben pro Set – 100% kostenlos.")
    st.markdown("---")

    # Dynamically fetch models to prevent deprecation errors
    available_models = get_available_models(api_key)
    if not available_models:
        st.error("Konnte keine Modelle von Groq abrufen. Bitte API-Key prüfen.")
        return

    selected_model = st.selectbox(
        "Wählen Sie ein aktives Groq-Modell aus:",
        options=available_models,
        help="Diese Liste wird live von Groq geladen. Alle hier angezeigten Modelle sind aktiv."
    )

    num_sets = st.number_input("Anzahl der benoetigten Aufgabensaetze:", min_value=1, max_value=10, value=1)

    if st.button(f"Starte Generierung ({num_sets} Sätze)", type="primary"):
        zip_buffer = BytesIO()
        has_fatal_error = False

        with st.status(f"Verbinde mit Groq API ({selected_model})...", expanded=True) as status:
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                
                for set_idx in range(1, int(num_sets) + 1):
                    if has_fatal_error: break
                    
                    all_problems_for_set = []
                    batch = 1
                    max_batches = 15 
                    
                    while len(all_problems_for_set) < 50 and batch <= max_batches:
                        needed = 50 - len(all_problems_for_set)
                        ask_count = min(10, needed) 
                        
                        status.write(f"➡️ **Set {set_idx}/{num_sets}:** Lade Batch {batch}/{max_batches} (Bisher {len(all_problems_for_set)}/50 Aufgaben)...")
                        
                        sampled_topics = random.choices(SYLLABUS_TOPICS, k=ask_count)
                        batch_problems = generate_problems_with_groq_json(api_key, selected_model, sampled_topics, expected_count=ask_count)
                        
                        if batch_problems and batch_problems[0].startswith("API-Fehler"):
                            status.error(f"❌ Kritischer Fehler: {batch_problems[0]}")
                            has_fatal_error = True
                            break
                        
                        all_problems_for_set.extend(batch_problems)
                        batch += 1
                        time.sleep(4) 
                    
                    if not has_fatal_error:
                        if len(all_problems_for_set) < 50:
                            status.warning(f"⚠️ Set {set_idx} unvollständig ({len(all_problems_for_set)}/50).")
                            
                        docx_bytes = create_word_document(all_problems_for_set, set_idx)
                        filename = f"Groq_Set_{set_idx:02d}.docx"
                        zf.writestr(filename, docx_bytes)
                        status.write(f"✅ {filename} fertiggestellt.")
                        time.sleep(5)

            zip_buffer.seek(0)
            if has_fatal_error:
                status.update(label="Generierung wegen API-Fehler abgebrochen.", state="error", expanded=True)
            else:
                status.update(label="Generierung abgeschlossen!", state="complete", expanded=False)

        if not has_fatal_error:
            st.download_button(
                label="Alle Saetze als ZIP-Datei herunterladen",
                data=zip_buffer,
                file_name="Mathe_Kl_5_6_Groq.zip",
                mime="application/zip",
                key="download_zip_groq"
            )

if __name__ == "__main__":
    st.set_page_config(page_title="Free Groq Math Generator")
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        main_app()
    else:
        login_form()