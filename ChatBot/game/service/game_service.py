from .competition_record_service import *
from .competition_service import *
from .riddle_service import *
from .leaderboard_service import *

'''后续看要不要放到缓存'''

# 当前谜题下标
current_riddle_index = 0
# 当前谜题答案
current_riddle_answer = ''
# 当前谜题类型
current_riddle_type = ''
# 当前谜题描述
current_riddle_description = ''
# 当前比赛ID
current_competition_id = None
# 当前比赛轮次
current_competition_turn = 0;

'''开始你画我猜游戏'''
def start_competition():

    global current_competition_id

    # 1.创建比赛
    competition_dto = CompetitionDTO(name='test',turn=0,)
    db_competition = CompetitionHandle.create(competition_dto)
    current_competition_id = db_competition.id

    # 2.开始下一个答题
    next_riddle()

'''提交谜题答案'''
def commit_riddle_answer(user_name:str,riddle_answer:str):

    global current_competition_id
    global current_riddle_answer
    global current_competition_turn

    if current_competition_id is None:
        return
    
    # 1.查询当前比赛实体
    competition =  CompetitionQuery.get(current_competition_id)
    
    # 2.查询用户当前比赛记录，如果没有比赛记录，初始化比赛记录
    competition_record = CompetitionRecordQuery.getByParticipantNameAndCompetitionId(user_name,current_competition_id)
    if competition_record is None:
        competition_record_dto = CompetitionRecordDTO(competition_id=current_competition_id,participant_name=user_name,score=0)
        competition_record = CompetitionRecordHandle.create(competition_record_dto)

    # 3.判断当前用户输入的谜题答案是否正确
    if(riddle_answer == current_riddle_answer):
        # 4.如果正确，比赛分数+1，保存到数据库，发送消息给前端刷新
        score = competition_record.score + 1
        competition_record_dto = CompetitionRecordDTO(competition_id=competition_record.competition_id,participant_name=competition_record.participant_name,score=score)
        CompetitionRecordHandle.update(competition_record_dto)
    else:
        # 5.回答错误，发送消息
        print()
   
    # 6.判断当前轮次，如果等于5，结束比赛
    if(competition.turn == 5):
        end_comptition()
    else:
        competition = CompetitionDTO(id=current_competition_id,turn=current_competition_turn)
        CompetitionHandle.update(competition)


def end_comptition():

    if current_competition_id is None:
        return
    
    # 1.查询当前比赛实体
    competition =  CompetitionQuery.get(current_competition_id)

    # 2.查询当前比赛记录，获取分数最高者
    competition_record = CompetitionRecordQuery.getMaxScoreCompetitionRecord(competition_id=current_competition_id)
    participant_name = competition_record.participant_name

    # 3.设置当前比赛的胜利者
    competition.victor_name = participant_name
    CompetitionDTO(id=current_competition_id,n)

    # 4.更新排行榜

    # 5.发送比赛结束消息

    return

def next_riddle():

    global riddle_index
    global current_competition_turn
    
    # 1. 通过当前下标获取谜题
    riddle = getRandomRiddle();

    # 2. 发送消息给前端渲染新的谜题

    # 3. 比赛轮次+1、谜题下标+1
    riddle_index = riddle_index + 1
    current_competition_turn = current_competition_turn + 1

'''随机获取谜题'''
def getRandomRiddle():
   
    riddles =  RiddleQuery.all()
    riddle = riddles[riddle_index]
    return riddle
