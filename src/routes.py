from src import api
from src.resources.aggregations import AggregationApi
from src.resources.auth import AuthRegister, AuthLogin
from src.resources.authors import AuthorListApi
from src.resources.books import BookListApi

# Registrations classes
api.add_resource(BookListApi, '/books', '/books/<uid>', strict_slashes=False)
api.add_resource(AuthorListApi, '/authors', '/authors/<uid>', strict_slashes=False)
api.add_resource(AggregationApi, '/aggregations', strict_slashes=False)
api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
