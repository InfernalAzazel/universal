<template>
  <pro-card>
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
import { Api } from "../../../utils";

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
    prop: 'describe',
    component: 'el-input',
    props: {
      type: 'textarea',
    },
    form: true,
    detail: true,
  },
  {
    label: '请求方式',
    prop: 'method',
    component: 'pro-select',
    form: true,
    search: true,
    detail: true,
    props:{
      data: selectData.value
    }
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
} = useCrud(Api.interfaceList, Api.interfaceAdd, Api.interfaceEdit, Api.interfaceDelete, true)







</script>
<style></style>