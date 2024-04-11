import { createGlobalState, useStorage } from '@vueuse/core'
import { ref } from 'vue'


export const useSidebarNavState = createGlobalState(() => {
    const selectId = ref<number>(-1)
    // 判断项目是否被选中
    const isSelected = (id: number) => selectId.value === id

    function setSelectId(id: number) {
      selectId.value = id
    }

    return { setSelectId, isSelected }
  }
)