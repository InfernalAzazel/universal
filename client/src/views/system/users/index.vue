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
        :table-columns="tableColumns"
        :total="total"
        @load="loadList"
        @search-reset="searchReset"
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
      <template #table-association_role="{row, column, $index }">
        <el-tag v-if="row.association_role.id==='***'" type="danger">
          {{ t(`system.users.association_role_delete`)}}
        </el-tag>
        <el-tag v-else>
          {{ state.locales === 'en-us'? row.association_role.name_en_us: row.association_role.name_zh_cn}}
        </el-tag>
      </template>
      <template #table-disabled="{row, column, $index }">
        {{ $t(`selectBool.${row.disabled}`) }}
      </template>
      <template #detail-association_role="{ size, item }">
        <div v-if="item.association_role.id==='***'">
          <span class="text-red-600">{{ t(`system.users.association_role_delete`)}}</span>
        </div>
        <div v-else>
          <li>ID: <span>{{item.association_role.id}}</span></li>
          <li>Name: <span>{{ state.locales === 'en-us'? item.association_role.name_en_us: item.association_role.name_zh_cn }}</span></li>
        </div>
      </template>
      <template #detail-disabled="{ size, item }">
        {{ $t(`selectBool.${item.disabled}`) }}
      </template>
    </pro-crud>
  </pro-card>
</template>
<script lang="ts" setup>
import {markRaw, ref} from 'vue'
import {
  defineCrudColumns,
  defineCrudMenuColumns,
  defineCrudSearch,

} from 'element-pro-components'
import {useCrud} from "../../../composables/crud";
import RoleSelect from './components/RoleSelect/index.vue'

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
    label: t(`system.users.id`),
    prop: 'id',
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
    label: t(`system.users.association_role`),
    prop: 'association_role',
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
  association_role: {required: true, message: t('rules.users.association_role'), trigger: 'blur'},
}

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
  // search,
  deleteRow
} = useCrud(Api.usersList,Api.usersAdd,Api.usersEdit, Api.usersDelete, true)

const search = defineCrudSearch(async (done, isValid, invalidFields) => {

  if (isValid) {
    let data = JSON.parse(JSON.stringify(serachForm.value))
    let temp = {'association_role': data.association_role}
    if (data.association_role){
      data.association_role_id = data.association_role.id
      delete data.association_role
      serachForm.value = data
      console.log(serachForm.value)
    }
    await loadList()
    serachForm.value = {...serachForm.value, ...temp}
  }
  done()
})
const searchReset = async () => {
  serachForm.value = {} as any
  await loadList()
}

</script>

<style></style>