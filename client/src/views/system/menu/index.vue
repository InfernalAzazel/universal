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
      <template #table-icon="{ row, size }">
        <el-button :icon="row.icon" type="text">
          {{ row.icon }}
        </el-button>
      </template>
    </pro-crud>
  </pro-card>
</template>

<script lang="ts" setup>
import {h, ref} from 'vue'
import {ElMessage} from 'element-plus'
import { Setting } from '@element-plus/icons-vue'
import { useGlobalState, useGet } from '../../../composables'
import ExSelect  from '../../../components/ExSelect/index.vue'
import {
  defineCrudColumns,
  defineCrudMenuColumns,
} from 'element-pro-components'
import { markRaw } from 'vue'
import {Api} from "../../../utils";
import {useCrud} from "../../../composables/crud";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const selectData = ref([
  { value: true, label: '是' },
  { value: false, label: '否' },
])
const selectIcon = ref<any[]>([])
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  selectIcon.value.push({
    value: key,
    label: key,
  })
}
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
  fixed:'right',
  width:'200'
  // detailProps: { type: 'success', plain: false },
  // editProps: { type: 'default', plain: true },
  // delProps: { type: 'info', plain: true },
})
const columns = defineCrudColumns([
  {
    label: 'ID',
    prop: 'id',
    component: 'el-input',
    search: true,
    detail: true,
    width: '200',
  },
  {
    label: '路由名称（标记）',
    prop: 'title',
    component: 'el-input',
    add: true,
    edit: true,
    search: true,
    detail: true,
    width: '200'
  },
  {
    label: 'URL路径',
    prop: 'path',
    component: 'el-input',
    add: true,
    search: true,
    detail: true,
    width: '500'
  },
  {
    label: '是否隐藏',
    prop: 'hide',
    component: 'pro-select',
    search: true,
    add: true,
    edit: true,
    detail: true,
    props:{
      data: selectData.value
    },
    width: '200'
  },
  {
    label: '节点',
    prop: 'key',
    component: 'el-input-number',
    props: {
      min:"0" ,
      max:"10000",
    },
    add: true,
    edit: true,
    search: true,
    detail: true,
    width: '200'
  },
  {
    label: '父节点',
    prop: 'father',
    component: 'el-input-number',
    props: {
      min:"0" ,
      max:"10000",
    },
    search: true,
    add: true,
    edit: true,
    detail: true,
    width: '200'
  },
  // {
  //   label: '排序',
  //   prop: 'sort',
  //   component: 'el-input',
  //   add: true,
  //   edit: true,
  //   detail: true,
  //   width: '200'
  // },
  {
    label: '页面路径',
    prop: 'component',
    component: 'el-input',
    search: true,
    add: true,
    edit: true,
    detail: true,
    width: '200'
  },
  {
    label: '图标',
    prop: 'icon',
    component: markRaw(ExSelect),
    props: {
      data: selectIcon.value,
    },
    search: true,
    add: true,
    edit: true,
    detail: true,
    width: '200'
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
} = useCrud(Api.menuList, Api.menuAdd, Api.menuEdit, Api.menuDelete, true)


</script>
<style>
/* 隐藏布局滚动条让谷歌浏览器更平滑*/
::-webkit-scrollbar{
  width:0px;
  height:0px;
}
</style>