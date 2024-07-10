import streamlit as st
from pdf import generatePdf
from llm import generateRoadmap
from model import processPredict
import base64
st.title("Healthy Lungs-Evergreen")

def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


name=st.sidebar.text_input("Enter patient name")
with st.sidebar:
    age=st.text_input("Enter patient age")
    gender=st.text_input("Enter patient gender")
    image=st.file_uploader("Upload Xray of lungs", type=["jpg","jpeg","png"],accept_multiple_files=False)
    symptoms=st.text_input("Enter patient symptoms")
    time=st.text_input("For how days/weeks/month")
    date=st.text_input("Enter the date")
    button=st.button("Generate PDF")




if button:
    text,_=processPredict(image)
    print(text)
    image.seek(0)
    llmOutput=generateRoadmap(text,symptoms,time)
    # st.write(llmOutput)
    generatePdf(name,age,gender,image.read(),symptoms,time,llmOutput)
    show_pdf('hello.pdf')
    print("Done")
    


