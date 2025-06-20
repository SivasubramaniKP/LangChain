import streamlit as st
from PIL import Image
from io import BytesIO
from pathlib import Path
import base64
from langchain.chat_models import init_chat_model
from langchain.schema import HumanMessage, AIMessage, SystemMessage
_FIRST = True

chat_model = init_chat_model(
    "gemini-2.0-flash",
    model_provider="google_genai"
)

prompt = st.chat_input("Ask a follow-up question...")
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("️Image Reporter ")

uploaded_file = st.file_uploader(
    label="Upload an image to analyze",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    Path("uploaded_file").mkdir(exist_ok=True)
    file_path = f"uploaded_file/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Image saved to: {file_path}")
    st.image(file_path, caption="Uploaded Image", use_container_width=True)

    with open(file_path, "rb") as img_file:
        base64_str = base64.b64encode(img_file.read()).decode("utf-8")

    
    first_message = HumanMessage(content=[
        {
            "type": "text",
            "text": "Describe in detail what's in the image. Answer in around 200 words."
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_str}"
            }
        },
    ])

    with st.spinner("Analyzing image"):
        response = chat_model.invoke([first_message])
        if _FIRST:
            st.session_state.messages.append(first_message)
            st.session_state.messages.append(AIMessage(content=response.content))
            _FIRST = False
    st.chat_message("assistant").write(response.content)


if prompt:
    user_message = HumanMessage(content=prompt)
    st.session_state.messages.append(user_message)

    with st.spinner("Thinking..."):
        response = chat_model.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response.content))

    print(len(st.session_state.messages))

    if len(st.session_state.messages) >= 2:
        last_user_msg = st.session_state.messages[-2]
        last_bot_msg = st.session_state.messages[-1]

        st.chat_message("User").write(last_user_msg.content)
        st.chat_message("Assistant").write(last_bot_msg.content)

    # for msg in st.session_state.messages:
    #     if isinstance(msg, HumanMessage):
    #         role = "user"
    #     else:
    #         role = "assistant"
    #     st.chat_message(role).write(msg.content)

 