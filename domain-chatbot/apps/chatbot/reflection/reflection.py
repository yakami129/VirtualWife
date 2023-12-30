import json
import logging
import time
from .reflection_template import ReflectionTemplate
from ..config import singleton_sys_config
from ..llms.llm_model_strategy import LlmModelDriver

logger = logging.getLogger(__name__)


class ImportanceRating:
    """判断记忆的重要性"""

    llm_model_driver: LlmModelDriver
    input_prompt: str = """
    <s>[INST] <<SYS>>
    On the scale of to 10, where 1 is purely mundane (e.g., brushing teeth, making bed) and 10 is extremely poignant (e.g., a break up, college acceptance), rate the likely poignancy of the following piece of memory.
    Memory: 
    ```
    {memory}
    ```
    """

    output_prompt: str = """
    Please output the result in all lowercase letters.
    Please only output the result, no need to output the reasoning process.
    Please use the output of your reasoning emotion.
    Please output the result strictly in JSON format. The output example is as follows:
    {"rating":"your reasoning rating"}
    <</SYS>>
    """

    def __init__(self, llm_model_driver: LlmModelDriver, llm_model_driver_type: str) -> None:
        self.llm_model_driver = llm_model_driver
        self.llm_model_driver_type = llm_model_driver_type

    def inference_rating(self, memory: str) -> str:
        input_prompt = self.input_prompt.format(memory=memory)
        prompt = input_prompt + self.output_prompt
        result = self.llm_model_driver.chat(
            prompt=prompt, type=self.llm_model_driver_type, role_name="", you_name="", query="",
            short_history=[], long_history="")
        logger.debug(f"=> rating:{result}")
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





class ReflectionGeneration():
    reflection_template: ReflectionTemplate

    def __init__(self) -> None:
        self.reflection_template = ReflectionTemplate()

    def generation(self, role_name: str) -> None:
        timestamp = time.time()
        expr = f'timestamp <= {timestamp}'
        result = singleton_sys_config.memory_storage_driver.pageQuery(
            1, 100, expr)

        result = [item['text'] for item in result]
        prompt = self.reflection_template.format(result)

        reflection_result = singleton_sys_config.memory_storage_driver.chat(prompt=prompt,
                                                                            type=singleton_sys_config.reflection_llm_model_driver_type,
                                                                            role_name=role_name, you_name="", query="",
                                                                            short_history="", long_history="")
        reflection_result_arr = self.reflection_template.output_format(
            reflection_result)

        # 批量写入到向量数据库中
        for i in range(len(reflection_result_arr)):
            item = reflection_result_arr[i].strip()
            pk = singleton_sys_config.memory_storage_driver.get_current_entity_id()
            singleton_sys_config.memory_storage_driver.save(pk, item, role_name)
