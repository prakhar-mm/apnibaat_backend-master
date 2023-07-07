import streamlit as st

genre = st.radio(
                    "Have you reviewed article?",
                    ('Publish', 'Abort'))
if genre == 'Publish':
    button_label = ":green[Publish]"
else:
    button_label = ":green[Abort]"

button_clicked = st.button(button_label)
if st.button(button_label):
    st.write("Button clicked!")