import json
import logging
import threading
from ..character.character_generation import singleton_character_generation
from ..config import singleton_sys_config
from ..insight.insight import TopicBot
from ..process import process_core

logger = logging.getLogger(__name__)


def observe_memory_job():
    topic_bot = TopicBot(llm_model_driver=singleton_sys_config.llm_model_driver,
                         llm_model_driver_type=singleton_sys_config.conversation_llm_model_driver_type)
    character = singleton_character_generation.get_character(singleton_sys_config.character)
    role_name = character.role_name;

    # 拉取最近的记忆和对话上下文
    local_memory = query_local_memory()
    local_memory_list = [f"{item['human']}\n{item['ai']}" for item in local_memory]
    local_memory_str = '\n'.join(local_memory_list)
    topic = topic_bot.generation_topic(role_name, local_memory_str)
    if topic != "":
        process_core.chat(you_name=role_name, query=f"{role_name}需要需要基于该建议`{topic}`回复内容")
    print("observe_memory_job..........")


def query_local_memory():
    local_memory = singleton_sys_config.memory_storage_driver.short_memory_storage.pageQuery(1, 5)
    dict_list = []
    for json_string in local_memory:
        json_dict = json.loads(json_string)
        dict_list.append(json_dict)
    return dict_list;


def run_observe_memory_job(interval, observe_memory_job):
    threading.Timer(interval, run_observe_memory_job, [interval, observe_memory_job]).start()
    observe_memory_job()
