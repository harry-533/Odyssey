from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('result/<int:pk>/', views.result, name='result'),
    path('profile/', views.profile, name='profile'),
    path('autocomplete/', views.autocomplete_cities, name='autocomplete_cities'),
    path('login/', views.custom_login, name='login'),
    path('register/', views.custom_register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('add-row/', views.add_itinerary, name="add_row"),
    path('delete-row/<int:itinerary_id>/', views.remove_itinerary, name="remove_row"),
    path('get-row/<int:itinerary_id>/', views.get_itinerary, name="get_row")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)