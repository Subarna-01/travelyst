from fastapi import APIRouter, Depends, Response, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.users_schema import CreateUser, UpdateUser
from controllers.users_controller import UserController

users_router = APIRouter(prefix='/user')

@users_router.post('/create-user')
async def create_user(payload: CreateUser,response: Response,background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    response = await UserController().create_user(payload,response,background_tasks,db)
    return jsonable_encoder(response)

@users_router.put('/update-user/{user_id}')
async def update_user(user_id: str,payload: UpdateUser,response: Response,db: Session = Depends(get_db)):
    response = await UserController().update_user(user_id,payload,response,db)
    return jsonable_encoder(response)

@users_router.put('/deactivate-user/{user_id}')
async def deactivate_user(user_id: str,response: Response,background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    response = await UserController().deactivate_user(user_id,response,background_tasks,db)
    return jsonable_encoder(response)
