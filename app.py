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

# -------------------------
# Load environment variables
# -------------------------
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not PINECONE_API_KEY or not OPENAI_API_KEY:
    raise ValueError("❌ Missing API keys. Check environment variables.")

# -------------------------
# Load embeddings model
# -------------------------
embeddings = download_hugging_face_embeddings()

# -------------------------
# Connect to Pinecone index
# -------------------------
index_name = "medical-chatbot"

docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Retriever for RAG
retriever = docsearch.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# -------------------------
# Chat Model
# -------------------------
chatModel = ChatOpenAI(model="gpt-4o-mini")

# -------------------------
# Prompt template
# -------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{question}")
])

# -------------------------
# Full RAG pipeline
# -------------------------
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | chatModel
)

# =========================================================
#                       ROUTES
# =========================================================

@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form.get("msg", "")

    if not user_msg:
        return "Please enter a message."

    print("User Input:", user_msg)

    response = rag_chain.invoke(user_msg)
    print("Response:", response.content)

    return response.content


# ---------- Health Check Route (important for deployment) ----------
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


# =========================================================
#      NOTE: We DO NOT run app.run() in production
#      Gunicorn will run: gunicorn app:app
# =========================================================

if __name__ == "__main__":
    # For local testing only
    app.run(host="0.0.0.0", port=5001, debug=True)
