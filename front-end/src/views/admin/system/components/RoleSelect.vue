<script lang="ts" setup>
import { onMounted, ref, toRefs } from 'vue'
import { useRoleArrayRequest } from '@/services'

const props = defineProps({
  modelValue: {
    type: Array,
    default: [] as string[],
  },
})
const {modelValue} = toRefs(props)
const roleQuery = ref({ is_all_query: true })
const data = ref([])

const {data: RoleData, execute: exeRoleArray} = useRoleArrayRequest(roleQuery)
const emit = defineEmits(['update:modelValue'])
const Change = (val:any) => {
  emit('update:modelValue', val)
}

onMounted(async () => {
  await exeRoleArray()
  data.value = []
  if(RoleData.value){
    RoleData.value?.data.forEach(item => {
      data.value.push({
        label: item.title,
        value: item.title
      })
    })
  }
})
</script>
<template>
  <el-select v-model="modelValue" multiple placeholder="Select" @change="Change">
    <el-option
      v-for="item in data"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    >
    </el-option>
  </el-select>
</template>