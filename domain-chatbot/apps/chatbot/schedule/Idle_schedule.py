
import logging
import threading
from ..emotion.behavior_action_management import IdleActionManagement
from ..output.realtime_message_queue import RealtimeMessage, put_message

logger = logging.getLogger(__name__)

def idle_action_job():
    # 创建 IdleActionManagement 实例
    manager = IdleActionManagement()
    # 调用 get_random_idle_action
    random_action = manager.random_action()
    logger.info(f"Random Idle Action: {random_action.action} Emote:{random_action.emote}")
    put_message(RealtimeMessage(
            type="behavior_action", user_name="", content=random_action.action, emote=random_action.emote))

def run_idle_action_job(interval, idle_action_job):
    threading.Timer(interval, run_idle_action_job, [interval, idle_action_job]).start()
    idle_action_job()

