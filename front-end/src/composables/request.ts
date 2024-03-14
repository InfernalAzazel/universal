import type { MaybeRef, UseFetchReturn } from '@vueuse/core'
import { createFetch, isObject } from '@vueuse/core'
import { computed, unref } from 'vue'
import { ElNotification } from 'element-plus'
import router from '@/router'
import type { LocationQueryRaw } from 'vue-router'
import { stringifyQuery } from 'vue-router'
import { useGlobalState } from '@/composables/store'
import i18n from '@/locales'

const t = i18n.global.t;
const useRequest = createFetch({
  // baseUrl: '', // 基础路由
  options: {
    immediate: false, // 是否在使用 useMyFetch 时自动运行 (推荐手动运行)
    timeout: 30000, // 请求过期时间
    // 在请求前修改配置，如：注入 token 值
    async beforeFetch({ options }) {
      const state = useGlobalState()
      options.headers = Object.assign(options.headers || {}, {
        // 如果 access_token 存在，则设置 Authorization 头部
        ...(state.value.access_token ? { 'Authorization': `Bearer ${state.value.access_token}` } : {}),
        // 如果locale存在，则设置 Customize-Language 头部
        ...(state.value.locale ? { 'Customize-Language': state.value.locale} : {}),
      })
      return { options }
    },
    // 在请求后处理数据，如：拦截错误、处理过期
    // 获取请求返回后将立即运行。在任何 2xx 响应后运行
    async afterFetch({ data, response }) {
      // 处理成功响应
      const state = useGlobalState()
      if(data.success){
        if(data.status_code !== 200){
          ElNotification({
            title:  t('multipurpose.info'),
            message: data.detail,
            type: 'info',
          })
        }
      }else {
        // 定义一个数组，包含导致访问令牌失效的HTTP状态码
        const resetTokenStatusCodes = [419, 423, 480];
        // JWT过期 用户被禁用
        // 检查返回的状态码是否需要重置访问令牌
        if (resetTokenStatusCodes.includes(data.status_code)) {
          state.value.access_token = '';
          await router.push({ path: `/login?redirect=${router.currentRoute.value.path}` })
        }
        ElNotification({
          title: t('multipurpose.error'),
          message: data.detail,
          type: 'error',
        })
      }
      return { data, response }
    },
    // 请求错误
    // 获取请求返回后将立即运行。在任何 4xx 和 5xx 响应之后运行
    async onFetchError({ data, response, error }) {
      ElNotification({
        title: t('multipurpose.error'),
        message: data.detail,
        type: 'error',
      })

      // console.error(error)
      return { data, error }
    }
  },
  fetchOptions: {
    mode: 'cors',
    credentials: 'include' // 请求时携带 cookie 值
  }
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
 * @param query 请求参数
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
