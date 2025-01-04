from django.urls import path, include

urlpatterns = [
    path('', include('blogapp.urls')),  # blogapp urls'e yönlendir
]
