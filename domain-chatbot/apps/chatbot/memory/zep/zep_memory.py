import json
import logging

from zep_python import ZepClient, Session, Message, Memory, MemorySearchPayload
from zep_python.user import User, CreateUserRequest

logger = logging.getLogger(__name__)


class ChatHistroy:
    role: str
    content: str

    def __init__(self, role: str, content: str) -> None:
        self.role = role
        self.content = content


class ZepService:
    zep_client: ZepClient
    search_memory_size: int

    def __init__(self, zep_url: str, zep_optional_api_key: str, search_memory_size: int = 10):
        self.zep_client = ZepClient(
            base_url=zep_url, api_key=zep_optional_api_key)
        self.search_memory_size = search_memory_size
        logger.info(f"ZEP_URL:{zep_url}")
        logger.info(f"ZEP_OPTIONAL_API_KEY:{zep_optional_api_key}")
        logger.info("Initialize ZepClient successfully")

    def add_user(self, user_id: str) -> User:

        # TODO 需要获取用户信息
        email = f"{user_id}@example.com"
        first_name = user_id
        last_name = user_id

        # 创建用户
        user_request = CreateUserRequest(
            user_id=user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            metadata={"foo": "bar"},
        )
        return self.zep_client.user.add(user_request)

    def get_user(self, user_id: str):
        try:
            return self.zep_client.user.get(user_id)
        except:
            logger.info(f"user_id:{user_id},If the user does not exist ")
            return None

    def add_session(self, user_id: str, channel_id: str) -> Session:
        session = Session(
            session_id=channel_id,
            user_id=user_id,
            metadata={"foo": "bar"}
        )
        return self.zep_client.memory.add_session(session)

    def get_session(self, user_id: str, channel_id: str):
        try:
            return self.zep_client.memory.get_session(channel_id)
        except:
            logger.info(
                f"session_id:{channel_id},If the session does not exist ")
            return None

    def add_memorys(self, channel_id: str, chat_histroys: list[ChatHistroy]):
        messages = [Message(role=m.role, content=m.content)
                    for m in chat_histroys]
        memory = Memory(messages=messages)
        self.zep_client.memory.add_memory(channel_id, memory)

    def get_memorys(self, channel_id: str) -> list[ChatHistroy]:
        memory = self.zep_client.memory.get_memory(
            session_id=channel_id, lastn=self.search_memory_size)
        chat_historys = [ChatHistroy(role=m.role, content=m.content)
                         for m in memory.messages]
        return chat_historys

    def search_mmr(self, query: str, channel_id: str, mmr_lambda: float = 0.5, limit: int = 10):
        # Initialize the Zep client before running this code
        search_payload = MemorySearchPayload(
            text=query,
            search_scope="messages",  # This could be messages or summary
            search_type="mmr",  # remove this if you'd prefer not to rerank results
            mmr_lambda=mmr_lambda,  # tune diversity vs relevance
        )
        search_results = self.zep_client.memory.search_memory(channel_id, search_payload, limit)
        chat_histroys = []
        for item in search_results:
            message = item.dict()["message"]
            chat_histroys.append(ChatHistroy(role=message["role"], content=message["content"]))
        return chat_histroys


class ChatHistroyService:
    zep_service: ZepService

    def __init__(self, zep_url: str, zep_optional_api_key: str, search_memory_size: int):
        self.zep_service = ZepService(zep_url, zep_optional_api_key, search_memory_size)

    def search(self, query: str, user_id: str, channel_id: str) -> list[ChatHistroy]:
        user_id = user_id
        channel_id = channel_id
        return self.zep_service.search_mmr(query=query, channel_id=channel_id)

    def push(self, user_id: str, channel_id: str, chat_histroy: ChatHistroy):

        # 查询用户是否存在，如果不存在初始化用户信息和会话
        user = self.zep_service.get_user(user_id)
        if not user:
            self.zep_service.add_user(user_id)
            self.zep_service.add_session(user_id, channel_id)

        # 添加聊天记录到内存
        self.zep_service.add_memorys(channel_id, [chat_histroy])

    def list(self, user_id: str, channel_id: str) -> list[ChatHistroy]:

        # 查询用户和会话是否，只要有一个不存在，直接返回空
        user = self.zep_service.get_user(user_id)
        session = self.zep_service.get_session(user_id, channel_id)
        if not user or not session:
            return []

        return self.zep_service.get_memorys(channel_id)
