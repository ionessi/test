from controllers.Init import Init
from controllers.Render import Render
from controllers.ConnectDb import ConnectDb


class Registration(Init, Render, ConnectDb):
    
    def index(self):
        if self.environ['REQUEST_METHOD'] == 'POST':
            import cgi
            
            post = cgi.FieldStorage(
                fp = self.environ['wsgi.input'],
                environ = self.environ,
            )
            
            login = post['login'].value.strip()
            password = post['password'].value.strip()
            
            conn, cursor = self.connect()
            
            cursor.execute('SELECT * FROM users WHERE login=%s', (login,))
            user = cursor.fetchone()
            
            if not user:
                import os
                import time
                import datetime
                
                os.environ['TZ'] = 'Asia/Krasnoyarsk'
                time.tzset()
                date = datetime.datetime.now()
                
                cursor.execute('INSERT INTO users (login, password, date) VALUES (%s, %s, %s)',
                    (login, password, date))
                conn.commit()
                
                self.status = '303 See Other'
                self.response_headers = [
                    ('Location', '/'),
                    ('Set-Cookie', 'login='+login+'; path=/; max-age=31536000'),
                    ('Set-Cookie', 'password='+password+'; path=/; max-age=31536000')
                ]
            
            else:
                self.status = '303 See Other'
                self.response_headers = [
                    ('Location', '/registration'),
                    #('Set-Cookie', 'team=user; path=/; max-age=31536000')
                ]

            cursor.close()
            conn.close()
            
            return self.status, self.response_headers, self.content
            
        self.content = self.render('registration.html')
        
        self.response_headers = [
            ('Content-type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(self.content))),
            ('Set-Cookie', 'login=''; path=/; max-age=0'),
            ('Set-Cookie', 'password=''; path=/; max-age=0')
        ]
        
        return self.status, self.response_headers, self.content
