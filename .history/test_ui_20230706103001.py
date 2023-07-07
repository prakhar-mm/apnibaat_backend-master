import streamlit as st

button_style = "color: green"

if st.button("Green Button", style=button_style):
    st.write("Button clicked!")