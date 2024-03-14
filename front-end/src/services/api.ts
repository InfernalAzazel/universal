import { usePost, useGet, usePut } from '@/composables/request'
import type { API, PagesData, ResponseMessages } from './typings.d'
import { useCrud } from '@/composables/crud'
import type { MaybeRef, UseFetchReturn } from '@vueuse/core'
import { computed, unref } from 'vue'
export function useAutoInitRequest(){
    return useGet('/api/v1/public/init/auto')
}

export function useLoginRequest(from: any) {
    const sp = new URLSearchParams(from)
    return  usePost<API.ResLogin>('/api/v1/public/auth/login', sp)
}
// 仪表盘
export function useMonitorDictRequest(){
    return useGet<ResponseMessages<API.Monitor>>('/api/v1/private/admin/dashboard/monitor')
}

// --- 菜单 ---
export function useMenuArrayRequest(query?: MaybeRef<unknown>){
    return useGet('/api/v1/private/admin/system/menu', query)
}
export function useMenuCrudRequest(immediate: boolean = false){
    return useCrud('/api/v1/private/admin/system/menu', immediate)
}
// --- 接口 ---
export function useInterfaceArrayRequest(query?: MaybeRef<unknown>){
    return useGet('/api/v1/private/admin/system/interface', query)
}
export function useInterfaceCrudRequest(immediate: boolean = false){
    return useCrud('/api/v1/private/admin/system/interface', immediate)
}

// --- 角色 ---
export function useRoleArrayRequest(query?: MaybeRef<unknown>){
    return useGet('/api/v1/private/admin/system/role', query)
}
export function useRoleEditRequest(uid: MaybeRef<string>, payload?: MaybeRef<unknown>) {
    const url = '/api/v1/private/admin/system/role';
    const _url = computed(() => {
        const _uid = unref(uid)
        return `${url}?uid=${_uid}`
    })
    return usePut(_url, payload);
}
export function useRoleCrudRequest(immediate: boolean = false){
    return useCrud('/api/v1/private/admin/system/role', immediate)
}
// --- 用户 ---
export function useUsersCrudRequest(immediate: boolean = false){
    return useCrud('/api/v1/private/admin/system/users', immediate)
}

// -------- 业务 ----------
// --- 信息 路由
export function useGetInfoRoutesRequest():  UseFetchReturn<ResponseMessages<any>>{
    return useGet('/api/v1/private/root/info/routes')
}

