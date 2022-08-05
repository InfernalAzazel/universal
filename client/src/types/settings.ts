
export interface Init{
    switch: boolean
}

export interface Shared {
    tz_info: String
}

export interface Mongodb {
    host: string
    username: string
    password: string
}

export interface Jwt {
    secret_key: string
    algorithm: string
    minutes: number
}

export interface Settings{
    init: Init
    shared: Shared
    mongodb: Mongodb
    jwt: Jwt
}