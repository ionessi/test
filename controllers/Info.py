from controllers.Init import Init
from controllers.Render import Render
from controllers.ConnectDb import ConnectDb


class Info(Init, Render, ConnectDb):
        
    def index(self):

        conn, cursor = self.connect()
        
        cursor.execute('SELECT login, user_agent, browser FROM webpush')
        subscriptions = cursor.fetchall()
        
        self.content = self.render('info.html', subscriptions=subscriptions)
        
        self.response_headers = [
            ('Content-type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(self.content)))
        ]
            
        
        cursor.close()
        conn.close()

        return self.status, self.response_headers, self.content
 
