import uuid
from datetime import datetime
from fastapi import status, Response, BackgroundTasks
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict
from schemas.users_schema import CreateUser, UpdateUser
from models.users_model import Users
from controllers.mails_controller import MailsController

class UserController():
    
    def __init__(self) -> None:
        pass
    
    # Method to create user
    async def create_user(self,payload: CreateUser,response: Response,background_tasks: BackgroundTasks,db: Session) -> Dict[str, any]:
        try:
            username_exists_mask = db.query(Users).filter(and_(Users.username == payload.username,Users.is_active == True)).first()
            if username_exists_mask:
                response.status_code = status.HTTP_409_CONFLICT
                return { 'msg': 'Username already exists', 'status': status.HTTP_409_CONFLICT }
    
            email_exists_mask = db.query(Users).filter(and_(Users.email == payload.email,Users.is_active == True)).first()
            if email_exists_mask:
                response.status_code = status.HTTP_409_CONFLICT
                return { 'msg': 'Email already exists', 'status': status.HTTP_409_CONFLICT }

            user_id = str(uuid.uuid1().hex)
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user = Users(
                user_id=user_id,
                username=payload.username,
                first_name=payload.first_name,
                middle_name=payload.middle_name,
                last_name=payload.last_name,
                email=payload.email,
                created_on=current_datetime,
                is_active=1
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            # This background task initiates the process for sending account creation email
            background_tasks.add_task(MailsController().send_account_creation_email,payload)
            response.status_code = status.HTTP_201_CREATED
            return { 'msg': 'User created successfully', 'status': status.HTTP_201_CREATED }

        except SQLAlchemyError as db_err:
            db.rollback()
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'User creation failed', 'error_detail': str(db_err), 'status': status.HTTP_400_BAD_REQUEST }
        except Exception as err:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'An unexpected error occurred', 'error_detail': str(err), 'status': status.HTTP_400_BAD_REQUEST }

    # Method to update user information
    async def update_user(self,user_id: str,payload: UpdateUser,response: Response,db: Session) -> Dict[str, any]:
        try:
            user = db.query(Users).filter(and_(Users.user_id == user_id,Users.is_active == True)).first()
            if not user:
                response.status_code = status.HTTP_404_NOT_FOUND
                return { 'msg': 'User not found', 'status': status.HTTP_404_NOT_FOUND }
            
            for field, value in payload.dict(exclude_unset=True).items():
                 if value is not None:
                    setattr(user, field, value)

            db.commit()
            db.refresh(user)
            response.status_code = status.HTTP_200_OK
            return { 'msg': 'User updated successfully', 'status': status.HTTP_200_OK }
        
        except SQLAlchemyError as db_err:
            db.rollback()
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'User updation failed', 'error_detail': str(db_err), 'status': status.HTTP_400_BAD_REQUEST }
        except Exception as err:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'An unexpected error occurred', 'error_detail': str(err.args), 'status': status.HTTP_400_BAD_REQUEST }
        
    # Method to deactivate user
    async def deactivate_user(self,user_id: str,response: Response,background_tasks: BackgroundTasks,db: Session) -> Dict[str, any]:
        try:
            current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user = db.query(Users).filter(and_(Users.user_id == user_id, Users.is_active == True)).first()

            if not user:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {'msg': 'User not found', 'status': status.HTTP_404_NOT_FOUND}
            
            user.is_active = False
            user.deactivated_on = current_datetime
            db.commit()
            
            deactivation_date = datetime.strptime(current_datetime, '%Y-%m-%d %H:%M:%S').strftime('%d-%b-%Y')

            # This background task initiates the process for sending account deactivation email
            background_tasks.add_task(MailsController().send_account_deactivation_email,user.email,user.first_name,deactivation_date)
            response.status_code = status.HTTP_200_OK
            return { 'msg': 'User deactivated successfully', 'status': status.HTTP_200_OK }
        except SQLAlchemyError as db_err:
            db.rollback()
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'User deactivation failed', 'error_detail': str(db_err), 'status': status.HTTP_400_BAD_REQUEST }
        except Exception as err:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'An unexpected error occurred', 'error_detail': str(err.args), 'status': status.HTTP_400_BAD_REQUEST }
        
    
    
        

       

