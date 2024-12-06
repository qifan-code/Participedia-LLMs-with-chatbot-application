from langchain_ollama import ChatOllama, OllamaEmbeddings
import faiss
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from flask import Flask, request


# Use Meta Llama 3.1 8B Instruct as the chat model
llm = ChatOllama(model="llama3.1")

# Use mxbai-embed-large as the embedding model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# use a single GPU for similarity search
res = faiss.StandardGpuResources()
# load the previously cached FAISS index
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
# convert the index from cpu-based to gpu-based for accelerated search
vector_store.index = faiss.index_cpu_to_gpu(res, 0, vector_store.index)
# use FAISS indexed vector store as the retriever
retriever = vector_store.as_retriever()

# Define the prompt template for the LLM
prompt = PromptTemplate(
    template="""You are an assistant for question-answering tasks.
    Use the following documents to answer the question.
    If you don't know the answer, just say that you don't know.
    Question: {question}
    Documents: {documents}
    Answer:
    """,
    input_variables=["question", "documents"],
)

# Create a chain combining the prompt template and LLM
rag_chain = prompt | llm | StrOutputParser()

# Define the RAG application class
class RAGApplication:
    def __init__(self, retriever, rag_chain):
        self.retriever = retriever
        self.rag_chain = rag_chain
    def run(self, question):
        # Retrieve relevant documents
        documents = self.retriever.invoke(question)
        # Extract content from retrieved documents
        doc_texts = "\\n".join([doc.page_content for doc in documents])
        # Get the answer from the language model
        answer = self.rag_chain.invoke({"question": question, "documents": doc_texts})
        return answer

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask():
    # Initialize the RAG application
    rag_application = RAGApplication(retriever, rag_chain)
    # Obtain the question
    question = request.json['question']
    # Get the answer
    answer = rag_application.run(question)
    return {'answer': answer}
