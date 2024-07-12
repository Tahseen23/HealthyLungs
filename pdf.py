from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import lightblue, black,green , lightgreen,white
from PIL import Image
from database import uploadData,getPdf
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
import datetime
from pdf2docx import Converter
from docx2pdf import convert 
import uuid
import io


def addText(pdf,x,y,color,fontSize,text):
    pdf.setFillColor(color)
    pdf.setFont("Times-Roman", fontSize)
    pdf.drawString(x, y, text)
def addText2(pdf,x,y,color,fontSize,text,text2):
    pdf.setFillColor(color)
    pdf.setFont("Times-Roman", fontSize)
    pdf.drawString(x, y, f"{text}:{text2}")
def generatePdf(patientId,name,age,gender,image,symptoms,time,llmOutput):
    buffer = io.BytesIO()
    pdf=Canvas(buffer)
    # pdf=Canvas("hello.pdf")
    addText(pdf,170,815,green,30,"Evergreen Hospital")
    addText(pdf,20,780,green,15,"PhoneNo-xxxxxxxxxxx")
    addText(pdf,430,780,green,15,"Address-Mumbai,India")
    pdf.line(0,760,800,760)
    addText2(pdf,20,730,black,15,"Name",name)
    addText2(pdf,190,730,black,15,"Age",str(age))
    addText2(pdf,330,730,black,15,"Sex",gender)
    addText2(pdf,440,730,black,15,"Date",time)
    image_obj = ImageReader(io.BytesIO(image))
    pdf.drawImage(image_obj,215,550,width=5*cm,height=5*cm)
    addText2(pdf,20,500,black,15,"Symptoms",symptoms)
    addText(pdf,20,450,black,15,"Roadmap")
    addText2(pdf,90,450,black,15,"Date",str(datetime.date.today()))
    p1=Paragraph(llmOutput)
    p1.wrapOn(pdf,500,100)
    p1.drawOn(pdf,20,190)
    pdf.save()
    buffer.seek(0)
    uploadData(patientId,name,age,gender,buffer,time)
    pdfFile=getPdf(f"evergreen{patientId}.pdf")
    return pdfFile
    # buffer.seek(0)

    










