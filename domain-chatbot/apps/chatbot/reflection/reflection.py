import json
import logging
from ..llms.llm_model_strategy import LlmModelDriver

logger = logging.getLogger(__name__)


class SummarizeAI:
    """将记忆进行总结的AI"""

    llm_model_driver: LlmModelDriver
    __system_prompt: str = """
        你现在是一名对话总结AI，我给定一批对话历史，你需要总结与“小王”有关的事件。
        Here are some examples:
        Chat History：
        ```
        景天说今天樱花开得真美，很高兴能和你一起赏花。
        曼玉说我也是，景天。你总能发现这样美丽的地方。
        
        景天说我在想，我们的下一个旅行目的地应该去哪里呢？
        曼玉说我听说海边的小镇很不错，我们可以去那里画画，放松一下。
        
        景天说听起来不错！我来规划我们的行程。
        曼玉说太好了，我已经开始期待我们的小冒险了。
        
        景天说曼玉，我今天尝试了画画，但我觉得我真的没有你那么有天赋。
        曼玉说每个人的开始都不容易，景天。我相信你会进步的，重要的是享受创作的过程。
        
        景天说谢谢你的鼓励，我会继续努力的。
        曼玉说我们一起进步，一起创造更多美好的回忆。
        ```
        Event:
        ```
        {"events":[
         "景天和曼玉在春季的樱花节相遇并坠入爱河。",
         "景天和曼玉计划了一次去海边小镇的旅行，希望在那里共同创作艺术作品。",
         "景天尝试学习绘画，虽然遇到了困难，但曼玉的鼓励让他没有放弃。",
         "景天和曼玉共同期待着更多的旅行和创作，希望通过这些经历加深彼此之间的理解和爱情。"
        ]
        ```
        遵守的规则：
        1. 请严格按照json格式输出内容。
       """
    __input_prompt: str = """
        下面是我的对话历史：
        Chat History：
        ```
        {chat_history}
        ```
        Event:
          """

    def __init__(self, llm_model_driver: LlmModelDriver, llm_model_driver_type: str) -> None:
        self.llm_model_driver = llm_model_driver
        self.llm_model_driver_type = llm_model_driver_type

    def summarize(self, chat_history: str) -> str:
        input_prompt = self.__input_prompt.format(chat_history=chat_history)
        prompt = self.__system_prompt + input_prompt
        result = self.llm_model_driver.chat(
            prompt=prompt, type=self.llm_model_driver_type, role_name="", you_name="", query="",
            short_history=[], long_history="")
        logger.debug(f"=># summarize # => \n {result}")
        summarize = []
        try:
            start_idx = result.find('{')
            end_idx = result.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = result[start_idx:end_idx + 1]
                json_data = json.loads(json_str)
                summarize = json_data["events"]
            else:
                logger.warn("未找到匹配的JSON字符串")
        except Exception as e:
            logger.error("SummarizeAI error: %s" % str(e))
        return summarize


class InsightAI:
    """需要根据以下陈述中推断出5个高级见解"""

    llm_model_driver: LlmModelDriver
    __system_prompt: str = """
    你是一名洞察AI，你需要根据以下陈述中推断出5个高级见解。
    Here are some examples:
    Statements:
    ```
    1. Klaus Mueller is writing a research paper
    2. Klaus Mueller enjoys reading a book on gentrification
    3. Klaus Mueller is conversing with Ayesha Khan about exercising
    ```
    Output:
    ```
    {
        "insights": [{
            "insight": "克劳斯·穆勒有学术倾向或从事学术活动。写研究论文表明深入参与学术或智力追求，表明克劳斯有学术或研究导向的心态。",
            "becauseOf": ["1"]
        }, {
            "insight": "克劳斯·穆勒对社会问题或城市发展感兴趣。阅读一本关于中产阶级化的书表明对复杂的社会和经济现象感兴趣，特别是那些影响城市环境的现象，表明克劳斯倾向于理解并可能解决社会挑战。",
            "becauseOf": ["2"]
        }, {
            "insight": "克劳斯·穆勒重视身体健康。与某人谈论锻炼表明克劳斯重视身体活动，这通常与对健康的关注有关。",
            "becauseOf": ["3"]
        }, {
            "insight": "克劳斯·穆勒是一个多维的个体，有着不同的兴趣。从事学术写作、阅读社会问题和讨论锻炼表明一个人在智力、社会和身体领域有着不同的兴趣。",
            "becauseOf": ["1", "2", "3"]
        }, {
            "insight": "克劳斯·穆勒重视人际沟通和协作。参与关于锻炼的对话，尤其是与提到名字的特定人，表明克劳斯重视社交互动，并可能将锻炼视为公共或共享活动，强调对话的重要性，以及可能的团队合作或个人或职业生活中的共享经验。",
            "becauseOf": ["3"]
        }]
    }
    ```
    """
    __input_prompt: str = """
      下面是我的Statements：
        Statements:
        ```
        {statements}
        ```
        Output:
   """

    def __init__(self, llm_model_driver: LlmModelDriver, llm_model_driver_type: str) -> None:
        self.llm_model_driver = llm_model_driver
        self.llm_model_driver_type = llm_model_driver_type

    def insight(self, statements: str) -> str:
        input_prompt = self.__input_prompt.format(statements=statements)
        prompt = self.__system_prompt + input_prompt
        result = self.llm_model_driver.chat(
            prompt=prompt, type=self.llm_model_driver_type, role_name="", you_name="", query="",
            short_history=[], long_history="")
        logger.debug(f"=># insight # => \n {result}")
        insights = []
        try:
            start_idx = result.find('{')
            end_idx = result.rfind('}')
            if start_idx != -1 and end_idx != -1:
                json_str = result[start_idx:end_idx + 1]
                json_data = json.loads(json_str)
                insights = json_data["insights"]
            else:
                logger.warn("未找到匹配的JSON字符串")
        except Exception as e:
            logger.error("InsightAI error: %s" % str(e))
        return insights


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
        initialization_prompt = self.initialization_prompt.format(memory=memory, portrait=portrait)
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