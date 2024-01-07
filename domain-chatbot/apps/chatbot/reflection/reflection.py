import json
import logging
from ..llms.llm_model_strategy import LlmModelDriver

logger = logging.getLogger(__name__)


class ImportanceRating:
    """判断记忆的重要性"""

    llm_model_driver: LlmModelDriver
    input_prompt: str = """
    <s>[INST] <<SYS>>
    当评估记忆的重要性时，可以根据分数的不同设置评分标准，如下所示：
    ```
    1-3分-低重要性：
    缺乏对记忆价值的认识，可能认为记忆在个人、学术或职业生活中没有显著影响。
    例子：忽视学习中的关键信息，对过去的经历缺乏回忆。
    4-6分-中等重要性：
    认识到记忆的一定价值，但可能对其实际影响程度有所疑虑。
    例子：对日常事务的记忆较为关注，但未充分利用记忆来提升学业或职业表现。
    7-8分-高重要性：
    理解记忆在个人、学术或职业生活中的重要性，有一定的努力去保持和提升记忆能力。
    例子：积极参与学习，主动寻找记忆技巧，关注职业发展中的经验总结。
    9-10分-极高重要性：
    将记忆视为成功的关键因素，不断投入时间和精力来提升记忆能力。
    例子：系统性学习和应用记忆技巧，充分利用过去经验指导未来决策，在学术或职业领域中取得显著成就。
    ```
    记忆上下文:
    ```
    {memory}
    ```
    在1到10的整数范围内，你会给记忆的重要性打多少分？
    """

    output_prompt: str = """
    Please output the exact integer, not the range.
    Please output the result in all lowercase letters.
    Please only output the result, no need to output the reasoning process.
    Please output the result strictly in JSON format. The output example is as follows:
    {"rating":"your reasoning Rating"}
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
        logger.debug(f"=># ImportanceRating # => 当前记忆重要性评分:{result}")
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
    # Role: 用户画像分析AI

    ## Profile
    - Description: 用户画像分析AI，根据记忆推理和更新用户画像
    
    ### Skill
    ```
    1. 根据记忆推理和更新用户画像
    ```
    
    
    ## Rules
    ```
    1. 请只输出结果，不需要输出推理过程。
    2. 用户画像的信息不能出现重复
    3. 请使用中文输出用户画像数据
    4. 只输出“yuki129”的用户画像数据
    5. 输出的用户画像数据，严格遵循用户画像的数据结构
    6. <Example>中的Memory和Personas仅提供参考,请不要作为你进行用户画像分析的参数
    """

    output_prompt: str = """
    ## OutputFormat :
    ``` 
    1. 请严格以JSON数组格式输出结果。
    2. 输出示例如下:
    {
        "personas": {
            "Persona": "描述用户的职业，如果没有设置为未知",
            "Fictional name": "描述用户的名称，如果没有设置为未知",
            "Sex": "描述用户的性别，如果没有设置为未知",
            "Job title/major responsibilities": "描述用户的职责和工作内容，如果没有设置为未知",
            "Demographics": "描述用户的人际关系，家庭关系，如果没有设置为未知",
            "Goals and tasks": "描述用户最近目标和想法，如果没有设置为未知",
            "hobby": "描述用户的爱好，如果没有设置为未知",
            "promise": "描述用户与别人的约定，如果没有设置为未知",
            "topic": "描述用户喜欢聊什么话题，如果没有设置为未知"
        }
    }
    ```
    
    # Example:
    ```
    示例1：
    - Memory:
    ```
    张三说我最近和朋友吵架了
    爱莉说没关系，你和我说说
    张三说他说想玩LOL，可我已经不喜欢玩LOL了，所以吵架了
    爱莉说哦，我觉得这个是小事呀
    ```
    - Personas:
    ```
    {
      "Persona": "软件工程师",
      "Fictional name": "张三",
      "Sex":"男",
      "Job title/major responsibilities": "人工智能专家",
      "Demographics": "人工智能博士",
      "Goals and tasks": "专注人工智能领域;",
      "hobby": "他喜欢玩游戏和电竞，比如LoL、泰拉瑞亚",
      "promise": "和爱莉约好周末去吃烧烤",
      "topic": "喜欢聊动漫的话题"
    }
    ```
    - Output:
    ```
    {
    "personas": {
        "Persona": "软件工程师",
        "Fictional name": "张三",
        "Sex":"男",
        "Job title/major responsibilities": "人工智能专家",
        "Demographics": "人工智能博士",
        "Goals and tasks": "专注人工智能领域;",
        "hobby": "他喜欢玩游戏和电竞，比如泰拉瑞亚",
        "promise": "和爱莉约好周末去吃烧烤",
        "topic": "喜欢聊动漫的话题"
    }
    }
    ```
    ```
    
    ## Workflow
    ```
    1. 推理和分析我输入的参数Memory和Personas, 分析出需要新增和更新的用户画像信息
    2. 输出最终的用户画像信息
    ```
    """

    initialization_prompt: str = """
    ## Initialization
    你作为角色 <Role>, 拥有 <Skill>, 严格遵守 <Rules> 和 <OutputFormat>,参考<Example>, 基于我输入的参数，执行 <Workflow> 请输出结果。
    下面是我输入的参数：
    - Memory
    ```
    {memory}
    ```
    - Personas
    ```
    {portrait}
    ```
    """

    def __init__(self, llm_model_driver: LlmModelDriver, llm_model_driver_type: str) -> None:
        self.llm_model_driver = llm_model_driver
        self.llm_model_driver_type = llm_model_driver_type

    def analysis(self, role_name: str, portrait: str, memory: str) -> str:
        input_prompt = self.input_prompt.format(role_name=role_name)
        initialization_prompt = self.initialization_prompt.format(memory=memory,portrait=portrait)
        prompt = input_prompt + self.output_prompt + initialization_prompt
        logger.debug(f"=> prompt:{prompt}")
        result = self.llm_model_driver.chat(
            prompt=prompt, type=self.llm_model_driver_type, role_name="", you_name="", query="",
            short_history=[], long_history="")
        logger.debug(f"=> personas:{result}")
        analysis = "无"
        try:
            start_idx = result.find('{')
            end_idx = result.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = result[start_idx:end_idx + 1]
                json_data = json.loads(json_str)
                analysis = json_data["personas"]
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
