# Load
from langchain.libs.langchain.langchain.chat_models import ChatOllama
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings import GPT4AllEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.libs.langchain.langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.libs.langchain.langchain.vectorstores import Chroma
from langchain.libs.core.langchain_core.output_parsers import StrOutputParser
from langchain.libs.core.langchain_core.pydantic_v1 import BaseModel
from langchain.libs.core.langchain_core.runnables import RunnableParallel, RunnablePassthrough

loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
data = loader.load()

# Split

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Add to vectorDB
vectorstore = Chroma.from_documents(
    documents=all_splits,
    collection_name="rag-private",
    embedding=GPT4AllEmbeddings(),
)
retriever = vectorstore.as_retriever()

# Prompt
# Optionally, pull from the Hub
# from langchain import hub
# prompt = hub.pull("rlm/rag-prompt")
# Or, define your own:
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# LLM
# Select the LLM that you downloaded
ollama_llm = "llama2:7b-chat"
model = ChatOllama(model=ollama_llm)

# RAG chain
chain = (
    RunnableParallel({"context": retriever, "question": RunnablePassthrough()})
    | prompt
    | model
    | StrOutputParser()
)


# Add typing for input
class Question(BaseModel):
    __root__: str


chain = chain.with_types(input_type=Question)
