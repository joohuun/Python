import motor.motor_asyncio
from bson.objectid import ObjectId
from ..env import MONGO_URI


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

db= client.students

student_collection = db.get_collection('student_collection')


# helper -> 데이터베이스 쿼리의 결과를 python dict로 구문 분석하기 위한 함수
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "year": student["year"],
        "gpa": student["gpa"],
    }


async def retrieve_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


async def add_student(student_data: dict):
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


async def retrieve_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


async def retrieve_student_by_email(email):
    student = await student_collection.find_one({"email": email})
    if student:
        return student_helper(student)


async def update_student(id: str, data: dict):
    if not data:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        return bool(updated_student)


async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True