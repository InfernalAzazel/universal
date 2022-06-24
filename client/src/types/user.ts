export interface LoginForm {
    username: string
    password: string
}

export interface InitSystemForm {
    username: string
    password: string
    verify_password: string
    tz_info: string
    db_host: string
    db_username: string
    db_password: string
    secret_key: string
    algorithm: string
    access_token_expire_minutes: number
    email_server: string
    email_domain: string
    email: string
    email_user: string
    email_pwd: string
    email_attachment_file_name: string
    push_email_task_hour: string
    push_email_task_minute: string
    push_email_task_second: string
}

export interface ResLogin {
    name: string
    avatar: string
    token: string
}

export interface UserItem {
    id: string
    name: string
    avatar: string
    role: string
    status: boolean
    createTime: string
}