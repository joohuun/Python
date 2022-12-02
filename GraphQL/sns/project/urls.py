from django.conf.urls import url
from django.contrib import admin
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .graphql.api import schema


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]