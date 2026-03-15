from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

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
conn=sqlite3.connect(database='chatbot3.db', check_same_thread=False)

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

# test
CONFIG={'configurable': {'thread_id': 'raja:thread-3'}}

# response=chatbot.invoke(
#                 {'messages': [HumanMessage(content='What is capital of India? Ack my name while answering.')]},
#                 config=CONFIG
# )

# print(response)
# ----------------------------------------------------------------------
hex_string = "7b22736f75726365223a20226c6f6f70222c202273746570223a20302c2022706172656e7473223a207b7d7d"

# decode it
print(bytes.fromhex(hex_string).decode('utf-8'))


# ----------------------------------------------------------

# extract threads from db

# checkpointer.list('thread-1')
print('--------------------------------------------')

def retrieve_all_threads():
    
    all_threads=set()
    user_threads=set()

    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
    
    for i in all_threads:
        if 'raja:' in i:
            user_threads.add(i)
    print(list(all_threads))
    print('--------------------------------------------')
    print(list(user_threads))

retrieve_all_threads()


