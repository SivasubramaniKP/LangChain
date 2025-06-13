# %% [markdown]
# Knowledge retrieval and Vector Store
# 
#     Knowledge is domain-specific information that the Agent can search at runtime to make better decisions
#     Knowledge is stored in a vector db and this searching on demand pattern is called Agentic RAG.
# 
#     Agno Agents use Agentic RAG by default, meaning if you add knowledge to an Agent, it will search this knowledge base, at runtime, for the specific information it needs to achieve its task.
# 
# 

# %%
from agno.knowledge.csv import CSVKnowledgeBase
from agno.embedder.google import GeminiEmbedder
from agno.vectordb.mongodb import MongoDb
from agno.models.google import Gemini
from agno.agent import Agent
import urllib.parse

# %%
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
vector_db = LanceDb(
    table_name="recipes",
    uri="/tmp/lancedb",
    search_type=SearchType.hybrid,
    embedder=GeminiEmbedder()
)

knowledge_base = CSVKnowledgeBase(
    path="../CSV/netflix_data.csv",
    vector_db=vector_db,
    num_documents=10,  # Number of documents to return on search
)

# %%
agent = Agent(
    knowledge=knowledge_base,
    model=Gemini(id = "gemini-2.0-flash"),
    search_knowledge=True,
    instructions=[
        "If the user asks about movie, first search the knowledge base. If no result is found in the knowledge base, then generate the answer",
        "If user asks about something other than movies, generate your own answer"
    ]
)


# %%
agent.knowledge.load()

# %%
# agent.print_response("Out of all the movies in the knowledge base what are the Tamil movies in the list", stream=True)

# %%
agent.cli_app()

# %%



