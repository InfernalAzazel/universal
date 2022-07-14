<template>
  <pro-card shadow="never">
    <pro-crud
        v-loading="isFetching"
        v-model="form"
        v-model:search="serachForm"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :columns="columns"
        :menu="menu"
        :data="list"
        :detail="detail"
        :before-open="beforeOpen"
        @search="search"
        @submit="submit"
        @delete="deleteRow"
        row-key="key"
        :table-columns="tableColumns"
        :total="total"
        @load="loadList"
        @search-reset="loadList"
        layout="total, ->, jumper, prev, pager, next, sizes"
        border
        stripe
        show-overflow-tooltip
    >
      <template #action>
        <pro-column-setting
            v-model="tableColumns"
            :allow-drag="(node) => console.log(node)"
            :allow-drop="(draggingNode, dropNode, type)=>console.log(draggingNode)"
            default-expand-all
            icon="SettingOutlined"
        />
      </template>
    </pro-crud>
  </pro-card>
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
import {useCrud} from "../../../composables/crud";
import {Api} from "../../../utils";

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
const tableColumns = ref(JSON.parse(JSON.stringify(columns)))


const {
  form,
  serachForm,
  detail,
  loadList,
  currentPage,
  pageSize,
  list,
  total,
  isFetching,
  beforeOpen,
  submit,
  search,
  deleteRow
} = useCrud(Api.usersList,Api.usersAdd,Api.usersEdit, Api.usersDelete, true)
</script>

<style></style>