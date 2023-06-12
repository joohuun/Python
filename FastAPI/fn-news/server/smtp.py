# # -*- coding:utf-8 -*-
# import smtplib
# from email.mime.text import MIMEText


# def send_confirm_email():
#     smtp = smtplib.SMTP('smtp.gmail.com', 587)
#     smtp.ehlo()     
#     smtp.starttls()  # TLS 사용시 필요
#     smtp.login('k00005781@gmail.com', 'muvtmumpugopmcjh')

#     msg = MIMEText('본문 테스트 메시지')
#     msg['Subject'] = '테스트'
#     msg['To'] = 'k00005781@gmail.com'

#     smtp.sendmail('k0005781@gmail.com', 'kimju0612@naver.com', msg.as_string())
#     smtp.quit()


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import bcrypt
import smtplib
from email.message import EmailMessage
import os


# MongoDB connection
client = MongoClient(os.environ.get('MONGODB_URI'))
db = client["mydatabase"]
users_collection = db["users"]

# FastAPI application
app = FastAPI()


# User model
class UserModel(BaseModel):
    email: str
    password: str
    is_active: bool = False


# User sign up
@app.post("/signup")
async def signup(user: UserModel):
    # Check if user already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    # Save user to database
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    users_collection.insert_one(user_dict)

    # Send verification email
    send_verification_email(user.email)

    return {"message": "User registered successfully"}


# Send verification email
def send_verification_email(email):
    # Create a verification URL or button, e.g., using Flask's url_for() function
    verification_url = "https://example.com/verify?email=" + email

    # Compose email
    msg = EmailMessage()
    msg["Subject"] = "Email Verification"
    msg["From"] = "noreply@example.com"
    msg["To"] = email
    msg.set_content(f"Click the link to verify your email: {verification_url}")

    # Send email using SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login("your_email@gmail.com", "your_password")
        smtp.send_message(msg)


# Verify email and activate user
@app.get("/verify")
async def verify_email(email: str):
    # Find user by email
    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # Update user's is_active field to True
    users_collection.update_one({"email": email}, {"$set": {"is_active": True}})

    return {"message": "Email verified successfully"}


# User login
@app.post("/login")
async def login(user: UserModel):
    # Find user by email
    user_data = users_collection.find_one({"email": user.email})
    if not user_data:
        raise HTTPException(status_code=400, detail="User not found")

    # Check password
    if bcrypt.checkpw(user.password.encode("utf-8"), user_data["password"]):
        if not user_data["is_active"]:
            raise HTTPException(status_code=400, detail="User is not active")

        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect password")