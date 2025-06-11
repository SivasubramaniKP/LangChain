from langgraph.graph import StateGraph, START
from typing import TypedDict, Literal
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from datetime import datetime
import geocoder
import weatherapi
from weatherapi.rest import ApiException


class State(TypedDict):
    typeOfQuestion: Literal['Weather', 'Course']
    weather: str
    CourseResult: str
    Query: str


model = init_chat_model("gemini-2.0-flash", model_provider="google_genai")


def getQuery(state: State):
    userInput = input("Enter your question: ")
    return {"Query": userInput}


def ClassifyQuery(state: State):
    prompt_template = PromptTemplate.from_template(
        "Classify if it's related to Weather or Course: {query}. Reply only with one word."
    )
    prompt = prompt_template.invoke({"query": state["Query"]})
    response = model.invoke(prompt)
    print("CLASSIFYING QUERY : " + response.content)
    return {"typeOfQuestion": response.content.strip()}


def getCourseInfo(state: State):
    from RAGCLI import graph
    response = graph.invoke({"question": state["Query"]})
    return {"CourseResult": response.content}


def predictWeather(state: State):
    g = geocoder.ip("me")
    lat, lng = g.latlng
    q = f"{lat},{lng}"
    dt = datetime.today().strftime("%Y-%m-%d")
    import os
    configuration = weatherapi.Configuration()
    configuration.api_key['key'] = os.getenv("GOOGLE_API_KEY")
    api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))

    try:
        api_response = api_instance.forecast_weather(q, dt)
        return {"weather": api_response['current']['condition']['text']}
    except ApiException as e:
        print("Weather API Error:", e)
        return {"weather": "unknown"}


graphBuilder = StateGraph(State)
graphBuilder.add_node("getQuery", getQuery)
graphBuilder.add_node("Weather", predictWeather)
graphBuilder.add_node("Course", getCourseInfo)

graphBuilder.add_edge(START, "getQuery")
graphBuilder.add_conditional_edges("getQuery", ClassifyQuery, {
    "Weather": "Weather",
    "Course": "Course"
})
graphBuilder.add_edge("Weather", "getQuery")
graphBuilder.add_edge("Course", "getQuery")

graph = graphBuilder.compile()

graph.invoke({
    "typeOfQuestion": "Course",  # dummy
    "weather": "",
    "CourseResult": "",
    "Query": ""
})
