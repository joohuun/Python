from graphene_federation import build_schema
from graphql_auth.schema import MeQuery

from .account.schema import AccountMutation
from .article.schema import ArticleMutation, ArticleQueries



class Query(
    ArticleQueries,
    MeQuery,
):
    pass


class Mutation(
    AccountMutation,
    ArticleMutation
):
    pass


schema = build_schema(Query, mutation=Mutation)