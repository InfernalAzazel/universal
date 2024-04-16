from casbin import persist

from app.models.admin import Role
from app.models.admin import Interface


class Adapter(persist.Adapter):
    """Casbin适配器的接口"""

    def __init__(self, roles: list[Role], interfaces: list[Interface]):
        self.roles = roles
        self.interfaces = interfaces

    def load_policy(self, model):
        """
        实现 casbin 的 add 接口
        从 mongodb 加载所有策略规则
        """
        # print('init load_policy')
        if not self.roles:
            # print('No role found')
            return

        # 多个角色合并一个
        ids = '|'.join([str(role.id) for role in self.roles])
        titles = '|'.join([role.title for role in self.roles])
        interface_permission = []

        for role in self.roles:
            interface_permission.extend(role.interface_permission)

        for interface in self.interfaces:
            line = f'p, {ids}, {interface.path}, {interface.method}'
            persist.load_policy_line(line, model)
        if interface_permission:
            line = f'g, {titles}, {ids}'
            persist.load_policy_line(line, model)
            # print('load policy success')
