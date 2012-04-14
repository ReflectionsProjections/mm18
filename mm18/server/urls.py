####
#
# URL Patterns for mapping URLs to the appropriate functions.
#
####

from mm18.server.api import *

urlpatterns = patterns(
		(r'^/(?P<obj>towers)/(?P<id>\d+)/upgrade$', POST, upgrade_object),
		(r'^/(?P<obj>towers)/(?P<id>\d+)$', GET, get_object),
)
