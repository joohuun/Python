import graphene
from account.models import User
from article.models import Article
from graphql import GraphQLError
from article.types import ArticleType, CommentType, LikeType
from graphql_jwt.decorators import login_required


class CreateArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        body = graphene.String()

    article = graphene.Field(ArticleType)

    @classmethod
    @login_required
    def mutate(cls, root, info, title, body):
        if info.context.user:
            print(info.context.user.id)
        article = Article(title=title, body=body)
        user = User.objects.get(id=info.context.user.id)
        is_verified = user.status.verified
        if not is_verified:
            raise GraphQLError("인증되지 않은 사용자입니다")

        article.user = user
        article.save()
        return CreateArticle(article=article)
