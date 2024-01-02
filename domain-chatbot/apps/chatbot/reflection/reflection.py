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
    一个用户画像通常会有以下属性，你推理的用户画像一定需要包含以下属性
    ```
    姓名、别名、年龄、家庭状况、工作、技能/知识、目标/动机、喜好、人生态度、特殊癖好
    ```
    用户画像数据请以{role_name}为主体，只能推理与{role_name}有关的数据，请严谨的保证用户画像只有{role_name}的数据
    下面是{role_name}的用户画像数据:
    ```text
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
