from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import modules.books.models as book_models
import modules.users.models as users_models

from modules.books.controllers import router as books_router
from modules.users import token_router, users_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router)
app.include_router(token_router)
app.include_router(users_router)


@app.on_event("startup")
async def startup_event():
    def init_tables():
        book_models.create_tables()
        users_models.create_tables()

    init_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}
