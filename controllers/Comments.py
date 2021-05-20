from controllers.Init import Init
from controllers.Render import Render
from controllers.ConnectDb import ConnectDb
from controllers.Default import Default
from controllers.Webpush import Webpush
 
class Comments(Init, Render, ConnectDb, Default, Webpush):
    
    def index(self):
        conn, cursor = self.connect()
        
        cursor.execute('SELECT COUNT(*) FROM comments')
        count = cursor.fetchone().count
        
        limit = 15
        
        import math
        pages = math.ceil(count/limit)

        from urllib.parse import parse_qs
        query_data = parse_qs(self.environ['QUERY_STRING'])
        
        if query_data:
            page = int(query_data.get('page')[0])
            offset = limit * (page - 1)
        else:
            page = 1
            offset = 0
            
        cursor.execute('SELECT id, sender, text, date, file_name, mime_type, message_id FROM comments ORDER BY id DESC LIMIT %s OFFSET %s', (limit, offset,))
                
        comments = cursor.fetchall()
        
        image, audio = self.get_mime_type_list()
        title = 'ТАТЫШЕВ | КОММЕНТАРИИ'
        self.content = self.render('comments.html', comments=comments, pages=pages, page=page, image=image, audio=audio)
        
        cursor.close()
        conn.close()

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
        
        text = self.get_link(post['text'].value.strip())
        #text = post['text'].value.strip()
        message_id = post['message_id'].value
        
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

            cursor.execute('INSERT INTO comments (sender, text, date, file_name, mime_type, file, user_id, message_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (login_cookie, text, message_date, file_name, mime_type, file_bin, user.id, message_id))
            
        else:
            cursor.execute('INSERT INTO comments (sender, text, date, user_id, message_id) VALUES (%s, %s, %s, %s, %s)',
                (login_cookie, text, message_date, user.id, message_id))

        conn.commit()
        cursor.close()
        conn.close()
        
        from threading import Thread
        Thread(target=self.send_push, args=(login_cookie, message_date.strftime('%H:%M (%d.%m.%Y)') + '\n комментарий от ' + login_cookie, 'http://localhost:8000/comments')).start()

        self.response_headers = [
            ('Location', '/message?id=' + message_id),
        ]
        self.status = '303 See Other'
        
        return self.status, self.response_headers, self.content
