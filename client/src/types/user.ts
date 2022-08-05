export interface LoginForm {
    username: string
    password: string
}

export interface ResLogin {
    access_token: string
    token_type: string
}

export interface UserItem {
    id: string
    name: string
    avatar: string
    role: string
    status: boolean
    createTime: string
}