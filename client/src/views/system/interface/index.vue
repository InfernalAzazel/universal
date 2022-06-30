<template>
  <pro-crud
      v-model="form"
      v-model:search="serachForm"
      :columns="columns"
      :menu="menu"
      :data="data"
      :detail="detail"
      :before-open="beforeOpen"
      label-width="100px"
      @search="search"
      @search-reset="reset"
      @submit="submit"
      @reset="reset"
      @delete="deleteRow"
  >
  </pro-crud>

</template>
<script lang="ts" setup>
import { defineComponent, ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  defineCrudColumns,
  defineCrudMenuColumns,
  defineCrudSubmit,
  defineCrudSearch,
  defineCrudBeforeOpen,
} from 'element-pro-components'

const menu = defineCrudMenuColumns({
  label: 'Operations',
  addText: 'New',
  detailText: '详细',
  editText: '编辑',
  delText: '删除',
  searchText: 'Search',
  searchResetText: 'Reset Search',
  submitText: '提交',
  resetText: 'Reset Form',
  detail: true,
  edit: true,
  del: true,
  searchReset: true,
  // detailProps: { type: 'success', plain: false },
  // editProps: { type: 'default', plain: true },
  // delProps: { type: 'info', plain: true },
})

const form = ref({})
const serachForm = ref({})
const detail = ref({})
const selectData = ref([
  { value: 'GET', label: 'GET' },
  { value: 'POST', label: 'POST' },
  { value: 'PUT', label: 'PUT' },
  { value: 'DELETE', label: 'DELETE' },
])
const columns = defineCrudColumns([
  {
    label: 'ID',
    prop: 'id',
    component: 'el-input',
    form: true,
    detail: true,
    props:{
      disabled: true
    }
  },
  {
    label: '路径',
    prop: 'path',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
  {
    label: '分组',
    prop: 'group',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
  {
    label: '接口简介(标志)',
    prop: 'interface_introduction',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
  {
    label: '请求方式',
    prop: 'request_method',
    component: 'pro-select',
    form: true,
    search: true,
    detail: true,
    props:{
      data: selectData.value
    }
  },
])
const data = ref([
  {
    id: '2016-05-03',
    path: 'Tom',
    group:'a',
    interface_introduction:'a',
    request_method:'GET',
  },
  {
    id: '2016-05-02',
    path: 'Tom',
    group:'a',
    interface_introduction:'a',
    request_method:'GET',
    children: [
      {
        id: '2016-05-02',
        path: 'Tom',
        group:'a',
        interface_introduction:'a',
        request_method:'GET',
      }
    ]
  },
  {
    id: '2016-05-04',
    path: 'Tom',
    group:'a',
    interface_introduction:'a',
    request_method:'GET',
  },
  {
    id: '2016-05-01',
    path: 'Tom',
    group:'a',
    interface_introduction:'a',
    request_method:'GET',
  },
])

const beforeOpen = defineCrudBeforeOpen((done, type, row) => {
  if (type === 'edit') {
    form.value = row || {}
  } else if (type === 'detail') {
    detail.value = row || {}
  }
  done()
})

const search = defineCrudSearch((done, isValid, invalidFields) => {
  ElMessage(`search: ${isValid}`)
  console.log('search', serachForm.value, isValid, invalidFields)
  setTimeout(() => {
    done()
  }, 1000)
})

const submit = defineCrudSubmit(
    (close, done, type, isValid, invalidFields) => {
      ElMessage(`submit: ${type}, ${isValid}`)
      console.log('submit', form.value, type, isValid, invalidFields)
      setTimeout(() => {
        isValid ? close() : done()
      }, 1000)
    }
)

const reset = () => {
  ElMessage('reset')
  console.log('reset')
}

const deleteRow = (row: any) => {
  ElMessage('deleteRow')
  console.log('deleteRow', row)
}


</script>
<style></style>