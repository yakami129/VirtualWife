from claude_api import Client
cookie = "sessionKey=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; intercom-device-id-lupk8zyo=65e8dbab-be2b-43fc-8651-46ffdf7138bf; intercom-session-lupk8zyo=ditaYTZnOURqSzdxVGlqeTNhOVA3WGFiOVlYS1VQbzFjSnFTNE1MRlAxZVcrVDhYQTRtQ0luT2dsWkRXNXBtay0tRlVnMUxEaXVCVGd5Z3BPQ051NFlrdz09--004f08bebf6ae49d8b52134733a2852297415939; __cf_bm=uJe_yqvvDOUjPkh5ivbFwg4ERDzHmQhX84Pg7hUTcPE-1691983126-0-AWYclNTAGMROg625miY1MnNjHqpCCB+K+PRI/7pv4QeTP44SQkysV+6jy2NrkQdJS6feQenSTlHr3xF+L8XwN+w="
claude_api = Client(cookie, True)

prompt = "Hello, Claude!"
conversation_id = claude_api.create_new_chat()['uuid']
response = claude_api.send_message(prompt, conversation_id)
print(response)
