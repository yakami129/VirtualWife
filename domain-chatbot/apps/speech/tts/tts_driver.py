from abc import ABC, abstractmethod
from .edge_tts import Edge, edge_voices
from .bert_vits2 import BertVits2


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

    def synthesis(self, text: str, voice_id: str, **kwargs) -> str:
        print("voiceId:", voice_id)
        print("text:", text)
        return Edge.create_audio(text=text, voiceId=voice_id)

    def get_voices(self) -> list[dict[str, str]]:
        return edge_voices


class BertVITS2TTS(BaseTTS):

    '''Bert-VITS2 语音合成类'''

    def synthesis(self, text: str, voice_id: str, **kwargs) -> str:
        noise = kwargs.get("noise", "0.5")
        noisew = kwargs.get("noisew", "0.9")
        sdp_ratio = kwargs.get("sdp_ratio", "0.2")
        return BertVits2.synthesis(text=text, speaker=voice_id, noise=noise, noisew=noisew, sdp_ratio=sdp_ratio)

    def get_voices(self) -> list[dict[str, str]]:
        return BertVits2.get_voices()


class TTSDriver:

    '''TTS驱动类'''

    def synthesis(self, type: str, text: str, voice_id: str, **kwargs) -> str:
        tts = self.get_strategy(type)
        return tts.synthesis(text=text, voice_id=voice_id, kwargs=kwargs)

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
