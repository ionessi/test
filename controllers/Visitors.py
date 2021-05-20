from controllers.Init import Init
from controllers.Render import Render
from controllers.ConnectDb import ConnectDb


class Visitors(Init, Render, ConnectDb):
    
    def index(self):

        conn, cursor = self.connect()
        
        cursor.execute('SELECT * FROM visitors ORDER BY date DESC')
        visitors = cursor.fetchall()
        
        self.content = self.render('visitors.html', visitors=visitors)

        self.response_headers = [
            ('Content-type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(self.content)))
        ]
        
        cursor.close()
        conn.close()
        
        return self.status, self.response_headers, self.content
    
    def add_visitor(self, text):
        
        conn, cursor = self.connect()
        
        try:
            ip = self.environ['HTTP_X_FORWARDED_FOR']
        except:
            ip = self.environ['REMOTE_ADDR']
            
        cursor.execute('SELECT * FROM visitors')
        visitors = cursor.fetchall()
        flag = False
        
        import os
        import time
        import datetime
        os.environ['TZ'] = 'Asia/Krasnoyarsk'
        #os.environ['TZ'] = 'UTC'
        time.tzset()
        visitor_date = datetime.datetime.now()
        
        if visitors:
            for visitor in visitors:
                if ip == visitor.ip:
                    cursor.execute('UPDATE visitors SET path=%(path)s, date = %(date)s, user_agent = %(user_agent)s WHERE id = %(id)s',
                                    {'path': text, 'date': visitor_date, 'user_agent': self.environ['HTTP_USER_AGENT'], 'id': visitor.id})
                    conn.commit()
                    
                    flag = True
                    
                    break
                    
        if flag == False:
            cursor.execute('INSERT INTO visitors (ip, path, user_agent, date) VALUES (%s, %s, %s, %s)',
                            (ip, text, self.environ['HTTP_USER_AGENT'], visitor_date))
                
            conn.commit()
            
        cursor.close()
        conn.close()
