from casbin import persist

from app.models.system.interface import InterfaceResponseModel
from app.models.system.role import RoleResponseModel


class Adapter(persist.Adapter):
    """Casbin适配器的接口"""

    def __init__(self, role_models: list[RoleResponseModel], interface_models: list[InterfaceResponseModel]):
        self.role_models = role_models
        self.interface_models = interface_models

    def load_policy(self, model):
        """
        实现 casbin 的 add 接口
        从 mongodb 加载所有策略规则
        """
        # print('init load_policy')
        if not self.role_models:
            # print('No role found')
            return

        # 多个角色合并一个
        uids = '|'.join([role_model.uid for role_model in self.role_models])
        titles = '|'.join([role_model.title for role_model in self.role_models])
        interface_permission = []

        for role_model in self.role_models:
            interface_permission.extend(role_model.interface_permission)

        for interface_model in self.interface_models:
            line = f'p, {uids}, {interface_model.path}, {interface_model.method}'
            persist.load_policy_line(line, model)
        if interface_permission:
            line = f'g, {titles}, {uids}'
            persist.load_policy_line(line, model)
            # print('load policy success')
