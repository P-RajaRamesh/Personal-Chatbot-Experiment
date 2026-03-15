import requests

def login(username,password):
    url = 'http://127.0.0.1:8000/login'
    payload= {"username": username, "password": password}
    response = requests.post(url=url,data=payload)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return None
    
def get_user_details(token: str):
    url = 'http://127.0.0.1:8000/users/user'
    header= {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = requests.get(url=url,headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def register(username: str, email: str, password: str):
    url = 'http://127.0.0.1:8000/register'
    header= {
        "Accept": "application/json"
    }
    payload= {"username": username, "email": email, "password": password}
    response = requests.post(url=url,headers=header,json=payload)
    if response.status_code == 200:
        return response.json()['username']
    else:
        return None
    
def load_conversation(token: str, thread_id: str):
    url_1= 'http://127.0.0.1:8000/users/messages'
    header= {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    payload= {"thread_id": thread_id}

    response = requests.post(url=url_1,headers=header,json=payload)
    if response.status_code == 200:
        messages =  response.json()['messages']
    else:
        messages = []
    
    return messages

def retrieve_all_threads(token: str):
    url= 'http://127.0.0.1:8000/users/threads'
    header= {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    response = requests.get(url,headers=header)
    if response.status_code == 200:
        return response.json()['threads']
    else:
        return []
    
def chatbot_invoke(token: str, message: str, thread_id: str):
    url= 'http://127.0.0.1:8000/users/invoke'
    header= {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    payload= {
        "msg": message,
        "thread_id": thread_id
    }
    response = requests.post(url=url,headers=header,json=payload)
    if response.status_code == 200:
        return response.json()['res']
    else:
        return None