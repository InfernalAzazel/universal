<template>
  <pro-card header="新建">
    <pro-form
        v-model="form"
        :columns="columns"
        label-width="100px"
        @submit="submit"
    />
  </pro-card>
</template>
<script lang="ts" setup>
import {h, markRaw, ref} from "vue";
import {ElMessage} from "element-plus";
import {defineFormSubmit} from "element-pro-components";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const icon_data = ref<Array<Record<string, string>>>([])
const form = ref({})
const data = ref([
  {
    label: '1',
    value: 1,
    children: [
      {
        value: 11,
        label: '1-1',
        children: [{value: 111, label: '1-1-1'}],
      },
    ],
  },
  {
    value: 2,
    label: '2',
    children: [
      {
        value: 21,
        label: '2-1',
        children: [{value: 211, label: '2-1-1'}],
      },
      {
        value: 22,
        label: '2-2',
        children: [{value: 221, label: '2-2-1'}],
      },
    ],
  },
  {
    value: 3,
    label: '3',
    children: [
      {
        value: 31,
        label: '3-1',
        children: [{value: 311, label: '3-1-1'}],
      },
      {
        value: 32,
        label: '3-2',
        children: [{value: 321, label: '3-2-1'}],
      },
    ],
  },
])
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  if (key) {
    icon_data.value?.push({value: key, label: key})
  }
}


const columns = [
  {
    label: '父级',
    prop: 'name',
    component: 'pro-tree-select',
    props: {
      data: data.value,
    }
  },
  {
    label: '菜单标识',
    prop: 'menu_id',
    component: 'el-input',
  },
  {
    label: '图标',
    prop: 'icon',
    component: 'pro-select',
    props: {
      data: icon_data.value,
    },
  },
  {
    label: '路径',
    prop: 'path',
    component: 'el-input',
  },

  {
    label: '角色',
    prop: 'role',
    component: 'pro-select',
    props: {
      multiple: true,
      data: icon_data.value,
    },
  },
]
const submit = defineFormSubmit((done, isValid, invalidFields) => {
  ElMessage(`submit: ${isValid}`)
  console.log(form.value, isValid, invalidFields)
  setTimeout(() => {
    done()
  }, 1000)
})
</script>
<style></style>