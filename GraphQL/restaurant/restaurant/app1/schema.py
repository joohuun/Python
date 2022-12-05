import graphene
from graphene_django import DjangoObjectType
from .models import Restaurant
from django_graphene_permissions import PermissionDjangoObjectType, permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated


class RestaurantType(PermissionDjangoObjectType):
    class  Meta:
        model = Restaurant
        fields = ("id", "name", "address")

    @staticmethod
    def permission_classes():
        return [IsAuthenticated]

        
class Query(graphene.ObjectType):
    """
    query {
        restaurants {
            id
            name
            address
        }
    }
    """
    restaurants = graphene.List(RestaurantType)

    def resolve_restaurants(self, info, **kwargs):
        return Restaurant.objects.all()
    

class CreateRestaurant(graphene.Mutation):
    """
    mutation {
        createRestaurant (
            name: "gkgk"
            address: "ghgh"
            ) {
            ok 
            restaurant {
                id
                name
                address
            }
        } 
    }
    """
    class Arguments:
        name = graphene.String()
        address = graphene.String()
    
    ok = graphene.Boolean()
    restaurant = graphene.Field(RestaurantType)

    # @permissions_checker([IsAuthenticated])
    def mutate(self, info, name, address):
        restaurant = Restaurant(name=name, address=address)
        restaurant.save()
        return CreateRestaurant(ok=True, restaurant=restaurant)
    

class DeleteRestaurant(graphene.Mutation):
    """
    mutation {
        deleteRestaurant (id:25) {
            ok
        }
    }   
    """
    class Arguments:
        id = graphene.Int()
    
    ok = graphene.Boolean()

    def mutate(self, info, id):
        restaurant = Restaurant.objects.get(id=id)
        restaurant.delete()
        return DeleteRestaurant(ok=True)
    

class UpdateRestaurant(graphene.Mutation):
    """
    mutation {
        updateRestaurant (
            id: 23
            name: "gkgasdasdk"
            address: "qweirufkjlsdkja"
            ) {
            ok
            restaurant {
                id
                name
                address
            }
        }
    }
    """
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        address = graphene.String()

    ok = graphene.Boolean()
    restaurant = graphene.Field(RestaurantType)

    def mutate(self, info, id, name, address):
        restaurant = Restaurant.objects.get(id=id)
        restaurant.name = name
        restaurant.address = address
        restaurant.save()
        return UpdateRestaurant(ok=True, restaurant=restaurant)


class Mutation(graphene.ObjectType):
    create_restaurant = CreateRestaurant.Field()
    delete_restaurant = DeleteRestaurant.Field()
    update_restaurant = UpdateRestaurant.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


