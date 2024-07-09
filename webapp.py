import streamlit as st
st.title("Healthy Lungs-Evergreen")


name=st.sidebar.text_input("Enter patient name")
with st.sidebar:
    age=st.text_input("Enter patient age")
    gender=st.text_input("Enter patient gender")
    image=st.file_uploader("Upload Xray of lungs", type=["jpg","jpeg","png"],accept_multiple_files=False)
    symptoms=st.text_input("Enter patient symptoms")
    time=st.text_input("For how days/weeks/month")
    st.button("Generate PDF")


