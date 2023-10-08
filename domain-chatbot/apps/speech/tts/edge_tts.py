import os
import subprocess

from ..utils.uuid_generator import generate


edge_voices = [
    {"id": "zh-CN-XiaoxiaoNeural", "name": "xiaoxiao"},
    {"id": "zh-CN-XiaoyiNeural", "name": "xiaoyi"},
    {"id": "zh-CN-YunjianNeural", "name": "yunjian"},
    {"id": "zh-CN-YunxiNeural", "name": "yunxi"},
    {"id": "zh-CN-YunxiaNeural", "name": "yunxia"},
    {"id": "zh-CN-YunyangNeural", "name": "yunyang"},
    {"id": "zh-CN-liaoning-XiaobeiNeural", "name": "xiaobei"},
    {"id": "zh-CN-shaanxi-XiaoniNeural", "name": "xiaoni"},
    {"id": "zh-HK-HiuGaaiNeural", "name": "hiugaai"},
    {"id": "zh-HK-HiuMaanNeural", "name": "hiumaan"},
    {"id": "zh-HK-WanLungNeural", "name": "wanlung"},
    {"id": "zh-TW-HsiaoChenNeural", "name": "hsiaochen"},
    {"id": "zh-TW-HsiaoYuNeural", "name": "hsioayu"},
    {"id": "zh-TW-YunJheNeural", "name": "yunjhe"}
]


class Edge():

    @staticmethod
    def remove_html(text: str):
        # TODO 待改成正则
        new_text = text.replace('[', "")
        new_text = new_text.replace(']', "")
        return new_text
    
    @staticmethod
    def create_audio(text, voiceId):
        new_text = Edge.remove_html(text)
        print(f"Text without html tags: {new_text}")
        pwdPath = os.getcwd()
        file_name = generate() + ".mp3"
        filePath = pwdPath + "/tmp/" + file_name
        dirPath = os.path.dirname(filePath)
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        if not os.path.exists(filePath):
            # 用open创建文件 兼容mac
            open(filePath, 'a').close()

        subprocess.run(["edge-tts", "--voice", voiceId, "--text", new_text,
                        "--write-media", str(filePath)])

        return file_name
