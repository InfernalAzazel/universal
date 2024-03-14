import type {RouteRecordRaw} from 'vue-router';
import {createRouter, createWebHashHistory} from 'vue-router';
import { AllowList } from '@/config';
import type { API } from '@/services'
import { useGetInfoRoutesRequest } from '@/services'
import { getTreeDataAndHalfCheckedKeys } from '@/utils';
import { useGlobalState } from '@/composables/store';
import i18n from '@/locales';


const t = i18n.global.t

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    meta:{ hidden: true },
    component: () => import('@/views/root/auth/login.vue'),
  },
  // {
  //   path: '/admin',
  //   redirect: '/admin/system/users',
  //   component: () => import('@/layouts/admin.vue'),
  //   meta:{ title: '系统', icon: 'icon-park-solid:system'},
  //   children: [
  //     {
  //       path: '/admin/system/users',
  //       meta:{ title: '用户', icon: 'ant-design:team-outlined'},
  //       component: () => import('@/views/admin/system/users.vue'),
  //     },
  //     {
  //       path: '/admin/system/role',
  //       meta:{ title: '角色', icon: 'ant-design:api-outlined'},
  //       component: () => import('@/views/admin/system/role.vue'),
  //     },
  //     {
  //       path: '/admin/system/interface',
  //       meta:{ title: '接口', icon: 'ant-design:api-outlined'},
  //       component: () => import('@/views/admin/system/interface.vue'),
  //     },
  //     {
  //       path: '/admin/system/menu',
  //       meta:{ title: '菜单', icon: 'ant-design:api-outlined'},
  //       component: () => import('@/views/admin/system/menu.vue'),
  //     },
  //   ]
  // },
]

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
})

let initRoute = false

router.beforeEach( async (to, form, next) => {
  const state = useGlobalState()
  const {data: infoRoutesData, execute: exeInfoRoutes} = useGetInfoRoutesRequest()
  if (!AllowList.includes(to.path) && !state.value.access_token) {
    next(`/login?redirect=${to.path}`)
  } else if (to.path === '/login' && state.value.access_token) {
    next('/')
  } else if (!initRoute && to.path !== '/login' && state.value.access_token) {
    // 获取路由 -> 转化 -> addRoute
    await exeInfoRoutes()
    if (infoRoutesData.value){
      const {treeData} = getTreeDataAndHalfCheckedKeys(infoRoutesData.value?.data || [])
      generateRoutes(treeData).forEach((item) => {
        router.addRoute(item)
        ;(router.options.routes as RouteRecordRaw[]).push(item)
      })
    }
    initRoute = true
    next({ ...to, replace: true })
  } else {
    next()
  }
})

/**
 * 转化路由 NOTE: 根据需要修改
 * @param list 需要转化的路由
 */
function generateRoutes(list: API.Router[]): RouteRecordRaw[] {
  return list.reduce((all, item) => {
    // NOTE: 这里可以进行一些权限筛选，排除没有权限的路由
    // if (item.roles?.length && item.roles.includes('admin')) return all

    const children = item.children?.length
      ? generateRoutes(item.children)
      : undefined


    const modules = import.meta.glob('../**/**.vue', );
    const current: RouteRecordRaw = {
      path: item.path,
      redirect: item.redirect,
      name: item.name,
      component: modules[`../${item.component}`],
      children,
      meta: {
        title: t(`router.menu.title_mark.${item.title_mark}`),
        icon: item.icon,
        hide: item.hide,
      },
    } as RouteRecordRaw

    return [...all, current]
  }, [] as RouteRecordRaw[])
}
export default router
