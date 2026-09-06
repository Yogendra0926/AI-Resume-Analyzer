import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
def load_resume(file_path):
    loader=PyPDFLoader(file_path)
    docs=loader.load()
    return docs
def split_text(docs):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.split_documents(docs)
def analyze_resume(chunks):
    llm=ChatOllama(
        model="qwen3:4b"
    )
    prompt=ChatPromptTemplate.from_template(
        """
        You are an expert HR Recruiter.
        Analyze the following resume and provide:
        1. key skills
        2. strengths
        3. weakness
        4. suggestions and improvements
        5. Job roles best suited
        6. Resume Score out of 10
        Resume:
        {text}
        """ 
    )
    chain=prompt | llm
    full_text="\n".join([doc.page_content for doc in chunks])
    response=chain.invoke({"text":full_text})
    return response.content
# # main
# file_path="Yogendra Jain CV.pdf"
# docs=load_resume(file_path)
# chunks=split_text(docs)
# result=analyze_resume(chunks)
# print("="*60)
# print("AI RESUME ANALYSIS")
# print("="*60)
# print(result)