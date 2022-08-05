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

<script setup>
import {markRaw, ref} from 'vue'
import {
  defineCrudColumns,
  defineCrudMenuColumns,


} from 'element-pro-components'
import {useCrud} from "../../../composables/crud";
import {Api} from "../../../utils";
import {useI18n} from "vue-i18n";
import {useGlobalState} from "../../../composables";

const {t} = useI18n()
const state = useGlobalState()

const menu = defineCrudMenuColumns({
  label: t(`crud.label`),
  addText: t(`crud.addText`),
  detailText: t(`crud.detailText`),
  editText: t(`crud.editText`),
  searchText: t(`crud.searchText`),
  searchResetText: t(`crud.searchResetText`),
  submitText: t(`crud.submitText`),
  resetText: t(`crud.resetText`),
  add: false,
  detail: true,
  edit: true,
  del: false,
  searchReset: true,
  fixed: 'right',
  width: '200'
})
const columns = defineCrudColumns([
  {
    label: t(`system.syslog.id`),
    prop: 'id',
    component: 'el-input',
    detail: true,
    props:{
      disabled: true
    },
    width: '200'
  },
  {
    label: t(`system.syslog.username`),
    prop: 'username',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
    width: '200'
  },
  {
    label: t(`system.syslog.host`),
    prop: 'host',
    component: 'el-input',
    detail: true,
    width: '200'
  },
  {
    label: t(`system.syslog.browser`),
    prop: 'browser',
    component: 'el-input',
    search: true,
    detail: true,
    width: '200'
  },
  {
    label: t(`system.syslog.os`),
    prop: 'os',
    component: 'el-input',
    detail: true,
    width: '200'
  },
  {
    label: t(`system.syslog.path`),
    prop: 'path',
    component: 'el-input',
    detail: true,
    width: '200'
  },
  {
    label: t(`system.syslog.query_params`),
    prop: 'query_params',
    component: 'el-input',
    detail: true,
    width: '200'
  },
  {
    label: t(`system.syslog.method`),
    prop: 'method',
    component: 'el-input',
    detail: true,
    width: '200'
  },
  {
    label: t(`system.syslog.text`),
    prop: 'text',
    component: 'el-input',
    detail: true,
    width: '200'
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
    width: '200'
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
} = useCrud(Api.syslogList,Api.syslogAdd,Api.syslogEdit, Api.syslogDelete, true)

const data = ref([
  {
    date: '2016-05-03',
    user: {
      name: 'John Brown',
      address: 'New York No. 1 Lake Park222',
    },
  }
])

</script>
