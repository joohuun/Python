import uuid
from typing import Any

import graphene
import graphql_jwt
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from ...core.mutations import AppResolverInfo, BaseMutation
from ...user import models
from .types import (
    ProfileFollowInput,
    UserCreateInputType,
    UserNode,
    UserUpdateInputType,
)


# 회원가입
class CreateUserMutation(BaseMutation):
    Input = UserCreateInputType

    user = graphene.Field(UserNode, required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info: AppResolverInfo, **data: Any) -> "CreateUserMutation":
        password = data.get("password")
        confirm_password = data.pop("confirm_password")
        if password != confirm_password:
            raise GraphQLError("password and confirm_password must match")
        
        user = models.User.objects.create_user(**data)
        return CreateUserMutation(success=True, user=user)


# 로그인
class loginMutation(graphql_jwt.relay.JSONWebTokenMutation):
    user = graphene.Field(UserNode)

    @classmethod
    def resolve(cls, _, info, **kwargs):
        return cls(user=info.context.user)



# 팔로우
class FollowProfileMutation(BaseMutation):
    Input = ProfileFollowInput

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info: AppResolverInfo, **data: Any) -> "BaseMutation":
        current_user = info.context.user
        username = data.get("username")
        profile = models.User.objects.get(username=username)
        result = models.Following.objects.follow(current_user, profile)
        if result:
            return FollowProfileMutation(success=True)
        return FollowProfileMutation(success=False)


# 언팔
class UnFollowProfileMutation(BaseMutation):
    Input = ProfileFollowInput

    """
    def unfollow(self, user, another_user):
        try:
            follow = self.get(follower=user, followed=another_user)
            follow.delete()
            return True
        except Following.DoesNotExist:
            return False
    """
    @classmethod
    def mutate_and_get_payload(cls, root, info: AppResolverInfo, **data: Any) -> "UnFollowProfileMutation":
        username = data.get("username")
        followed = models.User.objects.get(username=username)
        following = models.Following.objects.unfollow(info.context.user, followed)
        if following:
            return UnFollowProfileMutation(success=True)
        return UnFollowProfileMutation(success=False)

    

