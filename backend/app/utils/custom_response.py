import importlib
import os
from typing import List, Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, ORJSONResponse
from app.utils.i18n import CreateI18n


class StatusCode:
    ok: int = 200
    bad_request: int = 400
    unauthorized: int = 401
    forbidden: int = 403
    not_found: int = 404
    jwt_expired: int = 419
    jwt_decode_failed: int = 422
    illegal_login: int = 423
    username_password_error: int = 460
    user_disabled: int = 480
    get_roles_failed: int = 490
    internal_server_error: int = 500
    not_valid_object_id: int = 510
    # --------------自定义-------------------
    interface_add_successfully = 1001
    interface_add_failed = 1002
    interface_delete_successfully = 1003
    interface_delete_failed = 1004
    interface_get_successfully = 1005
    interface_get_failed = 1006
    interface_modify_successfully = 1007
    interface_modify_failed = 1008

    menu_add_successfully = 1101
    menu_add_failed = 1102
    menu_delete_successfully = 1103
    menu_delete_failed = 1104
    menu_get_successfully = 1105
    menu_get_failed = 1106
    menu_modify_successfully = 1107
    menu_modify_failed = 1108

    role_add_successfully = 1201
    role_add_failed = 1202
    role_delete_successfully = 1203
    role_delete_failed = 1204
    role_get_successfully = 1205
    role_get_failed = 1206
    role_modify_successfully = 1207
    role_modify_failed = 1208

    user_add_successfully = 1301
    user_add_failed = 1302
    user_delete_successfully = 1303
    user_delete_failed = 1304
    user_get_successfully = 1305
    user_get_failed = 1306
    user_modify_successfully = 1307
    user_modify_failed = 1308

    def __init__(self, locale: str, status_code: int = 200):
        """
        状态码

        Args:
            locale: 当前语言.
            status_code: 状态码.

        Returns:
            str: 返回 i18n 后的文本
        """
        self.locale = locale
        self.status_code = status_code

    @staticmethod
    def get_i18n(locale: str):
        def load_messages():
            _messages = {}
            path = os.path.join(os.getcwd(), 'app', 'locales')
            module_files = (f[:-3] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py')

            for module_name in module_files:
                try:
                    module = importlib.import_module(f"app.locales.{module_name}")
                    if hasattr(module, 'message'):
                        _messages[module_name] = module.message
                except Exception as e:
                    print(f"Failed to load module '{module_name}': {str(e)}")

            return _messages

        messages = load_messages()
        return CreateI18n(locale, messages)

    @classmethod
    def get_field_name(cls, value: int) -> str | None:
        for attr_name, attr_value in cls.__dict__.items():
            if attr_value == value:
                return attr_name
        return None

    def __str__(self) -> str:
        i18n = self.get_i18n(self.locale)
        return i18n.t(self.get_field_name(self.status_code))


class ExceptionResponse(Exception):
    def __init__(
            self,
            locale: str,
            status_code: int,
            detail: Any = None,
    ):
        message = StatusCode(locale=locale, status_code=status_code)
        self.locale = locale
        self.status_code = status_code
        self.detail = detail if detail is not None else str(message),


class ResponseMessages(ORJSONResponse):
    def __init__(
            self,
            locale: str,
            status_code: int = 200,
            success: bool | None = None,
            detail: str | None = None,
            data: List[Any] | Any | None = None,
            **kwargs
    ):
        """
        响应消息

        Args:
            locale: 当前语言.
            status_code: 状态码，默认值为 200.
            success: 成功，默认值为 状态码200 时 True，否则需要自行设置成功状态
            detail: 详细信息，默认自动安装状态码提取相对应字段的i18n信息
            data: 数据.
            kwargs: 添加额外字段.

        Returns:
            None
        """
        message = StatusCode(locale=locale, status_code=status_code)
        content = {
            "status_code": status_code,
            "success": success if success is not None else status_code == 200,
            "detail": detail if detail is not None else str(message),
            "data": data,
        }
        content.update(kwargs)
        super().__init__(content=jsonable_encoder(content))
