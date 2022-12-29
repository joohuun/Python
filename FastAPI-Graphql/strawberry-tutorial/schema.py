import strawberry
from book.book import Query







schema = strawberry.Schema(query=Query)