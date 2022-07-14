import { createFetch } from '@vueuse/core'
import {RequestAuthKey} from "../utils";
import {useGlobalState} from "./store";
import { isObject, MaybeRef, UseFetchReturn } from '@vueuse/core'
import {computed, unref} from "vue";
import {stringifyQuery, LocationQueryRaw} from "vue-router";

const useRequest = createFetch({
    baseUrl: '', // 基础路由
    options: {
        immediate: false, // 是否在使用 useMyFetch 时自动运行 (推荐手动运行)
        timeout: 30000, // 请求过期时间
        // 在请求前修改配置，如：注入 token 值
        async beforeFetch({ options }) {
            const state = useGlobalState()
            if (RequestAuthKey && state.value.token) {
                options.headers = Object.assign(options.headers || {}, {
                    [RequestAuthKey]: `Bearer ${state.value.token}`,
                })
            }
            return { options }
        },
        // 在请求后处理数据，如：拦截错误、处理过期
        afterFetch({ data, response }) {
            const state = useGlobalState()
            const status = data.code
            if (status === 401) {
                console.error(status)
                data = null
            }
            return { data, response }
        },
        // 请求错误
        onFetchError({ data, error }) {
            console.error(error)
            return { data, error }
        },
    },
    fetchOptions: {
        mode: 'cors',
        credentials: 'include', // 请求时携带 cookie 值
    },
})

/**
 * 封装 get 请求
 * @param url 请求地址
 * @param query 请求参数
 */
export function useGet<T = unknown>(
    url: MaybeRef<string>,
    query?: MaybeRef<unknown>
): UseFetchReturn<T> {
    const _url = computed(() => {
        const _url = unref(url)
        const _query = unref(query)
        const queryString = isObject(_query)
            ? stringifyQuery(_query as LocationQueryRaw)
            : _query || ''
        return `${_url}${queryString ? '?' : ''}${queryString}`
    })

    return useRequest<T>(_url).json()
}

/**
 * 封装 post 请求
 * @param url 请求地址
 * @param payload 请求参数
 */
export function usePost<T = unknown>(
    url: MaybeRef<string>,
    payload?: MaybeRef<unknown>
): UseFetchReturn<T> {
    return useRequest<T>(url).post(payload).json()
}

/**
 * 封装 put 请求
 * @param url 请求地址
 * @param payload 请求参数
 */
export function usePut<T = unknown>(
    url: MaybeRef<string>,
    payload?: MaybeRef<unknown>
): UseFetchReturn<T> {
    return useRequest<T>(url).put(payload).json()
}

/**
 * 封装 delete 请求
 * @param url 请求地址
 * @param payload 请求参数
 */
export function useDelete<T = unknown>(
    url: MaybeRef<string>,
    query?: MaybeRef<unknown>
): UseFetchReturn<T> {
    const _url = computed(() => {
        const _url = unref(url)
        const _query = unref(query)
        const queryString = isObject(_query)
            ? stringifyQuery(_query as LocationQueryRaw)
            : _query || ''
        return `${_url}${queryString ? '?' : ''}${queryString}`
    })
    return useRequest<T>(_url).delete().json()
}

/**
 * 封装获取Blob进行下载
 * @param url 请求地址
 */
export function useBlob(url: MaybeRef<string>): UseFetchReturn<Blob> {
    return useRequest(url).blob()
}