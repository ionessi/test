from controllers.Init import Init
from controllers.Render import Render
from controllers.ConnectDb import ConnectDb


class Admin(Init, Render, ConnectDb):
        
    def index(self):
        conn, cursor = self.connect()
        
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        self.content = self.render('admin.html', users=users)

        self.response_headers = [
            ('Content-type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(self.content)))
        ]
        
        return self.status, self.response_headers, self.content
    
    def delete_users(self):
        import cgi
        
        post = cgi.FieldStorage(
            fp=self.environ['wsgi.input'],
            environ=self.environ,
        )
        
        try:
            post_users = post['users']
        
            try:
                post_users = post['users'].value
                post_users = [post['users']]

            except:
                post_users = post['users']

            conn, cursor = self.connect()

            for post_user in post_users:
                cursor.execute('DELETE FROM users WHERE id=%s', (post_user.value,))

            conn.commit()
            cursor.close()
            conn.close()
        
        except:
            pass
        
        self.status = '303 See Other'
        self.response_headers = [
            ('Location', '/admin'),
        ]
        
        return self.status, self.response_headers, self.content
