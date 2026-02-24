from rest_framework import viewsets, permissions, status, parsers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from .models import Article
from .serializers import ArticleSerializer
from .permissions import IsEditorUser, IsAuthorOrReadOnly

class ArticleViewSet(viewsets.ModelViewSet):
    """
    Internal API for mobile integrations and external services.
    Enforces strict RBAC and state-based content exposure.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'publish']:
            return [IsEditorUser(), IsAuthorOrReadOnly()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role in ['ADMIN', 'EDITOR']:
                return Article.objects.all()
            return Article.objects.filter(status=Article.PUBLISHED) | Article.objects.filter(author=user)
        return Article.objects.filter(status=Article.PUBLISHED)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsEditorUser])
    def publish(self, request, slug=None):
        article = self.get_object()
        article.status = Article.PUBLISHED
        article.published_at = timezone.now()
        article.save()
        return Response({'status': 'article published'}, status=status.HTTP_200_OK)
