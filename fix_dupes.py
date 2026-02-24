import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.articles.models import Article

def fix_images():
    data = [
        {
            'search': 'Ethical AI Regulation',
            'url': 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1000'
        },
        {
            'search': 'Zero-Marginal Cost',
            'url': 'https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?q=80&w=1000'
        }
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    for item in data:
        try:
            print(f"Fixing: {item['search']}...")
            article = Article.objects.get(title__icontains=item['search'])
            resp = requests.get(item['url'], headers=headers, timeout=20)
            if resp.status_code == 200:
                article.image.save(f"unique_{article.slug}.jpg", ContentFile(resp.content), save=True)
                print(f"  [DONE] Unique image attached to {article.title}.")
            else:
                print(f"  [ERROR] Status {resp.status_code}")
        except Exception as e:
            print(f"  [FAIL] {e}")

if __name__ == "__main__":
    fix_images()
