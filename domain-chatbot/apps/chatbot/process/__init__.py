import logging
from .process import ProcessCore
logger = logging.getLogger(__name__)

# 单例 process_core
process_core = ProcessCore()
