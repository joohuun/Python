import graphene

from graphql_auth.schema import MeQuery
from graphql_auth import mutations

from article.models import Article

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()


class Query(MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)



# class CreateArticle(graphene.Mutation):
#     class Arguments:
#         title = 


#     class Meta:
#         model = 
