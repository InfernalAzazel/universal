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

// company: Optional[str] = None  # 公司
// department: Optional[str] = None  # 部门
// username: Optional[str] = None  # 帐号： quid1111
// name: Optional[str] = None  # 姓名拼音： DeSai
// mail: Optional[str] = None  # 邮箱
// disabled: Optional[bool] = False  # 禁用：True == 禁用
// role_name: Optional[str] = None  # 角色名称： user == 普通用户

const form = ref({})
const serachForm = ref({})
const detail = ref({})
const selectData = ref([
  { value: true, label: '是' },
  { value: false, label: '否' },
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
    label: '用户',
    prop: 'username',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
  {
    label: '名称',
    prop: 'name',
    component: 'el-input',
    detail: true,
  },
  {
    label: '邮箱',
    prop: 'mail',
    component: 'el-input',
    search: true,
    detail: true,
  },
  {
    label: '公司',
    prop: 'company',
    component: 'el-input',
    detail: true,
  },
  {
    label: '部门',
    prop: 'department',
    component: 'el-input',
    detail: true,
  },
  {
    label: '禁用',
    prop: 'disabled',
    component: 'pro-select',
    form: true,
    search: true,
    detail: true,
    props:{
      data: selectData.value
    }
  },
  {
    label: '角色',
    prop: 'role_name',
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