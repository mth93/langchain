import os

import cassio
import langchain.libs.langchain.langchain
from langchain.cache import CassandraCache
from langchain.libs.langchain.langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.libs.langchain.langchain.schema import BaseMessage
from langchain.libs.core.langchain_core.runnables import RunnableLambda

use_cassandra = int(os.environ.get("USE_CASSANDRA_CLUSTER", "0"))
if use_cassandra:
    from .cassandra_cluster_init import get_cassandra_connection

    session, keyspace = get_cassandra_connection()
    cassio.init(
        session=session,
        keyspace=keyspace,
    )
else:
    cassio.init(
        token=os.environ["ASTRA_DB_APPLICATION_TOKEN"],
        database_id=os.environ["ASTRA_DB_ID"],
        keyspace=os.environ.get("ASTRA_DB_KEYSPACE"),
    )

# inits
langchain.llm_cache = CassandraCache(session=None, keyspace=None)
llm = ChatOpenAI()


# custom runnables
def msg_splitter(msg: BaseMessage):
    return [w.strip() for w in msg.content.split(",") if w.strip()]


# synonym-route preparation
synonym_prompt = ChatPromptTemplate.from_template(
    "List up to five comma-separated synonyms of this word: {word}"
)

chain = synonym_prompt | llm | RunnableLambda(msg_splitter)
