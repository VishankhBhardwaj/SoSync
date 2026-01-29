from langchain.tools import tool
from make_call import call_sos

@tool
def sos_call_tool(message: str) -> str:
    """Place emergency SOS call"""
    call_sos(message)
    return "Emergency SOS call placed."
