import streamlit as st
from groq import Groq
import PyPDF2
from docx import Document
import tempfile

# -----------------------
# Utility: Extract text
# -----------------------

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


# -----------------------
# Streamlit App UI
# -----------------------

st.set_page_config(page_title="Syllabus → Math Questions Generator", layout="wide")
st.title("📘 Grade 5 Math Question Generator (Sachsen-Anhalt)")

st.write("""
Upload the **official syllabus** (PDF or DOCX).  
This app extracts the syllabus content and generates **50 difficult math questions** based on all topics.
""")

uploaded_file = st.file_uploader("Upload syllabus PDF or DOCX", type=["pdf", "docx"])

# -----------------------
# Load API key from secrets
# -----------------------

if "groq" not in st.secrets or "api_key" not in st.secrets["groq"]:
    st.error("❌ GROQ API key missing in .streamlit/secrets.toml under [groq] section.")
    st.stop()

API_KEY = st.secrets["groq"]["api_key"]
client = Groq(api_key=API_KEY)

syllabus_text = ""

# -----------------------
# File Processing
# -----------------------

if uploaded_file:
    filetype = uploaded_file.name.split(".")[-1].lower()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    if filetype == "pdf":
        st.info("Extracting text from PDF…")
        try:
            syllabus_text = extract_text_from_pdf(tmp_path)
        except Exception as e:
            st.error(f"Failed to extract PDF: {e}")

    elif filetype == "docx":
        st.info("Extracting text from DOCX…")
        try:
            syllabus_text = extract_text_from_docx(tmp_path)
        except Exception as e:
            st.error(f"Failed to extract DOCX: {e}")

    else:
        st.error("Unsupported file type.")


# -----------------------
# Show Preview + Generate Questions
# -----------------------

if syllabus_text:
    st.subheader("📄 Extracted Syllabus Text (Preview)")
    st.text_area("", syllabus_text[:4000], height=300)

    st.subheader("🧠 Generate 50 Tough Math Questions")

    if st.button("Generate Questions"):
        with st.spinner("Generating 50 challenging questions with Groq…"):
            prompt = f"""
            You are an expert mathematics teacher.

            Based on the following **grade 5 Gymnasium syllabus for Sachsen-Anhalt**, 
            generate **exactly 50 very challenging math questions**.

            Requirements:
            - Cover *every* topic mentioned in the syllabus.
            - Use a variety of question forms: word problems, multi-step reasoning,
              geometry, number theory, fractions, arithmetic, logic puzzles,
              real-world applications.
            - Difficulty should be high for 5th grade.
            - Do NOT include solutions.
            - Number each question 1–50 clearly.

            Syllabus content:
            {syllabus_text}
            """

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )

            questions = response.choices[0].message.content

            st.success("Done! 🎉")

            st.subheader("📝 50 Tough Math Questions")
            st.write(questions)

            st.download_button(
                label="📥 Download Questions (TXT)",
                data=questions,
                file_name="math_questions.txt",
                mime="text/plain"
            )
