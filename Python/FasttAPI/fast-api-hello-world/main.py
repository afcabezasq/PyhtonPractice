#Python
from doctest import Example
from email import message
from optparse import Option
from tkinter.tix import Form
from typing import Optional
from enum import Enum

#Pydantic


from pydantic import BaseModel, Field, EmailStr

#FastApi
from fastapi import FastAPI
from fastapi import Body, Query, Path, status, Form, Header, Cookie, File, UploadFile

app = FastAPI()

#Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Andres" 
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Cabezas"
    )
    age: int = Field(
        ...,
        gt = 0,
        le = 115,
        example=27
    )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None, example=True)
    

class Person(PersonBase):    
    password: str =  Field(..., min_length=8)

class PersonOut(PersonBase):
    pass


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example = "miguel2021")

    # class Config:
    #     schema_extra = {
    #         "example":{
    #             "first_name": "Andres Felipe",
    #             "last_name": "Cabezas Quicano",
    #             "age":27,
    #             "hair_color": "brown",
    #             "is_married": False                
    #         }
    #     }

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK)
def home():
    return {
        "Hello": "World"
    }

# Request and Response Body

@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED)
def create_person(person: Person = Body(...)): ## ... request body es obligario
    return person


#Query parameters validations

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title= "Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocio"
        ),
    age: Optional[str] = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25
        ) 
):
    return{name: age}

## Validation Query
# max_length
# min_length
# regex
#ge -> greater or equal than
#le -> less or equal than
#gt -> greater than
#lt -> less than

#title ->
#description ->

#Validations: path parameters
@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        ..., 
        gt=0, 
        title="Person Id",
        description="The id of a person. Should be a value greater than 0"), # ... parametro obligatorio,
        example= 123    
):
    return {person_id: "It exist"}


#Validations: request body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(
        ...,
        title="Person Id",
        description="This is the person ID",
        gt=0   
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    result = person.dict()
    result.update(location.dict())
    return result
    # return person
## Special Data Types

#classic ones
# string -> str
# int 
# float
# bool


#exotic ones
# enum
# httpUrl
# FilePath 
#Directory path
#EmailStr
#Payment Card Number
#IpvAnyAddress
# Negative Float
#Positive Float
#Negative Int
#Positive Int
# https://pydantic-docs.helpmanual.io/ 


@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username=username)


#Cookies and Headers

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str =  Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent


#Files

##Upload File

#  Filename    Content_type   File


@app.post(
    path="/post-image"
)
def post_image(
    image: UploadFile = File(...)
):
    return{
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }