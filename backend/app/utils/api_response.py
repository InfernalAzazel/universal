from dataclasses import dataclass
from enum import Enum, unique
from typing import List, Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse


@dataclass
class DefaultCodes:
    success_retrieve_code: int
    success_add_code: int
    success_modify_code: int
    success_delete_code: int
    failed_retrieve_code: int
    failed_add_code: int
    failed_modify_code: int
    failed_delete_code: int
    not_found_code: int


@unique
class StatusCode(Enum):
    """
    此类，用于表示带有消息的 HTTP 和自定义状态代码.

    Attributes:
        value (int): 状态代码的数值.
        message (str): 状态代码的说明消息.

    Example usage:
        >>> print(StatusCode.ok.value)  # Outputs 200
        >>> print(StatusCode.ok.message)  # Outputs "成功响应"
        >>> print(StatusCode.get_message(200))  # Outputs "成功响应"
    """
    ok = (200, "成功响应")
    bad_request = (400, "客户端请求的语法错误，服务器无法理解")
    unauthorized = (401, "请求要求用户的身份认证")
    forbidden = (403, "服务器理解请求客户端的请求，但是拒绝执行此请求")
    not_found = (404, "资源未找到")
    jwt_expired = (419, "JWT已过期")
    jwt_decode_failed = (422, "JWT解码失败")
    illegal_login = (440, "非法登录")
    login_failed = (450, "登录失败")
    credentials_invalid = (460, "用户凭证无效")
    user_disabled = (480, "用户被禁用")
    get_roles_failed = (490, "获取角色失败")
    internal_server_error = (500, "内部服务器错误")
    not_valid_object_id = (510, "无效的对象ID")
    interface_add_successfully = (1001, "接口添加成功")
    interface_add_failed = (1002, "接口添加失败")
    interface_delete_successfully = (1003, "接口删除成功")
    interface_delete_failed = (1004, "接口删除失败")
    interface_retrieve_successfully = (1005, "接口获取成功")
    interface_retrieve_failed = (1006, "接口获取失败")
    interface_modify_successfully = (1007, "接口修改成功")
    interface_modify_failed = (1008, "接口修改失败")
    interface_not_found = (1009, "未找到接口")
    menu_add_successfully = (1101, "菜单添加成功")
    menu_add_failed = (1102, "菜单添加失败")
    menu_delete_successfully = (1103, "菜单删除成功")
    menu_delete_failed = (1104, "菜单删除失败")
    menu_retrieve_successfully = (1105, "菜单获取成功")
    menu_retrieve_failed = (1106, "菜单获取失败")
    menu_modify_successfully = (1107, "菜单修改成功")
    menu_modify_failed = (1108, "菜单修改失败")
    menu_not_found = (1109, "未找到菜单")
    role_add_successfully = (1201, "角色添加成功")
    role_add_failed = (1202, "角色添加失败")
    role_delete_successfully = (1203, "角色删除成功")
    role_delete_failed = (1204, "角色删除失败")
    role_retrieve_successfully = (1205, "角色获取成功")
    role_retrieve_failed = (1206, "角色获取失败")
    role_modify_successfully = (1207, "角色修改成功")
    role_modify_failed = (1208, "角色修改失败")
    role_not_found = (1209, "未找到角色")
    role_delete_admin_failed = (12010, "超级管理员角色是不允许删除的，该操作已被记录")
    role_modify_admin_failed = (12011, "超级管理员账号才能编辑超级管理员角色，该操作已被记录")
    user_add_successfully = (1301, "用户添加成功")
    user_add_failed = (1302, "用户添加失败")
    user_delete_successfully = (1303, "用户删除成功")
    user_delete_failed = (1304, "用户删除失败")
    user_retrieve_successfully = (1305, "用户获取成功")
    user_retrieve_failed = (1306, "用户获取失败")
    user_modify_successfully = (1307, "用户修改成功")
    user_modify_failed = (1308, "用户修改失败")
    user_not_found = (1309, "未找到用户")
    user_delete_admin_failed = (13010, "超级管理员账号是不允许删除的，该操作已被记录")
    user_modify_admin_failed = (13011, "超级管理员账号才能编辑超级管理员账号，该操作已被记录")

    def __new__(cls, value, message):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.message = message
        return obj

    @classmethod
    def get_message(cls, code):
        """检索给定代码的消息."""
        for status in cls:
            if status.value == code:
                return status.message
        return "未知的状态"


class APIResponse(ORJSONResponse):
    def __init__(
            self,
            data: List[Any] | Any | None = None,
            code: int = StatusCode.ok.value,
            success: bool | None = None,
            detail: str | None = None,
            **kwargs
    ):
        """

        响应消息

        Args:
            data: 数据.
            code: 状态码，默认值为 200.
            success: 成功，默认值为 状态码200 时 True，否则需要自行设置成功状态
            detail: 详细和错误信息
            kwargs: 添加额外字段.

        Returns:
            JsonResponse
        """
        message = StatusCode.get_message(code)
        content = {
            "code": code,
            "success": success if success is not None else code == 200,
            "detail": detail if detail is not None else str(message),
            "data": data,
        }
        content.update(kwargs)
        super().__init__(content=jsonable_encoder(content, by_alias=False))


class ExceptionResponse(Exception):
    def __init__(
            self,
            code: int,
            detail: Any = None,
    ):
        message = StatusCode.get_message(code=code)
        self.code = code
        self.detail = detail if detail is not None else str(message)
