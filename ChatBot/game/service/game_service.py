from .competition_record_service import *
from .competition_service import *
from .riddle_service import *
from .leaderboard_service import *
from blivedm.core.chat_priority_queue_management import *
import queue
import logging
import random

'''临时使用'''
riddle_queue = queue.Queue()

'''后续看要不要放到缓存'''
# 当前谜题id
current_riddle_id = 0
# 当前谜题答案
current_riddle_answer = ''
# 当前谜题类型
current_riddle_type = ''
# 当前谜题答案字数
current_riddle_count = 0
# 当前谜题描述
current_riddle_description = ''
# 当前比赛ID
current_competition_id = None
# 当前比赛轮次
current_competition_turn = 1;

'''开始你画我猜游戏'''
def start_competition():

    global current_competition_id
    global current_competition_turn

    # 1.创建比赛
    competition_dto = CompetitionDTO(name='test',turn=0)
    db_competition = CompetitionHandle.create(competition_dto)
    logging.info('[BIZ] db_competition:'+json.dumps(db_competition))
    current_competition_id = db_competition["id"]
    current_competition_turn = 1

    cmd =  f'开始新一轮你画我猜游戏了，请你活跃一下气氛'
    message_body = {
        "type":"system",
        "content": '',
        "cmd" : cmd
    }
    put_chat_message(MessagePriority.GAME_MESSAGE,message_body)
    logging.info('[BIZ]开始新一轮的你画我猜游戏')

    # 2.开始下一个答题
    next_riddle()

'''提交谜题答案'''
def commit_riddle_answer(user_name:str,riddle_answer:str):

    global current_competition_id
    global current_riddle_answer
    global current_competition_turn

    if current_competition_id is None:
        return
    
    ## 格式化一下答案，去除#
    riddle_answer = riddle_answer.lstrip('#')
    
    # 1.查询当前比赛实体
    competition =  CompetitionQuery.get(current_competition_id)
    
    # 2.查询用户当前比赛记录，如果没有比赛记录，初始化比赛记录
    competition_record = CompetitionRecordQuery.getByCompetitionIdAndParticipantName(competition_id=current_competition_id,participant_name=user_name)
    if competition_record is None:
        competition_record_dto = CompetitionRecordDTO(competition_id=current_competition_id,participant_name=user_name,score=0)
        competition_record = CompetitionRecordHandle.create(competition_record_dto)
        logging.info(f'[BIZ]{user_name}第一次答题，初始化比赛记录')

    # 3.判断当前用户输入的谜题答案是否正确
    riddle_match = riddle_answer == current_riddle_answer;
    logging.info(f'[BIZ]{user_name}回答问题，riddle_answer：{riddle_answer} current_riddle_answer:{current_riddle_answer}')
    if(riddle_match):
        # 4.如果正确，比赛分数+1，保存到数据库，发送消息给前端刷新
        score = competition_record.score + 1
        competition_record_dto = CompetitionRecordDTO(id=competition_record.id,competition_id=competition_record.competition_id,participant_name=competition_record.participant_name,score=score)
        CompetitionRecordHandle.update(competition_record_dto)

        # 5.回答错误，发送消息
        cmd_str = f'{user_name}在你画我猜游戏中回答正确，请用简短的语言回复'
        content = f'{user_name}回答正确'
        message_body = {
            "type":"system",
            "content":content,
            'cmd': cmd_str
        }
        put_chat_message(MessagePriority.GAME_ERPLY_MESSAGE,message_body)

        # 6.继续下一轮游戏
        logging.info(f'当前游戏轮次：{current_competition_turn}')
        if(current_competition_turn <= 5):
            next_riddle()
         # 6.判断当前轮次，如果大于5，结束比赛
        elif(current_competition_turn > 5):
            end_comptition()
        else:
            competition = CompetitionDTO(id=current_competition_id,turn=current_competition_turn)
            CompetitionHandle.update(competition)

    else:
        # 5.回答错误，发送消息
        cmd_str = f'{user_name}在你画我猜游戏中回答错误，请用简短的语言回复'
        content = f'{user_name}回答错误'
        message_body = {
            "type":"system",
            "content": content,
            'cmd': cmd_str
        }
        put_chat_message(MessagePriority.GAME_ERPLY_MESSAGE,message_body)
   
   

def end_comptition():

    if current_competition_id is None:
        return
    
    # 1.查询当前比赛实体
    competition =  CompetitionQuery.get(current_competition_id)

    # 2.查询当前比赛记录，获取分数最高者
    competition_record = CompetitionRecordQuery.getMaxScoreCompetitionRecord(competition_id=current_competition_id)
    participant_name = competition_record.participant_name

    # 3.设置当前比赛的胜利者
    competition_dto = CompetitionDTO(id=competition.id,victor_name=participant_name,turn=current_competition_turn,end_date=timezone.now())
    CompetitionHandle.update(competition_dto=competition_dto)

    # TODO 4.更新排行榜

    # 5.发送比赛结束消息
    cmd_str = f'{participant_name}获得你画我猜游戏胜利'
    content = f'本轮你画我猜游戏结束，恭喜{participant_name}是本轮比赛的获胜者，开始下一轮比赛'
    message_body = {
        "type":"system",
        "content": content,
        'cmd': cmd_str
    }
    put_chat_message(MessagePriority.GAME_ERPLY_MESSAGE,message_body)

    # 6.开始下一轮比赛
    start_competition()

def next_riddle():

    global current_riddle_answer
    global current_riddle_type
    global current_riddle_description
    global current_riddle_count
    global current_competition_turn
    
    # 1. 通过当前下标获取谜题
    riddle = getRandomRiddle();
    current_riddle_answer = riddle.riddle_answer
    current_riddle_type = riddle.riddle_type
    current_riddle_description = riddle.riddle_description
    current_riddle_count = riddle.riddle_count

    riddle_message = {
        "current_riddle_answer":riddle.riddle_answer,
        "current_riddle_type":riddle.riddle_type,
        "current_riddle_description":riddle.riddle_description,
        "current_riddle_count":riddle.riddle_count,
    }
    riddle_queue.put(riddle_message)

    # 2. 发送消息给前端渲染新的谜题
    content = f"谜题类型：{current_riddle_type},谜题描述：{current_riddle_description},请你简述一下谜题的内容，告诉粉丝需要关注哪些内容"
    cmd_str = riddle.riddle_image_id
    message_body = {
        "type":"image",
        "content":"",
        'cmd': cmd_str
    }
    put_chat_message(MessagePriority.GAME_MESSAGE,message_body)

    # 3. 比赛轮次+1
    current_competition_turn = current_competition_turn + 1

'''随机获取谜题'''
def getRandomRiddle():

    global current_riddle_id

    riddles =  RiddleQuery.all()
    riddle = random.choice(riddles)

    if current_riddle_id == riddle.id:
        getRandomRiddle()
    else:
        current_riddle_id = riddle.id

    return riddle
