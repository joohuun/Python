from graphene_federation import build_schema
from graphql_auth.schema import MeQuery

from .account.schema import AccountMutation


class Query(
    MeQuery,
):
    pass


class Mutation(
    AccountMutation,
):
    pass


# schema = graphene.Schema(query=Query, mutation=Mutation)
schema = build_schema(Query, mutation=Mutation)