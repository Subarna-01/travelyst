import os
import httpx
import smtplib
from fastapi import status, Response
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import Dict
from dotenv import load_dotenv
from schemas.mails_schema import EmailSchema
from schemas.users_schema import CreateUser

load_dotenv()

class MailsController():

    def __init__(self) -> None:
        self.SMTP_SERVER = os.getenv('SMTP_SERVER')
        self.SMTP_PORT = os.getenv('SMTP_PORT')
        self.SMTP_USERNAME = os.getenv('SMTP_USERNAME')
        self.SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

    async def send_email(self,email: EmailSchema,response: Response) -> Dict[str, any]:
        try:
            msg = MIMEMultipart()
            msg['From'] = self.SMTP_USERNAME
            msg['To'] = ', '.join(email.to)
            msg['Subject'] = email.subject
            if email.cc:
                msg['Cc'] = ', '.join(email.cc)

            msg.attach(MIMEText(email.body, 'html'))

            if email.attachments:
                for file_path in email.attachments:
                    with open(file_path, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=file_path)
                    part['Content-Disposition'] = f'attachment; filename="{file_path}"'
                    msg.attach(part)

            recipients = email.to + (email.cc or []) + (email.bcc or [])

            with smtplib.SMTP(self.SMTP_SERVER, int(self.SMTP_PORT)) as server:
                server.starttls()
                server.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
                server.sendmail(self.SMTP_USERNAME, recipients, msg.as_string())
                server.quit()
            
            response.status_code = status.HTTP_200_OK
            return { 'msg': 'Email has been sent', 'status': status.HTTP_200_OK }
        except Exception as err:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return { 'msg': 'An unexpected error occurred', 'error_detail': str(err.args), 'status': status.HTTP_400_BAD_REQUEST }
        
    async def send_account_creation_email(self,payload: CreateUser) -> None:
        email_payload = {
            'to': [payload.email],
            'subject': 'Travelyst - New Sign Up',
            'body': f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Welcome to Travelyst!</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            color: #333;
                            background-color: #f4f4f4;
                            margin: 0;
                            padding: 0;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 20px auto;
                            padding: 20px;
                            background-color: #fff;
                            border-radius: 8px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        }}
                        .header {{
                            text-align: center;
                            padding-bottom: 20px;
                        }}
                        .header h1 {{
                            color: #4CAF50;
                            margin: 0;
                        }}
                        .content {{
                            text-align: center;
                        }}
                        .content p {{
                            font-size: 16px;
                            margin: 20px 0;
                        }}
                        .footer {{
                            text-align: center;
                            padding-top: 20px;
                            font-size: 12px;
                            color: #aaa;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>Welcome to Travelyst!</h1>
                        </div>
                        <div class="content">
                            <p>Hi {payload.first_name},</p>
                            <p>Congratulations on signing up with Travelyst!</p>
                            <p>We are thrilled to have you on board and can't wait for you to explore new experiences ahead with Travelyst.</p>
                            <p>Best regards,<br>The Travelyst Team</p>
                        </div>
                        <div class="footer">
                            <p>&copy; 2024 Travelyst. All rights reserved.</p>
                        </div>
                    </div>
                </body>
                </html>
            """
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post('https://travelyst.onrender.com/mail/send-email', json=email_payload)
                response.raise_for_status()
                response_json = response.json()
                if response_json['status'] == status.HTTP_200_OK:
                    print('Sign Up confirmation email has been sent')
        except Exception as err:
            print(f'Failed to send Sign Up confirmation email: {str(err.args)}')

    async def send_account_deactivation_email(self,email: str, first_name: str, deactivation_date: str) -> None:
        email_payload = {
            'to': [email],
            'subject': 'Travelyst - Account Deactivated',
            'body': f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Account Deactivated</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 20px auto;
                        padding: 20px;
                        background-color: #fff;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        text-align: center;
                        padding-bottom: 20px;
                    }}
                    .header h1 {{
                        color: #FF0000;
                        margin: 0;
                    }}
                    .content {{
                        text-align: center;
                    }}
                    .content p {{
                        font-size: 16px;
                        margin: 20px 0;
                    }}
                    .footer {{
                        text-align: center;
                        padding-top: 20px;
                        font-size: 12px;
                        color: #aaa;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Account Deactivated</h1>
                    </div>
                    <div class="content">
                        <p>Hi {first_name},</p>
                        <p>We regret to inform you that your Travelyst account has been deactivated effective from {deactivation_date}.</p>
                        <p>If you have any questions or believe this is a mistake, please contact our support team.</p>
                        <p>Best regards,<br>The Travelyst Team</p>
                    </div>
                    <div class="footer">
                        <p>&copy; 2024 Travelyst. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post('https://travelyst.onrender.com/mail/send-email', json=email_payload)
                response.raise_for_status()
                response_json = response.json()
                if response_json['status'] == status.HTTP_200_OK:
                    print('Account deactivation email has been sent')
        except Exception as err:
            print(f'Failed to send account deactivation email: {str(err.args)}')

    async def send_otp_email(self,email: str,first_name: str,otp: int) -> None:
        email_payload = {
            'to': [email],
            'subject': 'Travelyst - OTP Code',
            'body': f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Your OTP Code</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        color: #333;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    h1 {{
                        color: #007bff;
                    }}
                    p {{
                        font-size: 16px;
                        line-height: 1.5;
                    }}
                    .otp {{
                        font-size: 24px;
                        font-weight: bold;
                        color: #007bff;
                    }}
                    .footer {{
                        margin-top: 20px;
                        font-size: 12px;
                        color: #777;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Your OTP Code</h1>
                    <p>Hi {first_name},</p>
                    <p>Thank you for using our service. Your One-Time Password (OTP) for authentication is:</p>
                    <p class="otp">{otp}</p>
                    <p>Please enter this code to proceed. This OTP is valid for the next 10 minutes.</p>
                    <p>If you did not request this OTP, please ignore this email or contact our support team.</p>
                    <div class="footer">
                        <p>Best regards,</p>
                        <p>The Travelyst Team</p>
                        <p><a href="mailto:support@travelyst.com">support@travelyst.com</a></p>
                    </div>
                </div>
            </body>
            </html>
            """
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post('https://travelyst.onrender.com/mail/send-email', json=email_payload)
                response.raise_for_status()
                response_json = response.json()
                if response_json['status'] == status.HTTP_200_OK:
                    print('OTP request email has been sent')
        except Exception as err:
            print(f'Failed to send OTP request email: {str(err.args)}')

