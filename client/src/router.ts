import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'

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
    {
        path: '/',
        name: 'layout',
        meta: {title: 'home', icon: 'HomeFilled', hidden: false},
        redirect:'/home',
        component: () => import('./layout/base.vue'),
        children: [
            {
                path: '/home',
                meta: {title: 'home'},
                component: () => import('./views/home/index.vue'),
            },
        ]
    },
    {
        path: '/system',
        name: 'system',
        meta: {title: 'system', icon: 'Setting'},
        redirect: '/system/menu',
        component: () => import('./layout/base.vue'),
        children: [
            {
                path: '/system/menu',
                name: 'menu',
                meta: {title: 'menu', icon: 'DashboardOutlined'},
                component: () => import('./views/system/menu/index.vue'),
            },
            {
                path: '/system/menu2',
                name: 'menu2',
                meta: {title: 'menu', icon: 'DashboardOutlined'},
                component: () => import('./views/system/menu/index.vue'),
            },
        ]
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router