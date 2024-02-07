import logging
from .sys_config import SysConfig

logger = logging.getLogger(__name__)
singleton_sys_config = SysConfig()


