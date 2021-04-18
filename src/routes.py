from src import api
from src.resources.aggregations import AggregationApi
from src.resources.auth import AuthRegister, AuthLogin
from src.resources.authors import AuthorListApi
from src.resources.books import BookListApi

# Registrations classes
from src.resources.populate_db import PopulateDB, PopulateDBWithOutThreading, PopulateDBWithPoolExecutor

api.add_resource(BookListApi, '/books', '/books/<uid>', strict_slashes=False)
api.add_resource(AuthorListApi, '/authors', '/authors/<uid>', strict_slashes=False)
api.add_resource(AggregationApi, '/aggregations', strict_slashes=False)
api.add_resource(AuthRegister, '/register', strict_slashes=False)
api.add_resource(AuthLogin, '/login', strict_slashes=False)
api.add_resource(PopulateDB, '/populate-db', strict_slashes=False)
api.add_resource(PopulateDBWithPoolExecutor, '/populate-db-with-pool', strict_slashes=False)
api.add_resource(PopulateDBWithOutThreading, '/populate-db-without-threading', strict_slashes=False)
