import streamlit as st
import random
import time
import json
import re
from datetime import datetime
from groq import Groq, RateLimitError, APIError, NotFoundError, BadRequestError
from docx import Document
from io import BytesIO
import zipfile

# =============================================================================
#  v15 -- Production-Grade AI Math Generator (Groq Free Tier)
#  Multi-Format JSON Parsing & Strict Text-Model Filtering
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

PREFERRED_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "llama3-70b-8192",
    "llama3-8b-8192"
]

# Blacklist patterns to exclude speech, audio, guard, and unsupported vision models
EXCLUDED_MODEL_PATTERNS = ["whisper", "guard", "vision", "safeguard", "orpheus", "canopylabs", "tts", "stt"]

def sanitize_xml_string(text: str) -> str:
    """Removes all characters invalid according to W3C XML 1.0 standard."""
    if not text:
        return ""
    return re.sub(
        r'[^\x09\x0A\x0D\x20-\xD7FF\xE000-\xFFFD\U00010000-\U0010FFFF]',
        '',
        text
    )

@st.cache_data(ttl=1800)
def get_live_fallback_chain(api_key):
    """Interrogates Groq API to verify currently active, valid text models."""
    try:
        client = Groq(api_key=api_key)
        models_page = client.models.list()
        active_api_models = {m.id for m in models_page.data}
        
        valid_chain = [m for m in PREFERRED_MODELS if m in active_api_models]
        
        if not valid_chain:
            # Fall back to active text models while filtering out audio/speech/guard models
            valid_chain = sorted([
                m for m in active_api_models 
                if not any(pattern in m.lower() for pattern in EXCLUDED_MODEL_PATTERNS)
            ])
            
        return valid_chain if valid_chain else PREFERRED_MODELS
    except Exception:
        return PREFERRED_MODELS

def request_groq_batch(client, model_id, topics_sample, expected_count):
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
    
    # Robustly handle both JSON Dicts {"problems": [...]} and JSON Lists [{"problems": [...]}]
    problems = []
    if isinstance(data, dict):
        problems = data.get("problems", [])
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "problems" in item:
                problems.extend(item["problems"])
            elif isinstance(item, str):
                problems.append(item)
    
    cleaned_problems = []
    for p in problems:
        s = str(p).strip()
        if len(s) > 15:
            cleaned_problems.append(sanitize_xml_string(s))
            
    return cleaned_problems

def create_word_document(problems, set_number):
    document = Document()
    document.add_heading(f'Gymnasium Kl. 5 & 6 (Sachsen-Anhalt) - Set {set_number}', 0)
    document.add_paragraph("Dynamische Denkaufgaben mit erhoehtem Schwierigkeitsgrad.")
    document.add_paragraph(f"Erstellt am {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    
    for i, problem in enumerate(problems[:50], 1):
        clean_prob = re.sub(r'^\s*(?:\d+[\.\)]|Aufgabe\s*\d+[:\.]?)\s*', '', problem, flags=re.IGNORECASE).strip()
        safe_prob = sanitize_xml_string(clean_prob)
        document.add_paragraph(f"{i}. {safe_prob}")

    bio = BytesIO()
    document.save(bio)
    bio.seek(0)
    return bio.getvalue()

def login_form():
    try:
        STATIC_USER = st.secrets["auth"]["username"]
        STATIC_PASS = st.secrets["auth"]["password"]
    except KeyError:
        st.error("Konfigurationsfehler: Bitte stellen Sie sicher, dass '.streamlit/secrets.toml' existiert.")
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

    client = Groq(api_key=api_key)
    fallback_chain = get_live_fallback_chain(api_key)

    st.title("🧠 Zero-Cost Mathe-Generator (Production Ready)")
    st.markdown(f"**Aktivierte Modell-Kette:** `{ ' -> '.join(fallback_chain) }`")
    st.markdown("---")

    num_sets = st.number_input("Anzahl der benoetigten Aufgabensaetze:", min_value=1, max_value=20, value=3)

    if st.button(f"Starte Generierung ({num_sets} Sätze)", type="primary"):
        zip_buffer = BytesIO()
        has_fatal_error = False

        with st.status("Verbinde mit Groq Infrastructure...", expanded=True) as status:
            status.write(f"ℹ️ Verifizierte aktive Modelle: `{fallback_chain}`")
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                
                for set_idx in range(1, int(num_sets) + 1):
                    if has_fatal_error: break
                    
                    all_problems_for_set = []
                    batch = 1
                    max_batches = 15
                    active_model_idx = 0 
                    
                    while len(all_problems_for_set) < 50 and batch <= max_batches:
                        needed = 50 - len(all_problems_for_set)
                        ask_count = min(10, needed) 
                        sampled_topics = random.choices(SYLLABUS_TOPICS, k=ask_count)
                        
                        batch_success = False
                        
                        for i in range(active_model_idx, len(fallback_chain)):
                            target_model = fallback_chain[i]
                            
                            try:
                                status.write(f"➡️ **Set {set_idx}/{num_sets}:** Lade Batch {batch}/{max_batches} via `{target_model}`...")
                                batch_problems = request_groq_batch(client, target_model, sampled_topics, ask_count)
                                
                                if batch_problems:
                                    all_problems_for_set.extend(batch_problems)
                                    active_model_idx = i 
                                    batch_success = True
                                    break
                                
                            except (RateLimitError, BadRequestError, NotFoundError) as err:
                                status.warning(f"⚠️ Modell `{target_model}` meldet Limit oder ist ungeeignet ({type(err).__name__}). Wechsele zum Fallback...")
                                time.sleep(4)
                                continue
                            except APIError as e:
                                status.error(f"❌ API-Fehler ({target_model}): {str(e)}")
                                has_fatal_error = True
                                break
                            except Exception as e:
                                status.error(f"❌ Unerwarteter Fehler ({target_model}): {str(e)}")
                                has_fatal_error = True
                                break
                        
                        if has_fatal_error: break
                        
                        if not batch_success:
                            status.error("❌ Alle verfügbaren Fallback-Modelle sind momentan ausgelastet.")
                            has_fatal_error = True
                            break
                        
                        batch += 1
                        time.sleep(3)
                    
                    if not has_fatal_error:
                        docx_bytes = create_word_document(all_problems_for_set, set_idx)
                        filename = f"Set_{set_idx:02d}_Groq_AutoFallback.docx"
                        zf.writestr(filename, docx_bytes)
                        status.write(f"✅ {filename} gesichert.")
                        time.sleep(3)

            zip_buffer.seek(0)
            if has_fatal_error:
                status.update(label="Generierung abgebrochen.", state="error", expanded=True)
            else:
                status.update(label="Alle Sätze erfolgreich generiert!", state="complete", expanded=False)

        if not has_fatal_error:
            st.download_button(
                label="Alle Saetze als ZIP-Datei herunterladen",
                data=zip_buffer,
                file_name="Mathe_Kl_5_6_Dynamic.zip",
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