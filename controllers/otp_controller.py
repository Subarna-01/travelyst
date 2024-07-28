import random
from datetime import datetime, timedelta
from fastapi import Response, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict
from schemas.otp_schema import OTPRequest, OTPVerify
from models.users_model import Users
from controllers.mails_controller import MailsController

class OTPController():

    def __init__(self) -> None:
        pass

    # Method to check if otp received is valid
    def is_otp_valid(self,otp_generated_on,validity_minutes=10):
        
        if otp_generated_on is None:
            return False
        
        current_datetime = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
        return current_datetime - otp_generated_on < timedelta(minutes=validity_minutes)
    
    # Method to request otp
    async def request_otp(self,payload: OTPRequest,response: Response,background_tasks: BackgroundTasks,db: Session) -> Dict[str, any]:
        try:
            user = db.query(Users).filter(Users.username == payload.username, Users.email == payload.email, Users.is_active == True).first()
            
            if not user:
                response.status_code = status.HTTP_404_NOT_FOUND
                return {'msg': 'User not found', 'status': status.HTTP_404_NOT_FOUND}
            
            otp = random.randint(100000, 999999)
            user.otp = otp
            user.otp_generated_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            db.commit()
            
            # This background task initiates the process for sending otp email
            background_tasks.add_task(MailsController().send_otp_email,user.email,user.first_name,otp)
            response.status_code = status.HTTP_200_OK
            return { 'msg': 'OTP sent successfully', 'user_id': user.user_id, 'status': status.HTTP_200_OK }
        except SQLAlchemyError as db_err:
            db.rollback()
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'OTP request failed', 'error_detail': str(db_err), 'status': status.HTTP_400_BAD_REQUEST }
        except Exception as err:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'An unexpected error occurred', 'error_detail': str(err.args), 'status': status.HTTP_400_BAD_REQUEST }

    # Method to verify otp    
    async def verify_otp(self,user_id: str,payload: OTPVerify,response: Response,db: Session) -> Dict[str, any]:
        try:
            otp = int(payload.otp)
            user = db.query(Users).filter(Users.user_id == user_id,Users.is_active == True).first()

            if not user or user.otp != otp or not self.is_otp_valid(user.otp_generated_on):
                response.status_code = status.HTTP_400_BAD_REQUEST
                return { 'msg': 'Invalid OTP', 'status': status.HTTP_400_BAD_REQUEST }
    
            response.status_code = status.HTTP_200_OK
            return { 'msg': 'OTP verified successfully', 'status': status.HTTP_200_OK }
        except SQLAlchemyError as db_err:
            db.rollback()
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'OTP request failed', 'error_detail': str(db_err), 'status': status.HTTP_400_BAD_REQUEST }
        except Exception as err:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'An unexpected error occurred', 'error_detail': str(err.args), 'status': status.HTTP_400_BAD_REQUEST }
        

