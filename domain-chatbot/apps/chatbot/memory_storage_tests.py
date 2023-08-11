from memory.storage.memory_storage_strategy import MemoryStorageDriver

if __name__ == "__main__":

    memory_storage_config = {
        "host": "127.0.0.1",
        "port": "19530",
        "user": "root",
        "password": "Milvus",
        "db_name": "default"
    }

    sd = MemoryStorageDriver(
        type="milvus", memory_storage_config=memory_storage_config)

    # 插入数据
    sd.save(role_name="aili", you_name="alan",
            query_text="我喜欢看电影", answer_text="我也挺喜欢的")
    sd.save(role_name="aili", you_name="alan",
            query_text="猪肉涨价了", answer_text="真的吗？")
    sd.save(role_name="aili", you_name="alan",
            query_text="今天上海的天气怎么样？", answer_text="今天上海天气比较晴朗")

    # 搜索
    result = sd.search("猪肉怎么样了？", "alan")
    print("result:A", result)

    # 清空数据
    sd.clear("alan")

    result = sd.search("你知道我喜欢什么吗？", "alan")
    print("result:B", result)

     # 清空数据
    sd.clear("alan")
