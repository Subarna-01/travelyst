from fastapi import APIRouter, Response
from fastapi.encoders import jsonable_encoder
from schemas.mails_schema import EmailSchema
from controllers.mails_controller import MailsController

mails_router = APIRouter(prefix='/mail')

@mails_router.post('/send-email')
async def send_email(email: EmailSchema,response: Response):
    response = await MailsController().send_email(email,response)
    return jsonable_encoder(response)