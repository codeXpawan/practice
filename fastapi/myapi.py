from fastapi import FastAPI, Path, Query, Body, Response, Cookie, Header
from typing import Optional,Annotated,Union, List
from pydantic import BaseModel, Field
#different type of data types can be added like time, date, UUID (unique id-generally used for database)
# from uuid import UUID
# from datetime import datetime,time,timedelta


app = FastAPI()

students = {
    1: {
        "name": "pawan",
        "age": 21,
        "year": "year 12"
    }
}

@app.get("/")
def index():
    return {"name" : "First Data"}
#path parameter
@app.get("/get-student/{student_id}")
def get_student(student_id: Annotated[int,Path(title='ID of student',description="STUDENT_ID",ge=1,gt = 0,lt = 101,le = 100)] ):
    # if student_id not in students:
        # response.status_code = 404
    return students[student_id]
#validation for path parameters
#qwery parameter
@app.get("/get-by-name")
def get_student(name : Annotated[Union[str,None], Query(
    min_length=3,
    alias="item-query",
    title="student name",
    description="give the query of student name",
    max_length=50,
    deprecated=True)] = None): # for default value we can use default in place of None and also for explicitly required we can use '...'
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"data":"Not found"}

#getting multiple query paramter
@app.get('/get-multiple-query')
async def multiple_query(names: Annotated[list[str], Query()] = None ):
    if names is None:
        return {"data": "No names provided"}
    
    result = []
    for name in names:
        for student_id, student_info in students.items():
            if student_info["name"] == name:
                result.append(student_info)
                break  # Stop searching if found
    
    if result:
        return result
    else:
        return {"data": "Not found"}
#combination of query and path parameter
@app.get("/get-data/{student_id}")
def get_data(student_id: int, name : Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"data":"Not found"}
#post method
#for the validation of the model Fields are used
class Student(BaseModel):
    name : str = Field(examples=["pawan"],max_length=50)        #example is available in every Json schema like Path, Query, Header, Cookie, Body, Form, File 
    age : int = Field(gt= 10)
    year : str | None = Field(title="year")
    tags: list[str] =[] #list of string
    #tags: set[str] = set()
    # class Config:
    #     schema_extra = {
    #         "example":[
    #             {
    #                 "name":"Pawan",
    #                 "age":22,
    #                 "year":"year 001",
    #                 "tags":"01"
    #             }
    #         ]
    #     }
    
class Library(BaseModel):
    book_id : int
    student : Student #nested json object
@app.post("/create-student/{student_id}")
def create_student(student_id : int, student : Student,importance: Annotated[int, Body(gt=0)] ): #Body is used to define that it should accept it in json format
    if student_id in students:
        return {"Error": "Student exists"}
    
    students[student_id] = student
    return students[student_id]
#incase of passing the whole dictnory(JSON with a key) we can use Body(embed=True)
#will expect {"key":{"parameters1":"val"}}
#put method
class Update_student(BaseModel):
    name : Optional[str] = None
    age : Optional[int] = None
    year : Optional[int] = None
@app.put("/update-student/{student_id}",response_model=Student)
def student_update(student_id : int, student : Annotated[Update_student,Body(openapi_examples={
    "normal":{
        "summary":"A **normal** example",
        "description":"A **normal** item works correctly",
        "value":{
            "name":"pawan",
            "age": 12,
            "year":"year 001"
            }
    },
    "converted":{
        "description":"An example",
        "value":{
            "name":"pawan"
        }
    }
    
})]):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.year != None:
        students[student_id].year = student.year
    
    return students[student_id]
#delete method
@app.delete("/delete-student/{student_id}")
def delete_student(student_id : int):
    if student_id not in students:
        return {"Error":"Student do not exist"}
    del students[student_id]
    return {"Message": "Student deleted sucessfully"}

#getting int or float type data from api
#JSON only supports str as keys.
#But Pydantic has automatic data conversion.
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights

@app.get("/cookie-student/")
async def cookie(ads_id: Annotated[str,Cookie()]=None):
    return {"ads_id": ads_id}

@app.get("/header-student")
async def header(strange_header: Annotated[str| None,Header(convert_underscores=False)]):
    return {"strange_header": strange_header}

