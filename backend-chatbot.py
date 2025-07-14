from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain.text_splitter import TokenTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from PyPDF2 import PdfReader
import io
import os


GROQ_API_KEY = "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"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DB_PATH = "../data/faiss"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            return JSONResponse(status_code=400, content={"error": "Only PDF files are supported"})

        pdf_bytes = await file.read()
        pdf_stream = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_stream)

        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        if not text.strip():
            return JSONResponse(status_code=400, content={"error": "No extractable text found in PDF"})

        splitter = TokenTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        chunks = splitter.split_text(text)

        if not chunks:
            return JSONResponse(status_code=400, content={"error": "Text could not be chunked"})

        embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
        documents = [Document(page_content=chunk) for chunk in chunks]
        vectordb = FAISS.from_documents(documents, embedding_model)
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        vectordb.save_local(VECTOR_DB_PATH)

        return {
            "status": "success",
            "message": "PDF content extracted and embedded successfully",
            "chunks_stored": len(chunks)
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_vectorstore(request: QueryRequest):
    try:
        embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
        vectordb = FAISS.load_local(VECTOR_DB_PATH, embedding_model, allow_dangerous_deserialization=True)

        retriever = vectordb.as_retriever()
        docs = retriever.get_relevant_documents(request.question)

        context = "\n\n".join(doc.page_content for doc in docs[:3])
        prompt = f"Context:\n{context}\n\nQuestion: {request.question}\nAnswer:"

        llm = ChatGroq(api_key=GROQ_API_KEY, model_name="llama3-8b-8192")
        response = llm.invoke(prompt)

        return {
            "question": request.question,
            "answer": response.content.strip(),
            "context_snippets": [doc.page_content[:200] for doc in docs]
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
