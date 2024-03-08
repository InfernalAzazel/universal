export interface PagesData<T> extends ResponseMessages<T>{
    total: number
}

export interface ResponseMessages <T>{
    status_code: number
    success: boolean
    detail : string,
    data: T[] | any
}

declare namespace API {

   
    type LoginForm = {
        username: string
        password: string
    };
    type ResLogin = {
        access_token: string
        token_type: string
    };

    type User = {
        uid: string
        username: string
        disabled: boolean
        role_name: string[]
        name: string
        mail: string
        company: string
        department: string
        create_at: string
        update_at: string
    }

    type CreateUser = {
        username: string
        disabled: boolean
        password: string
        role_name: string
    }

    type Role = {
        uid: string
        title: string
        description: string
        menu_permission: string[]
        interface_permission: string[]
        create_at: string
        update_at: string
    }

    type Menu = {
        uid: string
        path: string
        order: number
        key: number
        father:number
        icon: string
        create_at: string
        update_at: string
    };
    type Interface = {
        uid: string
        title: string
        path: string
        group: string
        method: string
        create_at: string
        update_at: string
    }

    type Router = {
        key?: number
        father?: number
        path: string
        title?: string
        title_mark?: string
        name?: string
        redirect?: string
        icon?: string
        component?: string
        order?: number
        hide?: boolean
        children?: Router[]
    }

}