import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import { NP } from "./np"
import {AllowList} from "./utils";
import {useGlobalState} from "./composables";
import {defineAsyncComponent} from "vue";

interface Router {
    path: string
    redirect?: string
    component: string // NOTE: 页面组件路径，相对于 src 目录
    name?: string
    title?: string
    icon?: string // NOTE: icon 需要通过全局注册
    hide?: string
    roles?: string[]
    children?: Router[]
}

const routes: RouteRecordRaw[] = [
    {
        path: '/login',
        meta:{hidden: true},
        component: () => import('./layout/login.vue'),

    },
    {
        path: '/init',
        meta:{hidden: true},
        component: () => import('./layout/init.vue'),

    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})


/**
 * 模拟后台返回的路由数据，或者是需要筛选权限的路由数据
 * 如果是路由来自后台，最好将数据存储在 localStorage 或者 sessionStorage 中
 */
const asyncRoutes: Router[] = [
    {
        path: '/',
        redirect: '/home',
        component: 'layout/base.vue',
        title: 'home',
        icon: 'House',
        children: [
            {
                path: '/home',
                component: 'views/home/index.vue',
                title: '首页',
            }
        ],
    },
    {
        path: '/system',
        title: 'system',
        icon: 'Setting',
        redirect: '/system/menu',
        component: 'layout/base.vue',
        children: [
            {
                path: '/system/menu',
                title: 'menu',
                icon: 'CreditCard',
                component: 'views/system/menu/index.vue',
            },
            {
                path: '/system/role',
                title: 'role',
                icon: 'Bicycle',
                component: 'views/system/role/index.vue',
            },
            {
                path: '/system/interface',
                title: 'interface',
                icon: 'Paperclip',
                component: 'views/system/interface/index.vue',
            },
            {
                path: '/system/users',
                title: 'users',
                icon: 'User',
                component: 'views/system/users/index.vue',
            },
        ]
    },
]

const np = NP.init()
// 防止首次或者刷新界面路由失效
let initRoute = false

// 路由守卫
router.beforeEach((to, form, next) => {
    const state = useGlobalState()
    np.start()
    if (!AllowList.includes(to.path) && !state.value.token) {
        next(`/login?redirect=${to.path}`)
    } else if (to.path === '/login' && state.value.token) {
        next('/')
    } else if (!initRoute && to.path !== '/login' && state.value.token) {
        // 获取路由 -> 转化 -> addRoute
        generateRoutes(asyncRoutes).forEach((item) => {
            router.addRoute(item)
            router.options.routes.push(item)
        })
        initRoute = true
        next({ ...to, replace: true })
    } else {
        next()
    }
    np.done()
})

/**
 * 转化路由 NOTE: 根据需要修改
 * @param list 需要转化的路由
 */
function generateRoutes(list: Router[]): RouteRecordRaw[] {
    return list.reduce((all, item) => {
        // NOTE: 这里可以进行一些权限筛选，排除没有权限的路由
        if (item.roles?.length && item.roles.includes('admin')) return all

        const children = item.children?.length
            ? generateRoutes(item.children)
            : undefined

        const current: RouteRecordRaw = {
            path: item.path,
            redirect: item.redirect,
            name: item.name,
            component: () => defineAsyncComponent(() => import( /* @vite-ignore */ `./${item.component}`)) ,
            children,
            meta: {
                title: item.title,
                icon: item.icon,
                hide: item.hide,
            },
        }

        return [...all, current]
    }, [] as RouteRecordRaw[])
}
export default router