from bunnet import Document
from pydantic import Field
from app.utils.mixin import DBMixin


# ----------------- 系统 --------------------------
class User(DBMixin, Document):
    username: str = Field()  # 帐号： quid1111
    password: str = Field()  # 密码
    disabled: bool = Field(False)  # 禁用：True == 禁用
    is_super: bool = Field(False)  # 是否为超级管理员
    role_names: list[str] = Field([])  # 关联角色
    name: str | None = Field(None)  # 姓名:  张三
    mail: str | None = Field(None)  # 邮箱
    company: str | None = Field(None)  # 公司
    department: str | None = Field(None)  # 部门

    class Settings:
        name = "users"


class Role(DBMixin, Document):
    title: str | None = Field(None)
    description: str | None = Field(None)
    is_super: bool = Field(False)  # 是否超级管理员
    menu_permission: list[str] = Field([])
    interface_permission: list[str] = Field([])

    class Settings:
        name = "role"


class Interface(DBMixin, Document):
    title: str = Field()
    path: str = Field()
    group: str = Field()
    method: str = Field()

    class Settings:
        name = "interface"


class Menu(DBMixin, Document):
    key: int = Field()
    father: int = Field()
    path: str = Field()
    title: str = Field()
    title_mark: str = Field()
    name: str | None = Field(None)
    redirect: str | None = Field(None)
    icon: str | None = Field(None)
    component: str = Field()
    order: int = Field()

    class Settings:
        name = "menu"



