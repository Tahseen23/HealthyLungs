import firebase_admin
from firebase_admin import credentials,firestore,storage
import io

if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\hp\Downloads\lungcancer-9139e-firebase-adminsdk-y2opt-396ea4bafe.json")
    firebase_admin.initialize_app(cred,{'storageBucket':'lungcancer-9139e.appspot.com'})
db=firestore.client()


def uploadData(patientId,patientName,age,gender,pdf,date):
    bucket=storage.bucket()
    data={
        'patientName':patientName,
        'age':age,
        'gender':gender,
        'date':date
    }
    docRef=db.collection("lungsCollection").document(str(patientId))
    docRef.set(data)
    blob=bucket.blob(f"evergreen{patientId}.pdf")
    blob.upload_from_file(pdf,content_type='application/pdf') 

def getPdf(filePath):
    bucket=storage.bucket()
    blob = bucket.blob(filePath)
    pdf_bytes = blob.download_as_bytes()
    pdf_stream = io.BytesIO(pdf_bytes)
    return pdf_stream



def get_document(collectionName,documentID):
    docRef=db.collection(collectionName).document(documentID)
    doc=docRef.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return "Not Found"
# print(get_document("lungsCollection","2"))