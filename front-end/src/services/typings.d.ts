export interface PagesData<T> extends ResponseMessages<T>{
    total: number
}

export interface ResponseMessages <T>{
    status_code: number
    success: boolean
    detail : string,
    data: T[] | any
}

export interface OSInfo{
    operating_system: string
    os_version_detail: string
    os_release: string
    computer_network_name: string
    processor_info: string
    python_version: string
}
export interface CPUUsage {
    logical_cpus_total: string
    physical_cpus_total: string
    percent: string
}

export interface MemoryUsage {
    total: string
    used: string
    percent: string
}

export interface NetworkTraffic {
    bytes_sent: string
    bytes_recv: string
}

export interface Disk {
    device: string
    mountpoint: string
    total: string
    used: string
    percent: string
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
    type Monitor = {
        os_info: OSInfo
        cpu_usage: CPUUsage
        memory_usage: MemoryUsage
        network_traffic: NetworkTraffic
        disk_usage: Disk[]
    }

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