from controllers.Init import Init
from controllers.ConnectDb import ConnectDb

class Db(Init, ConnectDb):

    def create_tables(self):
        
        conn, cursor = self.connect()
        
        query = '''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                date TIMESTAMP NOT NULL
            )
        '''
        
        cursor.execute(query)
        conn.commit()
        
        query = '''
            CREATE TABLE IF NOT EXISTS visitors (
                id SERIAL PRIMARY KEY,
                ip TEXT NOT NULL,
                path TEXT NOT NULL,
                user_agent TEXT NOT NULL,
                date TIMESTAMP NOT NULL
            )
        '''
        
        cursor.execute(query)
        conn.commit()
        
        query = '''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                sender TEXT NOT NULL,
                text TEXT NOT NULL,
                date TIMESTAMP NOT NULL,
                file_name TEXT,
                mime_type TEXT,
                file BYTEA,
                user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE
            )
        '''

        cursor.execute(query)
        conn.commit()
        
        query = '''
            CREATE TABLE IF NOT EXISTS comments (
                id SERIAL PRIMARY KEY,
                sender TEXT NOT NULL,
                text TEXT NOT NULL,
                date TIMESTAMP NOT NULL,
                file_name TEXT,
                mime_type TEXT,
                file BYTEA,
                user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                message_id INT NOT NULL REFERENCES messages(id) ON DELETE CASCADE
            )
        '''
        
        cursor.execute(query)
        conn.commit()
        
        query = '''
            CREATE TABLE IF NOT EXISTS webpush (
                id SERIAL PRIMARY KEY,
                login TEXT NOT NULL,
                user_agent TEXT NOT NULL,
                browser TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                auth TEXT NOT NULL,
                p256dh TEXT NOT NULL,
                user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE
            )
        '''
        
        cursor.execute(query)
        conn.commit()
        
        cursor.close()
        conn.close()
        
        result = 'OK'
        self.content = result.encode()
        self.response_headers = [
            ('Content-type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(self.content)))
        ]
        
        return self.status, self.response_headers, self.content
    
    def drop_tables(self):

        conn, cursor = self.connect()
        
        
        cursor.execute('DROP TABLE comments')
        conn.commit()
        
        cursor.execute('DROP TABLE messages')
        conn.commit()
        
        #cursor.execute('DROP TABLE webpush')
        #conn.commit()
        
        #cursor.execute('DROP TABLE users')
        #conn.commit()
        
        cursor.execute('DROP TABLE visitors')
        conn.commit()
        
        cursor.close()
        conn.close()
        
        result = 'OK'
        self.content = result.encode()
        self.response_headers = [
            ('Content-type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(self.content)))
        ]
        
        return self.status, self.response_headers, self.content
