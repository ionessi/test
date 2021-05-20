import re
import urllib.request


class Default():
    
    def get_mime_type_list(self):
        image = ['image/gif', 'image/jpeg', 'image/png', 'image/webp']
        audio = ['audio/mpeg', 'audio/webm', 'audio/mp4', 'audio/ogg']

        return image, audio
    
    def get_link(self, message):
        if re.findall(r'https://\S+|http://\S+', message):
            urls = re.findall(r'https://\S+|http://\S+', message)
            
            for url in urls:
                title = self.get_title(url)
                
                if title == '':
                    title = 'не удалось получить заголовок'
                        
                message = message.replace(url, '<small>' + title + '</small>\n' + '<a class="cropped-link" href="' + url + '" target="_blank">' + url + '</a>')
        
        return message
        
    def get_titleeeeeeeee(self, url, coding):

        title_1 = ''
        title_2 = ''

        pattern = r'<title.*?>(.*?)</title>'

        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Android 9; Mobile; rv:81.0) Gecko/81.0 Firefox/81.0')
            res = urllib.request.urlopen(req).read().decode(coding).replace('\n', ' ').replace('\r', ' ').replace('  ', ' ')
            title_1 = re.findall(pattern, res)[0].strip()
        except:
            pass
            
        try:
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0')
            res = urllib.request.urlopen(req).read().decode(coding).replace('\n', ' ').replace('\r', ' ').replace('  ', ' ')
            title_2 = re.findall(pattern, res)[0].strip()
        except:
            pass

        lst = [title_1, title_2]
        lst.sort(key=len)
        title = lst[1]

        return title
    
    def get_title(self, url):
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0')
        
        try:
            res = urllib.request.urlopen(req)
            #print(type([1,2]))
            #print(res.headers)
        except:
            res = ''
            
        if res != '':
            content_type = res.headers['Content-Type']
            #print(content_type)
            pattern = r'charset=(\S+)'
            
            try:
                coding = re.findall(pattern, content_type)[0]
                #print(coding)
            except:
                coding = 'utf-8'
            #print(coding)
            try:
                html = res.read().decode(coding).replace('\n', ' ').replace('\r', ' ').replace('  ', ' ')
            except:
                html = ''
                
            pattern = r'<title.*?>(.+?)</title>'
            
            try:
                title = re.findall(pattern, html)[0].strip()
            except:
                title = ''
                
        else:
            title = ''
        
        #print(title)
        
        return title
        
