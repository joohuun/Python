import graphene

from graphql_auth.schema import MeQuery
from graphql_auth import mutations

class AccountMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()

# class Query(MeQuery, graphene.ObjectType):
#     pass


# class Mutation(AccountMutation):
#     pass


# schema = graphene.Schema(query=Query, mutation=Mutation)