<script setup lang="ts">
import { defineProps, onMounted } from 'vue'
import type { PropType } from 'vue'
import type { SidebarType } from './typings.d';
import { useSidebarNavState } from '@/components/DocsPress/state'

// 定义组件属性
const props = defineProps({
  data: Array as PropType<SidebarType[]>,
  onSelect: Function as PropType<(link: string) => void>,
  isTopLevel: {
    type: Boolean,
    default: true
  }
});

const {setSelectId, isSelected} = useSidebarNavState()


const selectItem = (item: SidebarType) => {
  if(!props.isTopLevel && item.link){
    setSelectId( item.id || -1);
    // 如果侧边栏项有链接，通知父组件该链接被选择
    props.onSelect && props.onSelect(item.link);
    console.log('hahah', item)
  }
};

onMounted(()=>{
  console.log('888')
})

</script>

<template>
  <ul class="sidebar-list">
    <li v-for="item in data" :key="item.title" class="sidebar-item">
      <span
        :class="{'selected': isSelected(item.id || -1) && !props.isTopLevel}"
        @click="selectItem(item)"
      >
        {{ item.title }}
      </span>
      <!-- 递归渲染子项 -->
      <SidebarNav
        v-if="item.items && item.items.length"
        :data="item.items"
        :onSelect="props.onSelect"
        :isTopLevel="false"
      />
    </li>
  </ul>
</template>

<style scoped>
/* 样式... */

/* 被选中的项的样式 */
.selected {
  color: green; /* 选中项变绿色 */
}
.not-selected {
  font-weight: normal; /* 正常字体 */
  color: #777; /* 灰色 */
}
</style>