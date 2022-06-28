from fastapi import HTTPException, status


# 自定义异常
class CustomHttpException:
    """
    信息响应 （ 100–199)
    成功响应 （ 200–299)
    重定向消息 （ 300–399)
    客户端错误响应 ( 400–499)
    服务器错误响应 ( 500–599)
    """

    # 客户端异常 -------------------------------------------------------------------------------------------------
    @staticmethod
    def client_err_no_init_system_config():
        """
        没有初始化系统配置
        """
        return HTTPException(498, 'System configuration not initialized')

    @staticmethod
    def client_err_re_init_system_config():
        """
        请勿重复初始化系统配置
        """
        return HTTPException(499, 'Do not initialize the system configuration repeatedly')

    @staticmethod
    def client_err_user_or_pwd():
        """
        用户名或密码错误
        """
        return HTTPException(460, 'Incorrect username or password', {"WWW-Authenticate": "Bearer"})

    @staticmethod
    def client_err_token_expired():
        """
        令牌过期
        """
        return HTTPException(461, 'token expired')

    # 服务器异常 ---------------------------------------------------------------------------------------------------
    @staticmethod
    def server_err_get_current_user_route():
        """
        获取当前用户路由失败
        """
        return HTTPException(520, 'Failed to get current user route')