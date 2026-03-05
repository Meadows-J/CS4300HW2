from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bookings.models import Movie, Seat
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **options):
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/admin123'))

        # Create test user
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user('testuser', 'test@example.com', 'password123')
            self.stdout.write(self.style.SUCCESS('Created test user: testuser/password123'))

        # Create movies
        movies_data = [
            {
                'title': 'The Matrix Resurrections',
                'description': 'An epic science fiction film about reality and illusion.',
                'release_date': datetime.now().date() - timedelta(days=30),
                'duration': 148
            },
            {
                'title': 'Avatar: The Way of Water',
                'description': 'An astonishing visual journey to the land of Pandora.',
                'release_date': datetime.now().date() - timedelta(days=60),
                'duration': 192
            },
            {
                'title': 'Oppenheimer',
                'description': 'The story of the father of the atomic bomb.',
                'release_date': datetime.now().date() - timedelta(days=90),
                'duration': 180
            },
            {
                'title': 'Barbie',
                'description': 'A fun and colorful adventure in a plastic world.',
                'release_date': datetime.now().date() - timedelta(days=120),
                'duration': 114
            }
        ]

        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'description': movie_data['description'],
                    'release_date': movie_data['release_date'],
                    'duration': movie_data['duration']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created movie: {movie.title}'))

                # Create seats for each movie
                seat_rows = ['A', 'B', 'C', 'D']
                for row in seat_rows:
                    for seat_num in range(1, 9):
                        seat_number = f'{row}{seat_num}'
                        Seat.objects.get_or_create(
                            movie=movie,
                            seat_number=seat_number,
                            defaults={'status': Seat.AVAILABLE}
                        )
                self.stdout.write(self.style.SUCCESS(f'Created 32 seats for {movie.title}'))

        self.stdout.write(self.style.SUCCESS('Database population complete!'))
