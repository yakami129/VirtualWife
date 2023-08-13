
from .memory_storage_strategy import MemoryStorageDriver


# 加载记忆模块配置
memory_type = 'milvus'
memory_storage_config = {
    "host": "127.0.0.1",
    "port": "19530",
    "user": "root",
    "password": "Milvus",
    "db_name": "default"
}

# 加载记忆模块驱动
singleton_memory_storage_driver = MemoryStorageDriver(
    type=memory_type, memory_storage_config=memory_storage_config)
