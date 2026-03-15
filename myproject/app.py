import streamlit as st
import uuid
import utils

st.set_page_config(page_title="Chatbot", page_icon="🔐", layout="centered")

st.title("Personal Chatbot 🤖")

# --------------------User Session Setup ------------------------

if "logged_in" not in st.session_state:
    st.session_state['logged_in'] = False
if "token" not in st.session_state:
    st.session_state['token'] = None
if "username" not in st.session_state:
    st.session_state['username'] = None
if "user_id" not in st.session_state:
    st.session_state['user_id'] = None



# ── LOGGED IN: Dashboard ──────────────────────────────────────────────────────

if st.session_state['logged_in']:

    # --------------------------utility funtions-------------------------------

    def generate_thread_id():
        unique_id=uuid.uuid4()
        user_id= st.session_state['user_id']
        return f'{user_id}:{unique_id}' 

    def add_thread(thread_id):
        if thread_id not in st.session_state['chat_threads']:
            st.session_state['chat_threads'].append(thread_id)

    def reset_chat():
        thread_id=generate_thread_id()
        st.session_state['thread_id']=thread_id
        add_thread(st.session_state['thread_id'])
        st.session_state['message_history']=[]

    # --------------------------Chatbot Session Steup---------------------------------

    if 'message_history' not in st.session_state:
        st.session_state['message_history'] = []

    if 'thread_id' not in st.session_state:
        st.session_state['thread_id'] = generate_thread_id()

    if 'chat_threads' not in st.session_state:
        token = st.session_state['token']
        st.session_state['chat_threads'] = utils.retrieve_all_threads(token)

    add_thread(st.session_state['thread_id'])

    # ------------------------------------------------------------------------------xxxxxxxxxxxxxxxxxxxx

    st.success(f"Welcome **{st.session_state['username']}**! 👋")
    st.divider()

    # ---------------------------Sidebar UI------------------------------------
    st.sidebar.title('LangGraph Chatbot')

    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        for key in ['token', 'username', 'user_id', 'chat_threads', 'message_history', 'thread_id']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state['logged_in'] = False
        st.rerun()

    if st.sidebar.button('New Chat'):
        reset_chat()

    st.sidebar.header('My Conversations')

    for thread_id in st.session_state['chat_threads'][::-1]:
        token = st.session_state['token']
        # Load messages for preview 
        messages = utils.load_conversation(token,thread_id) 

        # Default label if no messages yet 
        if messages: 
            # Take first message content (user or assistant) and slice first 10 chars 
            preview_text = messages[0]['content'][:10] + "..."  # this line will change----------------------------------------
        else: 
            preview_text = str(thread_id)[:8] # fallback to shortened thread_id

        if st.sidebar.button(preview_text, key=str(thread_id)): # unique key id given to button so that streamlit wont get confused with same widgets
            # now thread id will be assigned to session state only when button is clicked
            st.session_state['thread_id'] = thread_id
            messages = utils.load_conversation(token,thread_id) 

            temp_messages = []

            for msg in messages: # this loop will change----------------------------------------
                if msg['type'] == 'human':
                # if isinstance(msg,HumanMessage):
                    role='user'
                else:
                    role='assistant'
                temp_messages.append({'role': role, 'content': msg['content']})

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
        # CONFIG={
        #     'configurable': {'thread_id': st.session_state['thread_id']}
        # }

        with st.chat_message('assistant'):
            token = st.session_state['token']
            thread_id = st.session_state['thread_id']
            result = utils.chatbot_invoke(token,user_input,thread_id)

            ai_message = st.write(result)

        st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

# ── LOGGED OUT: Login / Register tabs ────────────────────────────────────────

else:
    tab_login, tab_register = st.tabs(["Login", "Register"])

    # ── Login ──
    with tab_login:
        st.subheader("Sign in to your account")

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", type="primary", use_container_width=True, key="login_btn"):
            if not username or not password:
                st.warning("Please fill in all fields.")
            else:
                token = utils.login(username,password)
                st.session_state['token'] = token
                if token:
                    user_details = utils.get_user_details(token)
                    if user_details:
                        st.session_state['username'] = user_details['username']
                        st.session_state['user_id'] = user_details['user_id']
                        st.session_state.logged_in = True
                        st.success("Logged in successfully!")
                        st.rerun()
                else:
                    st.error("Invalid username or password.")

    # ── Register ──
    with tab_register:
        st.subheader("Create a new account")

        new_username = st.text_input("Choose a username", key="reg_username")
        new_email = st.text_input("Choose a email", key="reg_email")
        new_password = st.text_input("Confirm password", type="password", key="reg_password")

        if st.button("Register", type="primary", use_container_width=True, key="register_btn"):
            if not new_username or not new_email or not new_password:
                st.warning("Please fill in all fields.")
            elif len(new_username) < 3:
                st.warning("Username must be at least 3 characters.")
            elif len(new_email) < 6:
                st.warning("Email must be at least 6 characters.")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                registered_user = utils.register(new_username,new_email,new_password)
                if registered_user:
                    st.success(f"Account created! {registered_user} can now log in.")
                else:
                    st.error('user name already exists!')
