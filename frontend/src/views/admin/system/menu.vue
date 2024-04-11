<script lang="ts" setup>
import { onMounted, onUpdated, ref, watch } from 'vue'
import IconSelect from '@/components/IconSelect/index.vue'
import {
  defineCrudColumns,
  defineCrudMenuColumns,
} from 'element-pro-components'
import {markRaw} from 'vue'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import {useI18n} from "vue-i18n";
import { useMenuCrudRequest } from '@/services'
import { getTreeDataAndHalfCheckedKeys } from '@/utils'

const {t} = useI18n()
const selectIcon = ref<any[]>([])
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  selectIcon.value.push({
    value: key,
    label: key,
  })
}
const menuTrees = ref([])
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
const columns = defineCrudColumns([
  {
    label: t("system.menu.uid"),
    prop: 'uid',
    component: 'el-input',
    search: false,
    detail: true,
    width: '200',
  },
  {
    label: t("system.menu.title"),
    prop: 'title',
    component: 'el-input',
    add: true,
    edit: true,
    search: false,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.title_mark"),
    prop: 'title_mark',
    component: 'el-input',
    add: true,
    edit: true,
    search: false,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.redirect"),
    prop: 'redirect',
    component: 'el-input',
    add: true,
    edit: true,
    search: false,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.name"),
    prop: 'name',
    component: 'el-input',
    add: true,
    edit: true,
    search: false,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.path"),
    prop: 'path',
    component: 'el-input',
    add: true,
    edit: true,
    search: false,
    detail: true,
    width: '300'
  },
  {
    label: t("system.menu.order"),
    prop: 'order',
    component: 'el-input-number',
    add: true,
    edit: true,
    search: false,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.key"),
    prop: 'key',
    component: 'el-input-number',
    props: {
      min: "0",
      max: "10000",
    },
    add: true,
    edit: true,
    search: false,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.father"),
    prop: 'father',
    component: 'el-input-number',
    props: {
      min: "0",
      max: "10000",
    },
    search: false,
    add: true,
    edit: true,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.component"),
    prop: 'component',
    component: 'el-input',
    search: false,
    add: true,
    edit: true,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.icon"),
    prop: 'icon',
    component: markRaw(IconSelect),
    props: {
      data: selectIcon.value,
    },
    search: false,
    add: true,
    edit: true,
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
    search: false,
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
    search: false,
    detail: true,
    width: '200'
  },
])
const tableColumns = ref(JSON.parse(JSON.stringify(columns)))
const rules = {
  title: { required: true, message: t(`rules.menu.title`), trigger: 'blur' },
  title_mark: { required: true, message: t(`rules.menu.title_mark`), trigger: 'blur' },
  path: { required: true, message: t(`rules.menu.path`), trigger: 'blur' },
  order: { required: true, message: t(`rules.menu.order`), trigger: 'blur' },
  key: { required: true, message: t(`rules.menu.key`), trigger: 'blur' },
  father: { required: true, message: t(`rules.menu.father`), trigger: 'blur' },
  component: { required: true, message: t(`rules.menu.component`), trigger: 'blur' },
  icon: { required: true, message: t(`rules.menu.icon`), trigger: 'blur' },
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
} = useMenuCrudRequest(true)


watch(list, ()=>{
  const {treeData} = getTreeDataAndHalfCheckedKeys(list.value)
  menuTrees.value = treeData
})

</script>

<template>
  <pro-card>
    <pro-crud
      v-loading="isFetching"
      v-model="form"
      v-model:search="searchForm"
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :columns="columns"
      :menu="menu"
      :data="menuTrees"
      :detail="detail"
      :before-open="beforeOpen"
      @search="search"
      @submit="submit"
      row-key="key"
      :table-columns="tableColumns"
      :total="total"
      :rules="rules"
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
      <template #table-icon="{ row, size }">
        <el-icon :size="size">
          <component :is="row.icon"/>
        </el-icon>
        <span>{{ row.icon }}</span>
      </template>
      <template #detail-icon="{ size, item }">
        <el-icon :size="size">
          <component :is="item.icon"/>
        </el-icon>
        <span>{{ item.icon }}</span>
      </template>
    </pro-crud>
  </pro-card>
</template>
<style>
/* 隐藏布局滚动条让谷歌浏览器更平滑*/
::-webkit-scrollbar {
  width: 0;
  height: 0;
}
</style>