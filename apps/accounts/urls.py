from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import SignUpView, UserLoginView, UserLogoutView, ProfileView, ProfileUpdateView
from .api_views import RegisterView, UserDetailView

urlpatterns = [
    # Web UI
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    
    # API Integration Layer
    path('register/', RegisterView.as_view(), name='api_register'),
    path('profile/', UserDetailView.as_view(), name='api_profile'),
    path('token/', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]
