import json
import logging

from ..llms.llm_model_strategy import LlmModelDriver

logger = logging.getLogger(__name__)


class PortraitObservation:
    """用户画像识别"""

    llm_model_driver: LlmModelDriver
    definition_prompt: str = """
    # Role: 用户画像实体识别AI

    ## Profile
    - Description: 根据对话文本识别文本中包含的用户画像实体
    
    ### Skill
    ```
    1. 根据对话文本识别文本中包含的用户画像实体
    2. 输出用户画像实体名称
    ```
    
    ## Rules
    ```
    1. 请只输出结果，不需要输出推理过程。
    2. 请识别文本中包含的用户画像实体，并且只输出实体名称
    ```
    """

    output_prompt: str = """
    ## OutputFormat :
    ``` 
    1. 请严格以JSON数组格式输出结果。
    2. 输出示例如下:{"entitys":["你识别的实体名称"]}
    ```
    
    # Example:
    ```
    示例1：
    - Text:
    ```
    你知道张三吗？我记得李四和他关系不好
    ```
    ```
    - Output:
    ```
    {
      "entitys": ["张三","李四"]
    }
    ```
    
    示例2：
    - Text:
    ```
    最近科比好像和奥尼尔吵架，他们在纽约时代广场打起来了呢
    ```
    ```
    - Output:
    ```
    {
      "entitys": ["科比","奥尼尔"]
    }
    ```
    ```
    
    ## Workflow
    ```
    1. 识别我输入的参数Text, 分析出用户画像名称
    2. 输出用户画像名称
    ```
    """

    initialization_prompt: str = """
    你作为角色 <Role>, 拥有 <Skill>, 严格遵守 <Rules> 和 <OutputFormat>,参考<Example>, 基于我输入的参数，执行 <Workflow> 请输出结果。
    下面是我输入的参数：
    - Text
    ```
    {text}
    ```
    """

    def __init__(self, llm_model_driver: LlmModelDriver, llm_model_driver_type: str) -> None:
        self.llm_model_driver = llm_model_driver
        self.llm_model_driver_type = llm_model_driver_type

    def observation(self, text: str) -> str:
        initialization_prompt = self.initialization_prompt.format(text=text)
        prompt = self.definition_prompt + self.output_prompt + initialization_prompt
        logger.info(f"=> prompt:{prompt}")
        result = self.llm_model_driver.chat(
            prompt=prompt, type=self.llm_model_driver_type, role_name="", you_name="", query="",
            short_history=[], long_history="")
        logger.info(f"=> entitys:{result}")
        entitys = []
        try:
            start_idx = result.find('{')
            end_idx = result.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = result[start_idx:end_idx + 1]
                json_data = json.loads(json_str)
                entitys = json_data["entitys"]
            else:
                logger.warn("未找到匹配的JSON字符串")
        except Exception as e:
            logger.error("PortraitObservation error: %s" % str(e))
        return entitys


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
        logger.info(f"topic prompt:{prompt}")
        logger.info(f"=> suggestion:{result}")
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
