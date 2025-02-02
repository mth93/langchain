from langchain import hub
from langchain.libs.langchain.langchain.chat_models import ChatAnthropic
from langchain.libs.core.langchain_core.output_parsers import StrOutputParser

# Create chain
prompt = hub.pull("hwchase17/anthropic-paper-qa")
model = ChatAnthropic(model="claude-2", max_tokens=10000)
chain = prompt | model | StrOutputParser()
