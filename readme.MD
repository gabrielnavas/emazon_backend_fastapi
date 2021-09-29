# Users

## Create user

```sh
curl --location --request POST 'http://localhost:5000/api/users' \
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
curl --location --request POST 'http://localhost:5000/api/users/token' \
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
curl --location --request GET 'http://localhost:5000/api/shop/book/{book_id}' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' 
```


## Get list of book.id

```sh
curl --location --request GET 'http://localhost:5000/api/shop/books/get_ids' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' 
```



## Get all book pagineted

```sh
# is_paginator_id =  {true or false}
# limit={limit number or 0 to all}
# book_per_page={how much por page}

curl --location --request GET 'http://localhost:5000/api/shop/book/?is_paginator_id=true&limit={0}&book_per_page={10}' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' 
```

## Get a page book pagineted

```sh
# is_paginator_id =  {true or false}
# limit={limit number or 0 to all}
# book_per_page={how much por page}
# page={page number}

curl --location --request GET 'http://localhost:5000/api/shop/book/?is_paginator_id=true&limit={0}&book_per_page={10}&page={0}' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' 
```