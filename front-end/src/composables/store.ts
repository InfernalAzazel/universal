import { createGlobalState, useStorage } from '@vueuse/core'
import { GlobalStorageKey } from '@/config'

interface GlobalState {
  token_type: string;
  access_token: string;
  locale: string;
}
/** 存储全局响应变量 */
export const useGlobalState = createGlobalState<any>(() =>
  useStorage<GlobalState>(GlobalStorageKey, {
    token_type: '',
    access_token: '',
    locale: '',
  })
);