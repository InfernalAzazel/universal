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
        :rules="rules"
        :data="list"
        :detail="detail"
        :before-open="beforeOpen"
        @search="search"
        @submit="submit"
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
      <template #menu="{ row, size }">
        <el-popconfirm :title="$t(`crud.isDelText`)" @confirm="deleteRow(row)">
          <template #reference>
            <el-button
                :size="size"
                type="danger"
                link
            >
              {{$t(`crud.delText`)}}
            </el-button>
          </template>
        </el-popconfirm>
      </template>
    </pro-crud>
  </pro-card>

</template>
<script lang="ts" setup>
import { ref } from 'vue'
import {
  defineCrudColumns,
  defineCrudMenuColumns,

} from 'element-pro-components'
import {useCrud} from "../../../composables/crud";
import { Api } from "../../../utils";
import {useI18n} from "vue-i18n";

const {t} = useI18n()
const menu = defineCrudMenuColumns({
  label: t(`crud.label`),
  addText: t(`crud.addText`),
  detailText: t(`crud.detailText`),
  editText: t(`crud.editText`),
  searchText: t(`crud.searchText`),
  searchResetText: t(`crud.searchResetText`),
  submitText: t(`crud.submitText`),
  resetText: t(`crud.resetText`),
  detail: true,
  edit: true,
  del: false,
  searchReset: true,
  fixed: 'right',
  width: '200'
})


const selectData = ref([
  { value: 'GET', label: 'GET' },
  { value: 'POST', label: 'POST' },
  { value: 'PUT', label: 'PUT' },
  { value: 'DELETE', label: 'DELETE' },
])
const columns = defineCrudColumns([
  {
    label: t(`system.interface.uid`),
    prop: 'uid',
    component: 'el-input',
    detail: true,
    props:{
      disabled: true
    }
  },
  {
    label: t(`system.interface.path`),
    prop: 'path',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
  {
    label: t(`system.interface.group`),
    prop: 'group',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
  {
    label: t(`system.interface.describe_zh_cn`),
    prop: 'describe_zh_cn',
    component: 'el-input',
    form: true,
    detail: true,
  },
  {
    label: t(`system.interface.describe_en_us`),
    prop: 'describe_en_us',
    component: 'el-input',
    form: true,
    detail: true,
  },
  {
    label: t(`system.interface.method`),
    prop: 'method',
    component: 'pro-select',
    form: true,
    search: true,
    detail: true,
    props:{
      data: selectData.value
    }
  },
  {
    label: t(`el-date-picker.create_at`),
    prop: 'create_at',
    component: 'el-date-picker',
    props: {
      type: 'datetimerange',
      rangeSeparator: '-',
      startPlaceholder: 'start',
      endPlaceholder: 'end',
      format:"YYYY-MM-DD",
      valueFormat:"YYYY-MM-DDTHH:mm:ss"
    },
    search: true,
    detail: true,
  },
  {
    label: t(`el-date-picker.update_at`),
    prop: 'update_at',
    component: 'el-date-picker',
    props: {
      type: 'datetimerange',
      rangeSeparator: '-',
      startPlaceholder: 'start',
      endPlaceholder: 'end',
      format:"YYYY-MM-DD",
      valueFormat:"YYYY-MM-DDTHH:mm:ss"
    },
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
} = useCrud(Api.interfaceList, Api.interfaceAdd, Api.interfaceEdit, Api.interfaceDelete, true)


const rules = {
  path: { required: true, message: t(`rules.interface.path`), trigger: 'blur' },
  group: { required: true, message: t(`rules.interface.group`), trigger: 'blur' },
  describe_zh_cn: { required: true, message: t(`rules.interface.describe_zh_cn`), trigger: 'blur' },
  describe_en_us: { required: true, message: t(`rules.interface.describe_en_us`), trigger: 'blur' },
  method: { required: true, message: t(`rules.interface.method`), trigger: 'blur' },
}




</script>
<style></style>