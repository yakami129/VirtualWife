import json
import os
import logging
from ..llms.llm_model_strategy import LlmModelDriver

config_dir = os.path.dirname(os.path.abspath(__file__)) 
config_path = os.path.join(config_dir, 'sys_config.json')

def lazy_memory_storage(sys_config_json:any,sys_cofnig:any):
    from ..memory.storage.memory_storage_strategy import MemoryStorageDriver
    # 加载记忆模块配置
    memory_type = sys_config_json["memoryStorageConfig"]["longTermMemoryType"]
    print(f"memory_type:{memory_type}")
    memory_storage_config = {
        "host": sys_config_json["memoryStorageConfig"]["milvusMemory"]["host"],
        "port": sys_config_json["memoryStorageConfig"]["milvusMemory"]["port"],
        "user": sys_config_json["memoryStorageConfig"]["milvusMemory"]["user"],
        "password": sys_config_json["memoryStorageConfig"]["milvusMemory"]["password"],
        "db_name": sys_config_json["memoryStorageConfig"]["milvusMemory"]["dbName"],
        "maxMemoryLoads": sys_config_json["memoryStorageConfig"]["localMemory"]["maxMemoryLoads"]
    }
    print(f"memory_storage_config:{memory_storage_config}")
    # 加载记忆模块驱动
    return MemoryStorageDriver(type=memory_type, memory_storage_config=memory_storage_config,sysConfig=sys_cofnig)

class SysConfig():

    llm_model_driver : LlmModelDriver
    conversation_llm_model_driver_type : str
    enable_summary: bool
    summary_llm_model_driver_type : str
    enable_reflection: bool
    reflection_llm_model_driver_type : str
    memory_storage_driver : any
    character: str
    your_name: str

    def __init__(self) -> None:
        self.load()

    def get(self):
        ## 获取当前目录下的sys_config.json文件,并转成json对象
        with open(config_path, 'r') as f:
            sys_config = json.load(f)
        return sys_config
    
    def save(self,sys_config_json:any):
        ## 将sys_config_json 写入到当前目录下的sys_config.json文件中
        with open(config_path, 'w') as f:
            json.dump(sys_config_json, f)
        return ""

    def load(self):

        print("========================load sys config ========================")

        sys_config_json = self.get();

        # 加载角色配置
        character = sys_config_json["characterConfig"]["character"]
        yourName = sys_config_json["characterConfig"]["yourName"]
        print("=> character Config")
        print(f"character:{character}")
        print(f"yourName:{yourName}")
        self.character = character
        self.yourName = yourName

        # 加载直播配置
        B_STATION_ID = str(sys_config_json["liveStreamingConfig"]["B_STATION_ID"])
        print("=> liveStreaming Config")
        print(f"B_STATION_ID:{B_STATION_ID}")
        os.environ['B_STATION_ID'] = B_STATION_ID

        # 加载大语言模型配置
        os.environ['OPENAI_API_KEY'] = sys_config_json["languageModelConfig"]["openai"]["OPENAI_API_KEY"]
        os.environ['OPENAI_BASE_URL'] = sys_config_json["languageModelConfig"]["openai"]["OPENAI_BASE_URL"]
        os.environ['TEXT_GENERATION_API_URL'] = sys_config_json["languageModelConfig"]["textGeneration"]["TEXT_GENERATION_API_URL"]

        # 是否开启proxy
        enableProxy = sys_config_json["enableProxy"]
        print("=> Proxy Config ")
        print(f"enableProxy:{enableProxy}")
        if enableProxy:
            os.environ['HTTP_PROXY'] = sys_config_json["httpProxy"]
            os.environ['HTTPS_PROXY'] = sys_config_json["httpsProxy"]
            os.environ['SOCKS5_PROXY'] = sys_config_json["socks5Proxy"]
            print(f"HTTP_PROXY:"+sys_config_json["httpProxy"])
            print(f"HTTPS_PROXY:"+sys_config_json["httpsProxy"])
            print(f"SOCKS5_PROXY:"+sys_config_json["socks5Proxy"])


        # 加载对话模块配置
        print("=> Chat Config")
        self.llm_model_driver = LlmModelDriver()
        self.conversation_llm_model_driver_type = sys_config_json["conversationConfig"]["languageModel"]
        print(f"conversation_llm_model_driver_type:"+self.conversation_llm_model_driver_type)

        # 是否开启记忆摘要
        print("=> Memory Config")
        self.enable_summary = sys_config_json["memoryStorageConfig"]["enableSummary"]
        print("enable_summary："+str(self.enable_summary))
        if(self.enable_summary):
             self.summary_llm_model_driver_type = sys_config_json["memoryStorageConfig"]["languageModelForSummary"]
             print("summary_llm_model_driver_type："+self.summary_llm_model_driver_type)

        self.enable_reflection = sys_config_json["memoryStorageConfig"]["enableReflection"]
        print("enableReflection"+str(self.enable_reflection))
        if(self.enable_reflection):
             self.reflection_llm_model_driver_type = sys_config_json["memoryStorageConfig"]["languageModelForReflection"]
             print("reflection_llm_model_driver_type"+self.summary_llm_model_driver_type)

        # 懒加载记忆模块
        self.memory_storage_driver = lazy_memory_storage(sys_config_json=sys_config_json,sys_cofnig=self)
      
