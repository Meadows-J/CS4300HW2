from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router
router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'bookings', views.BookingViewSet, basename='booking')

app_name = 'bookings'

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),

    # Template URLs
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:movie_id>/book/', views.book_seat, name='book_seat'),
    path('history/', views.booking_history, name='booking_history'),
]
