import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Add the project directory to sys.path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_theater_booking.settings')

# Setup Django
django.setup()

# Create test database
from django.test.runner import DiscoverRunner
runner = DiscoverRunner(verbosity=0, interactive=False, keepdb=True)

def before_all(context):
    """Setup test database and fixtures before running features"""
    context.test_runner = runner
    context.old_db_name = settings.DATABASES['default']['NAME']
    runner.setup_test_environment()
    context.test_db = runner.setup_databases()

def after_all(context):
    """Teardown test database after running features"""
    if hasattr(context, 'test_runner') and hasattr(context, 'test_db'):
        context.test_runner.teardown_databases(context.test_db)
        context.test_runner.teardown_test_environment()

def before_scenario(context, scenario):
    """Setup before each scenario"""
    # Import models here to ensure Django is setup
    from django.contrib.auth.models import User
    from bookings.models import Movie, Seat, Booking

    # Create test data
    context.test_user = User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )

    context.test_movie = Movie.objects.create(
        title='Test Movie',
        description='Test Description',
        release_date='2024-01-01',
        duration=120
    )

    # Create seats for the movie
    for i in range(1, 11):
        Seat.objects.create(
            movie=context.test_movie,
            seat_number=f'A{i}',
            status='available'
        )

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    from django.contrib.auth.models import User
    from bookings.models import Movie, Seat, Booking

    # Clean up test data
    User.objects.all().delete()
    Movie.objects.all().delete()
    Seat.objects.all().delete()
    Booking.objects.all().delete()
