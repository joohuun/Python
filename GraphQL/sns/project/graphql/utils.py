import json


def get_graphql_content_from_response(response):
    return json.loads(response.content.decode("utf8"))


def get_graphql_content(response, *, ignore_errors: bool = False):
    """Gets GraphQL content from the response, and optionally checks if it
    contains any operating-related errors, eg. schema errors or lack of
    permissions.
    """
    content = get_graphql_content_from_response(response)
    if not ignore_errors:
        assert "errors" not in content, content["errors"]
    return content