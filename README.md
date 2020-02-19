# Web-service "Library"
Simple example of a rest-service using Flask

## Installation
```bash
$ git clone git@github.com:rg-golubkov/library_rest_service.git
$ cd ./library_rest_service
$ docker build -t library_rest_service .
```

## Usage
```bash
$ docker run --rm -it -p 5000:5000 library_rest_service
```

Now you can test rest-api at the following urls:

- http://localhost:5000/api/books/
- http://localhost:5000/api/authors/

For example:
```bash
$ curl -i -H "Content-Type: application/json" \
     -X GET http://localhost:5000/api/authors/

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 160

{
    "authors": [
        {"author_id":1,"fullname":"Henry Charles Bukowski"},
        {"author_id":2,"fullname":"Nelle Harper Lee"},
        {"author_id":3,"fullname":"Arthur Conan Doyle"}
    ]
}

$ curl i -H "Content-Type: application/json" \
    -X POST -d '{"fullname":"Bjarne Stroustrup"}' \
    http://localhost:5000/api/authors/

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 47

{"author_id":4,"fullname":"Bjarne Stroustrup"}

$ curl -i -H "Content-Type: application/json" \
     -X GET http://localhost:5000/api/authors/4

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 47

{"author_id":4,"fullname":"Bjarne Stroustrup"}
```

## Configuration
You can configurate flask port using envairoment variable:
```bash
$ docker run --rm --env FLASK_PORT=5001 -it -p 5001:5001 library_rest_service
```

Use the file `application.cfg` in `instance` folder to configure Flask application.

## Tests
You can run tests with following command:
```bash
$ python3 -m unittest discover ./tests
```
