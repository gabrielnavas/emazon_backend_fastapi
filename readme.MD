# Users

## Create user

```sh
curl --location --request POST '/api/register' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "full_name": "user name",
    "email": "user@gmail.com",
    "password": "123456",
    "password_confirmation": "123456"
}'
```

## Login

```sh
curl --location --request POST '/api/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "user@gmail.com",
    "password": "123456",
}'
```

# Shop

## Get a book
```sh
# book_id={id from book}
curl --location --request GET '/api/shop/book/{book_id}' \
--header 'Content-Type: application/json' 
```

## get a img
```sh
curl --location --request GET 'http://localhost:5000/api/book/imgs?file_name=name_book.jpeg' \
--header 'Authorization: <token>'
```


## Get pages limit

```sh
# length_per_page={how much books per page}

curl --location --request GET '/api/shop/books/pages_limit?length_per_page=10' \
--header 'Content-Type: application/json' 
```

## Get a page book pagineted

```sh
# page={page of books}
# length_per_page={how much books per page}

curl --location --request GET '/api/shop/books/page?page=1&length_per_page=10' \
--header 'Content-Type: application/json' 
```


# Stores

# open store

```sh
curl --location --request POST 'http://localhost:5000/api/open_store' \
--header 'Authorization: <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "fantasy_name": "nome fantasia",
    "cpf": "cpf...",
    "cnpj": undefined
}
'
```

# add book
```sh
curl --location --request POST 'http://localhost:5000/api/book' \
--header 'Authorization: <token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "titulo do livro",
    "published_at": "2020-05-20",
    "description": "uma descricao legal",
    "price": 22.5,
    "discount": 0.20,
    "pages_amount": 101,
    "heigh": 0.40,
    "width": 0.20,
    "thickness": 0.05,
    "author_id": 1,
    "type_cover_id": 1,
    "language_id": 1,
    "category_id": 1,
    "publishing_company_id": 1,
    "store_id": 1
}'
```


# add book imgs
```sh
curl --location --request POST 'http://localhost:5000/api/book/imgs?book_id=51' \
--header 'Authorization: <token>' \
--form 'files=@"/home/navas/MEMES/FAjhTTzXEAMDd-4.jpeg"' \
--form 'files=@"/home/navas/MEMES/FATFHjQVIA8mmq5.jpeg"' \
--form 'files=@"/home/navas/MEMES/FAUJfqhVgAQlnan.png"'
```
