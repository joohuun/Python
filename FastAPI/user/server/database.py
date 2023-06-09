import motor.motor_asyncio
from bson.objectid import ObjectId
from ..env import MONGO_DETAILS


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

db= client.users

user_col = db.get_collection('users')


async def get_user(email):
    existed_user = await user_col.find_one({'email':email})
    if existed_user:
        return existed_user


async def add_user(user_data: dict):
    user = await user_col.insert_one(user_data)
    new_user = await user_col.find_one({"_id": user.inserted_id})
    return new_user


