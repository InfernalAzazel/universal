import { createGlobalState, useStorage } from '@vueuse/core'
import { GlobalStorageKey } from '../utils'
import type { ResLogin } from '../types'

/** 存储全局响应变量 */
export const useGlobalState = createGlobalState(() =>
    useStorage(GlobalStorageKey, {
        token_type: '',
        access_token: '',
        locales: '',
    })
)