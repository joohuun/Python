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

class AccountRegister(graphene.Mutation):
    class Arguments:
        input = AccountRegisterInput(
            description="Fields required to create a user", required=True
        )

    requires_confirmation = graphene.Boolean(
        description = "informs,,,"
    )

    class Meta:
        description = "Register a new user."
        exclude = ["password"]
        model = User
        # error_type_class = AccountError
        error_type_field = "account_errors"

    @classmethod
    def mutate(cls, root, info, **data):
        response = super().mutate(root, info, **data)
        response.requires_confirmation = True
        return response


