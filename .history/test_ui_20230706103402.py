import streamlit as st

genre = st.radio(
                    "Have you reviewed article?",
                    ('Publish', 'Abort'))
if genre == 'Publish':
button_style = "color: green"
else:
if st.button("Green Button", style=button_style):
    st.write("Button clicked!")