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
#  v15 -- Production-Grade AI Math Generator (Groq Free Tier Optimized)
#  Multi-Tier Rate-Limit Protection, Live Endpoint Verification & Safe Parsing
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

# Primary models ordered by reasoning performance and active deployment status
PRIMARY_FALLBACK_CHAIN = [
    "openai/gpt-oss-120b",  # Flagship open-weight reasoning model
    "openai/gpt-oss-20b",   # High-speed fallback
    "qwen/qwen3.8-27b"      # Alternative preview route
]

@st.cache_data(ttl=1800)
def get_verified_fallback_chain(api_key):
    """
    Interrogates the Groq API for currently active models and filters 
    the fallback chain against live endpoints.
    """
    try:
        client = Groq(api_key=api_key)
        live_models = {m.id for m in client.models.list().data}
        valid_chain = [m for m in PRIMARY_FALLBACK_CHAIN if m in live_models]
        
        # If primary choices are missing, use available text models
        if not valid_chain:
            valid_chain = sorted([m for m in live_models if "whisper" not in m and "guard" not in m])
        return valid_chain
    except Exception:
        return PRIMARY_FALLBACK_CHAIN

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
    problems = data.get("problems", [])
    
    return [str(p).strip() for p in problems if len(str(p).strip()) > 15]

def create_word_document(problems, set_number):
    document = Document()
    document.add_heading(f'Gymnasium Kl. 5 & 6 (Sachsen-Anhalt) - Set {set_number}', 0)
    document.add_paragraph("Dynamische Denkaufgaben mit erhoehtem Schwierigkeitsgrad.")
    document.add_paragraph(f"Erstellt am {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    
    for i, problem in enumerate(problems[:50], 1):
        # Precise prefix stripping that prevents removing leading math figures
        clean_prob = re.sub(r'^\s*(?:\d+[\.\)]|Aufgabe\s*\d*[:\.]?)\s*', '', problem, flags=re.IGNORECASE).strip()
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
        st.error("Konfigurationsfehler: '.streamlit/secrets.toml' prüfen.")
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
    fallback_chain = get_verified_fallback_chain(api_key)

    st.title("🧠 Zero-Cost Mathe-Generator (Production Ready)")
    st.markdown("Generiert 50 Aufgaben pro Set. Dynamic Fallback aktiv.")
    st.markdown("---")

    num_sets = st.number_input("Anzahl der benoetigten Aufgabensaetze:", min_value=1, max_value=20, value=3)

    if st.button(f"Starte Generierung ({num_sets} Sätze)", type="primary"):
        zip_buffer = BytesIO()
        has_fatal_error = False

        with st.status("Verbinde mit Groq Infrastructure...", expanded=True) as status:
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                
                for set_idx in range(1, int(num_sets) + 1):
                    if has_fatal_error: break
                    
                    all_problems_for_set = []
                    batch = 1
                    max_batches = 15
                    active_model_idx = 0 # Reset to top reasoning model for each new set
                    
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
                                
                            except (RateLimitError, BadRequestError, NotFoundError) as e:
                                status.warning(f"⚠️ `{target_model}` nicht verfügbar oder Limit erreicht. Wechsele zum Fallback...")
                                time.sleep(2)
                                continue
                            except APIError as e:
                                status.error(f"❌ Schwerer API-Fehler ({target_model}): {str(e)}")
                                has_fatal_error = True
                                break
                            except Exception as e:
                                status.error(f"❌ Unerwarteter Fehler: {str(e)}")
                                has_fatal_error = True
                                break
                        
                        if has_fatal_error: break
                        
                        if not batch_success:
                            status.error("❌ Alle verfügbaren Fallback-Modelle sind ausgelastet. Bitte später versuchen.")
                            has_fatal_error = True
                            break
                        
                        batch += 1
                        time.sleep(3) # Safe delay between micro-batches
                    
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