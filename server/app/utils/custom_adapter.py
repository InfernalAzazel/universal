from casbin import persist
from app.models.system.role import Role


class Adapter(persist.Adapter):
    """the interface for Casbin adapters."""

    def __init__(self, doc):
        self.doc = doc

    def load_policy(self, model):
        '''
        implementing add Interface for casbin \n
        load all policy rules from mongodb \n
        '''
        # print('init load_policy')
        if not self.doc:
            # print('No role found')
            return
        role = Role(**self.doc)
        for v in role.interface_permission:
            line = f'p, {role.uid}, {v["path"]}, {v["method"]}'
            persist.load_policy_line(line, model)
        if role.interface_permission:
            line = f'g, {role.name_en_us}, {role.uid}'
            persist.load_policy_line(line, model)
            # print('load policy success')
