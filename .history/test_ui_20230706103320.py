import streamlit as st

genre = st.radio(
                    "Have you reviewed article?",
                    ('Publish', 'Abort'))
button_style = "color: green"

if st.button("Green Button", style=button_style):
    st.write("Button clicked!")