# from fastapi import FastAPI
# from database import SessionLocal, engine
# import models
# from todo.database import SessionLocal, engine



# from routers import auth,todos,admin,users


# app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

# app.include_router(auth.router)
# app.include_router(todos.router)
# app.include_router(admin.router)
# app.include_router(users.router)

from fastapi import FastAPI
from todo.database import SessionLocal, engine
from todo import models
from todo.models import Todo

from todo.routers import auth, todos, admin, users

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


