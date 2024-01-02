import logging
from ..models import PortalUser
from ..utils import singleton_snow_flake

logger = logging.getLogger(__name__)


class PortalUserService:
    def create(self, name: str) -> PortalUser:
        portal_user = PortalUser(
            id=singleton_snow_flake.task(),
            name=name
        )
        portal_user.save()
        return portal_user

    def get_by_name(self, name: str) -> PortalUser:
        '''
            通过名称获取门户用户
        '''
        return PortalUser.objects.filter(name=name).last()

    def get_and_create(self, name: str) -> PortalUser:
        '''
            通过名称获取门户用户，如果门户不存在，会自动创建一个
        '''
        portal_user = self.get_by_name(name)
        if portal_user is None:
            portal_user = self.create(name)
        return portal_user
