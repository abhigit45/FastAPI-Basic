from fastapi import FastAPI,Body,Path,HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id:int
    title:str
    description:str
    author:str
    rating:int
    published_date: int
    
    def __init__(self,id,title,description,author,rating,publish_date):
        self.id = id
        self.title = title
        self.description = description
        self.author = author
        self.rating = rating
        self.published_date = publish_date
        
class BookRequest(BaseModel):
    id:Optional[int] = Field(description="ID is not neeeded to create",default=None)
    title:str = Field(min_length= 5)
    description:str = Field(min_length=5,max_length=100)
    author:str = Field(min_length=3)
    rating:int = Field(gt=-1,lt=6)
    published_date: int 
    
    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"write your book title",
                "description":"Enter your Descriotion here",
                "author":"Enter Author Name",
                "rating":"rating of book between 1 to 5",
                "published_date":"2012"
            }
        }
    }
    

BOOKS = [
    Book(1, "Python Basics", "Introduction to Python programming", "Guido van Rossum", 5,2013),
    Book(2, "Django for Beginners", "Web development using Django framework", "William S. Vincent", 4,2012),
    Book(3, "Flask Web Development", "Building web apps with Flask", "Miguel Grinberg", 4,2012),
    Book(4, "Data Structures in Python", "DSA concepts with Python examples", "Narasimha Karumanchi", 5,2015),
    Book(5, "Machine Learning Basics", "Introduction to ML algorithms", "Andrew Ng", 5,2012),
    Book(6, "Clean Code", "Best practices for writing clean code", "Robert C. Martin", 5,2011)
]

@app.get("/Books",status_code=status.HTTP_200_OK)
async def read_all_book():
    return BOOKS

 
@app.post("/create-book",status_code=status.HTTP_201_CREATED)    
async def add_Book(create_book : BookRequest):
    new_book = Book(**create_book.dict())
    print(new_book)
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    # book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book




@app.get("/getBook/{id}",status_code=status.HTTP_200_OK)
def find_book(id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == id:
            return book
    raise HTTPException(status_code=404,detail="Book not found")
      

@app.get("/by-rating",status_code=status.HTTP_200_OK)
def fetch_by_rating(rating:int):
    lst = []
    for book in BOOKS:
        if book.rating == rating:
            lst.append(book)
    return lst

@app.put("/updateBook",status_code=status.HTTP_204_NO_CONTENT)
def update_book(update : BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].title == update.title:
            BOOKS[i] = update
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not Updated")
        
        

@app.delete("/delete")
async def delete_book(id:int):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == id:
            BOOKS.pop(i)
            break
    if not book_changed:
        raise HTTPException(status_code=404,detail="Book not found for delete")

    
@app.get("/publishDate")
async def publish_date(publish:int):
    lst = []
    for book in BOOKS:
        if book.published_date == publish:
            lst.append(book)
    return lst