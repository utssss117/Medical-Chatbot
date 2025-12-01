from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Download HuggingFace Embeddings
embeddings = download_hugging_face_embeddings()

# Connect to existing Pinecone vector index
index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Create retriever
retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# Chat model (GPT-4o or GPT-4o-mini)
chatModel = ChatOpenAI(model="gpt-4o-mini")  # use mini to avoid quota issues

# Define prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}")
    ]
)

# ---- Modern LangChain RAG Pipeline (NO deprecated functions) ---- #

rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()} 
    | prompt
    | chatModel
)

# --------------------------------------------------------------- #


@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    print("User Input:", msg)

    response = rag_chain.invoke(msg)

    print("Response:", response.content)
    return response.content


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
