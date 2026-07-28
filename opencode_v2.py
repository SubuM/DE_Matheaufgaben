"""
Matheaufgaben Generator -- Streamlit Frontend
Gymnasium Klassen 5 & 6 (Sachsen-Anhalt)

Generiert schwere Mathematikaufgaben als Word-Dokumente im ZIP-Archiv.
Optionen: Klasse 5, Klasse 6, oder beide; 1-10 Saetze a 50 Aufgaben.
"""

import streamlit as st
import random
import time
from docx import Document
from docx.shared import Pt
from io import BytesIO
import zipfile
from datetime import datetime

# Generatoren aus opencode_v1 importieren
from opencode_v1 import (
    GENERATORS_KL5, GENERATORS_KL6,
    create_problem_set, create_word_document,
)


# =============================================================================
# Streamlit UI
# =============================================================================

def login_form():
    """Login-Formular mit Secrets."""
    try:
        STATIC_USER = st.secrets["auth"]["username"]
        STATIC_PASS = st.secrets["auth"]["password"]
    except KeyError:
        st.error(
            "Konfigurationsfehler: Bitte stellen Sie sicher, dass die Datei "
            "'.streamlit/secrets.toml' mit der Sektion [auth] existiert."
        )
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
    """Hauptanwendung nach erfolgreichem Login."""
    st.title("Matheaufgaben Generator -- Gymnasium Klasse 5 & 6")
    st.markdown(
        "Schwere Uebungsaufgaben basierend auf dem **Fachlehrplan Mathematik "
        "Gymnasium Sachsen-Anhalt** (Fassung 01.08.2022)."
    )
    st.markdown("---")

    # ---- Sidebar: Einstellungen ----
    st.sidebar.header("Einstellungen")

    klasse = st.sidebar.radio(
        "Klasse auswaehlen:",
        options=["Klasse 5", "Klasse 6", "Beide Klassen"],
        index=0,
        help="Waehlen Sie, fuer welche Klasse(n) Aufgaben generiert werden sollen."
    )

    st.sidebar.markdown("---")

    num_sets_kl5 = 0
    num_sets_kl6 = 0

    if klasse in ("Klasse 5", "Beide Klassen"):
        num_sets_kl5 = st.sidebar.number_input(
            "Sets Klasse 5 (1-10):",
            min_value=1,
            max_value=10,
            value=3,
            help="Anzahl der Aufgabensetze fuer Klasse 5 (je 50 Aufgaben)."
        )

    if klasse in ("Klasse 6", "Beide Klassen"):
        num_sets_kl6 = st.sidebar.number_input(
            "Sets Klasse 6 (1-10):",
            min_value=1,
            max_value=10,
            value=3,
            help="Anzahl der Aufgabensetze fuer Klasse 6 (je 50 Aufgaben)."
        )

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        f"**Generatoren:**  \n"
        f"- Klasse 5: {len(GENERATORS_KL5)} Themen  \n"
        f"- Klasse 6: {len(GENERATORS_KL6)} Themen"
    )

    # ---- Vorschau ----
    st.subheader("Vorschau")
    preview_gen = st.selectbox(
        "Beispielaufgabe auswaehlen zum Anzeigen:",
        options=["Klasse 5", "Klasse 6"],
        index=0,
    )
    if st.button("Zufaellige Aufgabe anzeigen", key="preview"):
        gens = GENERATORS_KL5 if preview_gen == "Klasse 5" else GENERATORS_KL6
        gen = random.choice(gens)
        st.info(gen())

    st.markdown("---")

    # ---- Generierung ----
    total = num_sets_kl5 + num_sets_kl6

    if klasse == "Klasse 5":
        summary = f"**Klasse 5:** {num_sets_kl5} Set(s) a 50 Aufgaben = **{num_sets_kl5 * 50} Aufgaben**"
    elif klasse == "Klasse 6":
        summary = f"**Klasse 6:** {num_sets_kl6} Set(s) a 50 Aufgaben = **{num_sets_kl6 * 50} Aufgaben**"
    else:
        summary = (
            f"**Klasse 5:** {num_sets_kl5} Set(s) a 50 Aufgaben = **{num_sets_kl5 * 50} Aufgaben**  \n"
            f"**Klasse 6:** {num_sets_kl6} Set(s) a 50 Aufgaben = **{num_sets_kl6 * 50} Aufgaben**  \n"
            f"**Gesamt: {total} Set(s) = {total * 50} Aufgaben**"
        )

    st.markdown(summary)

    if st.button(f"Generiere {total} Aufgabensetze und erstelle ZIP", type="primary"):

        zip_buffers = {}

        with st.status("Generiere Aufgaben...", expanded=True) as status:

            # --- Klasse 5 ---
            if num_sets_kl5 > 0:
                buf5 = BytesIO()
                status.write(f"Klasse 5: Erstelle {num_sets_kl5} Set(s)...")
                with zipfile.ZipFile(buf5, 'w', zipfile.ZIP_DEFLATED) as zf5:
                    for i in range(1, num_sets_kl5 + 1):
                        problems = create_problem_set(GENERATORS_KL5, 50)
                        title = (
                            f"Schwere Mathematikaufgaben -- Gymnasium Klasse 5 "
                            f"(Sachsen-Anhalt) -- Set {i}"
                        )
                        subtitle = (
                            f"Aufgabensatz {i} von {num_sets_kl5} | "
                            f"{len(problems)} Aufgaben | "
                            f"Erstellt am {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                        )
                        docx_bytes = create_word_document(problems, title, subtitle)
                        filename = f"Klasse_5_Set_{i:02d}.docx"
                        zf5.writestr(filename, docx_bytes)
                        status.write(f"  [OK] {filename} ({len(problems)} Aufgaben)")
                buf5.seek(0)
                zip_buffers["Klasse_5"] = buf5

            # --- Klasse 6 ---
            if num_sets_kl6 > 0:
                buf6 = BytesIO()
                status.write(f"Klasse 6: Erstelle {num_sets_kl6} Set(s)...")
                with zipfile.ZipFile(buf6, 'w', zipfile.ZIP_DEFLATED) as zf6:
                    for i in range(1, num_sets_kl6 + 1):
                        problems = create_problem_set(GENERATORS_KL6, 50)
                        title = (
                            f"Schwere Mathematikaufgaben -- Gymnasium Klasse 6 "
                            f"(Sachsen-Anhalt) -- Set {i}"
                        )
                        subtitle = (
                            f"Aufgabensatz {i} von {num_sets_kl6} | "
                            f"{len(problems)} Aufgaben | "
                            f"Erstellt am {datetime.now().strftime('%d.%m.%Y %H:%M')}"
                        )
                        docx_bytes = create_word_document(problems, title, subtitle)
                        filename = f"Klasse_6_Set_{i:02d}.docx"
                        zf6.writestr(filename, docx_bytes)
                        status.write(f"  [OK] {filename} ({len(problems)} Aufgaben)")
                buf6.seek(0)
                zip_buffers["Klasse_6"] = buf6

            status.update(
                label=f"Fertig! {total} Aufgabensaeetze sind bereit.",
                state="complete",
                expanded=False,
            )

        st.markdown("---")

        # ---- Downloads ----
        if "Klasse_5" in zip_buffers:
            st.download_button(
                label=f"Klasse 5 herunterladen ({num_sets_kl5} Sets, {num_sets_kl5 * 50} Aufgaben)",
                data=zip_buffers["Klasse_5"],
                file_name=f"Matheaufgaben_Klasse_5_SCHWER.zip",
                mime="application/zip",
                key="dl_kl5",
            )

        if "Klasse_6" in zip_buffers:
            st.download_button(
                label=f"Klasse 6 herunterladen ({num_sets_kl6} Sets, {num_sets_kl6 * 50} Aufgaben)",
                data=zip_buffers["Klasse_6"],
                file_name=f"Matheaufgaben_Klasse_6_SCHWER.zip",
                mime="application/zip",
                key="dl_kl6",
            )


# =============================================================================
# Hauptprogramm
# =============================================================================

if __name__ == "__main__":
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        main_app()
    else:
        login_form()
