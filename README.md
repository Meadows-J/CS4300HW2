# Movie Theater Booking Application

A RESTful Movie Theater Booking Application built with Python and Django. The application allows users to view movies, book seats, and check their booking history through both an attractive web interface and a complete REST API.

## Features
A home page that lists all moviues with title, information, and allows the user to click to the booking page.
Booking page allows for th user to select from open seats and confirm their booking.
On the bookings page it shows which movies are booked and which seats are saved.

## Tech Stack

Python 3.11.1
Django 6.0.3
Django REST Framework 3.16.1
SQLite (development) / PostgreSQL (production)
Bootstrap 5.3


### Local Development

The virtaul enviorment has Dijango, djangorestframework, and Behave.

Run this command From the homework2 folder to start the server.
python manage.py runserver 0.0.0.0:3000

Web Interface: http://localhost:3000/
Admin Panel: http://localhost:3000/admin/
API: http://localhost:3000/api/

## API Endpoints
/api/movies/ - List all movies
/api/seats/ - List all seats
/api/bookings/ - List user's bookings

## Running Tests
From the homework2 folder run:
python manage.py test

This will run all unit tests

## Deployment to Render
The main URL https://movie-theater-booking-5swg.onrender.com
To fill out the database go to https://movie-theater-booking-5swg.onrender.com/api/movies/ to add any movies you want.

## AI Usage Notes
I already have a lot of Dijango experince from previous classes so I read over all the documentation as a reminder. I used Cluade Haiku 4.5 in the terminal to help build out the project as this is the methoad my group has decided to do the project with. I practiced asking it to build out feature and reviewd all the code before using it. I used a variety of types of promt to experiment what claude would do or each feature and used a lot of its code in the final product after I tweaked it and reviewed it.
