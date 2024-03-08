<script setup lang="ts">
import DocsPress from '@/components/DocsPress/index.vue'
import type { SidebarType, DocsConfigType } from '@/components/DocsPress/typings'
import { nextTick, ref } from 'vue'
import { createFetch } from '@vueuse/core'

const en_us_data: SidebarType[] = [
  {
    title: 'start',
    items: [
      {
        title: 'intro',
        link: 'https://raw.githubusercontent.com/InfernalAzazel/universal/master/docs/developer/en_us/intro.md'
      },
      {
        title: 'get started quickly',
        link: 'https://raw.githubusercontent.com/InfernalAzazel/universal/master/docs/developer/en_us/faq.md'
      }
    ]
  },
  {
    title: 'other',
    items: [
      { title: 'QA', link: 'https://raw.githubusercontent.com/InfernalAzazel/universal/master/docs/developer/en_us/introduce.md' },
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