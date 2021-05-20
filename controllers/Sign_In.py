from controllers.Init import Init
from controllers.Render import Render
from controllers.ConnectDb import ConnectDb


class Sign_In(Init, Render, ConnectDb):
    
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

            cursor.execute('SELECT * FROM users WHERE login=%s AND password=%s', (login, password,))
            user = cursor.fetchone()

            cursor.close()
            conn.close()
            
            print(user)
            
            if user:
                self.status = '303 See Other'
                self.response_headers = [
                    ('Location', '/'),
                    ('Set-Cookie', 'login='+login+'; path=/; max-age=31536000'),
                    ('Set-Cookie', 'password='+password+'; path=/; max-age=31536000')
                ]
            
            else:
                self.status = '303 See Other'
                self.response_headers = [
                    ('Location', '/sign_in'),
                    #('Set-Cookie', 'team=user; path=/; max-age=31536000')
                ]

            return self.status, self.response_headers, self.content

        self.content = self.render('sign_in.html')

        self.response_headers = [
            ('Content-type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(self.content))),
            ('Set-Cookie', 'login=''; path=/; max-age=0'),
            ('Set-Cookie', 'password=''; path=/; max-age=0')
        ]
            
        return self.status, self.response_headers, self.content
    
    def check(self, text):
        from threading import Thread
        
        from controllers.Visitors import Visitors
        visitors = Visitors(self.environ)
        
        try:
            from urllib.parse import parse_qs
            
            cookies = parse_qs(self.environ['HTTP_COOKIE'], separator='; ')
            login_cookie = cookies.get('login')[0]
            password_cookie = cookies.get('password')[0]
            
            #print(login_cookie, password_cookie)
            
            if login_cookie != '' and password_cookie != '':

                conn, cursor = self.connect()

                cursor.execute('SELECT * FROM users WHERE login=%s AND password=%s', (login_cookie, password_cookie,))
                user = cursor.fetchone()
                
                cursor.close()
                conn.close()
                
                if user:
                    Thread(target=visitors.add_visitor, args=(text,)).start()
                    return True
                
                else:
                    Thread(target=visitors.add_visitor, args=(text + ' FALSE',)).start()
                    return False
                
            else:
                Thread(target=visitors.add_visitor, args=(text + ' FALSE',)).start()
                
                return False
                
        except:
            Thread(target=visitors.add_visitor, args=(text + ' FALSE',)).start()

            return False
