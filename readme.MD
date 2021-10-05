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