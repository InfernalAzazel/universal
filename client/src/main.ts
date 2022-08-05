import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './app.css'
import { createApp } from 'vue'
import ElementPro from 'element-pro-components'
import 'element-pro-components/lib/styles/index'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'

import router from './router'
import i18n from "./locales";


const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
app.use(i18n)
app.use(router)
app.use(ElementPlus)
app.use(ElementPro)
app.mount('#app') // mount app to '#app' element