import graphene
import graphene_django_optimizer as gql_optimizer
from django.db.models.query import QuerySet
from graphene import ObjectType
from graphql import GraphQLError
import graphql_jwt
from graphql_jwt.decorators import login_required

from ...core.mutations import AppResolverInfo
from ...user import models
from .types import (
    Profile,
    UserNode,
)
from .mutations import (
    CreateUserMutation,
    loginMutation,
    FollowProfileMutation,
    UnFollowProfileMutation,
)

class UsersQueries(ObjectType):
    current_user = graphene.Field(UserNode)
    get_profile = graphene.Field(Profile, username=graphene.String(required=True))

    @staticmethod
    def resolve_current_user(root, info: AppResolverInfo, **kwargs) -> QuerySet[models.User]:
        if not info.context.user or not info.context.user.is_authenticated:
            raise GraphQLError("No User Logged in")
        optimized_query = gql_optimizer.query(
            models.User.objects.filter(id=info.context.user.id), info
        )
        return optimized_query.first()

    @staticmethod
    @login_required
    def resolve_get_profile(
        root, info: AppResolverInfo, username: str
    ) -> QuerySet[models.User]:
        return gql_optimizer.query(models.User.objects.get(username=username), info)





class UserMutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field(description="create a new user")
    login_user = loginMutation.Field()
    verify_user = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Verify.Field()
    follow_profile = FollowProfileMutation.Field(description="follow a profile") 
    unfollow_profile = UnFollowProfileMutation.Field(description="unfollow a profile")