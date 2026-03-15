import streamlit as st
from test_langgraph_database_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

# --------------------------utility funtions-------------------------------

def generate_thread_id():
    thread_id=uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id=generate_thread_id()
    st.session_state['thread_id']=thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    # dont override session state here otherwise for everyloop without click of button last thread will be assigned for every new chat in the for loop.
    # dont upadte any sessions in a loop
    # st.session_state['thread_id'] = thread_id  
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values
    return state.get('messages',[])

# --------------------------Session Steup---------------------------------

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# ---------------------------Sidebar UI------------------------------------
st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')

for thread_id in st.session_state['chat_threads'][::-1]:
    # Load messages for preview 
    messages = load_conversation(thread_id) 

    # Default label if no messages yet 
    if messages: 
        # Take first message content (user or assistant) and slice first 10 chars 
        preview_text = messages[0].content[:10] + "..." 
    else: 
        preview_text = str(thread_id)[:8] # fallback to shortened thread_id

    if st.sidebar.button(preview_text, key=str(thread_id)): # unique key id given to button so that streamlit wont get confused with same widgets
        # now thread id will be assigned to session state only when button is clicked
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history']=temp_messages

# ----------------------------Main UI-------------------------------------

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)


    # CONFIG={'configurable': {'thread_id': st.session_state['thread_id']}}

    # Thraeds will be organised in Langsmith by passing metadata
    user_id='raja'
    CONFIG={
        'configurable': {'thread_id': f'{user_id}:{st.session_state['thread_id']}'},
        'metadata': {
            'thread_id': st.session_state['thread_id']
        },
        'run_name': 'chat_trun'
    }

    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})



