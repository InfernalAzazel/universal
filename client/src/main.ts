
import 'ant-design-vue/dist/antd.css'
import '@ant-design-vue/pro-layout/dist/style.css'
import './app.css'
import { createApp } from 'vue'
import { ConfigProvider } from 'ant-design-vue'
import ProLayout, { PageContainer } from '@ant-design-vue/pro-layout'
import Antd from 'ant-design-vue';
import icons from './icons';
import App from './App.vue'
import store  from './store'
import router from './router'
import VueAxios from "vue-axios"
import http from "./http"

const app = createApp(App)
app.use(router)
app.use(store)
app.use(VueAxios, http);
app.use(icons)
app.use(Antd)
app.use(ConfigProvider)
app.use(ProLayout)
app.use(PageContainer)
app.provide('axios', app.config.globalProperties.axios)  // provide 'axios'
app.mount('#app')

