<script setup lang="ts">
import { ElAvatar, ElMenu } from 'element-plus'
import logo from '@/assets/logo.svg'
import Markdown from './Markdown.vue'
import type { SidebarType } from './typings.d'
import './styles.css'
import { toRefs } from 'vue'
import Sidebar from '@/components/DocsPress/Sidebar.vue'

const props = defineProps<{
  sourceData: SidebarType[];
  currentArticle: string
}>()

const emit = defineEmits<{
  (event: 'onSidebarSelect', link: string): void;
}>()

// 分配ID
function getAssignIdsData(data: SidebarType[]) {
  let currentId = 0;
  const assignIds = (data: SidebarType[]) => {
    return data.map(item => {
      // 给当前项分配一个新的ID
      const newItem = { ...item, id: currentId++ };
      // 如果有子项，递归地给它们也分配ID
      if (newItem.items && newItem.items.length) {
        newItem.items = assignIds(newItem.items);
      }
      return newItem;
    });
  }
  return assignIds(data)
}
async function sidebarSelectArticle(link: string) {
  // 重置滚动位置
  const markdownContainer = document.querySelector('.markdown-container')
  if (markdownContainer) {
    markdownContainer.scrollTop = 0 // 将滚动位置重置为顶部
  }
  emit('onSidebarSelect', link)
}

</script>

<template>
  <div class="flex flex-col h-screen w-screen overflow-hidden">
    <ElMenu class="w-full" mode="horizontal">
      <el-menu-item index="0">
        <el-icon size="32">
          <component is="Reading"></component>
        </el-icon>
        <span> Element logo </span>
      </el-menu-item>
      <div class="flex-grow"/>

      <el-menu-item index="1">Processing Center</el-menu-item>
      <el-sub-menu index="2">
        <template #title>Workspace</template>
        <el-menu-item index="2-1">item one</el-menu-item>
        <el-menu-item index="2-2">item two</el-menu-item>
        <el-menu-item index="2-3">item three</el-menu-item>
        <el-sub-menu index="2-4">
          <template #title>item four</template>
          <el-menu-item index="2-4-1">item one</el-menu-item>
          <el-menu-item index="2-4-2">item two</el-menu-item>
          <el-menu-item index="2-4-3">item three</el-menu-item>
        </el-sub-menu>
      </el-sub-menu>
    </ElMenu>
    <div class="flex flex-row h-full w-full">
      <div class="docs-nav overflow-y-scroll">
        <Sidebar :data="getAssignIdsData(props.sourceData)" :onSelect="sidebarSelectArticle" />
      </div>
      <div class='w-full p-10 markdown-container'>
        <Markdown :markdown="props.currentArticle"></Markdown>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>