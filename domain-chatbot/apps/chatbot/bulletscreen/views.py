from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from asgiref.sync import async_to_sync

import asyncio
import logging
logging.basicConfig(level=logging.INFO)




