from behave import when
from django.test import Client
from bookings.models import Seat

@when('I navigate to the movie listing page')
def step_navigate_movie_list(context):
    """Navigate to movie listing page"""
    context.client = Client()
    response = context.client.get('/')
    context.response = response

@when('I navigate to the seat selection page')
def step_navigate_seat_selection(context):
    """Navigate to seat selection page"""
    context.client = Client()
    movie = context.selected_movie
    response = context.client.get(f'/movie/{movie.id}/book/')
    context.response = response

@when('I select an available seat')
def step_select_available_seat(context):
    """Select an available seat"""
    movie = context.selected_movie
    seat = Seat.objects.filter(movie=movie, status='available').first()
    context.selected_seat = seat

@when('I confirm the booking')
def step_confirm_booking(context):
    """Confirm the booking"""
    context.client = Client()
    movie = context.selected_movie
    seat = context.selected_seat

    response = context.client.post(
        f'/movie/{movie.id}/book/',
        {'seat_id': seat.id}
    )
    context.response = response

@when('I try to book the booked seat')
def step_try_book_booked_seat(context):
    """Try to book an already booked seat"""
    context.client = Client()
    movie = context.selected_movie
    seat = context.booked_seat

    response = context.client.post(
        f'/movie/{movie.id}/book/',
        {'seat_id': seat.id}
    )
    context.response = response

@when('I navigate to the booking history page')
def step_navigate_booking_history(context):
    """Navigate to booking history page"""
    context.client = Client()
    response = context.client.get('/history/')
    context.response = response
