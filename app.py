import streamlit as st
from standard_to_alternative import convert_standard_to_alternative
from alternative_to_standard import convert_alternative_to_standard

st.set_page_config(page_title="comversor de orrtografias", layout="wide")

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Underdog&display=swap');

/* =========================
   TÍTULO PRINCIPAL
   Ex.: "comversor de orrtografias"
   ========================= */

h1 {
    font-family: 'Underdog', sans-serif !important;
    font-size: 48px !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}


/* =========================
   SUBTÍTULOS COM SETA
   Ex.: "ofisiau → cucagrafia"
        "cucagrafia → ofisiau"
   ========================= */

h2, h3 {
    font-family: 'Underdog', sans-serif !important;
    font-size: 30px !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}


/* =========================
   TEXTO ABAIXO DO TÍTULO
   Ex.: "comverte da orrtografia..."
   ========================= */

div[data-testid="stMarkdownContainer"] p {
    font-family: 'Underdog', sans-serif !important;
    font-size: 20px !important;
    color: #ffffff !important;
}

/* =========================
   TEXTO GERAL DO APP
   ========================= */

html, body, [class*="css"] {
    font-family: 'Underdog', sans-serif;
}

/* =========================
   INSTRUÇÕES ACIMA DAS CAIXAS
   Ex.: "Escreva aqi como..."
   ========================= */

label[data-testid="stWidgetLabel"] p {
    font-family: 'Underdog', sans-serif;
    font-size: 20px !important;
    color: #e40032 !important;
    font-weight: 700 !important;
}

/* =========================
   BOTÕES
   ========================= */

div.stButton > button {
    font-family: 'Underdog', sans-serif;
    font-size: 20px !important;
    color: #ffffff !important;
    background-color: #000000 !important;
    border: 2px solid #f2c94c !important;
    border-radius: 10px !important;
    padding: 0.65em 1.1em !important;
    font-weight: 700 !important;
}

/* botão quando o mouse passa por cima */
div.stButton > button:hover {
    color: #ffffff !important;
    background-color: #8b1e3f !important;
    border-color: #8b1e3f !important;
}

/* =========================
   TEXTO DENTRO DAS CAIXAS
   quando o usuário digita
   ========================= */

textarea {
    font-family: 'Underdog', sans-serif !important;
    font-size: 22px !important;
    color: #ffffff !important;
    background-color: #24242e !important;
    line-height: 1.5 !important;
}

/* =========================
   TEXTO DENTRO DAS CAIXAS DESATIVADAS
   isto afeta as caixas de resultado
   ========================= */

textarea:disabled {
    font-family: 'Underdog', sans-serif !important;
    font-size: 22px !important;
    color: #e40032 !important;
    -webkit-text-fill-color: #f8f1d8 !important;
    opacity: 1 !important;
    background-color: #24242e !important;
}

/* borda das caixas */
textarea:focus {
    border-color: #f2c94c !important;
    box-shadow: 0 0 0 1px #f2c94c !important;
}
</style>
""")

if "alternative_output" not in st.session_state:
    st.session_state["alternative_output"] = ""

if "standard_output" not in st.session_state:
    st.session_state["standard_output"] = ""

st.title("comversor de orrtografias")
st.write("comverte da orrtografia ofisiau para a limda cucagrafia")

left, right = st.columns(2)

with left:
    st.subheader("ofisiau → cucagrafia")

    standard_input = st.text_area(
        "Escreva aqi como a orrtografia ofisiau manda:",
        height=220,
        key="standard_input"
    )

    if st.button("Fas a majia de converter para cucagrafia", key="btn_standard_to_alternative"):
        st.session_state["alternative_output"] = convert_standard_to_alternative(standard_input)

    st.text_area(
        "aqi o seu testo lindo e convertido:",
        value=st.session_state["alternative_output"],
        height=220,
        disabled=True
    )

with right:
    st.subheader("cucagrafia → ofisiau")

    alternative_input = st.text_area(
        "Escreva aqi de modo cucagrafico ou seja como qizer:",
        height=220,
        key="alternative_input"
    )

    if st.button("Muda pra orrtografia ofisiau (eca...), vai demorar um poco:", key="btn_alternative_to_standard"):
        try:
            st.session_state["standard_output"] = convert_alternative_to_standard(alternative_input)
        except Exception as e:
            st.session_state["standard_output"] = ""
            st.error(f"OpenAI conversion error: {e}")

    st.text_area(
        "aqi seu testo com xero de obediensia:",
        value=st.session_state["standard_output"],
        height=220,
        disabled=True
    )
