from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.users import login_router, register_router

from modules.books.controllers.get_book import router as get_book_router
from modules.books.controllers.get_books_page import router as get_books_page_router

from modules.stores.controllers import router as open_store_router

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
app.include_router(login_router)
app.include_router(register_router)

# books
app.include_router(get_book_router)
app.include_router(get_books_page_router)


# store
app.include_router(open_store_router)


@app.on_event("startup")
async def startup_event():
    import os

    env = os.getenv('ENV')
    if env == 'dev':
        from main.init_tables_database import init_tables
        from main.init_dev_data import init_dev_data
        for function_startup_before in [init_tables, init_dev_data]:
            # function_startup_before()
            pass


@app.get("/")
async def root():
    return {"message": "I AM WORKING. :)"}
