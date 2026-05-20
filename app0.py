import streamlit as st
from standard_to_alternative import convert_standard_to_alternative
from alternative_to_standard import convert_alternative_to_standard

st.set_page_config(page_title="comversor de orrtografias", layout="wide")

st.title("comversor de orrtografias")
st.write("comverte da orrtografia ofisiau para a linda cucagrafia")

left, right = st.columns(2)

with left:
    st.subheader("ofisiau → cucagrafia")
    standard_input = st.text_area(
        "Escreva aqi como a orrtografia ofisiau manda:",
        height=220,
        key="standard_input"
    )

    if st.button("Fas a majia de converter para cucagrafia"):
        st.session_state["alternative_output"] = convert_standard_to_alternative(standard_input)

    st.text_area(
        "aqi o seu testo lindo e convertido:",
        value=st.session_state.get("alternative_output", ""),
        height=220,
        key="alternative_output_box"
    )

with right:
    st.subheader("cucagrafia → ofisiau")
    alternative_input = st.text_area(
        "Escreva aqi de modo cucagrafico ou seja como qizer:",
        height=220,
        key="alternative_input"
    )

    if st.button("Muda pra orrtografia ofisiau (eca...), , vai demorar um poco:"):
        try:
            st.session_state["standard_output"] = convert_alternative_to_standard(alternative_input)
        except Exception as e:
            st.session_state["standard_output"] = ""
            st.error(f"OpenAI conversion error: {e}")

    st.text_area(
        "aqi seu testo com xero de obediensia:",
        value=st.session_state.get("standard_output", ""),
        height=220,
        key="standard_output_box"
    )
