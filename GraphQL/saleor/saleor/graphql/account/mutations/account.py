import graphene

from graphql_auth import mutations
from schema import Query
from account.models import User



class AccountRegisterInput(graphene.InputObjectType):
    email = graphene.String(description="The email address of the user.", required=True)
    username = graphene.String(description="The name of the user.", required=True)
    password = graphene.String(description="Password.", required=True)
    redirect_url = graphene.String(
        description=(
            "Base of frontend URL that will be needed to create confirmation URL."
        ),
        required=False,
    )

# class AccountRegister(graphene.Mutation):
#     class Arguments:
#         input = AccountRegisterInput(
#             description="Fields required to create a user", required=True
#         )

#     ok = graphene.Boolean()

#     class Meta:
#         model = User

#     @classmethod
#     def mutate(cls, info, email, username):
        