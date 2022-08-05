<template>
<el-config-provider :locale="state.locales==='en-us'? en :zhCn" >
  <router-view/>
</el-config-provider>
</template>
<script lang="ts" setup>
// @ts-ignore
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
// @ts-ignore
import en from 'element-plus/dist/locale/en.mjs'
import {useGlobalState} from "./composables";

const state = useGlobalState()


</script>
<style>
#app {
  @apply h-screen;
}
</style>
