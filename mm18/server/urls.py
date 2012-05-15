"""URL Patterns for mapping URLs to the appropriate functions."""

from mm18.server.server_test_api import *

urlpatterns = [
	(r'/api/tests/echo/(?P<code>\d+)', 'GET', echo_code),
	(r'/api/tests/post', 'POST', POST_method),
]
