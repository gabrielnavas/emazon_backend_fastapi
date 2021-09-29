from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.users import token_router, users_router
from modules.books.controllers.get_book import router as get_book_router
from modules.books.controllers.get_books_id import router as get_books_id_router
from modules.books.controllers.get_books import router as get_books_router

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

# users
app.include_router(token_router)
app.include_router(get_books_id_router)

# books
app.include_router(get_book_router)
app.include_router(get_book_router)
app.include_router(get_books_router)


@app.on_event("startup")
async def startup_event():
    # from main.init_tables_database import init_tables
    # init_tables()

    # from main.init_dev_data import init_dev_data
    # init_dev_data()
    pass


@app.get("/")
async def root():
    return {"message": "Hello World"}
