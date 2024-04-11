<script setup lang="ts">
import { RouterView } from 'vue-router'
import { useGlobalState } from '@/composables/store'
// @ts-ignore
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
// @ts-ignore
import enUS from 'element-plus/dist/locale/en.mjs'
const {locale} = useGlobalState()


</script>

<template>
  <el-config-provider :locale="locale==='en_us'? enUS :zhCn" >
    <router-view/>
  </el-config-provider>
</template>