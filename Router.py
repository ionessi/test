from importlib import import_module
from urllib.parse import parse_qs

from controllers.Init import Init
from controllers.Render import Render


class Router(Init, Render):
    import sys
    print(sys.version_info)
    def routing(self):
        
        if self.environ['wsgi.url_scheme'] == 'http' and self.environ['HTTP_HOST'] != 'localhost:8000':
            self.status = '303 See Other'
            self.response_headers = [
                ('Location', 'https://' + self.environ['HTTP_HOST'] + self.environ['PATH_INFO']),
            ]

            return self.status, self.response_headers, self.content
        
        pages_without_verification = [
                '/sw.js',
                '/index/save-information',
                '/robots.txt',
                '/static/get',
                '/sign_in',
                '/registration',
                '/file/message',
                '/file/comment',
                '/db/create-tables',
                '/db/drop-tables'
            ]
        
        if self.environ['PATH_INFO'] in pages_without_verification:
            pass
        
        else:
            from controllers.Sign_In import Sign_In
            sign_in = Sign_In(self.environ)
            res = sign_in.check(self.environ['PATH_INFO'])
            
            if not res:
                self.status = '303 See Other'
                self.response_headers = [
                    ('Location', '/sign_in')
                ]

                return self.status, self.response_headers, self.content
            
    
        if self.environ['PATH_INFO'] == '/':
            from controllers.Index import Index
            
            index = Index(self.environ)
            self.status, self.response_headers, self.content = index.index()
            
        elif self.environ['PATH_INFO'] == '/robots.txt':
            from controllers.Static import Static
            self.environ['QUERY_STRING'] = 'path=robots.txt'
            static = Static(self.environ)
            self.status, self.response_headers, self.content = static.get()
            
            from threading import Thread
            
            from controllers.Visitors import Visitors
            visitors = Visitors(self.environ)
            Thread(target=visitors.add_visitor, args=(self.environ['PATH_INFO'].upper() + ' TRUE ',)).start()
            
        elif self.environ['PATH_INFO'] == '/sw.js':
            from controllers.Static import Static
            self.environ['QUERY_STRING'] = 'path=js/sw.js'
            static = Static(self.environ)
            self.status, self.response_headers, self.content = static.get()
            
        else:
            parsed_string = self.environ['PATH_INFO'].replace('-', '_').split('/')
            
            module_name = parsed_string[1].title()
            
            #try:
            module = import_module('controllers.' + module_name)
            #except ModuleNotFoundError:
                #module = False
                
            if module:
                obj = getattr(module, module_name)(self.environ)
                
                try:
                    method = parsed_string[2]
                except:
                    method = 'index'
                    
                #try:
                self.status, self.response_headers, self.content = getattr(obj, method)()
                #except:
                    #method = False
            
            if not module or not method:
                self.content = self.content = self.render('404.html')
                self.status = '404 NOT FOUND'
                self.response_headers = [
                    ('Content-type', 'text/html; charset=UTF-8'),
                    ('Content-Length', str(len(self.content)))
                ]
            
        
        return self.status, self.response_headers, self.content      
