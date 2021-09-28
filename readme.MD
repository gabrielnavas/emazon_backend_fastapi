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

## Get books

```sh
curl --location --request GET 'http://localhost:5000/api/books' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' 
```


## Get a book

```sh
curl --location --request GET 'http://localhost:5000/api/books/1' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' 
```