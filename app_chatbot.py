import os  # noqa: F401

import streamlit as st
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage  # noqa: F401
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

### Page Configuration
st.set_page_config(page_title="ChatBot Powered by Google GenAI", page_icon="😉")

### Introduction
st.title("Kucing 😺")
st.markdown("ChatBot Powered by Google GenAI. 😉")
st.markdown("Hey Human ask me Anything...")


### Sidebar
with st.sidebar:
    st.markdown("Settings")

    ### api key
    api_Key = st.text_input(
        "api_key",
        type="password",
        help="get your own api key for free from https://aistudio.google.com/api-keys",
    )

    ### Model Selection
    model_name = st.selectbox(
        "Model",
        ["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-3.6-flash"],
        index=0,
    )

    ### clear session
    if st.button("clear chat"):
        st.session_state.messages = []
        st.rerun()

### chat history initialisation
if "messages" not in st.session_state:
    st.session_state.messages = []


### LLM initialise
@st.cache_resource
def get_chain(api_key, model_name):
    if not api_key:
        return None

    ### LLM creation
    llm = init_chat_model(
        api_Key=api_Key,
        model_provider="google_genai",
        model=model_name,
        streaming=True,
        temperature=0.7,
    )

    ### Prompt Assign
    Prompt = ChatPromptTemplate(
        [
            (
                "system",
                "You are KUCING. An AI chat assistant powered by Google GenAI. Answer the Quesion clearly and Concisely. You can also Provide Moral Support if asked.",
            ),
            ("user", "{Question}"),
        ]
    )

    ### Creating Chain
    chain = Prompt | llm | StrOutputParser()
    return chain


### get Chain
chain = get_chain(api_Key, model_name)

if not chain:
    st.warning("👆 Please Enter your Google GenAI API Key to start Chatting!!!")
    st.markdown(
        "[Get Your Free Api Key From Here](https://aistudio.google.com/api-keys)"
    )

### message Display

else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    ### chat Input
    if question := st.text_input("ask me anything..."):
        ### storing the user input
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        ### response Generation
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            ### feeding response recieved from llm
            try:
                ### stream response
                for chunk in chain.stream({"Question": question}):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "\u258c")
                message_placeholder.markdown(full_response)
                ### storing the assistant response
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

            except Exception as e:  # noqa: BLE001
                st.error(f"error={str(e)}")  # noqa: RUF010

###suggestions

st.markdown("---")
st.markdown("try these examples:😁👍 ")
col1, col2 = st.columns(2)
with col1:
    st.markdown("Help me with Homework😒")
    st.markdown("what is langchain?..")
with col2:
    st.markdown(
        "I can also Provide you summary for any Manga or Webnovel of Your Liking 😎"
    )
    st.markdown(
        "or i can also support your crazy theories and make some ammendments. Maybe tho... 😜"
    )

### footer
st.markdown("Made with Langchain and powered by Google GenAI(Lied Ahahahaha)🤣🤣🤣.")
