import requests
import os
import json
from ..utils.AuthV3Util import addAuthParams

# 您的应用ID
APP_KEY = os.getenv("YOUDAO_APP_KEY")
# 您的应用密钥
APP_SECRET = os.getenv("YOUDAO_SECRET_KEY")


class TranslationClient:

    @staticmethod
    def translation(query:str) -> str:
        q = query
        lang_from = 'zh-CHS'
        lang_to = 'ja'
        data = {'q': q, 'from': lang_from, 'to': lang_to}
        addAuthParams(APP_KEY, APP_SECRET, data)
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = requests.post('https://openapi.youdao.com/api', data, header)
        content = str(res.content, 'utf-8')
        return json.loads(content)