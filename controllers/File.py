import os
from urllib.parse import parse_qs

from controllers.Init import Init
from controllers.ConnectDb import ConnectDb

class File(Init, ConnectDb):
        
    def message(self):

        conn, cursor = self.connect()
        
        query_data = parse_qs(self.environ['QUERY_STRING'])
        ID = int(query_data.get('id')[0])
        
        #cursor.execute('SELECT mime_type, file FROM messages WHERE id = %(id)s', {'id': ID})
        cursor.execute('SELECT mime_type, file FROM messages WHERE id = %s', (ID,)) 
        
        row = cursor.fetchone()
        mime_type = row[0]

        data = bytes(row[1])

        cursor.close()
        conn.close()
        
        self.content = data
        self.response_headers = [
            ('Cache-Control', 'public, max-age=31536000'),
            ('Accept-Ranges', 'bytes'),
            ('Content-Type', mime_type),
            ('Content-Length', str(len(data)))
        ]
        
        return self.status, self.response_headers, self.content
        
    def comment(self):
        
        conn, cursor = self.connect()
        
        query_data = parse_qs(self.environ['QUERY_STRING'])
        ID = int(query_data.get('id')[0])
        
        cursor.execute('SELECT mime_type, file FROM comments WHERE id = %(id)s', {'id': ID})
            
        row = cursor.fetchone()
        mime_type = row[0]
    
        data = bytes(row[1])
        
        cursor.close()
        conn.close()
        
        self.content = data
        self.response_headers = [
            ('Cache-Control', 'public, max-age=31536000'),
            ('Accept-Ranges', 'bytes'),
            ('Content-type', mime_type),
            ('Content-Length', str(len(data)))
        ]
        
        return self.status, self.response_headers, self.content
