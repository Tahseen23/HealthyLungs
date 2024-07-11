import streamlit as st
from pdf import generatePdf
# from llm import generateRoadmap
from model import processPredict,drawRectangle
import base64
st.title("Healthy Lungs-Evergreen")


def show_pdf(file_stream):
    base64_pdf = base64.b64encode(file_stream.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


name=st.sidebar.text_input("Enter patient name")
with st.sidebar:
    patientId=st.text_input("Enter Patient Id")
    age=st.text_input("Enter patient age")
    gender=st.text_input("Enter patient gender")
    image=st.file_uploader("Upload Xray of lungs", type=["jpg","jpeg","png"],accept_multiple_files=False)
    symptoms=st.text_input("Enter patient symptoms")
    time=st.text_input("For how many days/weeks/month")
    date=st.text_input("Enter the date")
    button=st.button("Generate PDF")




if button:
    text,rectangle=processPredict(image)
    img=drawRectangle(rectangle,image)
    # llmOutput=generateRoadmap(text,symptoms,time)
    pdfFile=generatePdf(patientId,name,age,gender,img.read(),symptoms,date,"llmOutput")
    show_pdf(pdfFile)
    print("Done")
    


