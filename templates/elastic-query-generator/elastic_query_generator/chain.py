from elasticsearch import Elasticsearch
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.libs.core.langchain_core.pydantic_v1 import BaseModel

from .elastic_index_info import get_indices_infos
from .prompts import DSL_PROMPT

# Setup Elasticsearch
# This shows how to set it up for a cloud hosted version

# Password for the 'elastic' user generated by Elasticsearch
ELASTIC_PASSWORD = "..."

# Found in the 'Manage Deployment' page
CLOUD_ID = "..."

# Create the client instance
db = Elasticsearch(cloud_id=CLOUD_ID, basic_auth=("elastic", ELASTIC_PASSWORD))

# Specify indices to include
# If you want to use on your own indices, you will need to change this.
INCLUDE_INDICES = ["customers"]

# With the Elasticsearch connection created, we can now move on to the chain

_model = ChatOpenAI(temperature=0, model="gpt-4")

chain = (
    {
        "input": lambda x: x["input"],
        # This line only get index info for "customers" index.
        # If you are running this on your own data, you will want to change.
        "indices_info": lambda _: get_indices_infos(
            db, include_indices=INCLUDE_INDICES
        ),
        "top_k": lambda x: x.get("top_k", 5),
    }
    | DSL_PROMPT
    | _model
    | SimpleJsonOutputParser()
)


# Nicely typed inputs for playground
class ChainInputs(BaseModel):
    input: str
    top_k: int = 5


chain = chain.with_types(input_type=ChainInputs)
