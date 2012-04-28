def echo_code(regex, **json):
    """ API method to test echos of HTTP status codes.

    regex -- dictionary containing all data from URL path.
    json  -- unrolled dictionary of JSON data

    returns: a tuple with the status code and data
    """
    return (regex['code'], {})

def POST_method(regex, **json):
    """ API method to test POST request handling in general.
    Also used to make sure that GET requests to POST methods 
    get a 405 error.

    regex -- dictionary containing all data from URL path.
    json  -- unrolled dictionary of JSON data
    """
    return (200, {'method':'POST'})

