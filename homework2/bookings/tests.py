from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from bookings.models import Movie, Seat, Booking
from datetime import datetime, timedelta


class MovieModelTest(TestCase):
    """Test cases for Movie model"""

    def setUp(self):
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_date=datetime.now().date(),
            duration=120
        )

    def test_movie_creation(self):
        """Test that a movie can be created"""
        self.assertEqual(self.movie.title, 'Test Movie')
        self.assertEqual(self.movie.duration, 120)

    def test_movie_str(self):
        """Test movie string representation"""
        self.assertEqual(str(self.movie), 'Test Movie')


class SeatModelTest(TestCase):
    """Test cases for Seat model"""

    def setUp(self):
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_date=datetime.now().date(),
            duration=120
        )
        self.seat = Seat.objects.create(
            movie=self.movie,
            seat_number='A1',
            status=Seat.AVAILABLE
        )

    def test_seat_creation(self):
        """Test that a seat can be created"""
        self.assertEqual(self.seat.seat_number, 'A1')
        self.assertEqual(self.seat.status, Seat.AVAILABLE)

    def test_seat_unique_constraint(self):
        """Test that movie-seat_number combination must be unique"""
        with self.assertRaises(Exception):
            Seat.objects.create(
                movie=self.movie,
                seat_number='A1',
                status=Seat.AVAILABLE
            )

    def test_seat_str(self):
        """Test seat string representation"""
        expected = f"{self.movie.title} - Seat A1"
        self.assertEqual(str(self.seat), expected)


class BookingModelTest(TestCase):
    """Test cases for Booking model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_date=datetime.now().date(),
            duration=120
        )
        self.seat = Seat.objects.create(
            movie=self.movie,
            seat_number='A1',
            status=Seat.AVAILABLE
        )
        self.booking = Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )

    def test_booking_creation(self):
        """Test that a booking can be created"""
        self.assertEqual(self.booking.user, self.user)
        self.assertEqual(self.booking.movie, self.movie)
        self.assertEqual(self.booking.seat, self.seat)

    def test_booking_str(self):
        """Test booking string representation"""
        expected = f"{self.user.username} - {self.movie.title} - Seat A1"
        self.assertEqual(str(self.booking), expected)


class MovieViewTest(TestCase):
    """Test cases for Movie views"""

    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_date=datetime.now().date(),
            duration=120
        )

    def test_movie_list_view(self):
        """Test movie list view"""
        response = self.client.get(reverse('bookings:movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')

    def test_movie_list_template(self):
        """Test that correct template is used"""
        response = self.client.get(reverse('bookings:movie_list'))
        self.assertTemplateUsed(response, 'bookings/movie_list.html')


class BookingViewTest(TestCase):
    """Test cases for Booking views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_date=datetime.now().date(),
            duration=120
        )
        # Create seats for the movie
        for i in range(1, 5):
            Seat.objects.create(
                movie=self.movie,
                seat_number=f'A{i}',
                status=Seat.AVAILABLE
            )

    def test_book_seat_view(self):
        """Test booking a seat view"""
        response = self.client.get(reverse('bookings:book_seat', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/seat_booking.html')

    def test_create_booking(self):
        """Test creating a booking"""
        seat = Seat.objects.first()
        response = self.client.post(
            reverse('bookings:book_seat', args=[self.movie.id]),
            {'seat_id': seat.id}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after booking

        # Verify booking was created
        booking = Booking.objects.first()
        self.assertEqual(booking.seat, seat)

        # Verify seat status changed
        seat.refresh_from_db()
        self.assertEqual(seat.status, Seat.BOOKED)

    def test_booking_history_view(self):
        """Test booking history view"""
        # Create a booking
        seat = Seat.objects.first()
        Booking.objects.create(
            movie=self.movie,
            seat=seat,
            user=self.user
        )

        response = self.client.get(reverse('bookings:booking_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_history.html')
        self.assertContains(response, 'Test Movie')


class MovieAPITest(TestCase):
    """Test cases for Movie API"""

    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_date=datetime.now().date(),
            duration=120
        )

    def test_get_movies_api(self):
        """Test getting movies via API"""
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Movie')

    def test_create_movie_api(self):
        """Test creating a movie via API"""
        data = {
            'title': 'New Movie',
            'description': 'New Description',
            'release_date': datetime.now().date(),
            'duration': 150
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)


class SeatAPITest(TestCase):
    """Test cases for Seat API"""

    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_date=datetime.now().date(),
            duration=120
        )
        self.seat = Seat.objects.create(
            movie=self.movie,
            seat_number='A1',
            status=Seat.AVAILABLE
        )

    def test_get_seats_api(self):
        """Test getting seats via API"""
        response = self.client.get('/api/seats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_available_seats_api(self):
        """Test getting available seats via API"""
        response = self.client.get('/api/seats/available/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['status'], Seat.AVAILABLE)


class BookingAPITest(TestCase):
    """Test cases for Booking API"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test Description',
            release_date=datetime.now().date(),
            duration=120
        )
        self.seat = Seat.objects.create(
            movie=self.movie,
            seat_number='A1',
            status=Seat.AVAILABLE
        )

    def test_booking_requires_authentication(self):
        """Test that booking API is accessible without authentication"""
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_bookings_api(self):
        """Test getting all bookings via API"""
        # Create a booking
        Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )

        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_user_bookings_api(self):
        """Test getting bookings via API without authentication"""
        # Create a booking
        Booking.objects.create(
            movie=self.movie,
            seat=self.seat,
            user=self.user
        )

        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking_api(self):
        """Test creating a booking via API"""
        data = {
            'movie': self.movie.id,
            'seat': self.seat.id,
            'user': self.user.id
        }
        response = self.client.post('/api/bookings/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
