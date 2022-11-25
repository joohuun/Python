import graphene

# from graphene import relay
# from graphene_django import DjangoObjectType
# from graphene_django.filter import DjangoFilterConnectionField
# from ingredients.models import Category, Ingredient

import ingredients.schema
# DjangoObjectType으로 Django model들과 매핑시킴, GraphQL 필드를 자동으로 정의 해줌
# class CategoryType(DjangoObjectType):
#     class Meta:
#         model = Category
#         fields = ("id", "name", "ingredients")

# 
# class IngredientType(DjangoObjectType):
#     class Meta:
#         model = Ingredient
#         fields = ("id", "name", "notes", "category")


# DRF 에서 APIView의 역할
# class Query(graphene.ObjectType):
#     all_ingredients = graphene.List(IngredientType)
#     category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))

#     def resolve_all_ingredients(self, info):
#         # We can easily optimize query count in the resolve method
#         return Ingredient.objects.select_related("category").all()

#     def resolve_category_by_name(self, info, name):
#         try:
#             return Category.objects.get(name=name)
#         except Category.DoesNotExist:
#             return None

# schema = graphene.Schema(query=Query)



class Query(ingredients.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query)