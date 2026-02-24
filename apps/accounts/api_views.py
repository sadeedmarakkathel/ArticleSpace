from rest_framework import generics, permissions
from .serializers import UserSerializer
from .models import User

class RegisterView(generics.CreateAPIView):
    """
    Public endpoint for account registration via API.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    Secure endpoint for retrieving and updating authenticated user profiles.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
