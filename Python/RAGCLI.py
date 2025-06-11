import pypdf

reader = pypdf.PdfReader("./Course.pdf")


reader.pages[22].extract_text()

# %%
from langchain.chat_models import init_chat_model

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai") 

from langchain_core.messages import SystemMessage, HumanMessage

# %%
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# %%
from langchain_core.vectorstores import InMemoryVectorStore

vector_store = InMemoryVectorStore(embeddings)

# %%
from langchain_community.document_loaders import PyPDFLoader

filePath = "./Course.pdf"
loader = PyPDFLoader(file_path=filePath)

docs = loader.load()

# %%
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)


# %%
_ = vector_store.add_documents(documents=all_splits)

# %%
from langchain import hub
prompt = hub.pull("rlm/rag-prompt")

# %%
from typing_extensions import TypedDict, List
from langgraph.graph import START, StateGraph
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = model.invoke(messages)
    return {"answer": response.content}


# Compile application and test
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()


# while True:
#     userQuestion = input()
#     response = graph.invoke({
#         "question" : userQuestion
#     })
#     print(response["answer"])