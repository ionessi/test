from controllers.Init import Init
from controllers.Render import Render
from controllers.ConnectDb import ConnectDb
from controllers.Default import Default
from controllers.Webpush import Webpush


class Message(Init, Render, ConnectDb, Default, Webpush):
    
    def index(self):

        conn, cursor = self.connect()
        
        from urllib.parse import parse_qs
        query_data = parse_qs(self.environ['QUERY_STRING'])
        message_id = query_data.get('id')[0]
        
        cursor.execute('SELECT id, sender, text, date, file_name, mime_type FROM messages WHERE id=%s', (message_id,))
        message = cursor.fetchone()
        
        cursor.execute('SELECT id, sender, text, date, file_name, mime_type, message_id FROM comments WHERE message_id=%s ORDER BY date DESC', (message_id,))
        comments = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        image, audio = self.get_mime_type_list()

        self.content = self.render('add_comment.html', message=message, comments=comments, image=image, audio=audio)

        self.response_headers = [
            ('Content-type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(self.content)))
        ]
        
        return self.status, self.response_headers, self.content
        
    def add(self):
        self.content = self.render('add_message.html')
        
        self.response_headers = [
            ('Content-type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(self.content)))
        ]
        
        return self.status, self.response_headers, self.content
        
    def send(self):

        conn, cursor = self.connect()

        import cgi

        post = cgi.FieldStorage(
            fp = self.environ['wsgi.input'],
            environ = self.environ,
        )
        
        from urllib.parse import parse_qs
        
        cookies = parse_qs(self.environ['HTTP_COOKIE'], separator='; ')
        login_cookie = cookies.get('login')[0]
        
        cursor.execute('SELECT * FROM users WHERE login=%s', (login_cookie,))
        user = cursor.fetchone()

        sender = login_cookie

        text = self.get_link(post['text'].value.strip())
        #text = post['text'].value.strip()
        
        import os
        import time
        import datetime
        os.environ['TZ'] = 'Asia/Krasnoyarsk'
        time.tzset()
        message_date = datetime.datetime.now()
            
        if post['file'].filename != '':
            file_name = post['file'].filename
            mime_type = post['file'].type
            file_bin = post['file'].value
            
            cursor.execute('INSERT INTO messages (sender, text, date, file_name, mime_type, file, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (sender, text, message_date, file_name, mime_type, file_bin, user.id))
            
        else:
            cursor.execute('INSERT INTO messages (sender, text, date, user_id) VALUES (%s, %s, %s, %s)',
                (sender, text, message_date, user.id))

        conn.commit()
        cursor.close()
        conn.close()
        
        from threading import Thread
        Thread(target=self.send_push, args=(sender, message_date.strftime('%H:%M (%d.%m.%Y)') + '\n сообщение от ' + sender, 'https://stalevar.herokuapp.com',)).start()
        
        self.status = '303 See Other'
        self.response_headers = [
            ('Location', '/'),
        ]
        
        return self.status, self.response_headers, self.content
