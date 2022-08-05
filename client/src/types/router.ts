export interface Router {
    path: string
    redirect?: string
    component: string // NOTE: 页面组件路径，相对于 src 目录
    name?: string
    title_zh_cn?: string
    title_en_us?: string
    icon?: string // NOTE: icon 需要通过全局注册
    hide?: boolean // NOTE: 隐藏菜单
    roles?: string[]
    children?: Router[]
}