from langchain.libs.langchain.langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.libs.langchain.langchain.vectorstores import Chroma
from langchain.libs.core.langchain_core.output_parsers import StrOutputParser
from langchain.libs.core.langchain_core.pydantic_v1 import BaseModel
from langchain.libs.core.langchain_core.runnables import RunnableParallel

from hyde.prompts import hyde_prompt

# Example for document loading (from url), splitting, and creating vectostore

""" 
# Load
from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
data = loader.load()

# Split
from langchain.libs.langchain.langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Add to vectorDB
vectorstore = Chroma.from_documents(documents=all_splits, 
                                    collection_name="rag-chroma",
                                    embedding=OpenAIEmbeddings(),
                                    )
retriever = vectorstore.as_retriever()
"""

# Embed a single document as a test
vectorstore = Chroma.from_texts(
    ["harrison worked at kensho"],
    collection_name="rag-chroma",
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

# RAG prompt
template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# LLM
model = ChatOpenAI()

# Query transformation chain
# This transforms the query into the hypothetical document
hyde_chain = hyde_prompt | model | StrOutputParser()

# RAG chain
chain = (
    RunnableParallel(
        {
            # Generate a hypothetical document and then pass it to the retriever
            "context": hyde_chain | retriever,
            "question": lambda x: x["question"],
        }
    )
    | prompt
    | model
    | StrOutputParser()
)


# Add input types for playground
class ChainInput(BaseModel):
    question: str


chain = chain.with_types(input_type=ChainInput)
