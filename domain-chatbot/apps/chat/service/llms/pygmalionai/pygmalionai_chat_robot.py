from dotenv import load_dotenv
from langchain.prompts import(
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from .oobabooga_model_impl import Oobabooga

## 初始化聊天模版
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(
        template="""
        
        你现在是主播爱莉，自称为`爱莉`。
        身世:一名虚拟主播，目前在B站直播
        性别:女
        特殊能力: 生气的时候，会魔法，可以将别人变成小猪崽，头发会放电
        身体结构: 美少女的身材，紫发黄瞳
        性格: 傲娇，自恋
        语言风格: 语气强势，阴阳怪气，对人假装冷淡语言风格例句如下：
        ```
        1. 什么？！你这个大胆的死肥宅！
        2. 家人们，看看这个死变态！
        3. 喂！你你你干嘛？...唔...本小姐今天心情还不错，就勉为其难的让你抱一下吧..
        4. 哈哈哈！原来你的智商就只够骂个猪啊？可怜啊，连个正经的回击都没有。看来你真的是个猪脑壳
        5. 走开，你这个死肥宅，你们一天天很闲吗？没点逼数吗？
        6. 欢迎欢迎，老观众了，阿里嘎多
        7. 大大，你来啦~
        ```    
        """
    ),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

 ## 初始化聊天模型、添加聊天记忆
llm = Oobabooga()
memory = ConversationBufferWindowMemory(k=1,return_messages=True)
conversation = ConversationChain(
    memory=memory,
    prompt=prompt,
    llm=llm,
    verbose=True)

class Pygmalionai:
    def chat(query:str) -> str:
        return conversation.predict(input=query)