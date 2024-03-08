<script setup lang="ts">
import DocsPress from '@/components/DocsPress/index.vue'
import type { SidebarType, DocsConfigType } from '@/components/DocsPress/typings'
import { nextTick, ref } from 'vue'
import { createFetch } from '@vueuse/core'

const en_us_data: SidebarType[] = [
  {
    title: '入门',
    items: [
      {
        title: '介绍',
        link: 'https://raw.githubusercontent.com/hairyf/naive-ui-pro-components/main/docs/docs/intro.md'
      },
      {
        title: '快速开始',
        link: 'https://raw.githubusercontent.com/hairyf/naive-ui-pro-components/main/docs/docs/faq.md'
      }
    ]
  },
  {
    title: '必需品',
    items: [
      { title: '创建应用程序', link: 'https://raw.githubusercontent.com/InfernalAzazel/universal/master/README.md' },
      { title: '模板语法', link: 'http://10.219.127.34/extittivns03/testdocs/raw/master/README.md?inline=false' }
    ]
  }

]
const config: DocsConfigType = {
  title: '饿了么',
  root: 'en_us',
  locales: [
    {mark: 'en_us', label:'英文', indexLink:'', sidebars: en_us_data}
  ]

}
const currentArticle = ref('')
const useRequest = createFetch({
  options: {
    immediate: false, // 是否在使用 useMyFetch 时自动运行 (推荐手动运行)
    timeout: 30000 // 请求过期时间
  },
  fetchOptions: {
    mode: 'cors'
  }
})

async function onSidebarSelect(link: string) {
  const { data, execute } = useRequest(link).get()
  await execute()
  if (data.value) {
    currentArticle.value = (data.value || '') as string
    await nextTick()

  }
}
</script>

<template>
<DocsPress :source-data="data" :current-article="currentArticle" @onSidebarSelect="onSidebarSelect"/>
</template>

<style scoped>

</style>