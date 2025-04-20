# ----------------------------------------------------------------------------------------------------------EXAMPLE 2------------------------------------------------------------------------
#It is a straight forward example of how to use langgraph to that matches user queries with AI tools. Test in langgraph studio directly.

from openai import OpenAI
import os
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("openai_key"),
)

AI_TOOLS = [
    "ChatGPT",
    "DALL·E",
    "Whisper",
    "Midjourney",
    "AssemblyAI",
    "RunwayML",
    "Claude",
    "Bard",
    "Stable Diffusion",
    "ElevenLabs"
]

class State(TypedDict):
    query: Optional[str]
    llm_response: Optional[str]
    explanation: Optional[str]
    final_output: Optional[str]

def get_query(state: State) -> State:
    return {"query": state.get("query")}

def llm_match_tools(state: State) -> State:
    system_prompt = f"""You are an AI assistant that matches user requests with AI tools.
    Here are the available tools:
    {AI_TOOLS}

    Given a user query, return 1-3 relevant tools (only from the list), separated by commas.
    Just return tool names, nothing else.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": state["query"]},
        ],
        temperature=0
    )

    return {"llm_response": response.choices[0].message.content.strip()}

def explain_selection(state: State) -> State:
    system_prompt = """You are an AI assistant explaining the reasoning behind tool choices.
User query: {query}
Selected tools: {tools}

Write a short explanation (2–3 sentences) about why these tools are a good fit for the user query.
"""

    formatted_prompt = system_prompt.format(
        query=state["query"],
        tools=state["llm_response"]
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": formatted_prompt}
        ],
        temperature=0.7
    )

    return {"explanation": response.choices[0].message.content.strip()}

def combine_response(state: State) -> State:
    tools = state["llm_response"]
    explanation = state["explanation"]
    final = f"Recommended Tools: {tools}\n\n Why: {explanation}"
    return {"final_output": final}

def create_graph():
    builder = StateGraph(State)

    builder.add_node("start", get_query)
    builder.add_node("llm_match", llm_match_tools)
    builder.add_node("explain", explain_selection)
    builder.add_node("final", combine_response)

    builder.set_entry_point("start")
    builder.add_edge("start", "llm_match")
    builder.add_edge("llm_match", "explain")
    builder.add_edge("explain", "final")
    builder.add_edge("final", END)

    return builder.compile()

graph = create_graph()

def run_tool_match_graph(query: str) -> str:
    result = final_state.invoke({"query": query})
    return result.get("final_output", "")




# ----------------------------------------------------------------------------------------------------------EXAMPLE 2------------------------------------------------------------------------
# Uncomment below code to test confirmation flow, its same as above but with confirmation [only responds when yes is input or cancel when no is input]. To respond to confirmation, input yes or no like this: {"response":"yes"} / {"response":"no"} in langgraph studio as shown in READ-ME of github.


# import os
# from openai import OpenAI
# from langgraph.graph import StateGraph, END
# from typing import TypedDict, Optional
# from dotenv import load_dotenv
# from langgraph.types import interrupt

# load_dotenv()

# client = OpenAI(api_key=os.getenv("openai_key"))

# AI_TOOLS = """ DALL·E generates images from text prompts, allowing users to visualize their ideas creatively.
#     Whisper offers highly accurate speech-to-text conversion, making audio transcription seamless. 
#     ChatGPT is an advanced conversational chatbot capable of understanding and generating human-like responses. 
#     Midjourney specializes in creating artistic images based on short descriptions, catering to designers and creatives. 
#     AssemblyAI provides an API for robust speech recognition and transcription services.
#     Lastly, RunwayML is an AI-powered video editing platform that simplifies the editing process using advanced machine learning models."""

# class State(TypedDict):
#     query: Optional[str]
#     llm_response: Optional[str]
#     user_confirmation: Optional[str]
#     explanation: Optional[str]
#     final_output: Optional[str]

# def get_query(state: State) -> State:
#     return {"query": state.get("query")}

# def llm_match_tools(state: State) -> State:
#     system_prompt = f"""You are an AI assistant that matches user requests with AI tools.
#     Here are the available tools:

#     {AI_TOOLS}

#     Given a user query, return 1–3 relevant tools (only from the list), separated by commas.
#     Just return tool names, nothing else.
#     """
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": state["query"]},
#         ],
#         temperature=0,
#     )
#     return {"llm_response": response.choices[0].message.content.strip()}

# def ask_for_confirmation(state: State) -> State:
#     user_input = interrupt({"query": "Do you want to know why these tools were chosen? (yes/no)"})
#     user_response = str(user_input["response"]).strip().lower() if user_input else None
#     return {"user_confirmation": user_response}

# def explain_selection(state: State) -> State:
#     prompt = f"""You are an AI assistant explaining the reasoning behind tool choices.
#     User query: {state['query']}
#     Selected tools: {state['llm_response']}

#     Write a short explanation (2–3 sentences) about why these tools are a good fit for the user query.
#     """

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "system", "content": prompt}],
#         temperature=0.7,
#     )
#     return {"explanation": response.choices[0].message.content.strip()}

# def combine_response(state: State) -> State:
#     tools = state["llm_response"]
#     explanation = state["explanation"]
#     final = f" Recommended Tools: {tools}\n\n Why: {explanation}"
#     return {"final_output": final}

# def create_graph():
#     builder = StateGraph(State)

#     builder.add_node("start", get_query)
#     builder.add_node("llm_match", llm_match_tools)
#     builder.add_node("confirmation", ask_for_confirmation)
#     builder.add_node("explain", explain_selection)
#     builder.add_node("final", combine_response)

#     builder.set_entry_point("start")
#     builder.add_edge("start", "llm_match")
#     builder.add_edge("llm_match", "confirmation")

#     builder.add_conditional_edges(
#         "confirmation",
#         lambda state: "explain" if state["user_confirmation"] == "yes" else END,
#         {"explain": "explain", END: END}
#     )

#     builder.add_edge("explain", "final")
#     builder.add_edge("final", END)

#     return builder.compile()

# graph = create_graph()

# def run_tool_match_graph(query: str) -> str:
#     result = final_state.invoke({"query": query})
#     return result.get("final_output", "Okay, maybe next time.")
