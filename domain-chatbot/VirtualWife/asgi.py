"""
ASGI config for VirtualWife project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""


import os
from apps.chatbot.output.routing import websocket_urlpatterns
from apps.chatbot.output.realtime_message_queue import RealtimeMessageQueryJobTask
from apps.chatbot.chat.chat_history_queue import ChatHistoryMessageQueryJobTask
from apps.chatbot.insight.insight_message_queue import InsightMessageQueryJobTask
from apps.chatbot.insight.bilibili.bili_live_client import bili_live_client_main
from apps.chatbot.schedule.Idle_schedule import run_idle_action_job,idle_action_job
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VirtualWife.settings')

bili_live_client_main()
# run_idle_action_job(15, idle_action_job)
RealtimeMessageQueryJobTask.start()
ChatHistoryMessageQueryJobTask.start()
InsightMessageQueryJobTask.start()

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
})


