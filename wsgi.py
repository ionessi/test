
from Router import Router

def application(environ, start_response):
    router = Router(environ)
    status, response_headers, content = router.routing()
    
    start_response(status, response_headers)
    
    return [content]
    #yield content
