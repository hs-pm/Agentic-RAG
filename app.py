code = '''
import streamlit as st

st.title("My Awesome App 🚀")
st.write("This app is deployed on Streamlit Cloud!")
'''

# Save it as app.py
with open("app.py", "w") as f:
    f.write(code)
