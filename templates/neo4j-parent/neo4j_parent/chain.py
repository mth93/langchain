from langchain.libs.langchain.langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.libs.langchain.langchain.vectorstores import Neo4jVector
from langchain.libs.core.langchain_core.output_parsers import StrOutputParser
from langchain.libs.core.langchain_core.pydantic_v1 import BaseModel
from langchain.libs.core.langchain_core.runnables import RunnableParallel, RunnablePassthrough

retrieval_query = """
MATCH (node)-[:HAS_PARENT]->(parent)
WITH parent, max(score) AS score // deduplicate parents
RETURN parent.text AS text, score, {} AS metadata
"""

vectorstore = Neo4jVector.from_existing_index(
    OpenAIEmbeddings(),
    index_name="retrieval",
    node_label="Child",
    embedding_node_property="embedding",
    retrieval_query=retrieval_query,
)
retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI()

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
