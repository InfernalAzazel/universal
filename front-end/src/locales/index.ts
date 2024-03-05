import { createI18n } from 'vue-i18n';
import zhCN from './zhCN';
import enUS from './enUS';
import { useGlobalState } from '@/composables/store'

const state = useGlobalState()
const i18n = createI18n({
  inheritLocale: true,
  legacy: false,
  locale: state.value.locale = state.value.locale===''?'en_us':state.value.locale, // 设置语言环境
  // fallbackLocale: 'en_us', // 没有中文的话默认英文
  messages: {
    // 配置语言
    'zh_cn': zhCN,
    'en_us': enUS
  }
})

export default i18n