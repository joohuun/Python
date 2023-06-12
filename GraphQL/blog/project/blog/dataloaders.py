from django.db.models import Count, Exists, OuterRef
from promise.dataloader import DataLoader, Promise

from ..user import models
from ..blog import models



class ArticleFavoriteDataLoader(DataLoader):
    def batch_load_fn(self, article_users: list[tuple[models.User, models.Article]]):
        """preload article favorites to avoid N+1 problem
        .annotate(favorited=Exists(), favorites_count=Count(), ).values()
        """
        user, _ = article_users[0]
        article_ids = [article.id for _, article in article_users]
        favorites = (
            models.Article.objects.filter(id__in=article_ids)
            .annotate(favorited=Exists(models.FavoriteArticles.objects.filter(user=user, article_id=OuterRef("pk"))),
                favorites_count=Count("favorites")).values("favorited", "favorites_count")
        )
        return Promise.resolve(favorites)



