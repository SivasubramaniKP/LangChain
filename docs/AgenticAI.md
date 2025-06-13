Agentic AI:
    Agentic AI uses Sophisticated Reasoning and iterative planning to autonomously solve complex workflows.

Stages of Agentic AI:
    Perceive : AI agents collect information and process data from various sources such as databases, sensors and digital interfaces extracting meaningful patterns and objects

    Reason :  Usually an LLM acts as an orchestrator or reasoning engine, to produce results in Natural language

    Act : Interacts with external tools like API's.

    Learn : Learn through feedback loop,

AGNO Memory :
    Memory gives an agent the ability to recall

    Session Storage :
        Saves the agent's session in a database
    User Memories : 
        Agent can store the insights and facts about the user
    Session Summary : 
        Agents can store the chat's summary
    
Agents : 
    Take actions autonomously and dynamically change the course of action
    Model : The LLM model which controls the flow of execution
    Tools : Enable the model to interact with external tools
    Instructions : Teaching the model how to do things and how to proceed

    Reasoning : 
        Think before responding and analyze the results of the action

    Knowledge : Domain specific knowledge stored in VectorDB used in RAG

    Storage : 
        Session history and state in a database
        This makes agents stateful, have multi-turn conversation and long term
    Memory : 
        Store interactions of the user. It stores the user preferences 
    
    enable_agentic_memory: bool = False
    # If True, the agent creates/updates user memories at the end of runs
    enable_user_memories: bool = False
    # If True, the agent adds a reference to the user memories in the response