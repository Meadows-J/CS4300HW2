from behave import given
from bookings.models import Movie, Seat, Booking
from django.contrib.auth.models import User
from datetime import datetime

@given('there are movies available')
def step_create_movies(context):
    """Create test movies"""
    if not Movie.objects.filter(title='Test Movie').exists():
        Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_date='2024-01-01',
            duration=120
        )

@given('there are no movies available')
def step_no_movies(context):
    """Ensure no movies exist"""
    Movie.objects.all().delete()

@given('I have selected a movie')
def step_select_movie(context):
    """Select a movie for testing"""
    movie = Movie.objects.first()
    if not movie:
        movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_date='2024-01-01',
            duration=120
        )
    context.selected_movie = movie

@given('there are available seats')
def step_create_available_seats(context):
    """Create available seats for selected movie"""
    movie = context.selected_movie
    Seat.objects.filter(movie=movie).delete()
    for i in range(1, 6):
        Seat.objects.create(
            movie=movie,
            seat_number=f'A{i}',
            status='available'
        )

@given('there is a booked seat')
def step_create_booked_seat(context):
    """Create a booked seat"""
    movie = context.selected_movie
    seat = Seat.objects.create(
        movie=movie,
        seat_number='B1',
        status='booked'
    )
    context.booked_seat = seat

@given('I have made bookings')
def step_create_bookings(context):
    """Create test bookings"""
    user = context.test_user
    movie = context.test_movie
    seats = Seat.objects.filter(movie=movie, status='available')[:2]

    for seat in seats:
        Booking.objects.create(
            movie=movie,
            seat=seat,
            user=user
        )
        seat.status = 'booked'
        seat.save()

@given('I have not made any bookings')
def step_no_bookings(context):
    """Ensure no bookings exist"""
    Booking.objects.all().delete()
