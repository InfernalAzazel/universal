import { createI18n } from 'vue-i18n' // 引入vue-i18n组件
import zh_ch from './zh-cn'
import en from './en-us'
import {useGlobalState} from "../composables";
const state = useGlobalState()

const i18n = createI18n({
    locale: state.value.locales = state.value.locales===''?'en-us':state.value.locales, // 设置语言环境
    // fallbackLocale: 'en-us', // 没有中文的话默认英文
    messages: {
        // 配置语言
        'zh-cn': zh_ch,
        'en-us': en
    }
})

export default i18n