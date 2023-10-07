from jinja2 import (
    Environment,
    FileSystemLoader,
)


class MusicInfo:
    data: dict

    def __init__(self, data: dict) -> None:
        self.data = data

        if not 'artists_str' in self.data:
            self.data['artists_str'] = ', '.join(self.data['artists'])

    def generate_message(self, filename_txt: str) -> str:
        env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
        tmpl = env.get_template(filename_txt)
        message = tmpl.render(self.data)
        return message
