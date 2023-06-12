from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from ..database import (
    retrieve_students,
    add_student,
    retrieve_student,
    retrieve_student_by_email,
    update_student,
    delete_student,
)

from ..models.student import (
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel,
)

router = APIRouter()

@router.post("/", response_description="create student")
async def add_student_data(student: StudentSchema=Body(...)):
    student = jsonable_encoder(student)
    
    existing_student = await retrieve_student_by_email(student["email"])
    if existing_student:
        return ResponseModel(existing_student, "이미 존재 하는 학생입니다.")
    
    new_student = await add_student(student)
    return ResponseModel(new_student, "학생 추가")


@router.get("/", response_description="get students")
async def get_students_data():
    students = await retrieve_students()
    if students:
        return ResponseModel(students, "학생 리스트 조회")
    return ResponseModel(students, "학생 리스트 없음")


@router.get("/{id}", response_description="get student")
async def get_student_data(id):
    student = await retrieve_student(id)
    print(student)
    if student:
        return ResponseModel(student, "학생 조회")
    return ErrorResponseModel("에러", 404, "조회된 학생 없음")


@router.put("/{id}", response_description="update student")
async def update_student_data(id:str, req: UpdateStudentModel=Body(...)):
    update_data = req.dict(exclude_unset=True)
    updated_student = await update_student(id, update_data)
    if updated_student:
        return ResponseModel(update_data, "{} 학생 업데이트.".format(id))
    return ErrorResponseModel("에러", 404, "조회된 학생 없음")


@router.delete("/{id}", response_description="delete student")
async def delete_student_data(id:str):
    deleted_student = await delete_student(id)
    if deleted_student:
        return ResponseModel(deleted_student, "{} 학생 삭제".format(id))
    return ErrorResponseModel("에러", 404, "{} 조회된 학생 없음")