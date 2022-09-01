<template>
  <pro-card>
    <pro-crud
        v-model="form"
        v-model:search="serachForm"
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        v-loading="isFetching"
        :columns="columns"
        :menu="menu"
        :data="list"
        :total="total"
        :detail="detail"
        :before-open="beforeOpen"
        @search="search"
        @load="loadList"
        @search-reset="loadList"
        @submit="submit"
        :table-columns="tableColumns"
        :rules="rules"
        layout="total, ->, jumper, prev, pager, next, sizes"
        border
        stripe
    >
      <template #action>
        <pro-column-setting
            v-model="tableColumns"
        />
      </template>
      <template #menu="{row, size }">
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
        <el-button
            :size="size"
            type="success"
            link
            @click="openDrawer(row)"
        >
          {{ $t(`system.role.set_permissions`) }}
        </el-button>
      </template>
    </pro-crud>
    <el-drawer v-model="drawer" direction="rtl">
      <template #header>
        <h2>{{ $t(`system.role.set_permissions`) }}</h2>
      </template>
      <template #default>
        <el-tabs type="border-card">
          <el-tab-pane :label="$t(`system.role.menu_tab_label`)">
            <div class="relative w-full h-10">
              <el-button class="absolute top-0 right-0" type="primary" @click="handleMenuTreeOK">{{ $t(`system.role.permission_btu`) }}</el-button>
            </div>
            <el-tree
                ref="menuTreeRef"
                :data="menuTreeData"
                show-checkbox
                :default-checked-keys="menuCheckedKeys"
                node-key="uid"
                :props="menuDefaultProps"
            />
          </el-tab-pane>
          <el-tab-pane :label="$t(`system.role.interface_tab_label`)">
            <div class="relative w-full h-10">
              <el-button class="absolute top-0 right-0" type="primary" @click="handleInterfaceTreeOK">{{ $t(`system.role.permission_btu`) }}</el-button>
            </div>
            <el-tree
                ref="interfaceTreeRef"
                :data="interfaceTreeData"
                show-checkbox
                :default-checked-keys="interfaceCheckedKeys"
                node-key="uid"
                :props="interfaceDefaultProps"
            >
              <template #default="{ node, data }">
                <span class="custom-tree-node">
                  <span>{{ node.label }}</span>
                  <el-divider direction="vertical" />
                  <span>{{ data.group }}</span>
                  <el-divider direction="vertical" />
                  <el-tag v-if="data.method === 'GET'" type="" >{{ data.method }}</el-tag>
                  <el-tag v-if="data.method === 'POST'" type="success">{{ data.method }}</el-tag>
                  <el-tag v-if="data.method === 'PUT'" type="warning">{{ data.method }}</el-tag>
                  <el-tag v-if="data.method === 'DELETE'" type="danger">{{ data.method }}</el-tag>
                  <el-divider direction="vertical" />
                  <span>{{ data.path}}</span>
                </span>
              </template>
            </el-tree>
          </el-tab-pane>
        </el-tabs>
      </template>
    </el-drawer>
  </pro-card>

</template>
<script lang="ts" setup>
import {ref, toRefs, reactive} from 'vue'
import {useGlobalState, useGet, usePost, usePut, useDelete} from '../../../composables'
import {ElMessage, ElTree} from 'element-plus'
import {
  defineCrudColumns,
  defineCrudMenuColumns,
} from 'element-pro-components'
import {Api} from "../../../utils";
import {useCrud} from "../../../composables/crud";
import {useI18n} from "vue-i18n";
const {t} = useI18n()

interface Role {
  uid: string
  key: string
  name_zh_ch: string
  name_en_us: string
  describe: string
  menu_permission: any
  interface_permission: any
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
  width: '300'
})

const state = useGlobalState()
const drawer = ref(false)
// 当前
const currentRoleRow = ref<Role>({
  uid: '',
  key: '',
  name_zh_ch: '',
  name_en_us: '',
  describe: '',
  menu_permission: [],
  interface_permission: [],
})
const menuCheckedKeys = ref<string[]>([])
const interfaceCheckedKeys = ref<string[]>([])
const columns = defineCrudColumns([
  {
    label: t(`system.role.uid`),
    prop: 'uid',
    component: 'el-input',
    detail: true,
    props: {
      disabled: true
    }
  },
  {
    label: t(`system.role.name_zh_cn`),
    prop: 'name_zh_cn',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
  {
    label: t(`system.role.name_en_us`),
    prop: 'name_en_us',
    component: 'el-input',
    form: true,
    search: true,
    detail: true,
  },
  {
    label: t(`system.role.describe`),
    prop: 'describe',
    component: 'el-input',
    props: {
      type: 'textarea',
      rows: 14,
      minRows: 12,
      maxRows: 24,
    },
    form: true,
    detail: true,
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
const menuTreeRef = ref<InstanceType<typeof ElTree>>()
const menuDefaultProps = ref({
  children: 'children',
  label: 'title_en_us',
})

const interfaceTreeRef = ref<InstanceType<typeof ElTree>>()
const interfaceDefaultProps = ref({
  children: 'children',
  label: 'describe_en_us',
})

const {data: menuTreeData,  execute: exeMenuAll} = useGet(Api.menuAll)
const {data: interfaceTreeData, execute: exeInterfaceAll} = useGet(Api.interfaceAll)
const {execute: exeRoleMenuNodesEdit} = usePut(Api.roleEdit, currentRoleRow)

const rules = {
  key: {required: true, message: t(`rules.role.key`), trigger: 'blur'},
  name_zh_cn: {required: true, message: t(`rules.role.name_zh_cn`), trigger: 'blur'},
  name_en_us: {required: true, message: t(`rules.role.name_en_us`), trigger: 'blur'},
  describe: {required: true, message: t(`rules.role.describe`), trigger: 'blur'},
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
} = useCrud(Api.roleList, Api.roleAdd, Api.roleEdit, Api.roleDelete, true)


// 抽屉
const openDrawer = (row: any) => {
  drawer.value = true
  currentRoleRow.value = row
  menuDefaultProps.value.label = state.value.locales==='en-us' ?'title_en_us' : 'title_zh_cn'
  interfaceDefaultProps.value.label = state.value.locales==='en-us' ?'describe_en_us' : 'describe_zh_cn'
  // 更新菜单Tree
  exeMenuAll()
  // 添加菜单Tree状态
  menuCheckedKeys.value = []
  currentRoleRow.value.menu_permission.forEach((item: { uid: any }) => {
    menuCheckedKeys.value.push(item.uid)
  })
  // 更新接口Tree
  exeInterfaceAll()
  // 添加接口Tree状态
  interfaceCheckedKeys.value = []
  currentRoleRow.value.interface_permission.forEach((item: { uid: any }) => {
    interfaceCheckedKeys.value.push(item.uid)
  })
}

// 处理菜单提交
const handleMenuTreeOK = async () => {
  currentRoleRow.value.menu_permission = menuTreeRef.value?.getCheckedNodes()
  await exeRoleMenuNodesEdit()
  ElMessage.success(t(`system.role.permission_ok`))
  await loadList()
}

// 处理接口提交
const handleInterfaceTreeOK = async () => {
  currentRoleRow.value.interface_permission = interfaceTreeRef.value?.getCheckedNodes()
  await exeRoleMenuNodesEdit()
  ElMessage.success(t(`system.role.permission_ok`))
  await loadList()
}


</script>
<style></style>