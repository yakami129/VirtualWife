import json
import os
from ..base_translation_client import BaseTranslationClient
from volcengine.ApiInfo import ApiInfo
from volcengine.Credentials import Credentials
from volcengine.ServiceInfo import ServiceInfo
from volcengine.base.Service import Service


class HuoShanTranslationClient(BaseTranslationClient):

    access_key: str
    secret_key: str
    service_info: ServiceInfo
    query: dict[str, str]
    api_info: dict
    service: Service

    def __init__(self) -> None:

        self.access_key = os.environ.get("HUO_SHAN_ACCESS_KEY")
        self.secret_key = os.environ.get("HUO_SHAN_SECRET_KEY")
        self.service_info = ServiceInfo('translate.volcengineapi.com',
                                        {'Content-Type': 'application/json'},
                                        Credentials(self.access_key, self.secret_key,
                                                    'translate', 'cn-north-1'),
                                        5,
                                        5)
        self.query = {
            'Action': 'TranslateText',
            'Version': '2020-06-01'
        }
        self.api_info = {
            'translate': ApiInfo('POST', '/', self.query, {}, {})
        }
        self.service = Service(self.service_info, self.api_info)

    def translation(self, text: str, target_language: str) -> str:
        body = {
            'TargetLanguage': target_language,
            'TextList': [text],
        }
        res = self.service.json('translate', {}, json.dumps(body))
        res = json.loads(res)
        translation = res["TranslationList"][0]["Translation"]
        return translation
