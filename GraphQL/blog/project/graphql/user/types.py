from graphene import ID, Boolean, ObjectType, String, relay
from graphene_django import DjangoObjectType
# from graphene_file_upload.scalars import Upload
from ...core.mutations import AppResolverInfo
from ...user import models

################
# object types #
################

class UserNode(DjangoObjectType):
    class Meta:
        model = models.User
        exclude = ["password"]
        interfaces = (relay.Node, )


class UserDetailsType:
    email = String(required=True)
    username = String(required=True)
    bio = String()



class Profile(UserDetailsType, ObjectType):
    following = Boolean(required=True)
    id = ID()

    @staticmethod
    def reslove_following(root:models.User, info: AppResolverInfo) -> bool:
        follower = info.context.user
        following_exists = models.Following.objects.is_following(follower, root)
        return following_exists


###############
# input types #
###############

class UserCreateInputType(UserDetailsType):
    password = String(rquired=True)
    confirm_password = String(rquired=True)


class UserUpdateInputType:
    email = String()
    username = String()
    bio = String()


class ProfileFollowInput:
    username = String(required=True)
