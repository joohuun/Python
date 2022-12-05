import graphene

from graphql_auth.schema import MeQuery
from graphql_auth import mutations

from article.models import Article

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()

'''
    mutation {
        register (
            email: "test12@gmail.com"
            username: "teset12"
            password1: "1q2w3e!!"
            password2: "1q2w3e!!"
        ) {
            success
            errors
            token
        } 
    }

    mutation {
        verifyAccount (
        token: "토큰값"
        ) {
        success
        errors
        }
    }

    mutation {
        tokenAuth(
            email: "test12@gmail.com"
            password: "1q2w3e!!") {
            user {
                id
                username
                email
            }
        }
    }
'''

class Query(MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)



