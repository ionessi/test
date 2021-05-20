
class Render():
    
    def render(self, path, **kwargs):

        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader('./templates'))
        template = env.get_template(path)
        html = template.render(kwargs).encode()
        
        return html
