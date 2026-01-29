import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_classic.agents import create_tool_calling_agent,AgentExecutor
from streamlit_geolocation import streamlit_geolocation
from tools import sos_call_tool
from langchain_classic.agents import AgentType
from utils import reverse_geocode
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")


if "location" not in st.session_state:
    st.session_state.location = None

location = streamlit_geolocation()

if location and "latitude" in location:
    st.session_state.location = location
    st.success(f"📍 Location detected:-{location}")

st.title("🚨 Sentinel — AI Emergency Assistant")

user_input = st.text_input(
    "Describe your situation",
    placeholder="e.g. Someone is following me, I need help"
)

system_prompt = """
You are an emergency response agent.

RULES:
- Do NOT provide advice or explanations.
- If the user is in danger, you MUST call sos_call_tool.
- The message must be a single spoken emergency message.
- Always include the provided location.
- Also ensure that the provided location is spoken twice liek I repeat and then the address/location again to ensure delivery of message
- Once the call is made provide how should the user respond to such situation in output
- If there is no emergency, respond briefly in text.

"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

tools = [sos_call_tool]
llm = ChatGroq(groq_api_key=groq_api_key,model="openai/gpt-oss-120b")
agent = create_tool_calling_agent(llm,tools,prompt)
agent_executor = AgentExecutor(agent = agent,tools = tools,verbose=True)
panic_mode = st.button("🚨 PANIC SOS")



if user_input and st.session_state.location and st.button("🆘 Send SOS"):
    loc = st.session_state.location
    lat = loc["latitude"]
    lon = loc["longitude"]
    address = reverse_geocode(lat, lon)
    st.info(f"📍 Resolved address: {address}")
    agent_input = f"""
    Emergency message:
    {user_input}

    Location:
    {address}
    """

    with st.spinner("🚨 Assessing emergency..."):
        result = agent_executor.invoke({"input": agent_input})
        st.warning("""
        If you are in immediate danger:
        • Move to a crowded or well-lit area
        • Call local emergency number (112 in India)
        • Keep your phone unlocked and accessible
        • Try to alert people nearby
        """)


    st.success(result['output'])
elif st.session_state.location and panic_mode:
        loc = st.session_state.location
        lat = loc["latitude"]
        lon = loc["longitude"]
        address = reverse_geocode(lat, lon)
        with st.spinner("🚨 Assessing emergency..."):
            result = agent_executor.invoke({
                "input": f"""
                Emergency panic mode activated.
                User may not be able to speak.
                Location: {address}
                """
            })
            st.warning("""
            If you are in immediate danger:
            • Move to a crowded or well-lit area
            • Call local emergency number (112 in India)
            • Keep your phone unlocked and accessible
            • Try to alert people nearby
            """)
        

elif user_input and not st.session_state.location:
    st.warning("Please allow location access before sending SOS.")


