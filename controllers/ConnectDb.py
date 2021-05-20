import psycopg2
import psycopg2.extras

class ConnectDb():
    
    def connect(self):
        
        if self.environ['wsgi.url_scheme'] == 'https':
            import os
            
            DATABASE_URL = os.environ['DATABASE_URL']
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
            
        else:
            conn = psycopg2.connect('host=db port=5432 dbname=postgres user=postgres password=postgres')
            cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        
        return conn, cursor
