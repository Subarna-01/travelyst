from fastapi import APIRouter, Depends, Response, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database.connection import get_db
from schemas.otp_schema import OTPRequest, OTPVerify
from controllers.otp_controller import OTPController

otp_router = APIRouter(prefix='/otp')

@otp_router.post('/request-otp')
async def request_otp(payload: OTPRequest,response: Response,background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    response = await OTPController().request_otp(payload,response,background_tasks,db)
    return jsonable_encoder(response)

@otp_router.post('/verify-otp/{user_id}')
async def verify_otp(user_id: str,payload: OTPVerify,response: Response,db: Session = Depends(get_db)):
    response = await OTPController().verify_otp(user_id,payload,response,db)
    return jsonable_encoder(response)