
class Init:

     def __init__(self, environ):
        self.environ = environ
        
        self.status = '200 OK'
        self.content = b''
        self.response_headers = [
            ('Content-type', 'text/plain; charset=UTF-8'),
            ('Content-Length', str(len(self.content)))
        ]
