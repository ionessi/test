from controllers.Init import Init
from controllers.Render import Render
from controllers.ConnectDb import ConnectDb
from controllers.Default import Default


class Index(Init, Render, ConnectDb, Default):
        
    def index(self):
        conn, cursor = self.connect()

        cursor.execute('SELECT COUNT(id) FROM messages')
        count = cursor.fetchone().count

        limit = 10
        
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

        cursor.execute('SELECT id, sender, text, date, file_name, mime_type FROM messages ORDER BY id DESC LIMIT %s OFFSET %s', (limit, offset,))
        
        messages = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        image, audio = self.get_mime_type_list()
        
        self.content = self.render('index.html', messages=messages, pages=pages, page=page, image=image, audio=audio)
        self.response_headers = [
            ('Content-type', 'text/html; charset=UTF-8'),
            ('Content-Length', str(len(self.content)))
        ]

        return self.status, self.response_headers, self.content
    
    def save_information(self):

        conn, cursor = self.connect()
        
        import json
        
        post_data = json.loads(self.environ['wsgi.input'].read(int(self.environ['CONTENT_LENGTH'])).decode())
        subscription = post_data['subscription']
        
        cursor.execute('SELECT * FROM webpush WHERE auth=%s AND p256dh=%s', (subscription['keys']['auth'], subscription['keys']['p256dh'],))
        push = cursor.fetchone()

        if not push:
            try:
                ip = self.environ['HTTP_X_FORWARDED_FOR']
            except:
                ip = self.environ['REMOTE_ADDR']
                
            from urllib.parse import parse_qs
            
            cookies = parse_qs(self.environ['HTTP_COOKIE'], separator='; ')
            login_cookie = cookies.get('login')[0]
            
            cursor.execute('SELECT * FROM users WHERE login=%s', (login_cookie,))
            user = cursor.fetchone()
                
            cursor.execute('INSERT INTO webpush (login, user_agent, browser, endpoint, auth, p256dh, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                (login_cookie, self.environ['HTTP_USER_AGENT'], post_data['browser'], subscription['endpoint'], subscription['keys']['auth'], subscription['keys']['p256dh'], user.id))
            
            conn.commit()
        
        cursor.close()
        conn.close()

        return self.status, self.response_headers, self.content
