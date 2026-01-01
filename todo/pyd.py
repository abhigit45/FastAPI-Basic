from pydantic import Field,BaseModel

class CreateUser(BaseModel):
    username : str= Field(min_length=3)
    email : str 
    first_name : str = Field(min_length=3,max_length=15)
    last_name : str= Field(min_length=3,max_length=15)
    password : str
    role : str


class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    description: str = Field(max_length=100, min_length= 3)
    priority : int = Field(gt=0,lt=6)
    complete: bool