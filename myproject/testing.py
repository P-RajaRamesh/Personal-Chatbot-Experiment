import requests
# from langgraph_database_backend import chatbot

# def retrieve_all_threads1():
#     url= 'http://127.0.0.1:8000/users/threads'
#     header= {
#         "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzcyOTcxMjE0fQ.N9iyRzUtoJLa4tt64hJagS3tTB4RAlwU-vP3Zmkw6m4",
#         "Accept": "application/json"
#     }
#     response = requests.get(url,headers=header)
#     if response.status_code == 200:
#         return response.json()['messages']
#     else:
#         return []

# print(retrieve_all_threads1())



# print(retrieve_all_threads())


# (myenv) PS D:\fullstack> python myproject/testing.py
# ['raja:ede978b6-2844-4c3d-8a61-516bd5f15b36', 'raja:036ad1d3-f7a5-4f38-8612-b07e1e2f6407']
# ['user:5c88476b-5b65-41db-821d-bb9264770c96', 'raja:036ad1d3-f7a5-4f38-8612-b07e1e2f6407', 'user:431a94b2-91c2-4fc3-b091-0020826b6dd8', 'raja:ede978b6-2844-4c3d-8a61-516bd5f15b36']


# def load_conversation(thread_id):
#     # dont override session state here otherwise for everyloop without click of button last thread will be assigned for every new chat in the for loop.
#     # dont upadte any sessions in a loop
#     # st.session_state['thread_id'] = thread_id  
#     state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values
#     print(state.get('messages',[]))
#     # return state.get('messages',[])

# load_conversation('raju:someuniquethread2')

	
# Response body
# Download
# {
#   "messages": [
#     {
#       "content": "What is my name?",
#       "additional_kwargs": {},
#       "response_metadata": {},
#       "type": "human",
#       "name": null,
#       "id": "fb74d201-34eb-4ba8-9ec3-339f90ccdfb1"
#     },
#     {
#       "content": "I don't have any information about your name. I'm a conversational AI, and our conversation has just started. If you'd like to share your name with me, I'd be happy to learn it.",
#       "additional_kwargs": {},
#       "response_metadata": {
#         "token_usage": {
#           "completion_tokens": 44,
#           "prompt_tokens": 40,
#           "total_tokens": 84,
#           "completion_time": 0.069133901,
#           "completion_tokens_details": null,
#           "prompt_time": 0.002393007,
#           "prompt_tokens_details": null,
#           "queue_time": 0.045662963,
#           "total_time": 0.071526908
#         },
#         "model_name": "llama-3.1-8b-instant",
#         "system_fingerprint": "fp_f757f4b0bf",
#         "service_tier": "on_demand",
#         "finish_reason": "stop",
#         "logprobs": null,
#         "model_provider": "groq"
#       },
#       "type": "ai",
#       "name": null,
#       "id": "lc_run--019ccd86-ebab-7c21-8c7a-88afcde8df9b-0"
#     }
#   ]
# }


# def load_conversation(thread_id):
#     url_1= 'http://127.0.0.1:8000/users/messages'
#     header= {
#         "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYWphIiwiZXhwIjoxNzcyOTkyMzU4fQ.XZTUlo599g9DDQZUbr2jJtOy7hqdyOVZpTUWtsGDDUs",
#         "Accept": "application/json"
#     }
#     payload= {"thread_id": thread_id}

#     response = requests.post(url=url_1,headers=header,json=payload)
#     if response.status_code == 200:
#         messages =  response.json()['messages']
#     else:
#         messages = []
    
#     print(messages)


# load_conversation('raju:someuniquethread')

# response:
# [
# {'content': 'Hi i am Raju', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'human', 'name': None, 'id': 'bc55069a-2946-4705-935c-0360b20538fa'}, 
# {'content': 'Hello Raju, how are you today?', 'additional_kwargs': {}, 'response_metadata': {'token_usage': {'completion_tokens': 10, 'prompt_tokens': 40, 'total_tokens': 50, 'completion_time': 0.019963349, 'completion_tokens_details': None, 'prompt_time': 0.003126319, 'prompt_tokens_details': None, 'queue_time': 0.08141619, 'total_time': 0.023089668}, 'model_name': 'llama-3.1-8b-instant', 'system_fingerprint': 'fp_4387d3edbb', 'service_tier': 'on_demand', 'finish_reason': 'stop', 'logprobs': None, 'model_provider': 'groq'}, 'type': 'ai', 'name': None, 'id': 'lc_run--019ccd81-86c8-7411-879d-e8d29932587e-0'}, 
# {'content': 'What is my name?', 'additional_kwargs': {}, 'response_metadata': {}, 'type': 'human', 'name': None, 'id': 'b318aa5a-76a6-408f-8167-4fb7e1f4b777'}, 
# {'content': 'Your name is Raju.', 'additional_kwargs': {}, 'response_metadata': {'token_usage': {'completion_tokens': 7, 'prompt_tokens': 64, 'total_tokens': 71, 'completion_time': 0.009922556, 'completion_tokens_details': None, 'prompt_time': 0.00355088, 'prompt_tokens_details': None, 'queue_time': 0.04519093, 'total_time': 0.013473436}, 'model_name': 'llama-3.1-8b-instant', 'system_fingerprint': 'fp_4387d3edbb', 'service_tier': 'on_demand', 'finish_reason': 'stop', 'logprobs': None, 'model_provider': 'groq'}, 'type': 'ai', 'name': None, 'id': 'lc_run--019ccd86-75e4-7fa1-9449-c326cfefdc08-0'}
# ]



def login(username,password):
    url = 'http://127.0.0.1:8000/login'
    payload= {"username": username, "password": password}
    response = requests.post(url=url,data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None
    

print("printing----",login('raja','raja@123'))