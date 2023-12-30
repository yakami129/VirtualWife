from abc import ABC, abstractmethod
import logging
from .edge_tts import Edge, edge_voices
from .bert_vits2 import BertVits2

logger = logging.getLogger(__name__)


class BaseTTS(ABC):
    '''合成语音统一抽象类'''

    @abstractmethod
    def synthesis(self, text: str, voice_id: str, **kwargs) -> str:
        '''合成语音'''
        pass

    @abstractmethod
    def get_voices(self) -> list[dict[str, str]]:
        '''获取声音列表'''
        pass


class EdgeTTS(BaseTTS):
    '''Edge 微软语音合成类'''
    client: Edge

    def __init__(self):
        self.client = Edge()

    def synthesis(self, text: str, voice_id: str, **kwargs) -> str:
        return self.client.create_audio(text=text, voiceId=voice_id)

    def get_voices(self) -> list[dict[str, str]]:
        return edge_voices


class BertVITS2TTS(BaseTTS):
    '''Bert-VITS2 语音合成类'''
    client: BertVits2

    def __init__(self):
        self.client = BertVits2()

    def synthesis(self, text: str, voice_id: str, **kwargs) -> str:
        noise = kwargs.get("noise", 0.6)
        noisew = kwargs.get("noisew", 0.9)
        sdp_ratio = kwargs.get("sdp_ratio", 0.5)
        return self.client.synthesis(text=text, speaker=voice_id, noise=noise, noisew=noisew, sdp_ratio=sdp_ratio)

    def get_voices(self) -> list[dict[str, str]]:
        return self.client.get_voices()


class TTSDriver:
    '''TTS驱动类'''

    def synthesis(self, type: str, text: str, voice_id: str, **kwargs) -> str:
        tts = self.get_strategy(type)
        file_name = tts.synthesis(text=text, voice_id=voice_id, kwargs=kwargs)
        logger.info(f"TTS synthesis # type:{type} text:{text} => file_name: {file_name} #")
        return file_name;

    def get_voices(self, type: str) -> list[dict[str, str]]:
        tts = self.get_strategy(type)
        return tts.get_voices()

    def get_strategy(self, type: str) -> BaseTTS:
        if type == "Edge":
            return EdgeTTS()
        elif type == "Bert-VITS2":
            return BertVITS2TTS()
        else:
            raise ValueError("Unknown type")
