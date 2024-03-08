<script lang="ts" setup>
import { ref } from 'vue'
import {
  defineCrudColumns,
  defineCrudMenuColumns,

} from 'element-pro-components'
import {useI18n} from "vue-i18n";
import { useInterfaceCrudRequest } from '@/services'
import { getTagType, splitString } from '@/utils'

const {t} = useI18n()
const crudRef = ref()
const menu = defineCrudMenuColumns({
  label: t(`crud.label`),
  addText: t(`crud.addText`),
  detailText: t(`crud.detailText`),
  editText: t(`crud.editText`),
  searchText: t(`crud.searchText`),
  searchResetText: t(`crud.searchResetText`),
  submitText: t(`crud.submitText`),
  resetText: t(`crud.resetText`),
  detail: false,
  edit: false,
  del: false,
  searchReset: true,
  fixed: 'right',
  width: '230'
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
    search: true,
    detail: true,
  },
  {
    label: t(`system.interface.title`),
    prop: 'title',
    component: 'el-input',
    form: true,
    detail: true,
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
  searchForm,
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
} = useInterfaceCrudRequest(true)

const rules = {
  path: { required: true, message: t(`rules.interface.path`), trigger: 'blur' },
  group: { required: true, message: t(`rules.interface.group`), trigger: 'blur' },
  title: { required: true, message: t(`rules.interface.title`), trigger: 'blur' },
  method: { required: true, message: t(`rules.interface.method`), trigger: 'blur' },
}



function clone(row: any) {
  form.value = row;
  crudRef.value.openDialog('add')
}




</script>
<template>
  <pro-card>
    <pro-crud
      ref="crudRef"
      v-loading="isFetching"
      v-model="form"
      v-model:search="searchForm"
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
          default-expand-all
          icon="SettingOutlined"
        />
      </template>
      <template #menu="{ row, size }">
        <el-button :size="size" type="primary" @click="clone(row)" link> {{t(`crud.clone`)}} </el-button>
        <el-button :size="size" type="primary" @click="crudRef.openDialog('edit', row)" link> {{t(`crud.editText`)}} </el-button>
        <el-button :size="size" type="info" @click="crudRef.openDialog('detail', row)" link> {{t(`crud.detailText`)}} </el-button>
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
      <template #table-method="{ row, size }">
        <el-tag class="ml-1" :size="size" :type="getTagType(row?.method)">{{ row?.method }}</el-tag>
      </template>
      <template #table-group="{ row, size }">
        <template v-for="(value, index) in splitString(row?.group)" :key="index">
          <el-tag class="ml-1" :size="size" type="primary">{{ value }}</el-tag>
        </template>
      </template>
      <template #detail-method="{ item, size }">
        <el-tag class="ml-1" :size="size" :type="getTagType(item?.method)">{{ item?.method }}</el-tag>
      </template>
      <template #detail-group="{ item, size }">
        <template v-for="(value, index) in splitString(item?.group)" :key="index">
          <el-tag class="ml-1" :size="size" type="primary">{{ value }}</el-tag>
        </template>
      </template>
    </pro-crud>
  </pro-card>

</template>
<style></style>