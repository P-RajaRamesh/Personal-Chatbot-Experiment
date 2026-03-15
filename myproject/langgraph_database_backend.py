from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from langchain_groq import ChatGroq
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

full_path = Path(__file__).resolve()
folder_name = Path(full_path).parent.name

groq_api_key=os.getenv("GROQ_API_KEY")

llm=ChatGroq(model="llama-3.1-8b-instant",groq_api_key=groq_api_key)

# Define state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages] 

# Define node function
def chat_node(state: ChatState) -> ChatState:
    # take user query from state
    messages=state['messages']

    # send to llm
    response=llm.invoke(messages)

    # response store in state
    return {'messages': [response]}

# connection
conn=sqlite3.connect(database=f'./{folder_name}/dbfiles/chatbot.db', check_same_thread=False)

# Checkpoint
checkpointer=SqliteSaver(conn=conn)

# graph
graph=StateGraph(ChatState)

# add node
graph.add_node('chat_node',chat_node)

# add edges
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpointer)

