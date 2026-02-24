import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.accounts.models import User
from apps.articles.models import Article
from django.utils.text import slugify

def seed_data():
    # 1. Create a demo editor user if it doesn't exist
    editor, created = User.objects.get_or_create(
        username='demo_editor',
        defaults={
            'email': 'editor@example.com',
            'role': User.EDITOR
        }
    )
    if created:
        editor.set_password('demo1234')
        editor.save()
        print("Created demo_editor user (password: demo1234)")

    # 2. Create 10 sample articles
    articles_data = [
        ("The Future of Django 5.0", "Exploring the latest async features and simplified templates."),
        ("Modern Web Design Patterns", "Why glassmorphism and bento grids are taking over in 2026."),
        ("REST vs GraphQL in 2026", "A deep dive into API architecture for modern applications."),
        ("PostgreSQL Performance Tips", "Optimizing your database queries for high-traffic sites."),
        ("Dockerizing Python Apps", "A step-by-step guide to containerization for beginners."),
        ("The Rise of Agentic AI", "How AI assistants are changing the way we write code."),
        ("Mastering CSS Grid", "Creating complex layouts with minimal code and no frameworks."),
        ("Authentication Best Practices", "Moving beyond simple passwords to robust JWT and OAuth."),
        ("Building Scalable CMS Systems", "Architectural patterns for high-performance content hubs."),
        ("Why Python remains King", "Evaluating the ecosystem and developer productivity in 2026."),
    ]

    print("Seeding articles...")
    for i, (title, content) in enumerate(articles_data, 1):
        slug = slugify(title)
        # Ensure unique slug
        if Article.objects.filter(slug=slug).exists():
            slug = f"{slug}-{i}"
            
        Article.objects.get_or_create(
            title=title,
            slug=slug,
            defaults={
                'content': content,
                'author': editor,
                'status': Article.PUBLISHED if i % 2 == 0 else Article.DRAFT
            }
        )
    print(f"Successfully seeded {len(articles_data)} articles!")

if __name__ == "__main__":
    seed_data()
