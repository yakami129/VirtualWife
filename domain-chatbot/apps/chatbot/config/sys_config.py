import json
import os
from ..llms.llm_model_strategy import LlmModelDriver
from ..models import CustomRoleModel,SysConfigModel
from ..character.sys.maiko_zh import maiko_zh

config_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(config_dir, 'sys_config.json')
sys_code = "adminSettings"


def lazy_memory_storage(sys_config_json: any, sys_cofnig: any):
    from ..memory.memory_storage_strategy import MemoryStorageDriver
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
    return MemoryStorageDriver(type=memory_type, memory_storage_config=memory_storage_config, sysConfig=sys_cofnig)


class SysConfig():

    llm_model_driver: LlmModelDriver
    conversation_llm_model_driver_type: str
    enable_summary: bool
    summary_llm_model_driver_type: str
    enable_reflection: bool
    reflection_llm_model_driver_type: str
    memory_storage_driver: any
    character: int
    your_name: str
    room_id: str

    def __init__(self) -> None:
        self.load()

    def get(self):
        sys_config_obj = None;
        sys_config_json = "{}"
        with open(config_path, 'r') as f:
            sys_config_json = json.load(f)
        try:
            sys_config_obj = SysConfigModel.objects.filter(code=sys_code).first()
            if sys_config_obj == None:
                print("=> save sys config to db")
                sys_config_model = SysConfigModel(
                    code = sys_code,
                    config = json.dumps(sys_config_json)
                )
                sys_config_model.save()
            else:
                sys_config_json = json.loads(sys_config_obj.config)
        except Exception as e:
            print("=> load sys config error: %s" % str(e))
        return sys_config_json

    def save(self, sys_config_json: any):
        sys_config_obj = SysConfigModel.objects.get(code=sys_code)
        sys_config_obj.config = json.dumps(sys_config_json)
        sys_config_obj.save()

    def load(self):

        print("========================load sys config ========================")

        sys_config_json = self.get()

        # 初始化默认角色
        try:
            result = CustomRoleModel.objects.all()
            if len(result) == 0:
                print("=> load default character")
                custom_role = CustomRoleModel(
                    role_name=maiko_zh.role_name,
                    persona=maiko_zh.persona,
                    personality=maiko_zh.personality,
                    scenario=maiko_zh.scenario,
                    examples_of_dialogue=maiko_zh.examples_of_dialogue,
                    custom_role_template_type=maiko_zh.custom_role_template_type
                )
                custom_role.save()
        except Exception as e:
            print("=> load default character ERROR: %s" % str(e))
        
        # 加载角色配置
        character = sys_config_json["characterConfig"]["character"]
        yourName = sys_config_json["characterConfig"]["yourName"]
        print("=> character Config")
        print(f"character:{character}")
        print(f"yourName:{yourName}")
        self.character = character
        self.yourName = yourName

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
            print(f"HTTP_PROXY:" + os.environ['HTTP_PROXY'])
            print(f"HTTPS_PROXY:"+os.environ['HTTPS_PROXY'])
            print(f"SOCKS5_PROXY:"+os.environ['SOCKS5_PROXY'])

        # 加载对话模块配置
        print("=> Chat Config")
        self.llm_model_driver = LlmModelDriver()
        self.conversation_llm_model_driver_type = sys_config_json[
            "conversationConfig"]["languageModel"]
        print(f"conversation_llm_model_driver_type:" +
              self.conversation_llm_model_driver_type)

        # 是否开启记忆摘要
        print("=> Memory Config")
        self.enable_summary = sys_config_json["memoryStorageConfig"]["enableSummary"]
        print("enable_summary："+str(self.enable_summary))
        if (self.enable_summary):
            self.summary_llm_model_driver_type = sys_config_json[
                "memoryStorageConfig"]["languageModelForSummary"]
            print("summary_llm_model_driver_type：" +
                  self.summary_llm_model_driver_type)

        self.enable_reflection = sys_config_json["memoryStorageConfig"]["enableReflection"]
        print("enableReflection"+str(self.enable_reflection))
        if (self.enable_reflection):
            self.reflection_llm_model_driver_type = sys_config_json[
                "memoryStorageConfig"]["languageModelForReflection"]
            print("reflection_llm_model_driver_type" +
                  self.summary_llm_model_driver_type)

        # 懒加载记忆模块
        self.memory_storage_driver = lazy_memory_storage(
            sys_config_json=sys_config_json, sys_cofnig=self)

        # 加载直播配置
        # if self.bili_live_client != None:
        #     self.bili_live_client.stop()
        # room_id = str(sys_config_json["liveStreamingConfig"]["B_STATION_ID"])
        # print("=> liveStreaming Config")
        # self.room_id = room_id
        # self.bili_live_client = BiliLiveClient(room_id=room_id)
        # # 创建后台线程
        # background_thread = threading.Thread(
        #     target=asyncio.run(self.bili_live_client.start()))
        # # 将后台线程设置为守护线程，以便在主线程结束时自动退出
        # background_thread.daemon = True
        # # 启动后台线程
        # background_thread.start()
