import json
import logging

from ..llms.llm_model_strategy import LlmModelDriver

logger = logging.getLogger(__name__)


class TopicBot:
    """寻找话题的机器人"""
    llm_model_driver: LlmModelDriver
    input_prompt: str = """
    <s>[INST] <<SYS>>
    你现在是一名观察者AI，你需要基于{role_name}记忆上下文，提供建议，指导{role_name}回复内容
    {role_name}当前记忆中的相关上下文摘要：
    ```
    {memory}
    ```
    """

    output_prompt: str = """
    Please output the result in all lowercase letters.
    Please output content in Chinese
    Please output the result strictly in JSON format. The output example is as follows:
    {"suggestion":"your reasoning suggestion"}
    <</SYS>>
    """

    def __init__(self, llm_model_driver: LlmModelDriver, llm_model_driver_type: str) -> None:
        self.llm_model_driver = llm_model_driver
        self.llm_model_driver_type = llm_model_driver_type

    def generation_topic(self, role_name: str, memory: str) -> str:
        input_prompt = self.input_prompt.format(role_name=role_name, memory=memory)
        prompt = input_prompt + self.output_prompt
        result = self.llm_model_driver.chat(
            prompt=prompt, type=self.llm_model_driver_type, role_name="", you_name="", query="",
            short_history=[], long_history="")
        logger.debug(f"=> suggestion:{result}")
        suggestion = ""
        try:
            start_idx = result.find('{')
            end_idx = result.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = result[start_idx:end_idx + 1]
                json_data = json.loads(json_str)
                suggestion = json_data["suggestion"]
            else:
                logger.warn("未找到匹配的JSON字符串")
        except Exception as e:
            logger.error("TopicBot error: %s" % str(e))
        return suggestion
