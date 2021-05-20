import mimetypes
from urllib.parse import parse_qs

from controllers.Init import Init

class Static(Init):
        
    def get(self):

        query_data = parse_qs(self.environ['QUERY_STRING'])
        path = query_data.get('path')[0]

        file = open(path, 'rb')
        self.content = file.read()
        file.close()
        
        mime_type = mimetypes.guess_type(path)[0]

            
        self.response_headers = [
            ('Cache-Control', 'public, max-age=31536000'),
            ('Accept-Ranges', 'bytes'),
            ('Content-type', mime_type),
            ('Content-Length', str(len(self.content)))
        ]
        
        return self.status, self.response_headers, self.content
