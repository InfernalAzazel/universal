import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'
import { NP } from "./np"
import {AllowList} from "./utils";
import {useGet, useGlobalState} from "./composables";
import {Api} from "./utils";
import {defineAsyncComponent} from "vue";
import {Router} from "./types";



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

const np = NP.init()
// 防止首次或者刷新界面路由失效
let initRoute = false
// const {data: routesData, execute: exeUsersRoutes} = useGet<Router[]>(Api.usersRoutes)

// 路由守卫
router.beforeEach(async (to, form, next) => {
    const state = useGlobalState()
    const {data: routesData, execute: exeUsersRoutes} = useGet<Router[]>(Api.usersRoutes)
    np.start()
    if (!AllowList.includes(to.path) && !state.value.access_token) {
        next(`/login?redirect=${to.path}`)
    } else if (to.path === '/login' && state.value.access_token) {
        next('/')
    } else if (!initRoute && to.path !== '/login' && state.value.access_token) {
        initRoute = true
        await exeUsersRoutes()
        // 获取路由 -> 转化 -> addRoute
        if (routesData.value){
            generateRoutes(routesData.value).forEach((item) => {
                router.addRoute(item)
                //@ts-ignore
                router.options.routes.push(item)
            })
        }
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
    const state = useGlobalState()
    return list.reduce((all, item) => {
        // NOTE: 这里可以进行一些权限筛选，排除没有权限的路由
        // if (item.roles?.length && item.roles.includes('admin')) return all

        const children = item.children?.length
            ? generateRoutes(item.children)
            : undefined
        //@ts-ignore
        const current: RouteRecordRaw = {
            path: item.path,
            redirect: item.redirect,
            name: item.name,
            component: () => defineAsyncComponent(() => import( /* @vite-ignore */ `./${item.component}`)) ,
            children,
            meta: {
                title: state.value.locales === 'en-us' ? item.title_en_us: item.title_zh_cn ,
                icon: item.icon,
                hide: item.hide,
            },
        }

        return [...all, current]
    }, [] as RouteRecordRaw[])
}
export default router