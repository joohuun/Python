import graphene

from graphql_auth.schema import MeQuery
from graphql_auth import mutations

class AccountMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()