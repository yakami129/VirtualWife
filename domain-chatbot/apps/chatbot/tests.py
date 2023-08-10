from memory.storage.storage_strategy import StorageDriver

if __name__ == "__main__":

    storage_config = {
        "host": "127.0.0.1",
        "port": "19530",
        "user": "root",
        "password": "Milvus",
        "db_name": "default"
    }

    sd = StorageDriver(type="milvus", storage_config=storage_config)

    # 插入数据
    sd.save("我喜欢看电影", "alan")
    sd.save("今天天气真好", "alan")
    sd.save("猪涨价了", "alan")

    # 搜索
    result = sd.search("猪肉怎么样了？", "alan")
    print("result:A", result)

    # 清空数据
    sd.clear("alan")

    result = sd.search("你知道我喜欢什么吗？", "alan")
    print("result:B", result)
