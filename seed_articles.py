import os
import django
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.utils import timezone
import time

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.accounts.models import User
from apps.articles.models import Article

def seed_data():
    print("Clearing existing articles...")
    Article.objects.all().delete()

    users_data = [
        {'username': 'marcus_tech', 'first_name': 'Marcus', 'last_name': 'Thorne', 'role': User.EDITOR, 'email': 'marcus@articlespace.com'},
        {'username': 'elena_finance', 'first_name': 'Elena', 'last_name': 'Vance', 'role': User.EDITOR, 'email': 'elena@articlespace.com'},
        {'username': 'jordan_ai', 'first_name': 'Jordan', 'last_name': 'Blake', 'role': User.EDITOR, 'email': 'jordan@articlespace.com'},
    ]

    users = {}
    for u_data in users_data:
        user, created = User.objects.get_or_create(
            username=u_data['username'],
            defaults={
                'role': u_data['role'], 
                'email': u_data['email'],
                'first_name': u_data['first_name'],
                'last_name': u_data['last_name']
            }
        )
        if created:
            user.set_password('pass1234')
            user.save()
        users[u_data['username']] = user
    
    articles_data = [
        {
            'title': 'The NVIDIA Paradox: Can GPU Dominance Last into 2026?',
            'content': 'NVIDIA has become the backbone of the AI era, but as 2025 progresses, competitors are catching up. From custom silicon at Google to AMD’s new MI400 chips, the landscape is shifting. Can NVIDIA maintain its market share?',
            'author': users['marcus_tech'],
            'image_url': 'https://images.unsplash.com/photo-1591439657448-9f4b9ce436b9?q=80&w=1000&auto=format&fit=crop',
            'date': timezone.datetime(2025, 6, 10, 10, 0, tzinfo=timezone.utc)
        },
        {
            'title': 'Federal Reserve AI Dilemma: How Automation Warps Jobs Data',
            'content': 'The Fed is struggling to read productivity signals. As AI agents begin replacing mid-tier administrative roles, traditional metrics are failing. Is this a new era of growth?',
            'author': users['elena_finance'],
            'image_url': 'https://images.unsplash.com/photo-1611974714851-eb6077374246?q=80&w=1000&auto=format&fit=crop',
            'date': timezone.datetime(2025, 6, 18, 14, 30, tzinfo=timezone.utc)
        },
        {
            'title': 'DeepMind Gato 3: The First Truly General Robotic Intelligence?',
            'content': 'Google DeepMind announced Gato 3, a model that controls robotic arms with precision while processing language. This is a massive leap toward General Purpose Robotics.',
            'author': users['jordan_ai'],
            'image_url': 'https://images.unsplash.com/photo-1531746790731-6c087fecd05a?q=80&w=1000&auto=format&fit=crop',
            'date': timezone.datetime(2025, 6, 25, 9, 0, tzinfo=timezone.utc)
        },
        {
            'title': 'Crypto vs AI: Why VC Money is Choosing Silicon over Decentralization',
            'content': 'Venture capital is flowing into compute-heavy AI startups, leaving crypto fighting for scraps. Discover why automation is winning the investment war in late 2025.',
            'author': users['marcus_tech'],
            'image_url': 'https://images.unsplash.com/photo-1639762681485-074b7f938ba0?q=80&w=1000&auto=format&fit=crop',
            'date': timezone.datetime(2025, 7, 2, 11, 45, tzinfo=timezone.utc)
        },
        {
            'title': 'The Rise of AI Sovereignty: Why Nations are Building Own LLMs',
            'content': 'Nations are investing billions into local AI infrastructure. To avoid reliance on US giants, countries are developing "Sovereign AI" systems tuned to their culture.',
            'author': users['jordan_ai'],
            'image_url': 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1000&auto=format&fit=crop',
            'date': timezone.datetime(2025, 7, 8, 16, 20, tzinfo=timezone.utc)
        },
        {
            'title': 'Short-Selling in Age of LLMs: How AI Squeezes the Shorts',
            'content': 'AI-powered sentiment analysis allows retail traders to identify short-seller movements. AI is changing the game for hedge funds in 2025.',
            'author': users['elena_finance'],
            'image_url': 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?q=80&w=1000&auto=format&fit=crop',
            'date': timezone.datetime(2025, 7, 12, 13, 10, tzinfo=timezone.utc)
        },
        {
            'title': 'Apple Vision Pro 2: The Spatial Computing Moment',
            'content': 'Apple’s second-gen headset is finally here, and it’s all about AI. With real-time objects generation, Apple is redefining the wearable tech market.',
            'author': users['marcus_tech'],
            'image_url': 'https://images.unsplash.com/photo-1478416272538-5f7e51dc5400?q=80&w=1000&auto=format&fit=crop',
            'date': timezone.datetime(2025, 7, 15, 10, 0, tzinfo=timezone.utc)
        },
        {
            'title': 'Quantum Computing Stocks: The 2025 Hype Cycle',
            'content': 'IBM and IonQ are showing consistent progress in error correction. We explore why the next compute revolution might be closer than you think.',
            'author': users['elena_finance'],
            'image_url': 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=1000&auto=format&fit=crop',
            'date': timezone.datetime(2025, 7, 20, 15, 45, tzinfo=timezone.utc)
        },
        {
            'title': 'Ethical AI Regulation: EU’s New Framework',
            'content': 'The EU AI Act is entering enforcement. For startups, this means heavy compliance costs; for tech giants, it’s a competitive moat.',
            'author': users['jordan_ai'],
            'image_url': 'https://images.unsplash.com/photo-1589254065675-d0581bb4daec?q=80&w=1000&auto=format&fit=crop',
            'date': timezone.datetime(2025, 7, 25, 12, 0, tzinfo=timezone.utc)
        },
        {
            'title': 'The Zero-Marginal Cost Economy',
            'content': 'If AI can automate intelligence, will we enter an age of radical abundance? Or is our financial system unprepared for the collapse of production costs?',
            'author': users['marcus_tech'],
            'image_url': 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1000&auto=format&fit=crop',
            'date': timezone.datetime(2025, 7, 29, 17, 30, tzinfo=timezone.utc)
        }
    ]

    for a_data in articles_data:
        article = Article(
            title=a_data['title'],
            slug=slugify(a_data['title']),
            content=a_data['content'],
            author=a_data['author'],
            status=Article.PUBLISHED,
            published_at=a_data['date']
        )
        
        # Download image first
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            print(f"Downloading image for: {a_data['title']}")
            resp = requests.get(a_data['image_url'], headers=headers, timeout=20)
            if resp.status_code == 200:
                article.image.save(f"{article.slug}.jpg", ContentFile(resp.content), save=False)
                print("  [OK] Image downloaded.")
            else:
                print(f"  [ERR] Status {resp.status_code}")
        except Exception as e:
            print(f"  [FAIL] {e}")
        
        article.save()
        # Set created_at after save to bypass auto_now_add
        Article.objects.filter(pk=article.pk).update(created_at=a_data['date'])
        print(f"SAVED: {article.title}")

if __name__ == "__main__":
    seed_data()
