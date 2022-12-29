from graphene_federation import build_schema
from .user.schema import UserMutation, UsersQueries
from .blog.schema import ArticleQueries
from .blog.schema import ArticleMutation





class Query(
    UsersQueries,
    ArticleQueries,
):
    pass

class Mutation(
    UserMutation,
    ArticleMutation,

):
    pass

schema = build_schema(Query, mutation=Mutation)

