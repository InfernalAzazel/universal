<script setup lang="ts">
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark()
const toggleDark = useToggle(isDark)
</script>

<template>
  <div @click="toggleDark()">
    <el-icon v-if="isDark" :size="24"><Sunny /></el-icon>
    <el-icon v-else :size="24"><Moon /></el-icon>
  </div>
</template>