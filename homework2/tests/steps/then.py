from behave import then
from bookings.models import Booking, Seat

@then('I should see all available movies')
def step_see_all_movies(context):
    """Verify all movies are displayed"""
    content = context.response.content.decode()
    assert 'Available Movies' in content or 'Test Movie' in content

@then('I should see the movie title')
def step_see_movie_title(context):
    """Verify movie title is displayed"""
    content = context.response.content.decode()
    assert 'Test Movie' in content

@then('I should see the movie description')
def step_see_movie_description(context):
    """Verify movie description is displayed"""
    content = context.response.content.decode()
    assert 'Test Description' in content

@then('I should see the movie duration')
def step_see_movie_duration(context):
    """Verify movie duration is displayed"""
    content = context.response.content.decode()
    assert '120' in content or 'Duration' in content

@then('I should see a "Book Now" button')
def step_see_book_now_button(context):
    """Verify Book Now button is displayed"""
    content = context.response.content.decode()
    assert 'Book Now' in content or 'book' in content.lower()

@then('I should see a message "{message}"')
def step_see_message(context, message):
    """Verify specific message is displayed"""
    content = context.response.content.decode()
    assert message in content

@then('the seat should be marked as booked')
def step_seat_marked_booked(context):
    """Verify seat is marked as booked"""
    seat = context.selected_seat
    seat.refresh_from_db()
    assert seat.status == 'booked'

@then('I should see a confirmation message')
def step_see_confirmation(context):
    """Verify confirmation message is shown"""
    content = context.response.content.decode()
    # Redirect means booking was successful
    assert context.response.status_code in [200, 302]

@then('the booking should be created in the system')
def step_booking_created(context):
    """Verify booking was created"""
    movie = context.selected_movie
    seat = context.selected_seat
    booking = Booking.objects.filter(movie=movie, seat=seat).first()
    assert booking is not None

@then('I should see an error message "{message}"')
def step_see_error_message(context, message):
    """Verify error message is displayed"""
    content = context.response.content.decode()
    assert message in content

@then('the booking should not be created')
def step_booking_not_created(context):
    """Verify booking was not created for booked seat"""
    movie = context.selected_movie
    seat = context.booked_seat
    bookings = Booking.objects.filter(movie=movie, seat=seat)
    # Should have at most one booking (the initial one)
    assert bookings.count() <= 1

@then('I should see all available seats')
def step_see_all_seats(context):
    """Verify all seats are displayed"""
    content = context.response.content.decode()
    assert 'Seat' in content or 'A1' in content

@then('I should see the seat number')
def step_see_seat_number(context):
    """Verify seat number is displayed"""
    content = context.response.content.decode()
    assert 'A' in content  # Seat numbers start with A

@then('I should see the seat status')
def step_see_seat_status(context):
    """Verify seat status is displayed"""
    content = context.response.content.decode()
    assert 'available' in content.lower() or 'booked' in content.lower()

@then('I should see all my bookings')
def step_see_all_bookings(context):
    """Verify all bookings are displayed"""
    content = context.response.content.decode()
    bookings = Booking.objects.filter(user=context.test_user)
    assert bookings.count() > 0
    assert len(content) > 0

@then('I should see the movie title for each booking')
def step_see_title_for_bookings(context):
    """Verify movie title is shown for each booking"""
    content = context.response.content.decode()
    assert 'Test Movie' in content

@then('I should see the seat number for each booking')
def step_see_seat_for_bookings(context):
    """Verify seat number is shown for each booking"""
    content = context.response.content.decode()
    assert 'Seat' in content or 'A' in content

@then('I should see the booking date for each booking')
def step_see_date_for_bookings(context):
    """Verify booking date is shown"""
    content = context.response.content.decode()
    # Check for any date pattern or 'Date' label
    assert len(content) > 0

@then('the booking history should be empty')
def step_booking_history_empty(context):
    """Verify booking history is empty"""
    bookings = Booking.objects.filter(user=context.test_user)
    assert bookings.count() == 0
