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
    <template #menu="{ size }">
      <el-button
          :size="size"
          type="success"
          link
          @click="drawer = true"
      >
        设置权限
      </el-button>
    </template>
  </pro-crud>

  <el-drawer v-model="drawer" direction="rtl">
    <template #title>
      <h2>权限设置</h2>
    </template>
    <template #default>
      <el-tabs type="border-card">
        <el-tab-pane label="角色菜单">角色菜单</el-tab-pane>
        <el-tab-pane label="角色接口">角色接口</el-tab-pane>
      </el-tabs>
    </template>
    <template #footer>
      <div style="flex: auto">
       666
      </div>
    </template>
  </el-drawer>

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

const drawer = ref(false)
const form = ref({})
const serachForm = ref({})
const detail = ref({})
const columns = defineCrudColumns([
  {
    label: 'ID',
    prop: 'id',
    component: 'el-input',
    form: true,
    detail: true,
  },
  {
    label: '角色名称',
    prop: 'name',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
])
const data = ref([
  {
    id: '2016-05-03',
    name: 'Tom',
  },
  {
    id: '2016-05-02',
    name: 'Tom',
  },
  {
    id: '2016-05-04',
    name: 'Tom',
  },
  {
    id: '2016-05-01',
    name: 'Tom',
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