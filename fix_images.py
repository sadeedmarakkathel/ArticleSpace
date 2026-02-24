import os
import django
import requests
from django.core.files.base import ContentFile
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.articles.models import Article

def fix_missing_images():
    missing = Article.objects.filter(image='')
    print(f"Fixing {missing.count()} missing images...")
    
    # Very stable fallback URLs
    fallbacks = [
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1000",
        "https://images.unsplash.com/photo-1611974714851-eb6077374246?q=80&w=1000",
        "https://images.unsplash.com/photo-1591439657448-9f4b9ce436b9?q=80&w=1000",
        "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=1000"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for i, article in enumerate(missing):
        url = fallbacks[i % len(fallbacks)]
        print(f"Targeting: {article.title} with {url}")
        try:
            resp = requests.get(url, headers=headers, timeout=20)
            if resp.status_code == 200:
                article.image.save(f"fix_{article.slug}.jpg", ContentFile(resp.content), save=True)
                print(f"  [FIXED] {article.title}")
            else:
                print(f"  [ERROR] Status {resp.status_code}")
        except Exception as e:
            print(f"  [FAIL] {e}")
        time.sleep(1)

if __name__ == "__main__":
    fix_missing_images()
