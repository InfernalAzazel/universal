<script lang="ts" setup>
import {markRaw, ref} from 'vue'
import {
  defineCrudColumns,
  defineCrudMenuColumns,
} from 'element-pro-components'
import {useI18n} from "vue-i18n";
import { useUsersCrudRequest } from '@/services'
import RoleSelect from '@/views/admin/system/components/RoleSelect.vue'

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
const selectBool = ref([
  { value: true, label: t(`selectBool.true`) },
  { value: false, label: t(`selectBool.false`) },
])

const columns = defineCrudColumns([
  {
    label: t(`system.users.uid`),
    prop: 'uid',
    component: 'el-input',
    detail: true,
    props:{
      disabled: true
    },
    width: '200'
  },
  {
    label: t(`system.users.username`),
    prop: 'username',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
    width: '200'
  },
  {
    label: t(`system.users.name`),
    prop: 'name',
    component: 'el-input',
    detail: true,
    width: '200'
  },
  {
    label: t(`system.users.mail`),
    prop: 'mail',
    component: 'el-input',
    search: true,
    detail: true,
    width: '200'
  },
  {
    label: t(`system.users.company`),
    prop: 'company',
    component: 'el-input',
    detail: true,
    width: '200'
  },
  {
    label: t(`system.users.department`),
    prop: 'department',
    component: 'el-input',
    detail: true,
    width: '200'
  },
  {
    label: t(`system.users.disabled`),
    prop: 'disabled',
    component: 'pro-select',
    form: true,
    search: true,
    detail: true,
    props: {
      data: selectBool.value
    },
    width: '200'
  },
  {
    label: t(`system.users.role_names`),
    prop: 'role_names',
    component: markRaw(RoleSelect),
    search: true,
    form: true,
    detail: true,
    width: '200',
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

const rules = {
  username: {required: true, message: t('rules.users.username'), trigger: 'blur'},
  disabled: {required: true, message: t('rules.users.disabled'), trigger: 'blur'},
  role_names: {required: true, message: t('rules.users.role_names'), trigger: 'blur'},
}

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
} = useUsersCrudRequest( true)

</script>
<template>
  <pro-card shadow="never">
    <pro-crud
      v-loading="isFetching"
      v-model="form"
      v-model:search="searchForm"
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
      :rules="rules"
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
      <template #table-role_names="{ row, size }">
        <template v-for="(value, index) in row?.role_names" :key="index">
          <el-tag class="ml-1" :size="size" type="primary">{{ value }}</el-tag>
        </template>
      </template>
      <template #table-disabled="{row }">
        <el-switch v-model="row.disabled" disabled/>
      </template>
      <template #detail-role_names="{ item, size }">
        <template v-for="(value, index) in item?.role_names" :key="index">
          <el-tag class="ml-1" :size="size" type="primary">{{ value }}</el-tag>
        </template>
      </template>
      <template #detail-disabled="{item}">
        <el-switch v-model="item.disabled" disabled/>
      </template>
    </pro-crud>
  </pro-card>
</template>
<style></style>