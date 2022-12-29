import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from project.core.views import GraphQLPlaygroundView
from .graphql.api import schema

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "graphql",
        csrf_exempt(
            GraphQLView.as_view(
                graphiql=False,
                schema=schema
            )
        ),
    ),
    path("playground", csrf_exempt(GraphQLPlaygroundView.as_view(endpoint="graphql"))),
    path("__debug__/", include(debug_toolbar.urls)),
]
