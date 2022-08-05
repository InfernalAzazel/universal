<template>
  <el-divider :content-position="contentPosition">
    {{ title }}
  </el-divider>
</template>

<script lang="ts" setup>
import {onMounted, toRefs, watch} from "vue";
const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  title: {
    type: String,
    default: '',
  },
  contentPosition: {
    type: String,
    default: 'left',
  },
})

const {modelValue, title} = toRefs(props)
const emit = defineEmits(['update:modelValue'])
watch(title, (newVal, oldVal) => {
  emit('update:modelValue', newVal)
}, {
  immediate: true
})
</script>