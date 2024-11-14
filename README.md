# Airport Service API
**Airport Service API** is a REST API for managing airports, 
flights and flowers. The system allows you to manage information 
about the city, airports, routes, flights, 
as well as create and manage users, including administrators with 
advanced rights.

## Installing using GitHub

Python3 must be already installed
Install PostgresSQL and create DB 

``` shel
git clone https://github.com/AndreiVed/airport-service-api/
cd Airport-Service-API
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set POSTGRES_HOST=db
set POSTGRES_PORT=5432
set POSTGRES_NAME=airport
set POSTGRES_USER=airport
set POSTGRES_PASSWORD=airport
python manage.py migrate
python manage.py runserver 
```

## Run with docker

Docker should be installed

``` shel
docker-compose build
docker-compose up
```

## Getting access

* admin access:
    email: admin@admin.com
    password: 1qazcde3
* create user via /api/v1/user/register/
* get access token via /api/v1/user/token/

## Features

* JWT authenticated
* Admin panel
* Documentation is located at api/v1/schema/swagger/
* Managing orders and tickets 
* Ticket validation checks the uniqueness of the seat and row, 
and checks that the seat and row are present on the plane)
* Creating airplanes with airplane type and manufacturer
* Add image to airplanes
* Creating routes with source and destination airports, included cities and countries
* Creating flights with route, staff, departure and arrival date/time
* Date validation check that the departure date is earlier than the arrival date
* Filtering flights by routes, destination city and departure date
