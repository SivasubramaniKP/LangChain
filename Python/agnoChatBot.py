from agno.agent import Agent
from agno.models.google import Gemini
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage

_dbFile = "./temp/agentDB.db"
# Since relative file path is used
# Careful when running from the terminal
# The path where the terminal runs from decide which database to use
# Using different database yields different output

_session_id = "13-06-2025"
# Session is a period of interaction between the user and the model
# An user can have multiple sessions
# The chats from different sessions is remembered and can be retrieved
#  Think of it like a new Chat in Chat GPT
# An user can have multiple sessions

userMemories = Memory(
    model = Gemini(
        id = "gemini-2.0-flash"
    ),
    db = SqliteMemoryDb(
        # Memory stores the facts and preferences of the user
        # Example : The user name is Sivasu
        # The user like the color violet
        # The user prefers dark theme over light
        table_name="userMemories", db_file = _dbFile
    )
)

storage = SqliteStorage(
    # Session storage is entire chat history with the replies of the model and the queries of the user
    table_name="SessionStorage",
    db_file= _dbFile
) 

agent = Agent(
    model = Gemini(
        id = "gemini-2.0-flash"
    ),
    markdown=True,
    enable_agentic_memory=True,
    enable_user_memories=True,
    num_history_runs=1000,
    add_history_to_messages=True,
    memory=userMemories,
    storage= storage,
    session_id=_session_id
)

agent.cli_app(session_id=_session_id, user_id="100", stream= True )
# res = agent.run("explain 3nf").content
# print(res)