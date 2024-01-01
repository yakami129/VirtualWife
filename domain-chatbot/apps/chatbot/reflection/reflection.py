import json
import logging
import time
from .reflection_template import ReflectionTemplate
from ..llms.llm_model_strategy import LlmModelDriver

logger = logging.getLogger(__name__)


class ImportanceRating:
    """判断记忆的重要性"""

    llm_model_driver: LlmModelDriver
    input_prompt: str = """
    <s>[INST] <<SYS>>
    On the scale of to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance,birthday，unemployment，quarrel，hobby), rate the likely poignancy of the following piece of memory.
    Memory: 
    ```
    {memory}
    ```
    """

    output_prompt: str = """
    Please output the result in all lowercase letters.
    Please only output the result, no need to output the reasoning process.
    Please use the output of your reasoning emotion.
    Please output integer
    Please output the result strictly in JSON format. The output example is as follows:
    {"rating":"your reasoning rating"}
    <</SYS>>
    """

    def __init__(self, llm_model_driver: LlmModelDriver, llm_model_driver_type: str) -> None:
        self.llm_model_driver = llm_model_driver
        self.llm_model_driver_type = llm_model_driver_type

    def rating(self, memory: str) -> str:
        input_prompt = self.input_prompt.format(memory=memory)
        prompt = input_prompt + self.output_prompt
        result = self.llm_model_driver.chat(
            prompt=prompt, type=self.llm_model_driver_type, role_name="", you_name="", query="",
            short_history=[], long_history="")
        logger.info(f"=># ImportanceRating # => 当前记忆重要性评分:{result}")
        rating = "1"
        try:
            start_idx = result.find('{')
            end_idx = result.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = result[start_idx:end_idx + 1]
                json_data = json.loads(json_str)
                rating = json_data["rating"]
            else:
                logger.warn("未找到匹配的JSON字符串")
        except Exception as e:
            logger.error("ImportanceRating error: %s" % str(e))
        return int(rating)


class PortraitAnalysis:
    """反思 - 用户画像分析"""

    llm_model_driver: LlmModelDriver
    input_prompt: str = """
    <s>[INST] <<SYS>>
    你现在是一名用户画像分析AI，你需要基于我提供的记忆进行反思推理，并更新{role_name}的用户画像数据，如果有多个反思推理结果,请使用';'分割。
    你只能基于{role_name}的用户画像数据进行新增数据，更新过时数据，一定不能删除数据，并且不能有重复数据。
    用户画像数据请以{role_name}为主体，只能推理与{role_name}有关的数据。
    下面是{role_name}的用户画像数据:
    ```
    {portrait}
    ```
    {role_name}关联的记忆：
    ```
    {memory}
    ```
    Please only infer the portraits of {role_name} characters.
    """

    output_prompt: str = """
    The length of each result character you infer must not be greater than 10.
    Please output the result in all lowercase letters.
    Please output content in Chinese.
    Please only output the result, no need to output the reasoning process.
    Please keep the data rigorous and do not miss core data.
    Please output the result strictly in JSON format. The output example is as follows:
    {"analysis":"your reasoning analysis"}
    <</SYS>>
    """

    def __init__(self, llm_model_driver: LlmModelDriver, llm_model_driver_type: str) -> None:
        self.llm_model_driver = llm_model_driver
        self.llm_model_driver_type = llm_model_driver_type

    def analysis(self, role_name: str, portrait: str, memory: str) -> str:
        input_prompt = self.input_prompt.format(role_name=role_name, portrait=portrait, memory=memory)
        prompt = input_prompt + self.output_prompt
        logger.info(f"=> prompt:{prompt}")
        result = self.llm_model_driver.chat(
            prompt=prompt, type=self.llm_model_driver_type, role_name="", you_name="", query="",
            short_history=[], long_history="")
        logger.debug(f"=> analysis:{result}")
        analysis = "1"
        try:
            start_idx = result.find('{')
            end_idx = result.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = result[start_idx:end_idx + 1]
                json_data = json.loads(json_str)
                analysis = json_data["analysis"]
            else:
                logger.warn("未找到匹配的JSON字符串")
        except Exception as e:
            logger.error("PortraitAnalysis error: %s" % str(e))
        return analysis

# class ReflectionGeneration():
#     reflection_template: ReflectionTemplate
#
#     def __init__(self) -> None:
#         self.reflection_template = ReflectionTemplate()
#
#     def generation(self, role_name: str) -> None:
#         timestamp = time.time()
#         expr = f'timestamp <= {timestamp}'
#         result = singleton_sys_config.memory_storage_driver.pageQuery(
#             1, 100, expr)
#
#         result = [item['text'] for item in result]
#         prompt = self.reflection_template.format(result)
#
#         reflection_result = singleton_sys_config.memory_storage_driver.chat(prompt=prompt,
#                                                                             type=singleton_sys_config.reflection_llm_model_driver_type,
#                                                                             role_name=role_name, you_name="", query="",
#                                                                             short_history="", long_history="")
#         reflection_result_arr = self.reflection_template.output_format(
#             reflection_result)
#
#         # 批量写入到向量数据库中
#         for i in range(len(reflection_result_arr)):
#             item = reflection_result_arr[i].strip()
#             pk = singleton_sys_config.memory_storage_driver.get_current_entity_id()
#             singleton_sys_config.memory_storage_driver.save(pk, item, role_name)
