import {createRouter, createWebHistory, RouteRecordRaw} from 'vue-router'

const routes: RouteRecordRaw[] = [
    { 
      path: '/',
      name: 'layout',
      meta: { title: 'Home' }, 
      redirect: '/home',
      component: () => import('./layout/index.vue'),
      children: [
        {
          path: '/home',
          name: 'home',
          meta: { title: 'home', icon: 'DashboardOutlined' },
          component: () => import('./views/home/index.vue'),
        },
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('./views/login/index.vue'),
    }
  ]
  
const router = createRouter({
    history: createWebHistory(),
    routes,
  })

export default router