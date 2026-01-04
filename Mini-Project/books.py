from fastapi import FastAPI,Body
app = FastAPI()



Books = [
   {
     "isbn": "9781593275846",
     "title": "one",
     "subtitle": "A Modern Introduction to Programming",
     "author": "Sanjiv",
     "published": "2014-12-14T00:00:00.000Z",
     "publisher": "No Starch Press",
     "pages": 472,
     "category": "Math",
     "website": "http://eloquentjavascript.net/"
   },
   {
     "isbn": "9781449331818",
     "title": "Two",
     "subtitle": "A JavaScript and jQuery Developer's Guide",
     "author": "Addy Osmani",
     "published": "2012-07-01T00:00:00.000Z",
     "publisher": "O'Reilly Media",
     "pages": 254,
     "category": "Math",
     "website": "http://www.addyosmani.com/resources/essentialjsdesignpatterns/book/"
   },
   {
     "isbn": "9781449365035",
     "title": "Three",
     "subtitle": "An In-Depth Guide for Programmers",
     "author": "Sanjiv",
     "published": "2014-02-01T00:00:00.000Z",
     "publisher": "O'Reilly Media",
     "pages": 460,
     "category": "Like it or not, JavaScript is everywhere these days-from browser to server to mobile-and now you, too, need to learn the language or dive deeper than you have. This concise book guides you into and through JavaScript, written by a veteran programmer who once found himself in the same position.",
     "website": "http://speakingjs.com/"
   }
 ]


@app.get("/books")
async def getAlltBook():
    # return {"Message":"Hello Abhishek"}
    return Books


# path parameter
@app.get("/books/{bookTitle}")
def getBook(bookTitle: str):
    for book in Books:
        if book.get("title").casefold() == bookTitle.casefold():
            return book



# quary parameters
@app.get("/book/")
async def getBookByCategory(in_category: str):
    cat = []
    for book in Books:
        if book.get("category").casefold() == in_category.casefold():
            cat.append(book)
    return cat

@app.get("/book/{Authour}/")
async def getBookByAuthorAndCategory(in_Author:str,int_category:str):
    lst = []
    for book in Books:
        if book.get("author").casefold() == in_Author.casefold() and book.get("category").casefold() == int_category.casefold():
            lst.append(book)
    return lst

# post
@app.post("/createBody/")
async def addBook(new_body = Body()):
    Books.append(new_body)
        
# update
@app.put("/update/")
async def updateBook(update_book = Body()):
    for i in range(len(Books)):
        if Books[i].get("title").casefold() == update_book.get("title").casefold():
            Books[i] = update_book

# delete        
@app.delete("/delete/")
async def bookDelete(delete: str):
    for i in range(len(Books)):
        if Books[i].get("title").casefold() == delete.casefold():
            Books.pop(i)
            break
    
# Assigment
@app.get("/getBook/{in_author}")
async def fetchBookByAuthor(in_author:str):
    lst = []
    for book in Books:
        if book.get("author").casefold() == in_author.casefold():
            lst.append(book)
    return lst

        