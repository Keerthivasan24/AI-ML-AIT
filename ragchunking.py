from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

document = """
LangChain is a framework for developing applications powered by language models. 
It helps developers build context-aware and reasoning-capable LLM apps. 
LangChain has components for prompt templates, chains, agents, tools, memory, and more.
"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,     
    chunk_overlap=30   
)
chunks = splitter.create_documents([document])


embeddings = OpenAIEmbeddings(openai_api_key="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")
db = FAISS.from_documents(chunks, embeddings)


retriever = db.as_retriever()


qa = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=retriever,
    return_source_documents=True
)


query = "What does LangChain help developers build?"
result = qa({"query": query})


print("Answer:", result["result"])
print("\nRelevant Chunk(s):")
for doc in result["source_documents"]:
    print("-", doc.page_content)
