import pytest
from graphene.test import Client
from project.account.models import User
from project.graphql.api import schema
from project.graphql.utils import get_graphql_content
from django.test import override_settings

client = Client(schema)





REGISTER_MUTATION = """
mutation {
  register(
    email: "test1@gmail.com",
    username: "test1",
    password1: "Qwer1234!!",
    password2: "Qwer1234!!",
  ) {
    success
    errors
  }
}
"""

@pytest.mark.django_db
def test_register():
  mutation = REGISTER_MUTATION
  # response = client
  result = client.execute(mutation)
  print(result)
  assert result == True



