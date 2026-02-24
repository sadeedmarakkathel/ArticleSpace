from .models import User
from apps.articles.models import Article
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms

# HTML UI Views
class ProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Show all published articles by this user
        context['articles'] = Article.objects.filter(
            author=self.get_object(), 
            status=Article.PUBLISHED
        ).order_by('-created_at')
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'accounts/profile_form.html'
    
    def get_object(self):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

class UserRegisterForm(UserCreationForm):
    # Filter out ADMIN role for public registration
    REGISTRATION_CHOICES = [
        (User.EDITOR, 'Editor'),
        (User.VIEWER, 'Viewer'),
    ]
    role = forms.ChoiceField(choices=REGISTRATION_CHOICES, initial=User.VIEWER)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role',)

class SignUpView(CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self):
        return reverse_lazy('home')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')
