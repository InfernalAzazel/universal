<script lang="ts" setup>
import {ElSelect} from "element-plus";
import {toRefs, watch} from "vue";
const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  data: {
    type: [Array, Object],
    default: [] as any,
  },
})
const {modelValue} = toRefs(props)
const emit = defineEmits(['update:modelValue'])
const Change = (val:any) => {
  emit('update:modelValue', val)
}
</script>

<template>
  <el-select v-model="modelValue" placeholder="Select" @change="Change">
    <template #prefix>
      <el-icon :size="20">
        <component :is="modelValue"/>
      </el-icon>
    </template>
    <el-option
        v-for="item in data"
        :key="item.value"
        :label="item.label"
        :value="item.value"
    >
      <el-icon :size="20">
        <component :is="item.label "/>
      </el-icon>
      {{ item.label }}
    </el-option>
  </el-select>
</template>