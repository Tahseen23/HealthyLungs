from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import  ChatPromptTemplate
from langchain.chains import HypotheticalDocumentEmbedder

from chromadb import Client
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv()
import os


def formatDocs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

persist_directory="db"
repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1"
key=os.environ.get('api_key')
model=HuggingFaceEndpoint(repo_id=repo_id,huggingfacehub_api_token=key,add_to_git_credential=True)
embeddings=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
vectorStore=Chroma(persist_directory=persist_directory,embedding_function=embeddings)
retriever=vectorStore.as_retriever()

hyde_embeddings=HypotheticalDocumentEmbedder.from_llm(model,
                                                      embeddings,
                                                      prompt_key="web_search")
template = """
You are a lung cancer specialist. Your job is to provide a roadmap for the surgery and treatment of the patient. Junior doctors have already conducted imaging tests such as a chest CT scan and a PET scan, along with other lung cancer tests, and discussed the symptoms, medical history, and any other relevant information. The stage of lung cancer has already been determined and is provided below.

Your job is to generate a roadmap for how the doctor should proceed with the treatment of this particular patient, given the cancer stage and condition provided and also include potential drawbacks for each treatment. This should include recommendations for physical exercises the patient should do, things the patient needs to avoid, and a complete explanation of each step and potential drawbacks based on the context provided.

Context: {context}

Condition: {condition}

If you think the information provided is not relevant or the condition given to you by the junior doctor is not relevant, simply say, "Please provide correct information." If the patient is already in a normal condition, just simply say, "Don't worry, you are okay!" and don't need to generate a roadmap.
"""


def generateRoadmap(stage,symptoms,time):
    query=""
    if stage=="normal condition nothing to worry":
        query=f"On analysing patient lungs x ray it was found that patient is at {stage}.But Patient is experiencing {symptoms} from the past {time}."
    else:
        query=f"On analysing patient lungs x ray it was found that patient is at {stage} of lungs Cancer.And Patient is also experiencing {symptoms} from the past {time}."
    
    prompt = ChatPromptTemplate.from_template(template)
    rag_chain = (
   {"context": retriever|formatDocs , "condition": RunnablePassthrough()}
   | prompt
   | model
   | StrOutputParser())

    response=rag_chain.invoke(query)
    return response


