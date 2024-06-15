from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
		RegisterUserView, LoginUserView, LocationListCreateView, LocationUpdateRetrieveDeleteView,
		BoundaryListCreateView, BoundaryUpdateRetrieveDeleteView, CalculateDistanceView, CheckBoundryView,
		index
	)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token-view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh-view'),

    path('register/', RegisterUserView.as_view(), name='register-view'),
    path('login/', LoginUserView.as_view(), name='login-view'),

    path('api/locations/', LocationListCreateView.as_view(), name='location-list'),
    path('api/locations/<int:pk>/', LocationUpdateRetrieveDeleteView.as_view(), name='location-detail'),

    path('api/boundaries/', BoundaryListCreateView.as_view(), name='boundary-list'),
    path('api/boundaries/<int:pk>/', BoundaryUpdateRetrieveDeleteView.as_view(), name='boundary-update'),

    path('api/locations/distance/', CalculateDistanceView.as_view(), name='location-distance'),
    path('api/locations/within_boundary/', CheckBoundryView.as_view(), name='check-boundary'),

    path('', index, name='index')

]
