from chat.chat_service import ChatService

if __name__ == "__main__":

    cs = ChatService()
    result = cs.chat(role_name='Allie', you_name='alan',
                     query='What do you like?')
    print("===========================================")
    print("chat:", result)

    result = cs.chat(role_name='Allie', you_name='alan',
                     query='I like watching movies')
    print("===========================================")
    print("chat:", result)

    result = cs.chat(role_name='Allie', you_name='alan',
                     query='I like war type movies')
    print("===========================================")
    print("chat:", result)

    