import re

class MusicInfo:
    data: dict

    def __init__(self, data: dict) -> None:
        self.data = data

        if not 'artists_str' in self.data:
            self.data['artists_str'] = ', '.join(self.data['artists'])

    def _replace_param(self, txt: str, param: str) -> str:
        param_name = param.strip('{} ')
        txt = txt.replace(param, self.data[param_name])
        return txt
    
    def generate_message(self, filename_txt: str) -> str:
        with open(filename_txt, 'r') as f:
            message = f.read()
            replace_list = re.findall('{{.*?}}', message)
            for param in replace_list:
                message = self._replace_param(message, param)
        return message
