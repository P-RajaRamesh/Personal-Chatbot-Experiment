from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..import models, schemas
from .login import get_current_user

from ..langgraph_database_backend import checkpointer, chatbot
from langchain_core.messages import HumanMessage

router = APIRouter(
    tags=['Users'],
    prefix='/users'
)

@router.get('/', response_model=list[schemas.DisplayUser])
def get_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    users = db.query(models.User).all()
    print(current_user,'------in users---------------------------')
    return users

@router.get('/user', response_model=schemas.TokenData)
def get_user(current_user: schemas.TokenData = Depends(get_current_user)):
    print(current_user,'------in user---------------------------')
    return current_user

@router.post('/invoke', response_model=schemas.ResultMsg)
def invoke_model(request: schemas.RequestMsg, current_user = Depends(get_current_user)):
    print(current_user,'------------in invoke model----------------------')
    result = chatbot.invoke(
        {'messages': [HumanMessage(content=request.msg)]},
        config={"configurable": {"thread_id": request.thread_id}}
    )
    print(result['messages'][-1].content)
    return {'res': result['messages'][-1].content}

@router.post('/messages', response_model=schemas.AllMessages)
def retrieve_messages(request: schemas.RequestThreadID, current_user = Depends(get_current_user)):
    state = chatbot.get_state(config={'configurable': {'thread_id': request.thread_id}}).values
    thread_messages = state.get('messages',[])
    messages = schemas.AllMessages(messages=thread_messages)
    return messages

@router.get('/threads', response_model=schemas.AllThreads)
def retrieve_all_threads(current_user: schemas.TokenData = Depends(get_current_user)):
    user_threads=set()
    for checkpoint in checkpointer.list(None):
        thread = checkpoint.config['configurable']['thread_id']
        # if 'user:' in thread:
        if f'{current_user.user_id}:' in thread:
            user_threads.add(thread)
    threads = schemas.AllThreads(threads=list(user_threads))
    return threads


# def retrieve_all_threads():
    
#     all_threads=set()

#     for checkpoint in checkpointer.list(None):
#         all_threads.add(checkpoint.config['configurable']['thread_id'])

#     return list(all_threads)