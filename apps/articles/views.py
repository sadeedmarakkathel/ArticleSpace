from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify
from .models import Article

# HTML UI Views
class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'
    
    def get_queryset(self):
        return Article.objects.filter(status=Article.PUBLISHED)

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    lookup_field = 'slug'

class DashboardView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/dashboard.html'
    context_object_name = 'articles'

    def get_queryset(self):
        if self.request.user.role == 'ADMIN':
            return Article.objects.all()
        return Article.objects.filter(author=self.request.user)

class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    fields = ['title', 'content', 'image', 'status']
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('dashboard')

    def test_func(self):
        return self.request.user.role in ['ADMIN', 'EDITOR']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        # Check for slug collision
        original_slug = form.instance.slug
        counter = 1
        while Article.objects.filter(slug=form.instance.slug).exists():
            form.instance.slug = f"{original_slug}-{counter}"
            counter += 1
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'content', 'image', 'status']
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('dashboard')
    lookup_field = 'slug'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or self.request.user.role == 'ADMIN'

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('dashboard')
    lookup_field = 'slug'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author or self.request.user.role == 'ADMIN'

def publish_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.user == article.author or request.user.role == 'ADMIN':
        article.status = Article.PUBLISHED
        article.published_at = timezone.now()
        article.save()
    return redirect('dashboard')
