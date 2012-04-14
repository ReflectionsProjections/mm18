####
#
# URL Patterns for mapping URLs to the appropriate functions.
#
####

from mm18.server.api import *

urlpatterns = [
		# Example:
		# (r'^api/shoot', POST, shoot),
		(r'/api/tests/echo/(?P<code>\d+)', 'GET', echo_code),
]
