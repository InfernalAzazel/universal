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

<script lang="ts" setup>
import {h, ref} from 'vue'
import {ElMessage} from 'element-plus'
import {Setting} from '@element-plus/icons-vue'
import ExSelect from '../../../components/ExSelect/index.vue'
import {
  defineCrudColumns,
  defineCrudMenuColumns,
} from 'element-pro-components'
import {markRaw} from 'vue'
import {Api} from "../../../utils";
import {useCrud} from "../../../composables/crud";
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import {useI18n} from "vue-i18n";

const {t} = useI18n()
const selectData = ref([
  {value: true, label: '是'},
  {value: false, label: '否'},
])
const selectIcon = ref<any[]>([])
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  selectIcon.value.push({
    value: key,
    label: key,
  })
}
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
    label: t("system.menu.id"),
    prop: 'id',
    component: 'el-input',
    search: true,
    detail: true,
    width: '200',
  },
  {
    label: t("system.menu.title_zh_cn"),
    prop: 'title_zh_cn',
    component: 'el-input',
    add: true,
    edit: true,
    search: true,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.title_en_us"),
    prop: 'title_en_us',
    component: 'el-input',
    add: true,
    edit: true,
    search: true,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.path"),
    prop: 'path',
    component: 'el-input',
    add: true,
    edit: true,
    search: true,
    detail: true,
    width: '500'
  },
  {
    label: t("system.menu.order"),
    prop: 'order',
    component: 'el-input-number',
    add: true,
    edit: true,
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
    search: true,
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
    search: true,
    add: true,
    edit: true,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.component"),
    prop: 'component',
    component: 'el-input',
    search: true,
    add: true,
    edit: true,
    detail: true,
    width: '200'
  },
  {
    label: t("system.menu.icon"),
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
  title_zh_cn: { required: true, message: t(`rules.menu.title_zh_cn`), trigger: 'blur' },
  title_en_us: { required: true, message: t(`rules.menu.title_en_us`), trigger: 'blur' },
  path: { required: true, message: t(`rules.menu.path`), trigger: 'blur' },
  order: { required: true, message: t(`rules.menu.order`), trigger: 'blur' },
  key: { required: true, message: t(`rules.menu.key`), trigger: 'blur' },
  father: { required: true, message: t(`rules.menu.father`), trigger: 'blur' },
  component: { required: true, message: t(`rules.menu.component`), trigger: 'blur' },
  icon: { required: true, message: t(`rules.menu.icon`), trigger: 'blur' },
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
  search,
  deleteRow
} = useCrud(Api.menuList, Api.menuAdd, Api.menuEdit, Api.menuDelete, true)


</script>
<style>
/* 隐藏布局滚动条让谷歌浏览器更平滑*/
::-webkit-scrollbar {
  width: 0px;
  height: 0px;
}
</style>