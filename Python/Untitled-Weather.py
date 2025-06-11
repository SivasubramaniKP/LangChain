# %%
from langgraph.graph import Graph, START, END
from typing import TypedDict, List, Annotated, Literal

typeOfQuestion = "typeOfQuestion"
weather = "weather"
CourseResult = "CourseResult"
Query = "Query"
class State(TypedDict):
    typeOfQuestion : Literal['Weather', 'Course']
    weather : str
    CourseResult : str
    Query : str

# %%
from langchain.chat_models import init_chat_model

model =  init_chat_model(
    "gemini-2.0-flash",
    model_provider= "google_genai"
)


# %%
def getCourseInfo(state: State):
    from RAGCLI import graph
    response = graph.invoke({
        "question" : state["Query"]
    })
    return {
        "CourseResult" : response.content
    }

# %%
def getQuery(state: State):
    userInput = input()
    return {
        "Query" : userInput
    }

# %%
def ClassifyQuery(state: State):
    from langchain_core.prompts import PromptTemplate

    prompt_template = PromptTemplate.from_template("Classify if its related to Weather or Course: {query}. and provide output in a single word")

    prompt = prompt_template.invoke({
        "query" : state["Query"]
    })
    response = model.invoke(prompt)
    return {
        "typeOfQuestion" : response.content
    }

# %%
def predictWeather(state: State):
    import geocoder
    g = geocoder.ip("me")
    import time
    import weatherapi
    from weatherapi.rest import ApiException
    from pprint import pprint

    # Configure API key authorization: ApiKeyAuth
    configuration = weatherapi.Configuration()
    configuration.api_key['key'] = 'e00b8e34d43b4cbea5380937250906'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['key'] = 'Bearer'
    lat, long = g
    # create an instance of the API class
    api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
    q = lat + ',' + long # str | Pass US Zipcode, UK Postcode, Canada Postalcode, IP address, Latitude/Longitude (decimal degree) or city name. Visit [request parameter section](https://www.weatherapi.com/docs/#intro-request) to learn more.
    dt = '2025-05-09' # date | Date on or after 1st Jan, 2015 in yyyy-MM-dd format

    try:
        # Astronomy API
        api_response = api_instance.forecast_weather(q, dt)
        pprint(api_response['current']['condition']['text'])
        return {
            "weather" : api_response['current']['condition']['text']
        }
    except ApiException as e:
           print("Exception when calling APIsApi->astronomy: %s\n" % e)

# %%


# %%

from langchain_core.prompts import PromptTemplate
prompt_template = PromptTemplate.from_template("Classify if its related to Weather or Course: {query}. and provide output in a single word")
prompt = prompt_template.invoke({
    "query" : "no of credits for 22CS610" 
})
response = model.invoke(prompt)
response.content

# %%
from langgraph.graph import START, END, StateGraph

graphBuilder =  StateGraph(State)
graphBuilder.add_node("getQuery", getQuery)
# graphBuilder.add_node("ClassifyQuery", ClassifyQuery)
graphBuilder.add_node("Weather", predictWeather)
graphBuilder.add_node("Course", getCourseInfo)

graphBuilder.add_edge(START, "getQuery")
graphBuilder.add_conditional_edges("getQuery", ClassifyQuery)
graphBuilder.add_edge("Weather", "getQuery")
graphBuilder.add_edge("Course", "getQuery")


graph = graphBuilder.compile()
graph.invoke({
    "typeOfQuestion" : "Weather",
    "Weather" : "",
    "CourseResult" : "",
    "Query": ""
}) 

# %%


# %%


# %%



